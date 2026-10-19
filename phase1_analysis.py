"""
Phase 1F — analysis over saved files only (no API calls).

Reads data/raw + data/processed, writes one CSV per analysis to data/processed/ and
data/processed/phase1_stats.json (headline numbers for the report).

Usage:
    python phase1_analysis.py
"""

import glob
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

import dataforseo_client as c

RAW, OUT = Path("data/raw"), Path("data/processed")
D = "2026-10-12"
TOPIC = re.compile("|".join(re.escape(t) for t in c.TOPIC_TERMS), re.I)
GRAY = re.compile(r"gray|grey|white hair|hair color loss", re.I)
BRAND = re.compile(r"fully\s?vital|fullyvita", re.I)
LAST3, PRIOR_YEAR3, PREV3 = ["2026-07", "2026-08", "2026-09"], ["2025-07", "2025-08", "2025-09"], ["2026-04", "2026-05", "2026-06"]
MONTHS12 = [f"{y}-{m:02d}" for y, m in [(2025, 10), (2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 10)]]
stats = {}


def norm(u):
    if not isinstance(u, str):
        return u
    u = u.split("#")[0].split("?")[0].rstrip("/")
    return re.sub(r"^https?://(www\.)?", "https://", u).lower()


def scope(s: pd.Series) -> pd.Series:
    return s.fillna("").str.contains(TOPIC)


def cluster(s: pd.Series) -> pd.Series:
    return np.where(s.fillna("").str.contains(GRAY), "gray", "hair growth/loss")


# ---------- load ----------
inv = pd.read_csv(OUT / "content_inventory.csv")
inv["url_n"] = inv.url.map(norm)
pq = pd.read_csv(RAW / f"gsc_page_query_{D}.csv").dropna(subset=["query"])
pq90 = pd.read_csv(RAW / f"gsc_page_query_90d_{D}.csv").dropna(subset=["query"])
q = pd.read_csv(RAW / f"gsc_query_{D}.csv").dropna(subset=["query"])
pg = pd.read_csv(RAW / f"gsc_page_{D}.csv")
pg90 = pd.read_csv(RAW / f"gsc_page_90d_{D}.csv")
pm = pd.read_csv(RAW / f"gsc_page_monthly_{D}.csv")
dt = pd.read_csv(RAW / f"gsc_date_{D}.csv")
for df in (pq, pq90, pg, pg90, pm):
    df["url_n"] = df.page.map(norm)


def by_query_url(df):
    """Collapse URL variants (query strings, e.g. Shopify product_sync variants) to one row per query + clean URL."""
    df = df.assign(pxi=df.position * df.impressions)
    g = df.groupby(["query", "url_n"], as_index=False).agg(clicks=("clicks", "sum"), impressions=("impressions", "sum"), pxi=("pxi", "sum"))
    g["position"], g["ctr"], g["page"] = g.pxi / g.impressions, g.clicks / g.impressions, g.url_n
    return g.drop(columns="pxi")


pq, pq90 = by_query_url(pq), by_query_url(pq90)
fv_all = pd.read_csv(OUT / "dfs_ranked_keywords_fullyvital.csv")
fv_scope = pd.read_csv(OUT / "dfs_ranked_keywords_in_scope_fullyvital.csv")
comp_kw = pd.read_csv(OUT / "dfs_competitor_keywords_in_scope_top20.csv")
comp_sum = pd.read_csv(OUT / "dfs_competitor_summary.csv")


def agg_pages(df):
    df = df.assign(pxi=df.position * df.impressions)
    g = df.groupby("url_n", as_index=False).agg(clicks=("clicks", "sum"), impressions=("impressions", "sum"), pxi=("pxi", "sum"))
    g["position"] = g.pxi / g.impressions
    return g.drop(columns="pxi")


