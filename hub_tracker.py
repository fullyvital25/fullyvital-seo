"""
Track the hubs published on 2026-10-18 (read-only).

Groups, fixed at the first run (data/processed/hub_clusters.json):
  hub page + cluster = live articles linking to the hub at baseline + old URLs that now 301 to it.
Metrics (Search Console, page x date, blog pages, cached per run date):
  - 28 days before the change (baseline) vs the latest 28 days (after), for the hub page and its cluster.
  - Target searches: impressions, clicks and average position for each hub's head-term queries
    (page x query, latest 90 days; baseline from the 2026-10-12 pull).
  - Indexing: URL Inspection for each hub (read-only), with --inspect.

Usage:
    python hub_tracker.py             # baseline on first run, comparison after (rerun every 2-4 weeks)
    python hub_tracker.py --inspect   # also check whether Google has indexed each hub
Outputs: data/processed/hub_tracking.csv, data/processed/hub_tracking_queries.csv, reports/hub-tracking.md
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

import gsc_pull as g
from shopify_client import Shopify

CHANGE = date(2026, 10, 18)
TODAY = date.today()
END = TODAY - timedelta(days=3)
RAW_DATE = Path(f"data/raw/gsc_page_date_hubs_{TODAY}.csv")
RAW_QUERY = Path(f"data/raw/gsc_page_query_hubs_{TODAY}.csv")
RAW_INSPECT = Path(f"data/raw/gsc_url_inspection_hubs_{TODAY}.json")
CLUSTERS = Path("data/processed/hub_clusters.json")
B = "/blogs/hair-care/"
norm = lambda u: re.sub(r"^https?://(www\.)?[^/]+", "", str(u)).split("?")[0].split("#")[0].rstrip("/").lower()

# hub: (path, head-term query regex)
HUBS = {
    "Hair: how to stop hair loss": (B + "how-to-stop-hair-loss", r"(stop|prevent|reduce)\w* (hair loss|thinning|hair fall)|hair loss (treatment|remed)"),
    "Hair: vitamins": (B + "best-hair-growth-vitamins", r"vitamins? (for|to) .*hair|hair (growth )?vitamins|supplements? for hair|hair growth supplements"),
    "Hair: rosemary & oils": (B + "rosemary-oil-for-hair-growth", r"rosemary"),
    "Hair: protein & foods": (B + "foods-for-hair-growth", r"foods? (for|to|that) .*hair|protein .*hair|eggs? (for|and) hair"),
    "Hair: biotin": (B + "is-biotin-good-for-hair", r"biotin"),
    "Hair: receding hairline": (B + "receding-hairlines", r"hairline|temples"),
    "Hair: growth cycle": (B + "hair-cycle", r"hair (growth )?cycle|stages of hair|how (long|fast) .*hair.*grow|hair grow.* (per|a) (month|day)|anagen|catagen|hairs on (a|the) (human )?head"),
    "Hair: types of alopecia": (B + "types-of-alopecia", r"(?<!areata )alopecia(?! areata)|types of hair loss|scarring alopecia"),
    "Hair: alopecia areata": (B + "alopecia-areata", r"alopecia areata|alopecia universalis|alopecia totalis"),
    "Hair: serums": (B + "best-hair-growth-serums", r"serum"),
    "Hair: shampoo for thinning hair": (B + "thinning-hair-shampoo", r"shampoo.*(thin|hair loss|regrow|growth)|(thin|hair loss|regrow).*shampoo"),
    "Hair: styling": (B + "hairstyles-for-thinning-hair", r"(hairstyle|haircut|hair cut|cut).*(thin|hair loss|balding|receding)|(thin|hair loss|receding).*(hairstyle|haircut)"),
    "Hair: minoxidil & finasteride": (B + "minoxidil", r"minoxidil|finasteride|dutasteride|spironolactone|rogaine|propecia"),
    "Gray: causes": (B + "what-causes-gray-hair", r"(cause|reason)s? .*gr[ae]y|why .*gr[ae]y"),
    "Gray: premature": (B + "why-am-i-going-gray-causes-explained", r"(premature|early|young|20s|teen).*gr[ae]y|gr[ae]y.*(premature|early|young)"),
    "Gray: men": (B + "gray-hair-in-men", r"gr[ae]y.*\bmen\b|\bmen\b.*gr[ae]y|greying men|graying men"),
    "Gray: B12": (B + "vitamin-b12-deficiency-gray-hair", r"b12.*gr[ae]y|gr[ae]y.*b12"),
    "Gray: vitamins": (B + "vitamins-for-gray-hair", r"vitamin.*gr[ae]y|gr[ae]y.*vitamin|deficien.*gr[ae]y"),
    "Gray: stress": (B + "can-stress-cause-gray-hair", r"stress.*gr[ae]y|gr[ae]y.*stress"),
    "Gray: prevent": (B + "how-to-prevent-gray-hair-naturally", r"(prevent|stop|slow)\w* .*gr[ae]y"),
    "Gray: myths & white vs gray": (B + "gray-hair-myths-vs-facts", r"white .*gr[ae]y|gr[ae]y .*white|pluck|myth"),
    "Gray: products": (B + "best-anti-gray-hair-supplements-2026", r"(best|anti).?gr[ae]y.*(supplement|product|serum)|gr[ae]y hair (supplement|product)s?"),
}


def clusters() -> dict:
    if CLUSTERS.exists():
        return json.loads(CLUSTERS.read_text())
    s = Shopify()
    arts = {f"/blogs/{a['blog']['handle']}/{a['handle']}": a for a in s.articles()}
    reds = s.redirects()
    out = {}
    for k, (hub, _) in HUBS.items():
        linking = sorted(p for p, a in arts.items() if a["isPublished"] and p != hub and f"https://fullyvital.com{hub}" in (a["body"] or ""))
        merged = sorted(norm(r["path"]) for r in reds if norm(r["target"]) == hub)
        out[k] = {"hub": hub, "linking": linking, "merged": merged}
    CLUSTERS.write_text(json.dumps({"fixed_on": str(TODAY), **out}, indent=1))
    return json.loads(CLUSTERS.read_text())


def pull(raw, dims, start):
    if raw.exists():
        return pd.read_csv(raw)
    rows, start_row = [], 0
    while True:
        res = g.execute("GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY", {
            "site_url": g.SITE, "start_date": str(start), "end_date": str(END), "dimensions": dims,
            "row_limit": g.ROW_LIMIT, "start_row": start_row, "search_type": "web",
            "dimension_filter_groups": [{"filters": [{"dimension": "page", "operator": "contains", "expression": "/blogs/"}]}]})
        batch = res.get("rows") or []
        rows += [{**dict(zip(dims, r["keys"])), "clicks": r["clicks"], "impressions": r["impressions"], "position": r["position"]} for r in batch]
        if len(batch) < g.ROW_LIMIT:
            break
        start_row += g.ROW_LIMIT
    df = pd.DataFrame(rows)
    df.to_csv(raw, index=False)
    return df


def window(df, paths, a, b):
    x = df[df.path.isin(paths) & (df.date >= str(a)) & (df.date <= str(b))]
    imp = x.impressions.sum()
    return {"clicks": int(x.clicks.sum()), "impressions": int(imp),
            "position": round((x.position * x.impressions).sum() / imp, 1) if imp else None}


def main():
    cl = clusters()
    pdd = pull(RAW_DATE, ["page", "date"], CHANGE - timedelta(days=120)).assign(path=lambda d: d.page.map(norm))
    pre_a, pre_b = CHANGE - timedelta(days=28), CHANGE - timedelta(days=1)
    post_a = max(CHANGE + timedelta(days=1), END - timedelta(days=27))
    rows = []
    for k, c in cl.items():
        if k == "fixed_on":
            continue
        group = [c["hub"]] + c["linking"] + c["merged"]
        r = {"hub": k, "page": c["hub"], "linking_pages": len(c["linking"]), "merged_urls": len(c["merged"])}
        for name, paths in [("hub", [c["hub"]]), ("cluster", group)]:
            for w, (a, b) in [("pre28", (pre_a, pre_b)), ("post", (post_a, END))]:
                for m, v in window(pdd, paths, a, b).items():
                    r[f"{name}_{w}_{m}"] = v
        r["post_days"] = max(0, (END - post_a).days + 1)
        rows.append(r)
    t = pd.DataFrame(rows)
    t.to_csv("data/processed/hub_tracking.csv", index=False)

    # target searches: baseline from the 2026-10-12 90-day pull, latest from a fresh 90-day pull
    base_q = pd.read_csv("data/raw/gsc_page_query_90d_2026-10-12.csv")
    now_q = pull(RAW_QUERY, ["page", "query"], END - timedelta(days=89)) if (END - CHANGE).days >= 14 else None
    qrows = []
    for k, (hub, rx) in HUBS.items():
        for label, q in [("baseline_90d", base_q), ("latest_90d", now_q)]:
            if q is None:
                continue
            x = q[q["query"].str.contains(rx, case=False, regex=True)]
            imp = x.impressions.sum()
            on_hub = x[x.page.map(norm) == hub]
            qrows.append({"hub": k, "window": label, "queries": x["query"].nunique(), "impressions": int(imp), "clicks": int(x.clicks.sum()),
                          "avg_position": round((x.position * x.impressions).sum() / imp, 1) if imp else None,
                          "hub_page_impressions": int(on_hub.impressions.sum()),
                          "hub_page_position": round((on_hub.position * on_hub.impressions).sum() / on_hub.impressions.sum(), 1) if on_hub.impressions.sum() else None})
    qt = pd.DataFrame(qrows)
    qt.to_csv("data/processed/hub_tracking_queries.csv", index=False)

    ins = None
    if "--inspect" in sys.argv:
        ins = json.loads(RAW_INSPECT.read_text()) if RAW_INSPECT.exists() else {}
        for k, (hub, _) in HUBS.items():
            u = "https://fullyvital.com" + hub
            if u not in ins:
                try:
                    ins[u] = g.execute("GOOGLE_SEARCH_CONSOLE_INSPECT_URL", {"site_url": g.SITE, "inspection_url": u, "language_code": "en-US"})
                except Exception as e:
                    ins[u] = {"error": str(e)[:300]}
        RAW_INSPECT.write_text(json.dumps(ins))
    report(t, qt, ins, pre_a, pre_b, post_a)


def report(t, qt, ins, pre_a, pre_b, post_a):
    L = ["# Hub tracking", "",
         f"Hubs published or rebuilt on {CHANGE}. Search Console data to {END}.",
         f"- **Before:** the 28 days {pre_a}–{pre_b}.",
         f"- **After:** {post_a}–{END}" + (" (no data after the change yet)." if END <= CHANGE else "."),
         "- **Cluster:** the hub, every page that linked to it when tracking started, and old URLs that now redirect to it.",
         "- Rerun every 2–4 weeks with `python hub_tracker.py --inspect`. Google usually needs 4–8 weeks to reflect changes.", "",
         "| Hub | Linking / merged | Hub clicks before → after | Hub impressions before → after | Cluster clicks before → after | Cluster impressions before → after |",
         "|---|---|---|---|---|---|"]
    f = lambda v: "—" if v is None or (isinstance(v, float) and pd.isna(v)) else f"{v:,}"
    for r in t.itertuples():
        L.append(f"| {r.hub} (`{r.page.replace('/blogs/hair-care/', '')}`) | {r.linking_pages} / {r.merged_urls} | {f(r.hub_pre28_clicks)} → {f(r.hub_post_clicks) if r.post_days else '—'} | "
                 f"{f(r.hub_pre28_impressions)} → {f(r.hub_post_impressions) if r.post_days else '—'} | {f(r.cluster_pre28_clicks)} → {f(r.cluster_post_clicks) if r.post_days else '—'} | "
                 f"{f(r.cluster_pre28_impressions)} → {f(r.cluster_post_impressions) if r.post_days else '—'} |")
    L += ["", "## Target searches (sitewide, 90 days)", "",
          "Which page Google shows for each hub's head terms. The goal is for the hub page to take most of these impressions, at a better position.", "",
          "| Hub | Window | Matching queries | Impressions | Clicks | Avg position | Impressions on the hub page | Hub page position |", "|---|---|---|---|---|---|---|---|"]
    for r in qt.itertuples():
        L.append(f"| {r.hub} | {r.window} | {r.queries:,} | {r.impressions:,} | {r.clicks:,} | {f(r.avg_position)} | {r.hub_page_impressions:,} | {f(r.hub_page_position)} |")
    if ins is not None:
        L += ["", "## Indexing (URL Inspection)", "", "| Hub page | Coverage | Last crawl |", "|---|---|---|"]
        for u, v in ins.items():
            s = (v.get("inspectionResult") or {}).get("indexStatusResult") or {}
            L.append(f"| `{u.replace('https://fullyvital.com/blogs/hair-care/', '')}` | {s.get('coverageState') or v.get('error', '?')[:60]} | {(s.get('lastCrawlTime') or '')[:10]} |")
    Path("reports/hub-tracking.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:40]))


if __name__ == "__main__":
    main()
