"""
Gray hubs 5-8: extend existing pages in place (calendar posts are extended, never rebuilt; the survey statistic is
left exactly as it is). Each edit is anchored and must match exactly once, or the page is skipped.

  5 Stress    /can-stress-cause-gray-hair: short-answer box, links up to the causes/premature/men hubs, author fix.
  6 Prevent   /how-to-prevent-gray-hair-naturally: short-answer box, 2 FAQ answers (+ FAQ schema), Related Reading.
  7 Myths     /gray-hair-myths-vs-facts: "white vs. gray hair" section, 5 FAQ answers (+ schema), more related links.
  8 Products  /best-anti-gray-hair-supplements-2026: "choosing by age" section, comparison/review links; the three
              women's age listicles merge into it (cleanup_apply.py: 301s + internal link rewrites).
Then one sentence linking up to each hub on related spokes (before their FAQ).
Refresh-test pages are never edited. Each article is re-read right before it is written.

Usage: python gray_hubs_extend.py [--apply]
"""
import json
import re
import subprocess
import sys

from shopify_client import ARTICLE_FIELDS, Shopify

APPLY = "--apply" in sys.argv
B = "https://fullyvital.com/blogs/hair-care/"
H = {"stress": "can-stress-cause-gray-hair", "prevent": "how-to-prevent-gray-hair-naturally",
     "myths": "gray-hair-myths-vs-facts", "products": "best-anti-gray-hair-supplements-2026"}
LISTICLES = ["best-anti-gray-products-women-20s", "best-anti-gray-products-women-30s", "best-anti-gray-products-women-over-40"]
_rc = json.load(open("data/processed/refresh_controls.json"))
TEST = {re.sub(r"^https?://[^/]+", "", u) for k, v in _rc.items() for u in [k, *v]}

s = Shopify(apply=APPLY)
if APPLY:
    print("backup:", s.backup_articles())
arts = {a["handle"]: a for a in s.articles() if a["blog"]["handle"] == "hair-care"}
style_src = arts["what-causes-gray-hair"]["body"]
STYLE = {k: next(x for x in re.findall(r"<style>.*?</style>", style_src, re.S) if k in x) for k in (".fv-tldr", ".fv-related")}


def fresh(a):
    return s.gql(f"query($id: ID!) {{ article(id: $id) {{ {ARTICLE_FIELDS} }} }}", {"id": a["id"]})["article"]


def a_(h, text):
    return f'<a href="{B}{h}">{text}</a>'


def li(h, text):
    return f'<li class="fv-related__item"><a class="fv-related__link" href="{B}{h}">{text}</a></li>'


def tldr(items):
    return STYLE[".fv-tldr"] + '\n<div class="fv-tldr">\n<p class="fv-tldr__title">The Short Answer</p>\n<ul class="fv-tldr__list">\n' + \
        "\n".join(f"<li>{x}</li>" for x in items) + "\n</ul>\n</div>\n"


def faq(qas):
    return "".join(f"<h3>{q}</h3>\n<p>{a}</p>\n" for q, a in qas)


def add_schema(body, qas):
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', body, re.S)
    ld = json.loads(m.group(2))
    assert ld.get("@type") == "FAQPage"
    have = {q["name"] for q in ld["mainEntity"]}
    ld["mainEntity"] += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                         for q, a in qas if q not in have]
    return body[:m.start(2)] + "\n" + json.dumps(ld, indent=2, ensure_ascii=False) + "\n" + body[m.end(2):]


def insert(body, anchor, html, after=False):
    """anchor: regex that must match exactly once."""
    ms = list(re.finditer(anchor, body, re.S))
    if len(ms) != 1:
        raise ValueError(f"anchor {anchor!r} matched {len(ms)} times")
    i = ms[0].end() if after else ms[0].start()
    return body[:i] + html + body[i:]


def related_add(body, items):
    ms = list(re.finditer(r'(<section class="fv-related">.*?)(</ul>)', body, re.S))
    if len(ms) != 1:
        raise ValueError("related block not found once")
    new = "".join(x + "\n" for x in items if re.search(r'href="([^"]+)"', x).group(1) not in body)
    return body[:ms[0].start(2)] + new + body[ms[0].start(2):]


SURVEY = re.compile(r"survey[^.]{0,160}\d{2}%|\d{2}%[^.]{0,160}survey", re.I)


def write(h, fn):
    a = fresh(arts[h])
    before = a["body"]
    try:
        after = fn(before)
    except (ValueError, AssertionError) as e:
        print(f"SKIP {h}: {e}")
        return
    assert SURVEY.findall(before) == SURVEY.findall(after), f"{h}: survey text changed"
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', after, re.S):
        json.loads(m.group(1))
    print(f"{'UPDATED' if APPLY else 'would update'} /{h}: {len(before):,} -> {len(after):,} chars")
    s.update_article(a, {"body": after})


