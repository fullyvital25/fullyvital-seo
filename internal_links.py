"""
Internal links for refreshed articles (writes template.html only; rebuild + publish_refresh push it live).

1. Contextual sentences for hand-picked related pairs (PAIRS): one neutral sentence in each article, placed at the end
   of the research section (second half), linking to its partner.
2. A short "See also" line for every refreshed article: up to 2 related articles (TF-IDF similarity from
   data/processed/related_reading_proposal_2026-10-17.csv) not already linked by a sentence.

Links sit in the research section, never in Key Takeaways or FAQ. Re-running replaces earlier internal-link paragraphs.

    python internal_links.py            # report what would change
    python internal_links.py --write    # edit template.html files
"""
import csv, glob, json, re, sys
from pathlib import Path

WRITE = "--write" in sys.argv
D = Path("data/refresh_drafts")
idx = {}
for f in glob.glob(str(D / "*/published.json")):
    k = Path(f).parent.name
    blog, h = k.split("__", 1)
    idx[h] = dict(key=k, url=f"/blogs/{blog}/{h}", title=json.loads((D / k / "meta.json").read_text())["title"])

# (A, B, sentence about B shown on A, sentence about A shown on B); [[anchor]] is the link text
PAIRS = [
 ("kelp","iodine","Iodine is the mineral usually discussed with kelp, and our article on [[iodine and hair]] looks at it on its own.","Kelp is often marketed as an iodine source; see our article on [[kelp and hair]] for what the research says about it."),
 ("l-methionine","taurine","Taurine is another sulfur-containing amino acid; our article on [[taurine and hair]] covers what is known about it.","Methionine is the other sulfur-containing amino acid people ask about; see [[L-methionine and hair]]."),
 ("ultimate-guide-to-derma-roller","how-to-use-derma-roller-for-hair","Our step-by-step article explains [[how to use a derma roller for hair]].","For the wider overview of the tool, see our [[ultimate guide to the derma roller]]."),
 ("clogged-hair-follicles","what-causes-greasy-hair","Greasy hair is a related scalp concern; see [[what causes greasy hair]].","Scalp oil is sometimes linked with blocked follicles; see our article on [[clogged hair follicles]]."),
 ("pea-protein","whey-protein","Another protein people ask about is whey; see [[whey protein and hair]].","Plant protein is the other common option; see [[pea protein and hair]]."),
 ("borage-seed-oil","evening-primrose-oil","Evening primrose oil is another oil people compare it with; see [[evening primrose oil and hair]].","Borage seed oil is another oil people compare it with; see [[borage seed oil and hair]]."),
 ("n-acetyl-cysteine","glutathione","Glutathione is often discussed alongside N-acetyl cysteine; see [[glutathione and hair]].","N-acetyl cysteine is often discussed alongside glutathione; see [[N-acetyl cysteine and hair]]."),
 ("microneedling-before-and-after","microneedling-hairline","For what the trials say about the hairline specifically, see [[microneedling for the hairline]].","For what people report seeing from the procedure, see [[microneedling before and after]]."),
 ("biotin-vs-prenatal-vitamins-for-hair-growth","how-long-does-it-take-for-biotin-to-work","If you are wondering about timing, see [[how long biotin takes to work]].","For how biotin compares with prenatal vitamins, see [[biotin versus prenatal vitamins for hair]]."),
 ("fine-hair","density","Density and strand thickness are measured differently; see [[hair density]].","Fine hair describes more than density alone; see [[what fine hair is]]."),
 ("bamboo-extract","silica","Silica is the ingredient bamboo products are usually marketed for; see [[silica and hair]].","Bamboo extract is one product sold as a silica source; see [[bamboo extract and hair]]."),
 ("propanediol","caprylhydroxamic-acid","Caprylhydroxamic acid is another cosmetic ingredient with a safety literature of its own; see [[caprylhydroxamic acid]].","Propanediol is another common cosmetic ingredient we have reviewed; see [[propanediol in hair products]]."),
 ("how-to-use-derma-roller-for-hair","microneedling-before-and-after","To see what people report from microneedling, read [[microneedling before and after]].","For how the tool is used step by step, see [[how to use a derma roller for hair]]."),
 ("l-methionine","l-cysteine","L-cysteine is the related sulfur-containing amino acid people ask about; see [[L-cysteine and hair]].","Methionine is the related sulfur amino acid; see [[L-methionine and hair]]."),
 ("taurine","l-cysteine","Cysteine is the related sulfur-containing amino acid; see [[L-cysteine and hair]].","Taurine is a related sulfur-containing compound people ask about; see [[taurine and hair]]."),
 ("amino-acids-for-hair-growth","l-cysteine","For one amino acid on its own, see [[L-cysteine and hair]].","For the blend trials that include it, see [[amino acids for hair growth]]."),
 ("micro-bangs-short-hair","widows-peak-hair","Hairline shape matters for a fringe; see [[widow's peak hair]].","If you are considering a very short fringe, see [[micro bangs]]."),
 ("soy-isoflavones","phytosterols","Phytosterols are another plant compound people compare; see [[phytosterols and hair]].","Soy isoflavones are another plant compound people compare; see [[soy isoflavones and hair]]."),
 ("palmetto","hair-growth-supplements-for-men","For how it fits among other supplements studied in men, see [[hair growth supplements for men]].","For one ingredient in detail, see [[saw palmetto for hair]]."),
 ("dmdm-hydantoin-hair-loss","caprylhydroxamic-acid","Preservatives are a common question; see also [[caprylhydroxamic acid]].","Another preservative we have reviewed is [[DMDM hydantoin]]."),
 ("oyster-extract","zinc","Zinc is the mineral people most often ask about alongside oyster products; see [[zinc and hair loss]].","Oyster extract is a product people ask about alongside zinc; see [[oyster extract and hair]]."),
 ("oily-hair-shampoo","what-causes-greasy-hair","For the causes behind oily hair, see [[what causes greasy hair]].","For shampoo choices, see our article on [[oily hair shampoo]]."),
 ("batana-oil-for-hair-growth","vitamin-f-linoleic-acid","Fatty acids such as linoleic acid are discussed in [[vitamin F and linoleic acid]].","One oil people ask about that contains fatty acids is [[batana oil]]."),
 ("scalp-detox-treatment","clogged-hair-follicles","For the follicle side of scalp build-up, see [[clogged hair follicles]].","For a product category sold around this idea, see [[scalp detox treatments]]."),
 ("amino-acids-for-hair-growth","taurine","For one ingredient often found in amino acid blends, see [[taurine and hair]].","For the blend trials that include it, see [[amino acids for hair growth]]."),
 ("vitamin-a","vitamin-c","Vitamin C is another vitamin people ask about; see [[vitamin C and hair]].","Vitamin A is the other vitamin often discussed; see [[vitamin A and hair]]."),
 ("hesperidin","quercetin","Quercetin is a related plant flavonoid; see [[quercetin and hair]].","Hesperidin is a related plant flavonoid; see [[hesperidin and hair]]."),
 ("hair-crimping","cortex","To understand hair structure, see [[the hair cortex]].","If you are curious about styling, see [[hair crimping]]."),
 ("selenium","iron-deficiency-hair-loss","Iron is another nutrient with mixed findings; see [[iron deficiency and hair loss]].","Selenium is another mineral studied in hair loss; see [[selenium and hair]]."),
 ("zinc","selenium","Selenium is another trace mineral studied in hair loss; see [[selenium and hair]].","Zinc is another trace mineral studied in hair loss; see [[zinc and hair loss]]."),
 ("tulsi","ashwagandha","Ashwagandha is another herb studied mainly for stress; see [[ashwagandha for hair]].","Tulsi is another herb studied mainly for stress; see [[tulsi for hair]]."),
 ("tulsi","rhodiola-extract","Rhodiola is another herb we have reviewed; see [[Rhodiola extract and hair]].","Tulsi is another herb we have reviewed; see [[tulsi for hair]]."),
 ("raspberry-seed-oil","wheat-germ-oil","Wheat germ oil is another plant oil we have reviewed; see [[wheat germ oil]].","Raspberry seed oil is another plant oil we have reviewed; see [[raspberry seed oil]]."),
 ("inositol","magnesium","Magnesium is another supplement people pair with it; see [[magnesium and hair]].","Inositol is often taken alongside magnesium in the studies we reviewed; see [[inositol and hair]]."),
 ("normal-hair-part-vs-thinning","baby-hairs","Fine hairs along the hairline are covered in [[baby hairs]].","To tell a normal part from thinning, see [[normal hair part versus thinning]]."),
 ("amino-acids-for-hair-growth","l-methionine","For one sulfur amino acid in detail, see [[L-methionine and hair]].","For the blend trials that include it, see [[amino acids for hair growth]]."),
]