# ---------- visibility ----------
q["in_scope"], q["brand"] = scope(q["query"]), q["query"].str.contains(BRAND)
qs = q[q.in_scope & ~q.brand].assign(cluster=lambda x: cluster(x["query"]))
stats["gsc"] = {
    "range": "2025-06-10..2026-10-09",
    "site_clicks": int(dt.clicks.sum()), "site_impressions": int(dt.impressions.sum()),
    "query_level_clicks": int(q.clicks.sum()), "query_level_impressions": int(q.impressions.sum()),
    "anonymized_click_share": round(1 - q.clicks.sum() / dt.clicks.sum(), 3),
    "anonymized_impression_share": round(1 - q.impressions.sum() / dt.impressions.sum(), 3),
    "brand_clicks": int(q[q.brand].clicks.sum()), "brand_impressions": int(q[q.brand].impressions.sum()),
    "in_scope_nonbrand_queries": int(len(qs)), "in_scope_nonbrand_clicks": int(qs.clicks.sum()),
    "in_scope_nonbrand_impressions": int(qs.impressions.sum()),
    "by_cluster": qs.groupby("cluster").agg(queries=("query", "size"), clicks=("clicks", "sum"),
                                            impressions=("impressions", "sum")).astype(int).to_dict("index"),
    "in_scope_top3": int((qs.position <= 3).sum()), "in_scope_top10": int((qs.position <= 10).sum()),
    "in_scope_top20": int((qs.position <= 20).sum()),
}
dt["month"] = dt.date.str[:7]
site_m = dt.groupby("month").agg(clicks=("clicks", "sum"), impressions=("impressions", "sum")).astype(int)
site_m.to_csv(OUT / "site_monthly_trend.csv")
stats["site_monthly"] = site_m.reset_index().to_dict("records")
k = fv_scope.sort_values("position").drop_duplicates("keyword")
stats["dfs_fullyvital"] = {
    "total_ranked_keywords": 6694, "in_scope_keywords": int(len(k)),
    "top3": int((k.position <= 3).sum()), "top10": int((k.position <= 10).sum()), "top20": int((k.position <= 20).sum()),
    "gray_keywords": int(k.keyword.str.contains(GRAY).sum()),
    "gray_top10": int((k[k.keyword.str.contains(GRAY)].position <= 10).sum()),
    "gray_top20": int((k[k.keyword.str.contains(GRAY)].position <= 20).sum()),
}

# ---------- 1. page scorecard ----------
p16, p90 = agg_pages(pg), agg_pages(pg90)
topq = (pq.sort_values(["clicks", "impressions"], ascending=False).groupby("url_n")["query"]
        .apply(lambda s: " | ".join(s.head(5))).rename("top5_queries"))
nb = pq[~pq["query"].str.contains(BRAND)]
primary = nb.sort_values("impressions", ascending=False).drop_duplicates("url_n").set_index("url_n")["query"].rename("primary_keyword_guess")
mwide = pm.pivot_table(index="url_n", columns="month", values="clicks", aggfunc="sum").reindex(columns=sorted(pm.month.unique())).fillna(0)
trend = pd.DataFrame({
    "clicks_12m_by_month": mwide.reindex(columns=MONTHS12).fillna(0).astype(int).astype(str).agg(",".join, axis=1),
    "clicks_last3": mwide.reindex(columns=LAST3).fillna(0).sum(axis=1),
    "clicks_same3_last_year": mwide.reindex(columns=PRIOR_YEAR3).fillna(0).sum(axis=1),
    "clicks_prev3": mwide.reindex(columns=PREV3).fillna(0).sum(axis=1),
})
fv_union = pd.concat([fv_all, fv_scope]).drop_duplicates(["keyword", "url"]).assign(url_n=lambda x: x.url.map(norm))
dfs_pg = fv_union.groupby("url_n").agg(dfs_keywords=("keyword", "size"), dfs_top10=("position", lambda s: int((s <= 10).sum())),
                                       dfs_etv=("etv", "sum"))
