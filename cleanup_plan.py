"""Blog clean-up decision list + refresh candidates (pages that used to rank). Saved files only."""
import re
from collections import defaultdict

import numpy as np
import pandas as pd

import dataforseo_client as c

O, RAW, D = "data/processed/", "data/raw/", "2026-10-12"
pd.set_option("display.width", 260, "display.max_colwidth", 80)
TOPIC = re.compile("|".join(re.escape(t) for t in c.TOPIC_TERMS) + r"|hair health|hair follicle|bald|dht|scalp", re.I)
norm = lambda u: re.sub(r"^https?://(www\.)?", "https://", u.split("#")[0].split("?")[0].rstrip("/")).lower()
short = lambda u: u.replace("https://fullyvital.com", "")

card = pd.read_csv(O + "page_scorecard.csv")
inv = pd.read_csv(O + "content_inventory.csv")
a = card[card.type == "article"].merge(inv[["url", "h2_count", "external_link_count", "h1"]], on="url")
a["url_n"] = a.url.map(norm)
a["pub_year"] = a.published.str[:4]
text = (a.title.fillna("") + " " + a.url.str.split("/").str[-1].str.replace("-", " ") + " " + a.primary_keyword_guess.fillna(""))
a["in_scope"] = text.str.contains(TOPIC) | (a.blog == "hair-vitamins")

# positions before the first drop and now
pdte = pd.read_csv(RAW + f"gsc_page_date_{D}.csv")
pdte["url_n"] = pdte.page.map(norm)
def win(a0, b0, suffix):
    p = pdte[(pdte.date >= a0) & (pdte.date <= b0)]
    g = p.assign(pxi=p.position * p.impressions).groupby("url_n").agg(c=("clicks", "sum"), i=("impressions", "sum"), pxi=("pxi", "sum"))
    return pd.DataFrame({f"clicks_{suffix}": g.c, f"pos_{suffix}": g.pxi / g.i})
a = a.merge(win("2025-06-10", "2025-06-29", "jun2025"), on="url_n", how="left").merge(win("2026-07-01", "2026-09-23", "jul_sep2026"), on="url_n", how="left")
a["clicks_jun2025"] = a.clicks_jun2025.fillna(0)

# duplicate groups from cannibalization
can = pd.read_csv(O + "cannibalization.csv")
can["url_n"] = can.page.map(norm)
can = can[can.url_n.isin(set(a.url_n))]
pair = defaultdict(lambda: [0, 0])
for q, g in can.groupby("query"):
    us = sorted(g.url_n.unique())
    for i in range(len(us)):
        for j in range(i + 1, len(us)):
            pair[(us[i], us[j])][0] += 1
            pair[(us[i], us[j])][1] += g.q_impr.iloc[0]
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
edges = [(u, v, n, imp) for (u, v), (n, imp) in pair.items() if n >= 3 or imp >= 1500]
for u, v, _, _ in edges:
    parent[find(u)] = find(v)
a["dup_group"] = a.url_n.map(lambda u: find(u) if u in parent else None)
sizes = a.dup_group.value_counts()
a.loc[a.dup_group.map(sizes).fillna(0) < 2, "dup_group"] = None
keeper = a[a.dup_group.notna()].sort_values(["clicks_16m", "impressions_16m"], ascending=False).drop_duplicates("dup_group").set_index("dup_group").url
a["merge_target"] = a.dup_group.map(keeper)
pd.DataFrame(edges, columns=["url_a", "url_b", "shared_queries", "shared_query_impressions"]).to_csv(O + "blog_duplicate_pairs.csv", index=False)

def action(r):
    dup = isinstance(r.merge_target, str)
    if dup and r.merge_target != r.url:
        return "2 Merge into target, then 301"
    if dup:
        return "1 Keep as merge target and refresh"
    if r.pub_year == "2026":
        return "6 Leave (new in 2026, review at 6 months)"
    if (r.clicks_same3_last_year >= 10 or r.clicks_16m >= 20) and r.in_scope:
        return "3 Refresh (in scope, used to earn clicks)"
    if r.clicks_same3_last_year >= 10 or r.clicks_16m >= 20:
        return "5 Keep as is (off-topic but earned clicks)"
    if r.impressions_90d < 50 and r.clicks_16m <= 2:
        return "4a Rewrite or fold into a cluster page (in scope, no traffic)" if r.in_scope else "4b Remove or redirect (off-topic, no traffic)"
    return "7 Keep, monitor"
