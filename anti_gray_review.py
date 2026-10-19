"""
Review of the 66 anti-gray articles in data/reference/anti_gray_content_calendar.csv (read-only).

Per article: live state, traffic (GSC), index status, demand for its primary query, compliance wording,
citations, AI-chat artifacts, internal links to its cluster, and overlap with other FullyVital pages.

Outputs: data/processed/anti_gray_review.csv, data/processed/anti_gray_overlap.csv, reports/anti-gray-review.md
"""
import json
import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

O, RAW = "data/processed/", "data/raw/"
norm = lambda u: re.sub(r"^https?://(www\.)?", "https://", str(u).split("?")[0].split("#")[0].rstrip("/")).lower()
short = lambda u: str(u).replace("https://fullyvital.com", "")
CLAIM = re.compile(r"\b(revers\w*|cure[sd]?|treat(s|ed|ing|ment)?|prevent(s|ed|ing|ion)?|restor\w*|repigment\w*|clinically proven|guarantee\w*|"
                   r"\d{2,3}% (saw|of (users|customers|people|participants))|stop(s|ped)? gr[ae]y)\b", re.I)
AI = re.compile(r"chat\.openai\.com|chatgpt\.com|utm_source=(chatgpt|openai)|user-content-fn|data-footnote-backref|oaicite|contentReference|turn0search", re.I)

cal = pd.read_csv("data/reference/anti_gray_content_calendar.csv")
cal["url_n"] = cal.shopify_url.map(norm)
backup = sorted(Path("data/shopify_backup").glob("articles_*.json"))[-1]
arts = {norm(f"https://fullyvital.com/blogs/{a['blog']['handle']}/{a['handle']}"): a for a in json.loads(backup.read_text())}
idx = pd.read_csv(O + "index_status_all.csv").assign(url_n=lambda d: d.url.map(norm)).set_index("url_n")
pg = pd.read_csv(RAW + "gsc_page_2026-10-12.csv").assign(url_n=lambda d: d.page.map(norm)).groupby("url_n")[["clicks", "impressions"]].sum()
pg90 = pd.read_csv(RAW + "gsc_page_90d_2026-10-12.csv").assign(url_n=lambda d: d.page.map(norm)).groupby("url_n")[["clicks", "impressions"]].sum()
pq = pd.read_csv(RAW + "gsc_page_query_2026-10-12.csv").dropna(subset=["query"]).assign(url_n=lambda d: d.page.map(norm))
uni = pd.read_csv(O + "phase2_keyword_universe.csv")
aeo = pd.read_csv(O + "aeo_tracking.csv")
aeo = aeo[aeo.run == aeo.run.max()].set_index("keyword")
STOP = set("for the and of to in a is with on does do can how what your my are it be you i".split())
stems = lambda t: {("gray" if w in ("grey", "greying", "graying") else re.sub(r"(ies|es|s)$", "", w)) for w in re.findall(r"[a-z0-9]+", str(t).lower()) if w not in STOP}
uni["st"] = uni.keyword.map(stems)


def demand(q):
    """Exact match volume if known, else the largest volume among close variants (>=75% word overlap)."""
    q = str(q).lower()
    ex = uni[uni.keyword == q].volume.dropna()
    if len(ex):
        return ex.iat[0], "exact"
    s = stems(q)
    m = uni[uni.st.map(lambda k: len(s & k) / max(1, len(s | k)) >= 0.75)].volume.dropna()
    return (m.max(), "close variant") if len(m) else (None, "no data")


