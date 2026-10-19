"""
Phase 1B — Google Search Console pulls via the Composio CLI (read-only actions only).

Writes raw CSV/JSON to data/raw/gsc_<what>_<date>. Existing files are reused.

Usage:
    python gsc_pull.py
"""

import json
import os
import subprocess
import tempfile
from datetime import date
from pathlib import Path

import pandas as pd

COMPOSIO = os.path.expanduser("~/.local/bin/composio")
ACCOUNT = "google_search_console_paw-dujan"
SITE = "sc-domain:fullyvital.com"
TODAY = date.today().isoformat()
RAW = Path("data/raw")
START, END = "2025-06-10", "2026-10-09"       # 16 months, ending 3 days back (GSC data lag)
START_90, START_PRIOR_YEAR = "2026-07-12", "2025-07-12"
ROW_LIMIT = 25000


def execute(slug: str, args: dict) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(args, f)
    try:
        p = subprocess.run([COMPOSIO, "execute", slug, "--account", ACCOUNT, "-d", f"@{f.name}"],
                           capture_output=True, text=True, timeout=300)
    finally:
        os.unlink(f.name)
    out = p.stdout[p.stdout.index("{"):]
    data = json.loads(out)
    if not data.get("successful"):
        raise RuntimeError(f"{slug}: {data.get('error')}")
    if data.get("storedInFile"):  # large responses are written to a temp file by the CLI
        data = json.loads(Path(data["outputFilePath"]).read_text())
    return data.get("data", data)


def query(what: str, dims: list[str], start: str = START, end: str = END) -> pd.DataFrame:
    path = RAW / f"gsc_{what}_{TODAY}.csv"
    existing = sorted(RAW.glob(f"gsc_{what}_????-??-??.csv"))
    if existing:
        print(f"reuse {existing[-1]}")
        return pd.read_csv(existing[-1])
    rows, start_row = [], 0
    while True:
        res = execute("GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY", {
            "site_url": SITE, "start_date": start, "end_date": end, "dimensions": dims,
            "row_limit": ROW_LIMIT, "start_row": start_row, "search_type": "web"})
        batch = res.get("rows") or []
        rows += [{**dict(zip(dims, r["keys"])), "clicks": r["clicks"], "impressions": r["impressions"],
                  "ctr": r["ctr"], "position": r["position"]} for r in batch]
        print(f"  {what}: start_row={start_row} got {len(batch)}", flush=True)
        if len(batch) < ROW_LIMIT:
            break
        start_row += ROW_LIMIT
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"saved {path} rows={len(df)}")
    return df


def main():
    pq = query("page_query", ["page", "query"])
    pq90 = query("page_query_90d", ["page", "query"], start=START_90)
    q = query("query", ["query"])
    p = query("page", ["page"])
    p90 = query("page_90d", ["page"], start=START_90)
    pd_ = query("page_date", ["page", "date"])
    d = query("date", ["date"])

    monthly = RAW / f"gsc_page_monthly_{TODAY}.csv"
    if not monthly.exists():
        m = pd_.assign(month=pd_.date.str[:7])
        m["pos_x_impr"] = m.position * m.impressions
        m = m.groupby(["page", "month"], as_index=False).agg(
            clicks=("clicks", "sum"), impressions=("impressions", "sum"), pos_x_impr=("pos_x_impr", "sum"))
        m["position"] = m.pos_x_impr / m.impressions
        m.drop(columns="pos_x_impr").to_csv(monthly, index=False)

    sm = RAW / f"gsc_sitemaps_{TODAY}.json"
    if not sm.exists():
        sm.write_text(json.dumps(execute("GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS", {"site_url": SITE})))

    print(f"\nproperty: {SITE}  range {START}..{END}")
    print(f"site totals (date dim): clicks={d.clicks.sum():.0f} impressions={d.impressions.sum():.0f}")
    print(f"query-level:            clicks={q.clicks.sum():.0f} impressions={q.impressions.sum():.0f}")
    print(f"anonymized/missing share: clicks {1 - q.clicks.sum() / d.clicks.sum():.1%}, "
          f"impressions {1 - q.impressions.sum() / d.impressions.sum():.1%}")
    print(f"rows: page_query={len(pq)} page_query_90d={len(pq90)} query={len(q)} page={len(p)} "
          f"page_90d={len(p90)} page_date={len(pd_)}")
    print("sitemaps:", sm.read_text()[:600])


if __name__ == "__main__":
    main()
