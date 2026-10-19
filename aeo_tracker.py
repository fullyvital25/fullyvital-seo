"""
Monthly AEO/GEO tracker: for each priority search, is there an AI Overview, does it cite FullyVital,
where does FullyVital rank organically, and which People Also Ask questions appear.

Keywords = Phase 2 priority-cluster head terms + anti-gray pillar queries (+ data/reference/aeo_keywords_extra.txt).
Each run pulls fresh SERPs (cost ~$0.002 each), keeps raw JSON in data/raw/aeo/<date>/, and appends results.

Outputs:
    data/processed/aeo_tracking.csv            one row per keyword per run
    data/processed/aeo_ai_overview_refs.csv    every AI Overview citation per run
    reports/aeo-tracking.md

Usage:
    python aeo_tracker.py            # monthly
"""
import json
import time
from datetime import date
from pathlib import Path

import pandas as pd

import dataforseo_client as c

TODAY = str(date.today())
RAW = Path(f"data/raw/aeo/{TODAY}")
OUT, REFS = Path("data/processed/aeo_tracking.csv"), Path("data/processed/aeo_ai_overview_refs.csv")


def keywords() -> list[str]:
    cl = pd.read_csv("data/processed/phase2_cluster_scores.csv")
    pri = cl[(cl.score > 0) & ~cl.cluster.str.endswith("general") &
             (((cl.line == "gray") & (cl.line_rank <= 10)) | ((cl.line == "growth") & (cl.line_rank <= 20)))]
    cal = pd.read_csv("data/reference/anti_gray_content_calendar.csv")
    kws = list(pri.head_term) + list(cal[cal.role == "pillar"].primary_query)
    extra = Path("data/reference/aeo_keywords_extra.txt")
    if extra.exists():
        kws += [k.strip() for k in extra.read_text().splitlines() if k.strip()]
    return list(dict.fromkeys(k.lower() for k in kws))


def main():
    kws = keywords()
    print(f"{len(kws)} keywords; estimate ${len(kws) * 0.002:.2f}")
    d = c.DFS()
    RAW.mkdir(parents=True, exist_ok=True)
    rows, refs = [], []
    for k in kws:
        f = RAW / f"{k.replace(' ', '_')[:80]}.json"
        if f.exists():  # resume: today's result already saved, don't pay twice
            r = json.loads(f.read_text())
            if "organic" not in r:  # raw DataForSEO response saved by an earlier run
                r = c.parse_serp_features(r, k)
        else:
            r = None
            for attempt in range(3):
                try:
                    r = d.serp_features(k, refresh=True)
                    break
                except RuntimeError as e:
                    err = str(e)
                    time.sleep(5 * (attempt + 1))
            if r is None:
                rows.append({"run": TODAY, "keyword": k, "error": err[:120]})
                continue
            r.pop("_raw")
            f.write_text(json.dumps(r))
        fv_org = [o["position"] for o in r["organic"] if o["domain"] and "fullyvital" in o["domain"]]
        fv_ref = [x for x in r["ai_overview_refs"] if x["domain"] and "fullyvital" in x["domain"]]
        rows.append({"run": TODAY, "keyword": k, "has_ai_overview": r["has_ai_overview"], "aio_refs": len(r["ai_overview_refs"]),
                     "fullyvital_cited_in_aio": bool(fv_ref), "fullyvital_aio_url": fv_ref[0]["url"] if fv_ref else None,
                     "fullyvital_organic_position": min(fv_org) if fv_org else None, "has_featured_snippet": r["has_featured_snippet"],
                     "people_also_ask": " | ".join(r["people_also_ask"])})
        refs += [{"run": TODAY, "keyword": k, **x} for x in r["ai_overview_refs"]]
    new, newr = pd.DataFrame(rows), pd.DataFrame(refs)
    hist = pd.concat([pd.read_csv(OUT), new]) if OUT.exists() else new
    histr = pd.concat([pd.read_csv(REFS), newr]) if REFS.exists() else newr
    hist = hist.drop_duplicates(["run", "keyword"], keep="last"); hist.to_csv(OUT, index=False)
    new = new[new.get("error").isna()] if "error" in new else new
    histr.to_csv(REFS, index=False)
    s = d.summary(); spent = s.cost_usd.sum()

    runs = hist.groupby("run").agg(keywords=("keyword", "size"), with_aio=("has_ai_overview", "sum"),
                                   fv_cited=("fullyvital_cited_in_aio", "sum"),
                                   fv_top10=("fullyvital_organic_position", lambda x: int((x <= 10).sum()))).reset_index()
    top = newr.assign(domain=newr.domain.str.replace(r"^www\.", "", regex=True)).domain.value_counts().head(15)
    L = ["# AEO / GEO tracking\n", f"Latest run {TODAY}: {len(new)} priority searches. Cost ${spent:.2f}.\n",
         "| Run | Searches | With AI Overview | FullyVital cited in AI Overview | FullyVital organic top 10 |", "|---|---|---|---|---|"]
    L += [f"| {r.run} | {r.keywords} | {r.with_aio} | {r.fv_cited} | {r.fv_top10} |" for r in runs.itertuples()]
    L += ["\n## Most-cited sources in AI Overviews (latest run)\n", "| Domain | Citations |", "|---|---|"]
    L += [f"| {dm} | {n} |" for dm, n in top.items()]
    L += ["\n## FullyVital per search (latest run)\n", "| Search | AI Overview | FullyVital cited | FullyVital organic position |", "|---|---|---|---|"]
    L += [f"| {r.keyword} | {'yes' if r.has_ai_overview else 'no'} | {r.fullyvital_aio_url or 'no'} | "
          f"{int(r.fullyvital_organic_position) if pd.notna(r.fullyvital_organic_position) else '—'} |" for r in new.itertuples()]
    Path("reports/aeo-tracking.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:8])); print("top cited:", top.head(8).to_dict()); print(f"spent ${spent:.3f}")


if __name__ == "__main__":
    main()