# ---------- 5: stress ----------
def stress(b):
    b = b.replace("(Picard et al., <em>eLife</em>, 2021)", "(Rosenberg et al., <em>eLife</em>, 2021)")
    b = insert(b, r"\A.*?</figure>", "\n" + tldr([
        "Yes. Research links chronic stress to faster graying, partly through stress hormones that exhaust the pigment stem cells in the follicle (shown in mice).",
        "A 2021 study of individual human hairs found some recently grayed hairs regained pigment when stress eased.",
        "Stress isn't the only cause: genes, age, smoking and low vitamin B12 matter too.",
        "Any change shows only in new growth, so judge it over months.",
    ]), after=True)
    b = insert(b, r'<h2>Can Stress-Related Gray Hair Be Reversed\?</h2>',
               f'<p>Stress is one of several causes. For the full picture, see {a_("what-causes-gray-hair", "what causes gray hair")}, '
               f'{a_("why-am-i-going-gray-causes-explained", "premature graying")} and {a_("gray-hair-in-men", "gray hair in men")}.</p>\n')
    return related_add(b, [li("what-causes-gray-hair", "What Causes Gray Hair? Every Cause, Explained"),
                           li("why-am-i-going-gray-causes-explained", "Premature Gray Hair: Why You're Going Gray Early"),
                           li("what-causes-sudden-gray-hair", "What Causes Sudden Gray Hair?"),
                           li("gray-hair-myths-vs-facts", "Gray Hair Myths vs. Facts")])


# ---------- 6: prevent ----------
PREVENT_FAQ = [
    ("Can vitamin C help prevent gray hair?",
     "There's no good evidence that vitamin C on its own prevents gray hair. It's an antioxidant and helps you absorb iron, so it belongs in a nutrient-rich diet, but deficiency is rare. Low vitamin B12 has the most consistent link to early graying."),
    ("What age is normal for gray hair?",
     "Most people notice their first grays in their 30s, but it varies with ancestry and family history. Graying is usually called premature if it starts before about 20 in white Europeans, 25 in Asians and 30 in people of African descent."),
]


def prevent(b):
    b = insert(b, r"\A.*?</figure>", "\n" + tldr([
        "You can't change genetic graying, but some causes are within your control: smoking, low vitamin B12, thyroid problems and chronic stress.",
        "Eat a nutrient-rich diet, and ask for a B12 and thyroid check if you're graying young.",
        "Don't smoke, and manage long-term stress.",
        "Any change shows only in new growth, over months rather than weeks.",
    ]), after=True)
    rel = STYLE[".fv-related"] + '\n<section class="fv-related">\n<h2 class="fv-related__title">Related Reading</h2>\n<ul class="fv-related__list">\n' + "\n".join([
        li("foods-to-prevent-gray-hair", "Foods That May Slow Premature Graying"),
        li("vitamins-for-gray-hair", "Which Vitamins Help With Gray Hair?"),
        li("vitamin-b12-deficiency-gray-hair", "Vitamin B12 Deficiency and Gray Hair"),
        li("does-copper-deficiency-cause-gray-hair", "Does Copper Deficiency Cause Gray Hair?"),
        li("does-smoking-cause-gray-hair", "Does Smoking Cause Gray Hair?"),
        li("can-stress-cause-gray-hair", "Can Stress Cause Gray Hair?"),
        li("what-causes-gray-hair", "What Causes Gray Hair? Every Cause, Explained"),
        li("can-gray-hair-be-reversed", "Can Gray Hair Be Reversed?"),
        li("anti-gray-hair-ingredients-what-actually-works", "Anti-Gray Hair Ingredients: What Actually Works"),
    ]) + "\n</ul>\n</section>\n"
    b = insert(b, r'<section class="fv-refs"', faq(PREVENT_FAQ) + rel)
    return add_schema(b, PREVENT_FAQ)


# ---------- 7: myths ----------
MYTHS_FAQ = [
    ("How do I tell if my hair is white or gray?",
     "Pull out a single hair and look at it against a white background. A strand with no pigment is white; hair only looks gray when white strands are mixed in with darker ones."),
    ("Why did my hair turn white, not gray?",
     "It didn't skip a stage. Each hair goes from pigmented to unpigmented. When most of your hairs have lost their pigment, your hair looks white rather than salt-and-pepper."),
    ("Can gray hair regain its color?",
     "Occasionally, for individual hairs. A 2021 study found white and gray hairs that naturally regained pigment, sometimes alongside lower stress, but it's uncommon and can't be relied on."),
    ("Does gray or white hair make you look older?",
     "Generally, yes. In studies where people rated photos of the same face with and without gray hair, gray hair made faces look older."),
    ("What blood test is recommended for early gray hair?",
     "If graying starts very early, doctors often check vitamin B12, folate, iron stores, vitamin D and thyroid function."),
]


