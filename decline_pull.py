"""Extra read-only GSC pulls for the traffic-decline diagnosis: brand daily, device daily, country daily, URL inspection sample."""
import json
import sys
from pathlib import Path

import pandas as pd

import gsc_pull as g

RAW = Path("data/raw")
D = g.TODAY


def pull(what, dims, filters=None):
    path = RAW / f"gsc_{what}_{D}.csv"
    if path.exists():
        return pd.read_csv(path)
    rows, start = [], 0
    while True:
        args = {"site_url": g.SITE, "start_date": g.START, "end_date": g.END, "dimensions": dims,
                "row_limit": g.ROW_LIMIT, "start_row": start, "search_type": "web"}
        if filters:
            args["dimension_filter_groups"] = [{"filters": filters}]
        batch = g.execute("GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY", args).get("rows") or []
        rows += [{**dict(zip(dims, r["keys"])), "clicks": r["clicks"], "impressions": r["impressions"], "position": r["position"]} for r in batch]
        if len(batch) < g.ROW_LIMIT:
            break
        start += g.ROW_LIMIT
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(what, len(df), flush=True)
    return df


def inspect(urls):
    path = RAW / f"gsc_url_inspection_{D}.json"
    done = json.loads(path.read_text()) if path.exists() else {}
    for u in urls:
        if u in done:
            continue
        try:
            done[u] = g.execute("GOOGLE_SEARCH_CONSOLE_INSPECT_URL", {"site_url": g.SITE, "inspection_url": u, "language_code": "en-US"})
        except Exception as e:
            done[u] = {"error": str(e)[:300]}
        path.write_text(json.dumps(done))
    return done


if __name__ == "__main__":
    pull("date_brand", ["date"], [{"dimension": "query", "operator": "includingRegex", "expression": "fully ?vital|fullyvita"}])
    pull("date_device", ["date", "device"])
    pull("date_country", ["date", "country"])
    dec = pd.read_csv("data/processed/decay.csv")
    zp = pd.read_csv("data/processed/zero_performers.csv")
    zp = zp[zp.published.str[:4] != "2026"]
    sample = list(dec.url.head(20)) + list(zp.sort_values("impressions_16m", ascending=False).url.head(10)) + list(zp[zp.impressions_16m == 0].url.head(10)) \
        + list(zp.sample(10, random_state=3).url)
    res = inspect(list(dict.fromkeys(sample)))
    k = next(iter(res.values()))
    print(json.dumps(k)[:1500])