card = (inv[["url", "url_n", "type", "blog", "title", "word_count", "published", "updated", "sitemap_lastmod", "author",
             "product_link_count", "study_citation_count"]]
        .merge(p16.rename(columns={"clicks": "clicks_16m", "impressions": "impressions_16m", "position": "avg_position_16m"}), on="url_n", how="left")
        .merge(p90.rename(columns={"clicks": "clicks_90d", "impressions": "impressions_90d", "position": "avg_position_90d"}), on="url_n", how="left")
        .merge(topq, on="url_n", how="left").merge(primary, on="url_n", how="left")
        .merge(trend, on="url_n", how="left").merge(dfs_pg, on="url_n", how="left"))
for col in ["clicks_16m", "impressions_16m", "clicks_90d", "impressions_90d", "clicks_last3", "clicks_same3_last_year", "clicks_prev3"]:
    card[col] = card[col].fillna(0).astype(int)
card["in_scope_primary"] = scope(card.primary_keyword_guess)
card.sort_values("clicks_16m", ascending=False).to_csv(OUT / "page_scorecard.csv", index=False)
art = card[card.type == "article"]
stats["inventory"] = {
    "articles": int(len(art)), "pages": int((card.type == "page").sum()),
    "by_blog": art.blog.value_counts().to_dict(),
    "median_word_count": float(art.word_count.median()),
    "articles_with_byline": int(inv[inv.type == "article"].has_byline.sum()),
    "authors": inv[inv.type == "article"].author.value_counts().head(5).to_dict(),
    "articles_with_study_citation": int((art.study_citation_count > 0).sum()),
    "articles_with_any_external_link": int((inv[inv.type == "article"].external_link_count > 0).sum()),
    "articles_with_product_link": int((art.product_link_count > 0).sum()),
    "schema_types": inv[inv.type == "article"].schema_types.value_counts().head(4).to_dict(),
    "published_by_year": inv[inv.type == "article"].published.str[:4].value_counts().sort_index().to_dict(),
    "lastmod_by_year": inv[inv.type == "article"].sitemap_lastmod.str[:4].value_counts().sort_index().to_dict(),
    "articles_zero_clicks_16m": int((art.clicks_16m == 0).sum()),
    "articles_clicks_16m": int(art.clicks_16m.sum()),
    "top10_articles_click_share": round(art.clicks_16m.nlargest(10).sum() / max(1, art.clicks_16m.sum()), 3),
    "gsc_pages_not_in_inventory_clicks": int(p16[~p16.url_n.isin(inv.url_n)].clicks.sum()),
}
by_type = p16.assign(kind=np.select(
    [p16.url_n.str.contains("/blogs/"), p16.url_n.str.contains("/products/"), p16.url_n.str.contains("/collections/"),
     p16.url_n.str.contains("/pages/"), p16.url_n.eq("https://fullyvital.com")],
    ["blog", "product", "collection", "page", "home"], "other")).groupby("kind")[["clicks", "impressions"]].sum().astype(int)
stats["gsc_by_page_type"] = by_type.to_dict("index")

