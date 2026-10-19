"""Phase 1F.8 / 1F.9 — compliance flags (articles, pages, products) and E-E-A-T comparison vs competitor samples."""
import json
import re

import pandas as pd
from bs4 import BeautifulSoup

import crawl_inventory as ci

OUT = "data/processed/"
inv = pd.read_csv(OUT + "content_inventory.csv")
sm = json.loads(ci.SITEMAP.read_text())
products = [u for k, v in sm.items() if "sitemap_products" in k for u, _ in v if "/products/" in u]

REVERSE = re.compile(r"\brevers\w*\s+(?:\w+\s+){0,3}?(?:gray|grey|white)\w*|\b(?:gray|grey|white) hair\s+(?:\w+\s+){0,2}?revers\w*", re.I)
CLAIM = re.compile(r"\b(cur(?:e|es|ed|ing)|treat(?:s|ed|ing|ment)?|prevent(?:s|ed|ing|ion)?|heal(?:s|ed|ing)?|"
                   r"stop(?:s|ped|ping)?\s+(?:hair loss|balding|gray|grey)|regrow(?:s|th|ing)?|clinically proven|fda[- ]approved|guarantee\w*)\b", re.I)
DISEASE = re.compile(r"\b(alopecia|baldness|androgenetic|telogen effluvium|pcos|thyroid|cancer|chemo\w*|lupus|diabet\w+|"
                     r"psoriasis|dermatitis|eczema|anemia|hair loss|infection|disease|disorder|hormonal imbalance)\b", re.I)
OURS = re.compile(r"fully\s?vital|\bour (?:\w+\s){0,3}?(?:serum|supplement|product|formula|vitamin|system|bundle|roller)s?\b|enhance hair", re.I)
SPLIT = re.compile(r"(?<=[.!?])\s+")


def text_of(html, article):
    soup = BeautifulSoup(html, "lxml")
    body = None
    for sel in ([".fv-article-col .prose", ".prose"] if article else []) + ["main"]:
        cands = soup.select(sel)
        if cands:
            body = max(cands, key=lambda x: len(x.get_text()))
            break
    for junk in (body.select("script,style,noscript,nav,form") if body else []):
        junk.decompose()
    head = " ".join(filter(None, [soup.title.get_text(" ", strip=True) if soup.title else "",
                                  ci.meta(soup, name="description") or "",
                                  " ".join(h.get_text(" ", strip=True) for h in soup.find_all("h1"))]))
    return head, (body.get_text(" ", strip=True) if body else "")


rows = []
targets = [(u, t) for u, t in zip(inv.url, inv.type)] + [(u, "product") for u in products]
for url, kind in targets:
    html, status = ci.fetch(url)
    if status != 200:
        rows.append({"url": url, "type": kind, "http_status": status})
        continue
    head, body = text_of(html, kind == "article")
    sents = SPLIT.split(body)
    rev = [s for s in sents if REVERSE.search(s)]
    own_dis = [s for s in sents if OURS.search(s) and CLAIM.search(s) and DISEASE.search(s)]
    own_rev = [s for s in rev if OURS.search(s)]
    rows.append({
        "url": url, "type": kind, "http_status": 200,
        "head_reverse_gray": bool(REVERSE.search(head)),
        "head_disease_claim": bool(CLAIM.search(head) and DISEASE.search(head)),
        "head_text": head[:300],
        "reverse_gray_sentences": len(rev),
        "product_reverse_gray_sentences": len(own_rev),
        "product_disease_claim_sentences": len(own_dis),
        "example_product_reverse": (own_rev[0][:300] if own_rev else ""),
        "example_product_disease": (own_dis[0][:300] if own_dis else ""),
        "example_reverse": (rev[0][:300] if rev else ""),
        "has_fda_disclaimer": bool(re.search(r"not been evaluated by the food and drug|not intended to diagnose", body, re.I)),
    })