def myths(b):
    sec = ("<h2>White vs. Gray Hair: What's the Difference?</h2>\n"
           "<p>There's no difference in the hair itself. Individual hairs don't turn gray: each strand is either pigmented or has little or no pigment, which looks white. "
           "\"Gray\" describes the overall effect of white hairs mixed in with your natural color. As the share of white hairs rises, hair looks grayer, then silver, then white.</p>\n"
           f"<p>White hairs can also look yellowish or dull because of light, minerals in water or styling products, and they often feel coarser. {a_('why-is-gray-hair-different-texture', 'Why gray hair feels different')}.</p>\n"
           f"<p>For the causes behind it all, see {a_('what-causes-gray-hair', 'what causes gray hair')}, {a_('can-stress-cause-gray-hair', 'stress and gray hair')} and {a_('how-to-prevent-gray-hair-naturally', 'how to prevent gray hair naturally')}.</p>\n")
    b = insert(b, r"<h2>Frequently Asked Questions</h2>", sec)
    b = insert(b, r"<!-- FullyVital — Related Reading Block", faq(MYTHS_FAQ))
    b = add_schema(b, MYTHS_FAQ)
    return related_add(b, [li("why-is-gray-hair-different-texture", "Why Is Gray Hair a Different Texture?"),
                           li("can-stress-cause-gray-hair", "Can Stress Cause Gray Hair?"),
                           li("how-to-prevent-gray-hair-naturally", "How to Prevent Gray Hair Naturally"),
                           li("what-causes-gray-hair", "What Causes Gray Hair? Every Cause, Explained"),
                           li("gray-hair-in-men", "Gray Hair in Men")])


# ---------- 8: products ----------
def products(b):
    for h in LISTICLES:  # drop related items and unwrap links to the listicles that merge into this page (no self-links)
        b = re.sub(r'<li class="fv-related__item">\s*<a[^>]*href="[^"]*/' + h + r'"[^>]*>.*?</a>\s*</li>\s*', "", b, flags=re.S)
        b = re.sub(r'<a\b[^>]*href="[^"]*/' + h + r'"[^>]*>(.*?)</a>', r"\1", b, flags=re.S)
    sec = ("<h2>Choosing by Age</h2>\n"
           f"<p><strong>In your 20s:</strong> early graying is usually genetic, but it's worth a blood test for vitamin B12 and thyroid function, especially if it's sudden. {a_('going-gray-in-your-20s-causes-what-you-can-do', 'Going gray in your 20s')} and {a_('why-am-i-going-gray-causes-explained', 'premature graying')}.</p>\n"
           f"<p><strong>In your 30s:</strong> some gray is common. Consistency matters more than a stronger product. {a_('going-gray-in-your-30s-why-it-happens', 'Going gray in your 30s')}.</p>\n"
           f"<p><strong>In your 40s and beyond:</strong> hormonal changes around perimenopause can coincide with more gray, and texture often changes too. {a_('going-gray-40s-50s-what-helps', 'Going gray in your 40s and 50s')}, {a_('perimenopause-and-gray-hair-hormone-connection', 'perimenopause and gray hair')} and {a_('why-is-gray-hair-different-texture', 'why gray hair feels different')}.</p>\n"
           f"<p><strong>For men:</strong> {a_('gray-hair-in-men', 'gray hair in men')}.</p>\n"
           f"<p>Comparing brands? See {a_('fullyvital-vs-arey-anti-gray-comparison', 'FullyVital vs. Arey')}, {a_('fullyvital-vs-particle-anti-gray-comparison', 'FullyVital vs. Particle')}, "
           f"{a_('do-anti-gray-supplements-work-honest-review', 'do anti-gray supplements work?')} and {a_('how-to-choose-anti-gray-product', 'how to choose an anti-gray product')}.</p>\n")
    b = insert(b, r"<h2>Frequently Asked Questions</h2>", sec)
    return related_add(b, [li("fullyvital-vs-arey-anti-gray-comparison", "FullyVital vs. Arey: An Honest Comparison"),
                           li("fullyvital-vs-particle-anti-gray-comparison", "FullyVital vs. Particle: An Honest Comparison"),
                           li("fullyvital-vs-mayraki-anti-gray-comparison", "FullyVital vs. Mayraki"),
                           li("do-anti-gray-supplements-work-honest-review", "Do Anti-Gray Supplements Really Work?"),
                           li("fullyvital-anti-gray-reviews", "FullyVital Anti-Gray Reviews"),
                           li("how-to-choose-anti-gray-product", "How to Choose an Anti-Gray Product")])