# ---------- 2. striking distance (last 90 days) ----------
nb16 = pq[~pq["query"].str.contains(BRAND)].assign(pos=lambda x: x.position.round().clip(1, 20))
ctr_curve = nb16[nb16.position <= 20.5].groupby("pos").agg(clicks=("clicks", "sum"), impressions=("impressions", "sum"))
ctr_curve["ctr"] = ctr_curve.clicks / ctr_curve.impressions
ctr_curve.to_csv(OUT / "own_ctr_curve_nonbrand.csv")
target_ctr = float(ctr_curve.loc[[1.0, 2.0, 3.0]].clicks.sum() / ctr_curve.loc[[1.0, 2.0, 3.0]].impressions.sum())
stats["own_nonbrand_ctr_top3"] = round(target_ctr, 4)
sd = pq90[(pq90.position >= 4) & (pq90.position <= 20) & (pq90.impressions >= 100) & ~pq90["query"].str.contains(BRAND)].copy()
sd["in_scope"], sd["cluster"] = scope(sd["query"]), cluster(sd["query"])
sd["expected_click_gain_90d"] = (sd.impressions * (target_ctr - sd.ctr).clip(lower=0)).round(1)
vol = pd.concat([fv_union[["keyword", "volume", "kd", "intent"]]]).drop_duplicates("keyword").rename(columns={"keyword": "query"})
sd = sd.merge(vol, on="query", how="left").sort_values("expected_click_gain_90d", ascending=False)
sd[["query", "page", "clicks", "impressions", "ctr", "position", "expected_click_gain_90d", "in_scope", "cluster", "volume", "kd", "intent"]] \
    .to_csv(OUT / "striking_distance.csv", index=False)
stats["striking_distance"] = {"pairs": int(len(sd)), "in_scope_pairs": int(sd.in_scope.sum()),
                              "in_scope_expected_gain_90d": float(sd[sd.in_scope].expected_click_gain_90d.sum())}

# ---------- 3. cannibalization (16 months) ----------
cq = pq[~pq["query"].str.contains(BRAND)].copy()
cq["q_impr"] = cq.groupby("query").impressions.transform("sum")
cq["share"] = cq.impressions / cq.q_impr
cq = cq[(cq.q_impr >= 200) & (cq.share >= 0.10)]
cq["n_urls"] = cq.groupby("query").page.transform("nunique")
cq = cq[cq.n_urls >= 2].sort_values(["q_impr", "query", "share"], ascending=[False, True, False])
cq["in_scope"] = scope(cq["query"])
cq[["query", "q_impr", "n_urls", "page", "impressions", "share", "clicks", "position", "in_scope"]].to_csv(OUT / "cannibalization.csv", index=False)
can = cq.groupby("query").agg(total_impressions=("q_impr", "first"), urls=("n_urls", "first"), in_scope=("in_scope", "first"),
                              clicks=("clicks", "sum"), best_position=("position", "min"),
                              pages=("url_n", lambda s: " | ".join(u.split("fullyvital.com")[1] for u in s))) \
    .sort_values("total_impressions", ascending=False)
can.to_csv(OUT / "cannibalization_by_query.csv")
stats["cannibalization"] = {"queries": int(len(can)), "in_scope_queries": int(can.in_scope.sum())}

# ---------- 4. decay ----------
dec = card[(card.clicks_same3_last_year >= 10)].copy()
dec["change_yoy"] = dec.clicks_last3 / dec.clicks_same3_last_year - 1
dec = dec[dec.change_yoy <= -0.30].sort_values("clicks_same3_last_year", ascending=False)
dec[["url", "type", "clicks_same3_last_year", "clicks_last3", "change_yoy", "clicks_prev3", "primary_keyword_guess", "word_count",
     "sitemap_lastmod"]].to_csv(OUT / "decay.csv", index=False)
elig = card[card.clicks_same3_last_year >= 10]
stats["decay"] = {"pages_with_10plus_clicks_last_year_window": int(len(elig)), "decayed_30pct": int(len(dec)),
                  "clicks_lost": int((dec.clicks_same3_last_year - dec.clicks_last3).sum()),
                  "all_pages_clicks_jul_sep_2025": int(mwide.reindex(columns=PRIOR_YEAR3).sum().sum()),
                  "all_pages_clicks_jul_sep_2026": int(mwide.reindex(columns=LAST3).sum().sum())}

# ---------- 5. zero performers ----------
zp = art[art.impressions_90d < 50].sort_values("impressions_16m")
zp[["url", "blog", "title", "word_count", "published", "sitemap_lastmod", "impressions_90d", "clicks_90d", "impressions_16m", "clicks_16m"]] \
    .to_csv(OUT / "zero_performers.csv", index=False)
