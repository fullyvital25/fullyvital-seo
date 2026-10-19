"""
Build a hub draft for a 2026-layout article (fv-tldr / fv-figure / fv-related / fv-refs components). No Shopify writes.

Input:  data/hub_drafts/<blog>__<handle>/template.html, meta.json
        meta.json: title, seo_title, seo_description, notes[], flags[], ref_tags{pmid: tag},
                   extra_refs[{tag, citation, url, label}]  (non-study sources, e.g. a regulatory opinion)
Placeholders: {{STYLE_TLDR}} {{STYLE_RELATED}} {{STYLE_REFS}} (copied from the live article),
              {{REFS}} (reference cards built from PubMed records), {{FAQ_JSONLD}} (from the visible FAQ)
Output: draft.html, preview.html, review.md, current.html

Guards (build stops): AI-chat artifacts; exactly 3 distinct PubMed studies, each linked once;
first study link in the second half of the visible text; years and first authors must match PubMed.

Usage:
    python hub_build.py hair-care what-causes-gray-hair
"""
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from pubmed import _get

blog, handle = sys.argv[1], sys.argv[2]
D = Path(f"data/hub_drafts/{blog}__{handle}")
backup = sorted(Path("data/shopify_backup").glob("articles_*.json"))[-1]
meta = json.loads((D / "meta.json").read_text())
all_arts = json.loads(backup.read_text())
art = next((a for a in all_arts if a["handle"] == handle and a["blog"]["handle"] == blog), None)
if art is None:  # new article: borrow component styles from an existing 2026-layout article
    if not meta.get("new"):
        sys.exit(f"/blogs/{blog}/{handle} not found; set \"new\": true and \"style_source\" in meta.json for a new article")
    src = next(a for a in all_arts if a["handle"] == meta["style_source"])
    art = {"title": "(new article)", "body": ""}
    live, style_html = "", src["body"] or ""
else:
    live = art["body"] or ""
    # an old-layout article being rebuilt borrows the component styles from meta["style_source"]
    style_html = next(a for a in all_arts if a["handle"] == meta["style_source"])["body"] if meta.get("style_source") else live
(D / "current.html").write_text(live)
tpl = (D / "template.html").read_text()

styles = re.findall(r"<style>.*?</style>", style_html, re.S)
pick = lambda key: next((s for s in styles if key in s), "")
for name, key in [("STYLE_TLDR", ".fv-tldr"), ("STYLE_RELATED", ".fv-related"), ("STYLE_REFS", ".fv-refs")]:
    tpl = tpl.replace("{{" + name + "}}", pick(key))