for key, fn in [("products", products), ("stress", stress), ("prevent", prevent), ("myths", myths)]:
    write(H[key], fn)

# ---------- merge the women's listicles into the products hub ----------
sheet = "data/processed/gray_hub8_merges.csv"
open(sheet, "w").write("path,decision,redirect_to\n" + "".join(f"/blogs/hair-care/{h},MERGE: unpublish + 301 to target,/blogs/hair-care/{H['products']}\n" for h in LISTICLES))
r = subprocess.run([sys.executable, "cleanup_apply.py", "--sheet", sheet] + (["--apply"] if APPLY else []), capture_output=True, text=True)
print("merges:", r.returncode, r.stdout[-700:], r.stderr[-300:])

# ---------- spokes link up ----------
SPOKES = {
    "stress": ("For how stress affects hair color, and what the research says about reversing it, see {a}.", "can stress cause gray hair?",
               ["what-causes-sudden-gray-hair", "hydrogen-peroxide-gray-hair-oxidative-stress", "premature-gray-hair-reversal-early-action",
                "going-gray-in-your-20s-causes-what-you-can-do", "going-gray-in-your-30s-why-it-happens", "perimenopause-and-gray-hair-hormone-connection",
                "catalase-gray-hair-explained", "gray-hair-research-studies"]),
    "prevent": ("For the steps that can help slow graying, see our guide to {a}.", "how to prevent gray hair naturally",
                ["hydrogen-peroxide-gray-hair-oxidative-stress", "reverse-gray-hair-naturally-without-dye", "how-long-to-see-less-gray-hair",
                 "astaxanthin-for-gray-hair", "catalase-gray-hair-explained", "anti-gray-hair-ingredients-what-actually-works", "can-gray-hair-be-reversed",
                 "glutathione-for-gray-hair", "premature-gray-hair-reversal-early-action", "going-gray-in-your-20s-causes-what-you-can-do",
                 "going-gray-in-your-30s-why-it-happens", "going-gray-40s-50s-what-helps", "nutrient-deficiency-gray-hair", "does-smoking-cause-gray-hair",
                 "thyroid-and-gray-hair", "can-medications-cause-gray-hair"]),
    "myths": ("For the most common gray-hair myths, and the difference between white and gray hair, see {a}.", "gray hair myths vs. facts",
              ["why-is-gray-hair-different-texture", "gray-hair-science-glossary", "what-causes-hair-to-turn-gray-melanocyte-story", "gray-hair-research-studies",
               "columbia-gray-hair-reversal-study-2021", "can-gray-hair-be-reversed", "what-causes-sudden-gray-hair"]),
    "products": ("Comparing options? See our guide to {a}.", "the best anti-gray hair supplements",
                 ["best-anti-gray-serums", "fullyvital-vs-arey-anti-gray-comparison", "fullyvital-vs-particle-anti-gray-comparison",
                  "fullyvital-vs-mayraki-anti-gray-comparison", "fullyvital-vs-heyhair-anti-gray-comparison", "particle-anti-gray-alternative",
                  "particle-anti-gray-serum-reviews", "do-anti-gray-supplements-work-honest-review", "fullyvital-anti-gray-reviews",
                  "how-to-choose-anti-gray-product", "anti-gray-hair-care-for-women", "anti-gray-treatment-no-stain",
                  "anti-gray-vitamins-ingredients-explained", "anti-gray-serum-ingredients-explained", "fullyvital-anti-gray-system-explained",
                  "anti-gray-hair-routine", "how-to-use-anti-gray-90-day-system", "anti-gray-first-90-days-results-timeline", "inside-out-gray-hair-treatment"]),
}


def spoke_link(body, sentence):
    para = f'\n<p class="fv-hub-link">{sentence}</p>\n'
    m = re.search(r"<h[23][^>]*>(?:(?!</h[23]>).){0,80}?(frequently asked|faq)", body, re.I | re.S) or \
        re.search(r'<!-- FullyVital — Related Reading|<section class="fv-related"|<section class="fv-refs"', body)
    return body[:m.start()] + para + body[m.start():] if m else body + para


arts = {a["handle"]: a for a in s.articles() if a["blog"]["handle"] == "hair-care"}
for key, (tpl, anchor, spokes) in SPOKES.items():
    url = B + H[key]
    n = 0
    for h in spokes:
        a = arts.get(h)
        if not a or not a["isPublished"] or f"/blogs/hair-care/{h}" in TEST:
            continue
        a = fresh(a)
        if url in (a["body"] or "") or f'/blogs/hair-care/{H[key]}"' in (a["body"] or ""):
            continue
        s.update_article(a, {"body": spoke_link(a["body"], tpl.format(a=f'<a href="{url}">{anchor}</a>'))})
        n += 1
    print(f"spokes linked to /{H[key]}: {n}")
