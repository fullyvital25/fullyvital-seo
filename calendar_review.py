"""
Review a content-calendar CSV (e.g. data/reference/hair_growth_content_calendar.csv), read-only.

Per article: live/indexed, traffic, demand (calendar volume + Phase 2 data), claim wording, survey statistics,
study links, AI-chat artifacts, links to its cluster pillar, and overlap with OTHER live posts on the same topic.

Usage:
    python calendar_review.py data/reference/hair_growth_content_calendar.csv growth
Outputs: data/processed/<prefix>_calendar_review.csv, data/processed/<prefix>_calendar_overlap.csv
"""
import json
import re
import sys
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

cal_path, prefix = sys.argv[1], sys.argv[2]
O = "data/processed/"
norm = lambda u: re.sub(r"^https?://(www\.)?", "https://", str(u).split("?")[0].rstrip("/")).lower()
short = lambda u: str(u).replace("https://fullyvital.com", "")
cal = pd.read_csv(cal_path)
cal["u"] = cal.shopify_url.map(norm)
arts = {norm(f"https://fullyvital.com/blogs/{a['blog']['handle']}/{a['handle']}"): a
        for a in json.loads(sorted(Path("data/shopify_backup").glob("articles_*.json"))[-1].read_text())}
idx = pd.read_csv(O + "index_status_all.csv").assign(u=lambda d: d.url.map(norm)).set_index("u").coverage
pg = pd.read_csv("data/raw/gsc_page_2026-10-12.csv").assign(u=lambda d: d.page.map(norm)).groupby("u")[["clicks", "impressions"]].sum()
uni = pd.read_csv(O + "phase2_keyword_universe.csv")
CLAIM = re.compile(r"\b(cur(e|es|ed|ing)|treat(s|ed|ing|ment)?|prevent(s|ed|ing)?|revers\w*|regrow\w*|stop(s|ped)? (hair loss|shedding|thinning)|clinically proven|guarantee\w*|heal(s|ed)?)\b", re.I)
OURS = re.compile(r"fully\s?vital|\bour (serum|supplement|formula|system|kit|products?)\b|hair revival|this (serum|system|formula|kit)", re.I)
NEG = re.compile(r"\bno (study|product|supplement|serum)|isn't|not (been )?(shown|proven)|can't|cannot|doesn't|won't", re.I)
SURVEY = re.compile(r"survey[^.]{0,160}\d{2}%|\d{2}%[^.]{0,160}survey", re.I)
AI = re.compile(r"chat\.openai\.com|chatgpt\.com|utm_source=(chatgpt|openai)|user-content-fn|data-footnote-backref|oaicite|contentReference", re.I)
STOP = set("for the and of to in a is with on does do can how what your my are it be you i vs or".split())
toks = lambda t: {re.sub(r"(ies|es|s)$", "", w) for w in re.findall(r"[a-z0-9]+", str(t).lower()) if w not in STOP}

rows, overlaps = [], []
others = {u: a for u, a in arts.items() if a["isPublished"] and u not in set(cal.u)}
for r in cal.itertuples():
    a = arts.get(r.u)
    body = (a or {}).get("body") or ""
    text = BeautifulSoup(body, "html.parser").get_text(" ", strip=True)
    sents = re.split(r"(?<=[.!?])\s+", text)
    prod_claims = [x.strip()[:200] for x in sents if OURS.search(x) and CLAIM.search(x) and not NEG.search(x)]
    head = " ".join(filter(None, [a.get("title") if a else "", ((a or {}).get("seoTitle") or {}).get("value", "") if a and a.get("seoTitle") else "",
                                  ((a or {}).get("seoDescription") or {}).get("value", "") if a and a.get("seoDescription") else ""]))
    links = {norm(h if h.startswith("http") else "https://fullyvital.com" + h) for h in re.findall(r'href="([^"]+)"', body) if "/blogs/" in h}
    pillar = cal[(cal.cluster == r.cluster) & (cal.role.isin(["pillar", "hub"]))].u
    pillar = pillar.iat[0] if len(pillar) else None
    ex = uni[uni.keyword == str(r.primary_query).lower()].volume.dropna()
    rows.append({"url": short(r.shopify_url), "cluster": r.cluster, "role": r.role, "primary_query": r.primary_query,
                 "calendar_volume": r.monthly_volume, "dfs_volume": ex.iat[0] if len(ex) else None,
                 "live": bool(a and a.get("isPublished")), "index": idx.get(r.u), "clicks_16m": pg.clicks.get(r.u, 0), "impressions_16m": pg.impressions.get(r.u, 0),
                 "words": len(text.split()), "pubmed_links": len(set(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", body))),
                 "study_links_any": len(re.findall(r'href="[^"]*(?:pubmed|ncbi|doi\.org|sciencedirect|nature\.com|elifesciences|frontiersin|jamanetwork)', body)),
                 "ai_artifacts": len(AI.findall(body)), "survey_stats": len(SURVEY.findall(text)),
                 "claim_in_title_meta": bool(CLAIM.search(head)), "title": a.get("title") if a else None,
                 "product_claim_sentences": len(prod_claims), "product_claim_example": prod_claims[0] if prod_claims else "",
                 "links_to_pillar": (pillar in links) if (pillar and r.role not in ("pillar", "hub")) else None})
    # overlap with older live posts: shared topic words in the URL slug
    st = toks(r.u.rsplit("/", 1)[-1].replace("-", " ") + " " + str(r.primary_query)) - {"hair", "loss", "growth"}
    for u, oa in others.items():
        ot = toks(u.rsplit("/", 1)[-1].replace("-", " ")) - {"hair", "loss", "growth"}
        shared = st & ot
        if len(shared) >= 2 and len(shared) / max(1, len(st | ot)) >= 0.4:
            overlaps.append({"calendar_post": short(r.shopify_url), "other_live_post": short(u), "shared_words": " ".join(sorted(shared)),
                             "other_clicks_16m": pg.clicks.get(u, 0), "other_index": idx.get(u)})
rv = pd.DataFrame(rows); ov = pd.DataFrame(overlaps)
rv.to_csv(O + f"{prefix}_calendar_review.csv", index=False); ov.to_csv(O + f"{prefix}_calendar_overlap.csv", index=False)
pd.set_option("display.width", 260, "display.max_colwidth", 120)
print("articles:", len(rv), "| live:", int(rv.live.sum()), "| index:", rv["index"].value_counts(dropna=False).to_dict())
print("clicks:", int(rv.clicks_16m.sum()), "| impressions:", int(rv.impressions_16m.sum()), "| AI artifacts:", int(rv.ai_artifacts.sum()), "| survey stats on", int((rv.survey_stats > 0).sum()), "pages")
print("claim in title/meta:", int(rv.claim_in_title_meta.sum()), "| product-tied claim sentences on", int((rv.product_claim_sentences > 0).sum()), "pages")
print("no study links:", int((rv.study_links_any == 0).sum()), "| spokes linking to pillar:", int(rv.links_to_pillar.fillna(False).sum()), "of", int(rv.links_to_pillar.notna().sum()))
print(rv[["url", "cluster", "role", "calendar_volume", "dfs_volume", "index", "words", "study_links_any", "survey_stats", "product_claim_sentences", "links_to_pillar"]].to_string(index=False))
print("\nclaims in title/meta:"); print(rv[rv.claim_in_title_meta][["url", "title"]].to_string(index=False))
print("\nproduct-tied claims:"); print(rv[rv.product_claim_sentences > 0][["url", "product_claim_example"]].to_string(index=False))
print("\noverlap with older live posts:", len(ov)); print(ov.to_string(index=False) if len(ov) else "")