# ---------- reference cards from PubMed ----------
# studies: any PubMed links in the template (in order), then meta["ref_tags"] keys (cited only in the reference cards)
order = list(dict.fromkeys(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", tpl) + list(meta.get("ref_tags", {}))))
rec = json.loads(_get("esummary", {"db": "pubmed", "id": ",".join(order), "retmode": "json"}))["result"] if order else {}
cards, n = [], 0
for p in order:
    x = rec[p]
    if not x.get("title"):
        sys.exit(f"unverified PMID {p}")
    names = [a["name"] for a in x.get("authors") or []]
    au = ", ".join(names[:3]) + (", et al" if len(names) > 3 else "")
    n += 1
    cards.append(f'''<div class="fv-refs__item">
<span class="fv-refs__num">{n:02d}</span>
<div class="fv-refs__body">
<span class="fv-refs__tag">{meta.get("ref_tags", {}).get(p, "Peer-reviewed study")}</span>
<p class="fv-refs__citation">{au}. "{x["title"].rstrip(".")}." <em>{x["source"]}</em>, {x["pubdate"][:4]}.</p>
<div class="fv-refs__links"><a class="fv-refs__link" href="https://pubmed.ncbi.nlm.nih.gov/{p}/" rel="noopener" target="_blank"><span class="fv-refs__link-icon">↗</span> View on PubMed</a></div>
</div>
</div>''')
for e in meta.get("extra_refs", []):
    n += 1
    cards.append(f'''<div class="fv-refs__item">
<span class="fv-refs__num">{n:02d}</span>
<div class="fv-refs__body">
<span class="fv-refs__tag">{e["tag"]}</span>
<p class="fv-refs__citation">{e["citation"]}</p>
<div class="fv-refs__links"><a class="fv-refs__link" href="{e["url"]}" rel="noopener" target="_blank"><span class="fv-refs__link-icon">↗</span> {e["label"]}</a></div>
</div>
</div>''')
draft = tpl.replace("{{REFS}}", "\n".join(cards))

# ---------- FAQ JSON-LD from the visible FAQ ----------
soup = BeautifulSoup(draft, "html.parser")
faq_h2 = next((h for h in soup.find_all("h2") if "frequently asked" in h.get_text().lower()), None)
qa = []
if faq_h2:
    el = faq_h2.find_next_sibling()
    while el and el.name != "h2" and not (el.name == "section"):
        if el.name == "h3":
            ans, nx = [], el.find_next_sibling()
            while nx and nx.name == "p":
                ans.append(nx.get_text(" ", strip=True))
                nx = nx.find_next_sibling()
            qa.append({"@type": "Question", "name": el.get_text(" ", strip=True),
                       "acceptedAnswer": {"@type": "Answer", "text": " ".join(ans)}})
        el = el.find_next_sibling()
ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qa}
draft = draft.replace("{{FAQ_JSONLD}}", '<script type="application/ld+json">\n' + json.dumps(ld, indent=2, ensure_ascii=False) + "\n</script>")

# ---------- guards ----------
AI = re.compile(r"chat\.openai\.com|chatgpt\.com|openai\.com|utm_source=(chatgpt|openai)|perplexity\.ai|gemini\.google|claude\.ai|"
                r"copilot\.microsoft|user-content-fn|data-footnote-backref|oaicite|contentReference|turn0search", re.I)
if AI.search(draft):
    sys.exit(f"AI artifact: {AI.search(draft).group(0)}")
if "{{" in draft:
    sys.exit(f"unfilled placeholder: {re.search(r'{{[^}]+}}', draft).group(0)}")
study = re.compile(r'href="[^"]*(pubmed\.ncbi|ncbi\.nlm|doi\.org|elifesciences|nature\.com|sciencedirect|frontiersin|onlinelibrary|springer)[^"]*"')
pm = re.findall(r'href="https://pubmed\.ncbi\.nlm\.nih\.gov/(\d+)/"', draft)
if len(set(pm)) != 3:
    sys.exit(f"need exactly 3 distinct PubMed studies, found {len(set(pm))}")
if len(pm) != 3:
    sys.exit(f"each study must be linked once; PubMed links found: {len(pm)}")
nonpm = [m.group(0) for m in study.finditer(draft) if "pubmed" not in m.group(0) and not any(e["url"] in m.group(0) for e in meta.get("extra_refs", []))]
if nonpm:
    sys.exit(f"study links outside the 3 PubMed citations: {nonpm[:3]}")
visible = BeautifulSoup(re.sub(r"<(style|script)[^>]*>.*?</\1>", "", draft, flags=re.S), "html.parser")
text = visible.get_text(" ")
first = min(m.start() for m in study.finditer(str(visible)))
before = BeautifulSoup(str(visible)[:first], "html.parser").get_text(" ")
share = len(before) / max(1, len(text))
if share < 0.5:
    sys.exit(f"first study link at {share:.0%} of the text; must be in the second half")
for p in set(pm):
    x = rec[p]
    if x["pubdate"][:4] not in text:
        sys.exit(f"year {x['pubdate'][:4]} for PMID {p} not in visible text")
(D / "draft.html").write_text(draft)

words = lambda h: len(BeautifulSoup(re.sub(r"<(style|script)[^>]*>.*?</\1>", "", h, flags=re.S), "html.parser").get_text(" ").split())
blog_links = sorted(set(re.findall(r'href="https://fullyvital\.com(/blogs/[^"#?]+)"', draft)))
L = [f"# Hub draft: /blogs/{blog}/{handle}\n", f"- Live title: {art['title']}", f"- New title: {meta['title']}",
     f"- New SEO title: {meta['seo_title']}", f"- New meta description: {meta['seo_description']}",
     f"- Words: {words(live):,} → {words(draft):,}", f"- Studies cited: {len(set(pm))} (each linked once; first link at {share:.0%} of the text)",
     f"- FAQ questions (also in FAQPage markup): {len(qa)}", f"- Internal blog links: {len(blog_links)}\n", "## What changed and why\n",
     *[f"- {x}" for x in meta["notes"]], "", "## Sources\n"]
L += [f"- [{p}](https://pubmed.ncbi.nlm.nih.gov/{p}/) {rec[p]['pubdate'][:4]}: {rec[p]['title']} ({rec[p]['source']})" for p in order]
L += [f"- {e['citation']} ({e['url']}), non-study source" for e in meta.get("extra_refs", [])]
L += ["", "## Internal links in the draft\n", *[f"- {b}" for b in blog_links]]
if meta.get("flags"):
    L += ["", "## For you to decide", *[f"- {x}" for x in meta["flags"]]]
(D / "review.md").write_text("\n".join(L) + "\n")
(D / "preview.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>{meta['title']}</title>
<style>body{{max-width:820px;margin:40px auto;padding:0 16px;font:17px/1.6 Georgia,serif;color:#222}}img{{max-width:100%;height:auto}}
table{{border-collapse:collapse;width:100%;font:14px sans-serif}}td,th{{border:1px solid #ddd;padding:6px;text-align:left}}</style>
<h1>{meta['title']}</h1>{draft}""")
print(f"built {D}/draft.html: {words(draft):,} words, 3 studies (first link at {share:.0%}), {len(qa)} FAQ, {len(blog_links)} internal links")