rows = []
for r in cal.itertuples():
    a = arts.get(r.url_n)
    body = (a or {}).get("body") or ""
    soup = BeautifulSoup(body, "html.parser")
    text = soup.get_text(" ", strip=True)
    head = " ".join(filter(None, [a.get("title") if a else "", ((a or {}).get("seoTitle") or {}).get("value", "") if a and a.get("seoTitle") else "",
                                  ((a or {}).get("seoDescription") or {}).get("value", "") if a and a.get("seoDescription") else ""]))
    sents = re.split(r"(?<=[.!?])\s+", text)
    claim_s = [x.strip()[:200] for x in sents if CLAIM.search(x) and not re.search(r"\bno (study|product|research)|isn't|not (been )?(shown|proven)|can't|cannot|doesn't", x, re.I)]
    links = [norm(h if h.startswith("http") else "https://fullyvital.com" + h) for h in re.findall(r'href="([^"]+)"', body) if "/blogs/" in h]
    siblings = set(cal[(cal.cluster == r.cluster) & (cal.url_n != r.url_n)].url_n)
    pillar = cal[(cal.cluster == r.cluster) & (cal.role == "pillar")].url_n
    pillar = pillar.iat[0] if len(pillar) else None
    vol, how = demand(r.primary_query)
    ix = idx.coverage.get(r.url_n) if r.url_n in idx.index else None
    rows.append({
        "url": short(r.shopify_url), "cluster": r.cluster, "role": r.role, "primary_query": r.primary_query, "intent": r.intent,
        "published": str(r.date_published)[:10], "live": bool(a and a.get("isPublished")),
        "words": len(text.split()), "pubmed_links": len(set(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", body))),
        "study_links_any": len(re.findall(r'href="[^"]*(?:pubmed|ncbi|doi\.org|sciencedirect|nature\.com|elifesciences|frontiersin)', body)),
        "ai_artifacts": len(AI.findall(body)),
        "claim_in_title_meta": bool(CLAIM.search(head)), "title": a.get("title") if a else None,
        "claim_sentences": len(claim_s), "claim_example": claim_s[0] if claim_s else "",
        "links_to_siblings": len(set(links) & siblings), "siblings": len(siblings),
        "links_to_pillar": (pillar in links) if (pillar and r.role == "spoke") else None,
        "query_volume": vol, "volume_source": how,
        "clicks_16m": pg.clicks.get(r.url_n, 0), "impressions_16m": pg.impressions.get(r.url_n, 0),
        "clicks_90d": pg90.clicks.get(r.url_n, 0), "impressions_90d": pg90.impressions.get(r.url_n, 0),
        "index": ix,
        "aio_present": aeo.has_ai_overview.get(str(r.primary_query).lower()) if str(r.primary_query).lower() in aeo.index else None,
    })
rv = pd.DataFrame(rows)
rv.to_csv(O + "anti_gray_review.csv", index=False)

# overlap: queries where 2+ anti-gray (or other gray) pages each get >=15% of impressions
gray_pages = set(cal.url_n) | {u for u in arts if re.search(r"gr[ae]y", u)}
x = pq[pq.url_n.isin(gray_pages)].groupby(["query", "url_n"], as_index=False).impressions.sum()
x["q_tot"] = x.groupby("query").impressions.transform("sum")
x["share"] = x.impressions / x.q_tot
ov = x[(x.q_tot >= 50) & (x.share >= 0.15)]
ov = ov[ov.groupby("query").url_n.transform("nunique") >= 2]
pairs = (ov.groupby("query").agg(impressions=("q_tot", "first"), pages=("url_n", lambda s: " | ".join(sorted(short(u) for u in s))))
         .reset_index().sort_values("impressions", ascending=False))
pairs.to_csv(O + "anti_gray_overlap.csv", index=False)
not_in_cal = sorted(short(u) for u, a in arts.items() if a.get("isPublished") and re.search(r"gr[ae]y", u) and u not in set(cal.url_n)
                    and (a.get("publishedAt") or "")[:4] == "2026")

pd.set_option("display.width", 250, "display.max_colwidth", 70)
print("articles:", len(rv), "| live:", int(rv.live.sum()), "| index:", rv["index"].value_counts().to_dict())
print("clicks 16m total:", int(rv.clicks_16m.sum()), "| impressions 16m:", int(rv.impressions_16m.sum()), "| 90d clicks:", int(rv.clicks_90d.sum()))
print("claim in title/meta:", int(rv.claim_in_title_meta.sum()), "| with claim sentences:", int((rv.claim_sentences > 0).sum()), "| AI artifacts:", int(rv.ai_artifacts.sum()))
print("pubmed links: 0 ->", int((rv.pubmed_links == 0).sum()), "| any study links 0 ->", int((rv.study_links_any == 0).sum()), "| median words", rv.words.median())
print("spokes linking to pillar:", int(rv.links_to_pillar.fillna(False).sum()), "of", int(rv.role.eq("spoke").sum()))
print(rv.groupby("cluster").agg(n=("url", "size"), clicks16=("clicks_16m", "sum"), impr16=("impressions_16m", "sum"), demand=("query_volume", "sum"),
                                not_indexed=("index", lambda s: int((s != "Submitted and indexed").sum()))).sort_values("demand", ascending=False).to_string())
print("\noverlap queries:", len(pairs)); print(pairs.head(15).to_string(index=False))
print("\ngray 2026 posts not in calendar:", not_in_cal)
print("\nclaims in title/meta:"); print(rv[rv.claim_in_title_meta][["url", "title"]].to_string(index=False))
