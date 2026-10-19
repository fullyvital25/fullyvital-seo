"""
Build a refresh draft for one article. No writes to Shopify.

Input:  data/refresh_drafts/<blog>__<handle>/template.html  (new prose, with placeholders)
        data/refresh_drafts/<blog>__<handle>/meta.json      (title, seo_title, seo_description, notes)
Output: data/refresh_drafts/<blog>__<handle>/current.html, draft.html, review.md

Placeholders are filled with blocks copied from the live article (latest backup), unchanged:
    {{PROOF}}         testimonial block (div.fv-blog-proof)
    {{PRODUCTS_n}}    nth "Our Best Sellers" widget (div.fv-blog-product-wrap), 1-based
    {{IMAGE_n}}       nth centred image block
    {{FOOTER}}        the closing FullyVital product table
    {{LINKIMG_n}}     nth product-linked image paragraph (older posts without the standard widgets)
    {{CTA_n}}         nth short product-recommendation paragraph (links to /products/, 30 words or fewer)
    (PROOF and PRODUCTS fall back to the unclassed testimonial / "Our Best Sellers" blocks of older hand-edited posts)

Guard: every PubMed link in the draft must be a PMID fetched through pubmed.py, and the
reference list must name that study's real year. Unverified citations stop the build.

Usage:
    python refresh_build.py hair-vitamins boron
"""

import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from pubmed import abstract, summaries

def enhance(html: str, title: str) -> str:
    """SEO/AEO pass: alt text on every image that lacks it (article title), and FAQPage JSON-LD built from the visible FAQ."""
    from bs4 import BeautifulSoup as _BS
    soup = _BS(html, "html.parser")
    for img in soup.find_all("img"):
        if not (img.get("alt") or "").strip():
            img["alt"] = title
    faq_h2 = next((h for h in soup.find_all("h2") if "Frequently Asked Questions" in h.get_text()), None)
    qa = []
    if faq_h2:
        for el in faq_h2.find_next_siblings():
            if el.name == "h2":
                break
            if el.name == "h3":
                q = el.get_text(" ", strip=True)
                a = []
                for n in el.find_next_siblings():
                    if n.name in ("h2", "h3"):
                        break
                    if n.name == "p":
                        a.append(n.get_text(" ", strip=True))
                if q and a:
                    qa.append((q, " ".join(a)))
    out = str(soup)
    if qa:
        ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
        out = out.rstrip() + '\n<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"
    return out

blog, handle = sys.argv[1], sys.argv[2]
D = Path(f"data/refresh_drafts/{blog}__{handle}")
backup = sorted(Path("data/shopify_backup").glob("articles_*.json"))[-1]
art = next(a for a in json.loads(backup.read_text()) if a["handle"] == handle and a["blog"]["handle"] == blog)
body = art["body"] or ""
(D / "current.html").write_text(body)

soup = BeautifulSoup(body, "html.parser")
blocks = {
    "PROOF": [str(x) for x in soup.select("div.fv-blog-proof")],
    "PRODUCTS": [str(x) for x in soup.select("div.fv-blog-product-wrap")],
    "IMAGE": [str(x.parent) for x in soup.find_all("img") if x.parent.name == "div"
              and "text-align: center" in (x.parent.get("style") or "")],
    "FOOTER": [str(x) for x in soup.find_all("table")][-1:],
}
# ---- fallbacks for older hand-edited posts whose blocks lack the standard classes ----
# Copied verbatim by position; nothing is typed by hand.
top = [c for c in soup.children if getattr(c, "name", None)]
blocks["LINKIMG"] = [str(c) for c in top if c.name in ("p", "h2", "h3", "div") and c.find("a", href=re.compile(r"/products/"))
                     and c.find("img") and not c.get_text(strip=True)]
blocks["CTA"] = [str(c) for c in top if c.name == "p" and c.find("a", href=re.compile(r"/products/"))
                 and not c.find("img") and len(c.get_text(" ", strip=True).split()) <= 30]
if not blocks["IMAGE"]:
    blocks["IMAGE"] = [str(c) for c in top if c.name == "p" and c.find("img") and not c.find("a") and not c.get_text(strip=True)
                       ]
if not blocks["PROOF"]:
    blocks["PROOF"] = [str(c) for c in top if c.name == "div" and any("verified" in (i.get("src") or "") for i in c.find_all("img"))][:1]
if not blocks["PRODUCTS"]:
    blocks["PRODUCTS"] = [str(c) for c in top if c.name == "div" and "Our Best Sellers" in c.get_text(" ", strip=True)[:40]]
tpl = (D / "template.html").read_text()


def fill(m):
    name, idx = m.group(1), m.group(2)
    items = blocks[name]
    i = int(idx) - 1 if idx else 0
    if i >= len(items):
        sys.exit(f"placeholder {m.group(0)} has no matching block in the live article")
    return items[i]


draft = re.sub(r"\{\{(PROOF|PRODUCTS|IMAGE|FOOTER|LINKIMG|CTA)(?:_(\d+))?\}\}", fill, tpl)


