"""
Phase 1C / 1D — DataForSEO pulls for fullyvital.com (live API, via dataforseo_client only).

Usage:
    python phase1_dfs.py 1c
    python phase1_dfs.py 1d "<kw1>" "<kw2>" ...
"""

import json
import sys
from pathlib import Path

import pandas as pd

import dataforseo_client as c

assert not c.IS_SANDBOX, "switch DATAFORSEO_BASE back to live"
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)
T = "fullyvital.com"
d = c.DFS()


def finish(tag: str, bal0: float):
    s = d.summary()
    s.to_csv(OUT / f"dfs_spend_{tag}.csv", index=False)
    bal1 = d.balance()["balance_usd"]
    print(s.groupby("endpoint").agg(calls=("cost_usd", "size"), rows=("rows", "sum"),
                                    cost=("cost_usd", "sum")).to_string())
    print(f"spent(log)=${s.cost_usd.sum():.4f}  balance {bal0} -> {bal1}  diff=${bal0 - bal1:.4f}")


def step_1c():
    bal0 = d.balance()["balance_usd"]
    rk = d.ranked_keywords(T, limit=1000)
    rk.to_csv(OUT / "dfs_ranked_keywords_fullyvital.csv", index=False)
    sc = d.ranked_keywords_in_scope(T)
    sc.to_csv(OUT / "dfs_ranked_keywords_in_scope_fullyvital.csv", index=False)
    ov = d.domain_rank_overview(T)
    ov.to_csv(OUT / "dfs_domain_rank_overview_fullyvital.csv", index=False)
    rp = d.relevant_pages(T, limit=100)
    rp.to_csv(OUT / "dfs_relevant_pages_fullyvital.csv", index=False)
    try:
        bl = d.backlinks_summary(T)
    except RuntimeError as e:
        bl = {"error": str(e)}
    (OUT / "dfs_backlinks_summary_fullyvital.json").write_text(json.dumps(bl))
    print("ranked:", rk.shape, "in-scope:", sc.shape, "pages:", rp.shape)
    print("backlinks:", bl)
    pat = "|".join(c.TOPIC_TERMS)
    print("in-scope rows not matching a topic term:", int((~sc.keyword.str.contains(pat, case=False)).sum()))
    print("in-scope by position:", pd.cut(sc.position, [0, 3, 10, 20, 100]).value_counts().sort_index().to_dict())
    cols = [x for x in ov.columns if x.startswith("metrics.organic.") and "clickstream" not in x]
    print(ov[cols].iloc[0].to_dict() if len(ov) else "no overview")
    print(sc.sort_values("volume", ascending=False).head(25).to_string())
    finish("1c", bal0)


def step_1d(keywords: list[str]):
    bal0 = d.balance()["balance_usd"]
    comp = d.competitors_domain(T, limit=20)
    comp.to_csv(OUT / "dfs_competitors_domain_fullyvital.csv", index=False)
    serps = pd.concat([d.serp(k) for k in keywords], ignore_index=True)
    serps.to_csv(OUT / "dfs_serp_seed_keywords.csv", index=False)
    keep = ["domain", "avg_position", "intersections", "full_domain_metrics.organic.etv",
            "full_domain_metrics.organic.count", "metrics.organic.etv", "metrics.organic.count"]
    print(comp[[k for k in keep if k in comp.columns]].to_string())
    serps["domain"] = serps.domain.str.replace(r"^www\.", "", regex=True)
    agg = serps.groupby("domain").agg(serps=("keyword", "nunique"), best=("position", "min"),
                                      avg=("position", "mean")).sort_values(["serps", "avg"], ascending=[False, True])
    print(agg.head(45).to_string())
    print("rows per keyword:", serps.groupby("keyword").size().to_dict())
    finish("1d", bal0)


def step_1e(competitors: list[str]):
    bal0 = d.balance()["balance_usd"]
    kws, pages, summary = [], [], []
    for comp in competitors:
        ov = d.domain_rank_overview(comp)
        try:
            bl = d.backlinks_summary(comp)
        except RuntimeError as e:
            bl = {"error": str(e)}
        k = d.ranked_keywords_in_scope(comp, limit_per_chunk=500, max_position=20)
        rp = d.relevant_pages(comp, limit=50)
        kws.append(k.assign(domain=comp))
        pages.append(rp.assign(domain=comp))
        o = ov.iloc[0] if len(ov) else {}
        summary.append({
            "domain": comp, "organic_etv": o.get("metrics.organic.etv"),
            "organic_keywords": o.get("metrics.organic.count"),
            "top3": (o.get("metrics.organic.pos_1") or 0) + (o.get("metrics.organic.pos_2_3") or 0),
            "top10": (o.get("metrics.organic.pos_1") or 0) + (o.get("metrics.organic.pos_2_3") or 0)
                     + (o.get("metrics.organic.pos_4_10") or 0),
            "rank": bl.get("rank"), "backlinks": bl.get("backlinks"),
            "referring_domains": bl.get("referring_domains"),
            "referring_main_domains": bl.get("referring_main_domains"),
            "in_scope_top20_rows": len(k), "in_scope_top20_keywords": k.keyword.nunique() if len(k) else 0,
            "max_position_seen": k.position.max() if len(k) else None,
        })
        print(comp, "in-scope top20 rows:", len(k), flush=True)
    pd.concat(kws, ignore_index=True).to_csv(OUT / "dfs_competitor_keywords_in_scope_top20.csv", index=False)
    pd.concat(pages, ignore_index=True).to_csv(OUT / "dfs_competitor_relevant_pages.csv", index=False)
    sm = pd.DataFrame(summary)
    sm.to_csv(OUT / "dfs_competitor_summary.csv", index=False)
    print(sm.to_string())
    finish("1e", bal0)


if __name__ == "__main__":
    {"1c": step_1c, "1d": lambda: step_1d(sys.argv[2:]), "1e": lambda: step_1e(sys.argv[2:])}[sys.argv[1]]()