stats["zero_performers"] = {"articles_under_50_impr_90d": int(len(zp)), "of_articles": int(len(art)),
                            "with_zero_impr_90d": int((zp.impressions_90d == 0).sum()),
                            "words_total": int(zp.word_count.sum())}

# ---------- 6. keyword gap ----------
fv_pos = fv_scope.groupby("keyword").position.min()
g = comp_kw.sort_values("position").drop_duplicates(["keyword", "domain"])
gap = g.groupby("keyword").agg(competitors=("domain", "nunique"), best_competitor_position=("position", "min"),
                               volume=("volume", "max"), kd=("kd", "max"), intent=("intent", "first"),
                               who=("domain", lambda s: ", ".join(f"{d}" for d in s)),
                               positions=("position", lambda s: ", ".join(str(int(p)) for p in s)))
gap["fullyvital_position"] = gap.index.map(fv_pos)
gap = gap[(gap.competitors >= 2) & (gap.fullyvital_position.isna() | (gap.fullyvital_position > 50))]
gap["cluster"] = cluster(gap.index.to_series())
# competition strength of the current top 10, from the raw Labs rows (avg_backlinks_info)
bl = {}
for p in glob.glob("data/raw/dataforseo/*ranked_keywords*"):
    for i in json.load(open(p))["tasks"][0]["result"][0]["items"] or []:
        kd_ = i["keyword_data"]
        b = kd_.get("avg_backlinks_info") or {}
        bl[kd_["keyword"]] = (b.get("main_domain_rank"), b.get("referring_main_domains"), b.get("rank"))
gap["top10_avg_domain_rank"] = [bl.get(x, (None,) * 3)[0] for x in gap.index]
gap["top10_avg_page_ref_domains"] = [bl.get(x, (None,) * 3)[1] for x in gap.index]
gap = gap.sort_values("volume", ascending=False)
gap.to_csv(OUT / "keyword_gap.csv")
stats["keyword_gap"] = {"keywords": int(len(gap)), "volume_sum": int(gap.volume.sum()),
                        "by_cluster": gap.groupby("cluster").agg(keywords=("volume", "size"), volume=("volume", "sum")).astype(int).to_dict("index"),
                        "fullyvital_absent": int(gap.fullyvital_position.isna().sum()),
                        "by_intent": gap.intent.value_counts().to_dict()}

# ---------- 7. authority gap ----------
fvb = json.loads((OUT / "dfs_backlinks_summary_fullyvital.json").read_text())
fvo = pd.read_csv(OUT / "dfs_domain_rank_overview_fullyvital.csv").iloc[0]
me = {"domain": "fullyvital.com", "organic_etv": fvo["metrics.organic.etv"], "organic_keywords": fvo["metrics.organic.count"],
      "top3": fvo["metrics.organic.pos_1"] + fvo["metrics.organic.pos_2_3"],
      "top10": fvo["metrics.organic.pos_1"] + fvo["metrics.organic.pos_2_3"] + fvo["metrics.organic.pos_4_10"],
      "rank": fvb.get("rank"), "backlinks": fvb.get("backlinks"), "referring_domains": fvb.get("referring_domains"),
      "referring_main_domains": fvb.get("referring_main_domains"),
      "in_scope_top20_keywords": stats["dfs_fullyvital"]["top20"]}
auth = pd.concat([pd.DataFrame([me]), comp_sum.drop(columns=["in_scope_top20_rows", "max_position_seen"])], ignore_index=True)
auth["etv_per_keyword"] = auth.organic_etv / auth.organic_keywords
auth["top10_share"] = auth.top10 / auth.organic_keywords
auth.to_csv(OUT / "authority_gap.csv", index=False)

(OUT / "phase1_stats.json").write_text(json.dumps(stats, indent=1, default=str))
print(json.dumps(stats, indent=1, default=str))