def reference_list(html: str) -> str:
    """Numbered list built from PubMed records, in order of first citation. Nothing typed by hand."""
    from pubmed import _get
    order = list(dict.fromkeys(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", html)))
    rec = json.loads(_get("esummary", {"db": "pubmed", "id": ",".join(order), "retmode": "json"}))["result"]
    items = []
    for p in order:
        x = rec[p]
        names = [a["name"] for a in x.get("authors") or []]
        au = ", ".join(names[:3]) + (", et al" if len(names) > 3 else "")
        items.append(f'<li>{au}. {x["title"].rstrip(".")}. <em>{x["source"]}</em>. {x["pubdate"][:4]}. '
                     f'<a href="https://pubmed.ncbi.nlm.nih.gov/{p}/" target="_blank" rel="noopener">PubMed</a></li>')
    return "<ol>\n" + "\n".join(items) + "\n</ol>"


if "{{REFERENCES}}" in draft:
    draft = draft.replace("{{REFERENCES}}", reference_list(draft))

# ---------- AI-artifact guard: never publish links to AI chats or pasted-chat markup ----------
AI_PAT = re.compile(r"chat\.openai\.com|chatgpt\.com|openai\.com|utm_source=(chatgpt|openai)|perplexity\.ai|gemini\.google|"
                    r"claude\.ai|copilot\.microsoft|user-content-fn|data-footnote-backref|oaicite|contentReference|turn0search|"
                    r"as an ai language model", re.I)
if AI_PAT.search(draft):
    sys.exit(f"AI artifact found in draft: {AI_PAT.search(draft).group(0)}")

# ---------- citation guard ----------
pmids = sorted(set(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", draft)))
refs = summaries(pmids)
bad = [r["pmid"] for r in refs if not r["title"]]
if bad:
    sys.exit(f"unverified PMIDs: {bad}")
for r in refs:
    if r["year"] not in draft:
        sys.exit(f"PMID {r['pmid']}: year {r['year']} not found in draft text")
# first author's surname must appear in the reference-list entry that links the PMID
for r in refs:
    first = (r["authors"].split(",")[0] or "").split(" ")[0]
    li = re.findall(r"<li>((?:(?!</li>).)*pubmed\.ncbi\.nlm\.nih\.gov/%s/(?:(?!</li>).)*)</li>" % r["pmid"], draft, re.S)
    if not li or first not in li[0]:
        sys.exit(f"PMID {r['pmid']}: reference entry missing or first author '{first}' not in it")
draft = enhance(draft, json.loads((D / "meta.json").read_text())["title"])
(D / "draft.html").write_text(draft)

# ---------- review file ----------
meta = json.loads((D / "meta.json").read_text())
txt = lambda h: BeautifulSoup(h, "html.parser").get_text(" ", strip=True)
words = lambda h: len(txt(h).split())
old_links = len(re.findall(r'href="[^"]*(?:pubmed|ncbi|doi\.org)', body))
L = [f"# Refresh draft: /blogs/{blog}/{handle}\n",
     f"- Live title: {art['title']}", f"- New title: {meta['title']}",
     f"- New SEO title: {meta.get('seo_title') or '(unchanged)'}",
     f"- New meta description: {meta.get('seo_description') or '(unchanged)'}",
     f"- Words: {words(body):,} → {words(draft):,}", f"- Study links: {old_links} → {len(pmids)}",
     f"- Product widgets, testimonial, images and footer: copied unchanged from the live article\n",
     "## What changed and why\n", *[f"- {n}" for n in meta["notes"]], "",
     "## Sources (each checked against its PubMed record)\n", "| PMID | Year | Study | Journal | Used for |", "|---|---|---|---|---|"]
for r in refs:
    L.append(f"| [{r['pmid']}]({r['url']}) | {r['year']} | {r['title']} | {r['journal']} | {meta['sources'].get(r['pmid'], '—')} |")
if meta.get("flags"):
    L += ["", "## For you to decide", *[f"- {f}" for f in meta["flags"]]]
(D / "review.md").write_text("\n".join(L) + "\n")
# readable local preview (Shopify's theme styles the real thing)
(D / "preview.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>{meta['title']}</title>
<style>body{{max-width:760px;margin:40px auto;padding:0 16px;font:17px/1.6 Georgia,serif;color:#222}}
img{{max-width:100%;height:auto}}.fv-blog-product-wrap,.fv-blog-proof{{border:1px dashed #bbb;padding:12px;margin:20px 0;font:14px sans-serif;color:#666}}
.fv-blog-products{{display:flex;gap:16px}}.fv-blog-product img{{max-width:140px}}a{{color:#0b5cad}}</style>
<h1>{meta['title']}</h1>{draft}""")
print(f"built {D}/draft.html: {words(draft):,} words, {len(pmids)} verified citations, blocks used: "
      f"{ {k: len(v) for k, v in blocks.items()} }")