a["action"] = a.apply(action, axis=1)
cols = ["url", "action", "merge_target", "in_scope", "blog", "pub_year", "word_count", "clicks_16m", "clicks_90d", "impressions_90d", "clicks_jun2025", "pos_jun2025",
        "pos_jul_sep2026", "clicks_same3_last_year", "clicks_last3", "study_citation_count", "external_link_count", "primary_keyword_guess", "title"]
a.sort_values(["action", "clicks_16m"], ascending=[True, False])[cols].to_csv(O + "blog_cleanup_plan.csv", index=False)
print(a.groupby("action").agg(posts=("url", "size"), clicks_16m=("clicks_16m", "sum"), clicks_90d=("clicks_90d", "sum"), words=("word_count", "sum")).to_string())
print("dup groups:", a.dup_group.nunique(), "posts in groups:", int(a.dup_group.notna().sum()), "largest:", sizes[sizes >= 2].head(5).tolist())
for gname in list(sizes[sizes >= 2].index[:6]):
    g = a[a.dup_group == gname].sort_values("clicks_16m", ascending=False)
    print("  ", " | ".join(f"{short(u)} ({cl})" for u, cl in zip(g.url, g.clicks_16m)))
print("in scope:", int(a.in_scope.sum()), "off-topic:", int((~a.in_scope).sum()), "| off-topic share of clicks_16m:", round(a[~a.in_scope].clicks_16m.sum() / a.clicks_16m.sum(), 2),
      "| off-topic share of Jun-2025 clicks:", round(a[~a.in_scope].clicks_jun2025.sum() / a.clicks_jun2025.sum(), 2))
print("off-topic examples:", [short(u) for u in a[~a.in_scope].sort_values("clicks_16m", ascending=False).url.head(12)])

# uniformity / publishing pattern
old = a[a.pub_year.isin(["2023", "2024"])]
print("2023-24 posts:", len(old), "word count p25/p50/p75:", old.word_count.quantile([.25, .5, .75]).astype(int).tolist(), "h2 p25/p50/p75:", old.h2_count.quantile([.25, .5, .75]).astype(int).tolist(),
      "| titles with a colon:", round(old.title.str.contains(":").mean(), 2), "| with >=1 study link:", round((old.study_citation_count > 0).mean(), 2))
print("published per month, busiest:", inv[inv.type == "article"].published.str[:7].value_counts().head(8).to_dict())

# refresh candidates: pages that used to rank
ref = a[(a.clicks_same3_last_year >= 10) | (a.clicks_jun2025 >= 5)].copy()
ref = ref[ref.pub_year != "2026"].sort_values("clicks_jun2025", ascending=False)
ref["priority"] = np.where(ref.in_scope, "in scope", "off-topic")
ref[["url", "priority", "action", "clicks_jun2025", "pos_jun2025", "clicks_same3_last_year", "clicks_last3", "pos_jul_sep2026", "word_count", "study_citation_count",
     "external_link_count", "primary_keyword_guess"]].to_csv(O + "refresh_candidates.csv", index=False)
print("\nrefresh candidates:", len(ref), "in scope:", int(ref.in_scope.sum()), "| with zero study links:", int((ref.study_citation_count == 0).sum()),
      "| in-scope with zero study links:", int(((ref.study_citation_count == 0) & ref.in_scope).sum()))
x = ref[ref.in_scope].head(25).copy()
x["url"] = x.url.map(short)
print(x[["url", "clicks_jun2025", "pos_jun2025", "clicks_last3", "pos_jul_sep2026", "study_citation_count", "primary_keyword_guess"]].round(1).to_string())

ir = pd.read_csv(O + "index_status_sample.csv").merge(a[["url", "pub_year", "impressions_16m", "in_scope"]], on="url", how="left")
print(ir[ir.coverage != "Submitted and indexed"].groupby(["coverage", "pub_year"]).size().to_string())
print(ir[ir.coverage == "URL is unknown to Google"].url.map(short).head(6).tolist())