from bs4 import BeautifulSoup
moved = []

def first_link_share(t):
    body = t.split("<h2><strong>References")[0]
    words = lambda h: len(BeautifulSoup(re.sub(r"\{\{[A-Z_0-9]+\}\}", "", h), "html.parser").get_text(" ").split())
    i = body.find("pubmed.ncbi")
    return words(body[:i]) / words(body)

def a(h, text):
    return f'<a href="{idx[h]["url"]}">{text}</a>'

def render(sentence):
    return re.sub(r"\[\[(.+?)\]\]", lambda m: m.group(0), sentence)  # placeholder, replaced per target below

sent = {h: [] for h in idx}      # handle -> [(partner_handle, html_sentence)]
for A, B, sA, sB in PAIRS:
    for page, partner, s in ((A, B, sA), (B, A, sB)):
        html = re.sub(r"\[\[(.+?)\]\]", lambda m: a(partner, m.group(1)), s)
        sent[page].append((partner, html))

related = {}
for r in csv.DictReader(open("data/processed/related_reading_proposal_2026-10-17.csv")):
    related.setdefault(r["page"].split("/")[-1], []).append((r["related_url"].split("/")[-1], float(r["similarity"])))

report = []
for h, v in idx.items():
    p = D / v["key"] / "template.html"
    t = p.read_text()
    t = re.sub(r'<p class="fv-internal">.*?</p>\n?', "", t, flags=re.S)
    linked = {x[0] for x in sent[h]}
    see = [x for x, s in sorted(related.get(h, []), key=lambda y: -y[1]) if x in idx and x != h and x not in linked and s >= 0.08][:2]
    parts = [f'<p class="fv-internal">{s}</p>' for _, s in sent[h]]
    if see:
        parts.append('<p class="fv-internal"><strong>See also:</strong> ' + " &middot; ".join(a(x, idx[x]["title"]) for x in see) + "</p>")
    mark = "<h2><strong>Frequently Asked Questions"
    if mark not in t:
        report.append((h, "NO FAQ MARKER")); continue
    block = "\n".join(parts) + "\n"
    if parts:
        t2 = t.replace(mark, block + mark, 1)
        if first_link_share(t2) < 0.5:
            # keep the first study link in the second half: place the block before the section that holds it
            first = t.find("pubmed.ncbi")
            heads = [m.start() for m in re.finditer(r"<h2><strong>", t[:first])]
            t2 = t[:heads[-1]] + block + t[heads[-1]:]
            moved.append(h)
        t = t2
    report.append((h, len(sent[h]), len(see)))
    if WRITE:
        p.write_text(t)
n_sent = sum(len(v) for v in sent.values())
print(f"pages {len(idx)} | contextual sentences {n_sent} on {sum(1 for v in sent.values() if v)} pages | pages with See also {sum(1 for r in report if len(r)==3 and r[2])} | mode {'WRITE' if WRITE else 'dry'}")
bad = [r for r in report if len(r) == 2]
print("problems:", bad)
print("placed before the research section to keep study links in the second half:", moved)
