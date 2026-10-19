"""
Review every live hair-growth article against the four hair-growth hubs (read-only).

For each live growth article: traffic, top queries, status (refreshed / new in 2026 / calendar / control),
which hub topic it belongs to, and whether it already links to that hub.
For each hub: which existing pages already get Google impressions for the hub's searches (cannibalization check).

Usage: python growth_corpus_review.py
Outputs: data/processed/growth_corpus_review.csv, data/processed/growth_hub_query_overlap.csv
"""
import json
import re
from pathlib import Path

import pandas as pd

O = "data/processed/"
arts = json.loads(sorted(Path("data/shopify_backup").glob("articles_*.json"))[-1].read_text())
path = lambda a: f"/blogs/{a['blog']['handle']}/{a['handle']}"
live = {path(a): a for a in arts if a["isPublished"]}
m = pd.read_csv(O + "phase2_page_cluster_map.csv").drop_duplicates("path").set_index("path")
strip = lambda u: re.sub(r"^https?://[^/]+", "", str(u)).split("?")[0].rstrip("/")
# refresh test: keys are treated pages, values their controls
_rc = json.load(open(O + "refresh_controls.json"))
TEST = {strip(u): ("treated" if u in _rc else "control") for k, v in _rc.items() for u in [k, *v]}
cal = set(pd.read_csv("data/reference/hair_growth_content_calendar.csv").shopify_url.str.replace("https://fullyvital.com", "").str.rstrip("/"))
pq = pd.read_csv("data/raw/gsc_page_query_2026-10-12.csv").assign(path=lambda d: d.page.map(strip))
pg = pq.groupby("path")[["clicks", "impressions"]].sum()

HUBS = {
    "stop": "/blogs/hair-care/how-to-stop-hair-loss",
    "oils": "/blogs/hair-care/rosemary-oil-for-hair-growth",
    "vitamins": "/blogs/hair-care/best-hair-growth-vitamins",
    "foods": "/blogs/hair-care/foods-for-hair-growth",
}
GRAY = re.compile(r"gr[ae]y|white hair|silver|pigment|melanin", re.I)
# topic rules on handle + title, first match wins
TOPIC = [
    ("foods", r"protein|food|diet|\beat|egg|nutrition|whey|keravis|creatine|collagen"),
    ("oils", r"\boil\b|-oil|rosemary|essential-oils?|peppermint|lavender|tea-tree|castor|batana|jojoba|argan|coconut"),
    ("vitamins", r"vitamin|biotin|zinc|\biron\b|-iron|selenium|folate|b12|magnesium|supplement|mineral|deficien|silica|prenatal|multivitamin|nutrafol|viviscal"),
    ("stop", r"hair-loss|thinning|balding|bald|shedding|alopecia|regrow|grow-back|minoxidil|finasteride|dutasteride|dht|receding|hairline|crown|telogen|derma-?roller|microneedl|laser|prp|pattern|hair-fall"),
]
# searches each hub should own
HUBQ = {
    "stop": r"(how to|ways to|can you|best way to)?\s*(stop|prevent|reduce|reverse|treat|cure|fix)\w*\s.*(hair loss|thinning|balding|hair fall)|(hair loss|thinning hair|hair thinning)\s(treatment|remed|solution|cure)",
    "oils": r"rosemary|hair (growth )?oils?\b|oils? for hair (growth|loss)|best oils? for hair",
    "vitamins": r"(vitamins?|supplements?)\s(for|to)\s.*hair (growth|loss|thinning)|hair (growth |loss )?(vitamins|supplements)|best vitamins? for hair|which vitamin",
    "foods": r"foods?\s(for|to|that).*hair|protein.*hair (growth|loss)|eggs? (for|and) hair|diet.*hair (growth|loss)|hair growth foods?",
}

rows = []
for p, a in live.items():
    text = f"{a['handle'].replace('-', ' ')} {a['title']}"
    line = m.line.get(p) if p in m.index else ("gray" if GRAY.search(text) else "growth")
    if line != "growth" or GRAY.search(a["handle"]):
        continue
    topic = next((t for t, r in TOPIC if re.search(r, a["handle"] + " " + a["title"].lower())), "other")
    q = pq[pq.path == p].sort_values("impressions", ascending=False)
    body = a["body"] or ""
    rows.append({"path": p, "title": a["title"], "status": m.status.get(p) if p in m.index else "new in 2026",
                 "phase2_cluster": m.cluster.get(p) if p in m.index else None, "hub_topic": topic,
                 "is_hub": p in HUBS.values(), "calendar": p in cal, "refresh_test": TEST.get(p),
                 "clicks_16m": int(pg.clicks.get(p, 0)), "impressions_16m": int(pg.impressions.get(p, 0)),
                 "top_queries": " | ".join(q["query"].head(3)),
                 "links_to_hub": (HUBS[topic] in body) if topic in HUBS else None})
df = pd.DataFrame(rows).sort_values(["hub_topic", "impressions_16m"], ascending=[True, False])
df.to_csv(O + "growth_corpus_review.csv", index=False)

ov = []
for h, r in HUBQ.items():
    qq = pq[pq["query"].str.contains(r, regex=True, case=False) & ~pq["query"].str.contains(GRAY)]
    g = qq.groupby("path").agg(impressions=("impressions", "sum"), clicks=("clicks", "sum"), queries=("query", "nunique"),
                               best_pos=("position", "min"), example=("query", "first")).reset_index()
    g = g[g.path.isin(live)].sort_values("impressions", ascending=False)
    g.insert(0, "hub", h)
    ov.append(g)
ov = pd.concat(ov)
ov.to_csv(O + "growth_hub_query_overlap.csv", index=False)

pd.set_option("display.width", 250, "display.max_colwidth", 70, "display.max_rows", 500)
print("live hair-growth articles:", len(df), "| by topic:", df.hub_topic.value_counts().to_dict())
print(df.groupby("hub_topic")[["clicks_16m", "impressions_16m"]].sum())
for h in HUBS:
    print(f"\n=== {h}: pages already getting impressions for the hub's searches")
    print(ov[ov.hub == h].head(12).to_string(index=False))