cf = pd.DataFrame(rows)
cf["severity"] = (3 * (cf.type == "product") * ((cf.product_reverse_gray_sentences > 0) | (cf.reverse_gray_sentences > 0) | (cf.product_disease_claim_sentences > 0) | cf.head_reverse_gray | cf.head_disease_claim)
                  + 2 * cf.head_reverse_gray.fillna(False) + 2 * (cf.product_reverse_gray_sentences > 0)
                  + 2 * (cf.product_disease_claim_sentences > 0) + 1 * cf.head_disease_claim.fillna(False))
cf = cf.sort_values(["severity", "product_disease_claim_sentences"], ascending=False)
cf.to_csv(OUT + "compliance_flags.csv", index=False)
ok = cf[cf.http_status == 200]
print("scanned", len(ok), "errors", int((cf.http_status != 200).sum()))
print(ok.groupby("type").agg(n=("url", "size"), head_reverse=("head_reverse_gray", "sum"), any_reverse=("reverse_gray_sentences", lambda s: (s > 0).sum()),
                             product_reverse=("product_reverse_gray_sentences", lambda s: (s > 0).sum()),
                             head_disease=("head_disease_claim", "sum"),
                             product_disease=("product_disease_claim_sentences", lambda s: (s > 0).sum()),
                             fda_disclaimer=("has_fda_disclaimer", "sum")).to_string())
pd.set_option("display.width", 300, "display.max_colwidth", 230)
for kind in ["product", "page", "article"]:
    x = ok[(ok.type == kind) & (ok.severity > 0)].head(7)
    for r in x.itertuples():
        print(f"[{kind}] sev={r.severity} {r.url.replace('https://fullyvital.com','')}\n    HEAD: {r.head_text[:160]}\n    REV: {(r.example_product_reverse or r.example_reverse)[:220]}\n    DIS: {r.example_product_disease[:220]}")

# ---------- E-E-A-T: sample of competitor articles ----------
ck = pd.read_csv(OUT + "dfs_competitor_keywords_in_scope_top20.csv")
blogish = ck[ck.url.str.contains(r"/blog|/blogs/|/article|/learn|/journal|/guide|/conditions|/hair-loss/|/news", case=False, na=False)]
top = (blogish.groupby(["domain", "url"]).agg(kws=("keyword", "size"), etv=("etv", "sum")).reset_index()
       .sort_values(["domain", "kws"], ascending=[True, False]).groupby("domain").head(3))
erows = []
for r in top.itertuples():
    try:
        html, status = ci.fetch(r.url)
        if status != 200:
            erows.append({"domain": r.domain, "url": r.url, "http_status": status})
            continue
        p = ci.parse(r.url, html, None)
        erows.append({"domain": r.domain, "url": r.url, "http_status": 200, "kws_top20": r.kws,
                      **{k: p[k] for k in ["word_count", "h2_count", "has_byline", "author", "schema_types", "published", "updated",
                                           "external_link_count", "study_citation_count", "body_selector"]},
                      "mentions_reviewer": bool(re.search(r"(medically |clinically )?reviewed by|fact[- ]checked", BeautifulSoup(html, "lxml").get_text(" "), re.I))})
    except Exception as e:
        erows.append({"domain": r.domain, "url": r.url, "http_status": repr(e)[:60]})
ee = pd.DataFrame(erows)
ee.to_csv(OUT + "eeat_competitor_sample.csv", index=False)
print(ee.drop(columns=["url"]).to_string())
a = inv[inv.type == "article"]
txt_reviewed = 0
for u in a.url.sample(60, random_state=1):
    h, _ = ci.fetch(u)
    txt_reviewed += bool(re.search(r"(medically |clinically )?reviewed by|fact[- ]checked", BeautifulSoup(h, "lxml").get_text(" "), re.I))
print("FV: reviewed-by mention in 60-article sample:", txt_reviewed, "| median citations", a.study_citation_count.median(), "mean", round(a.study_citation_count.mean(), 2),
      "| share with >=1 citation", round((a.study_citation_count > 0).mean(), 3), "| share with updated date in schema", round(a.updated.notna().mean(), 3))
