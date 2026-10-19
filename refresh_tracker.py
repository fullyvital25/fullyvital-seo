"""
Measure whether article refreshes work: refreshed pages vs a fixed, matched control group.

- Treatment = every draft with data/refresh_drafts/*/published.json (new batches join automatically,
  each with its own publish date).
- Controls = 2 matched untouched articles per treatment page, chosen once by pre-change clicks and
  impressions (unique within a batch; reused across batches), saved to data/processed/refresh_controls.json and never re-picked. Pool: published,
  in-scope, not in the refresh queue, not removed, not a brand comparison, not a 2026 post.
- Data = Search Console page x date for blog pages (read-only), cached per run date.
- Output = data/processed/refresh_tracking_weekly.csv, data/processed/refresh_tracking_pages.csv,
  reports/refresh-tracking.md

Usage:
    python refresh_tracker.py          # rerun every few weeks
"""

import json
import re
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

import gsc_pull as g

TODAY = date.today()
END = TODAY - timedelta(days=3)                 # GSC data lag
START = date(2026, 6, 1)
PRE_DAYS = 56                                   # 8 weeks before each page's change
RAW = Path(f"data/raw/gsc_page_date_tracker_{TODAY}.csv")
CONTROLS = Path("data/processed/refresh_controls.json")
norm = lambda u: re.sub(r"^https?://(www\.)?", "https://", str(u).split("?")[0].split("#")[0].rstrip("/")).lower()


def pull() -> pd.DataFrame:
    if RAW.exists():
        return pd.read_csv(RAW)
    rows, start_row = [], 0
    while True:
        res = g.execute("GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY", {
            "site_url": g.SITE, "start_date": str(START), "end_date": str(END), "dimensions": ["page", "date"],
            "row_limit": g.ROW_LIMIT, "start_row": start_row, "search_type": "web",
            "dimension_filter_groups": [{"filters": [{"dimension": "page", "operator": "contains", "expression": "/blogs/"}]}]})
        batch = res.get("rows") or []
        rows += [{"page": r["keys"][0], "date": r["keys"][1], "clicks": r["clicks"], "impressions": r["impressions"],
                  "position": r["position"]} for r in batch]
        if len(batch) < g.ROW_LIMIT:
            break
        start_row += g.ROW_LIMIT
    df = pd.DataFrame(rows)
    df.to_csv(RAW, index=False)
    return df


def treatment() -> dict:
    out = {}
    for p in Path("data/refresh_drafts").glob("*/published.json"):
        blog, handle = p.parent.name.split("__")
        out[f"https://fullyvital.com/blogs/{blog}/{handle}"] = json.loads(p.read_text())["published_at"][:10]
    return out


def pick_controls(treat: dict, gsc: pd.DataFrame) -> dict:
    controls = json.loads(CONTROLS.read_text()) if CONTROLS.exists() else {}
    new = [u for u in treat if u not in controls]
    if not new:
        return controls
    rev = pd.read_csv("data/processed/blog_cleanup_review.csv")
    rev["url"] = ("https://fullyvital.com" + rev.path).str.lower()
    queue = set(("https://fullyvital.com" + pd.read_csv("data/processed/refresh_queue.csv").path).str.lower())
    pool = rev[rev.decision.isin(["KEEP, MONITOR"]) & rev.in_scope & ~rev.is_comparison & (rev.pub_year.astype(str) != "2026")
               & ~rev.url.isin(queue) & ~rev.url.isin(set(treat))]
    for u in new:
        # unique within a batch (same change date); later batches may reuse controls, since the pool is ~100 posts
        used = {c for t, cs in controls.items() if treat.get(t) == treat[u] for c in cs}
        cut = pd.Timestamp(treat[u])
        pre = gsc[(gsc.date >= cut - pd.Timedelta(days=PRE_DAYS)) & (gsc.date < cut)].groupby("url")[["clicks", "impressions"]].sum()
        if u not in pre.index:
            pre.loc[u] = [0, 0]
        cand = pre.reindex(pool.url).fillna(0)
        cand = cand[~cand.index.isin(used)]
        dist = (np.log1p(cand.clicks) - np.log1p(pre.loc[u, "clicks"])) ** 2 + \
               (np.log1p(cand.impressions) - np.log1p(pre.loc[u, "impressions"])) ** 2
        pick = list(dist.nsmallest(2).index)
        controls[u] = pick
    CONTROLS.write_text(json.dumps(controls, indent=1))
    return controls


def window(df, start, end):
    if end <= start:  # no data yet after the change
        return {"clicks_per_day": np.nan, "impr_per_day": np.nan, "position": np.nan, "ctr": np.nan, "days": 0}
    x = df[(df.date >= start) & (df.date < end)]
    days = (end - start).days
    c, i = x.clicks.sum(), x.impressions.sum()
    return {"clicks_per_day": c / days, "impr_per_day": i / days,
            "position": (x.position * x.impressions).sum() / i if i else np.nan, "ctr": c / i if i else np.nan, "days": days}


def main():
    gsc = pull()
    gsc["url"] = gsc.page.map(norm)
    gsc["date"] = pd.to_datetime(gsc.date)
    gsc = gsc.groupby(["url", "date"], as_index=False).apply(
        lambda x: pd.Series({"clicks": x.clicks.sum(), "impressions": x.impressions.sum(),
                             "position": (x.position * x.impressions).sum() / max(1, x.impressions.sum())})).reset_index(drop=True)
    treat = {norm(k): v for k, v in treatment().items()}
    controls = pick_controls(treat, gsc)
    end = pd.Timestamp(END) + pd.Timedelta(days=1)

    rows = []
    for u, d in treat.items():
        cut = pd.Timestamp(d)
        for role, urls in [("refreshed", [u]), ("control", controls.get(u, []))]:
            for x in urls:
                g_ = gsc[gsc.url == x]
                pre, post = window(g_, cut - pd.Timedelta(days=PRE_DAYS), cut), window(g_, cut + pd.Timedelta(days=7), end)
                rows.append({"pair": u.replace("https://fullyvital.com", ""), "role": role, "url": x.replace("https://fullyvital.com", ""),
                             "changed": d, **{f"pre_{k}": v for k, v in pre.items()}, **{f"post_{k}": v for k, v in post.items()}})
    pages = pd.DataFrame(rows)
    pages.to_csv("data/processed/refresh_tracking_pages.csv", index=False)

    # weekly series per group, aligned to weeks since each page's change
    w = []
    for u, d in treat.items():
        cut = pd.Timestamp(d)
        for role, urls in [("refreshed", [u]), ("control", controls.get(u, []))]:
            x = gsc[gsc.url.isin(urls)].copy()
            x["week"] = ((x.date - cut).dt.days // 7).astype(int)
            x["role"] = role
            w.append(x)
    weekly = pd.concat(w).groupby(["role", "week"]).agg(clicks=("clicks", "sum"), impressions=("impressions", "sum")).reset_index()
    weekly = weekly[weekly.week >= -PRE_DAYS // 7]
    weekly.to_csv("data/processed/refresh_tracking_weekly.csv", index=False)

    grp = pages.groupby("role")[["pre_clicks_per_day", "post_clicks_per_day", "pre_impr_per_day", "post_impr_per_day"]].sum(min_count=1)
    post_days = max(0, pages.post_days.min())
    L = [f"# Refresh tracking\n", f"Run {TODAY}; Search Console data through {END}. Refreshed pages: {len(treat)}; controls: {sum(len(v) for v in controls.values())}. "
         f"Pre window: {PRE_DAYS} days before each change. Post window: from 7 days after the change to the latest data "
         f"({int(post_days)} days for the most recent batch).\n"]
    if post_days < 21:
        L.append(f"**Too early to judge.** The post window is only {int(post_days)} days. Google needs to recrawl; read results from about 6–8 weeks after each change.\n")
    L += ["| Group | Clicks/day before | Clicks/day after | Change | Impressions/day before | Impressions/day after | Change |", "|---|---|---|---|---|---|---|"]
    for role in ["refreshed", "control"]:
        if role in grp.index:
            r = grp.loc[role]
            ch = lambda a, b: f"{(b / a - 1):+.0%}" if a and pd.notna(b) else "—"
            f1 = lambda v, n: "no data yet" if pd.isna(v) else f"{v:.{n}f}"
            L.append(f"| {role} | {f1(r.pre_clicks_per_day, 1)} | {f1(r.post_clicks_per_day, 1)} | {ch(r.pre_clicks_per_day, r.post_clicks_per_day)} | "
                     f"{f1(r.pre_impr_per_day, 0)} | {f1(r.post_impr_per_day, 0)} | {ch(r.pre_impr_per_day, r.post_impr_per_day)} |")
    if {"refreshed", "control"} <= set(grp.index) and grp.loc[["refreshed", "control"], "post_impr_per_day"].notna().all():
        t = grp.loc["refreshed", "post_impr_per_day"] / grp.loc["refreshed", "pre_impr_per_day"]
        c = grp.loc["control", "post_impr_per_day"] / grp.loc["control", "pre_impr_per_day"]
        L.append(f"\nRelative effect on impressions (refreshed vs control): **{t / c - 1:+.0%}**. Impressions react before clicks; use clicks once volumes are large enough.\n")
    L += ["\n## Per page\n", "| Refreshed page | Changed | Clicks/day before → after | Impr/day before → after | Avg position before → after | Controls: impr/day before → after |", "|---|---|---|---|---|---|"]
    for pair, x in pages.groupby("pair"):
        t = x[x.role == "refreshed"].iloc[0]
        c = x[x.role == "control"]
        f = lambda v, n: "—" if pd.isna(v) else f"{v:.{n}f}"
        L.append(f"| {pair} | {t.changed} | {f(t.pre_clicks_per_day, 2)} → {f(t.post_clicks_per_day, 2)} | {f(t.pre_impr_per_day, 0)} → {f(t.post_impr_per_day, 0)} | "
                 f"{f(t.pre_position, 1)} → {f(t.post_position, 1)} | {f(c.pre_impr_per_day.sum(), 0)} → {f(c.post_impr_per_day.sum(min_count=1), 0)} |")
    L += ["\n## Controls\n", "Fixed at first run; never re-picked. Don't refresh these pages until the test is over.\n"]
    L += [f"- {k.replace('https://fullyvital.com', '')}: " + ", ".join(v.replace("https://fullyvital.com", "") for v in vs) for k, vs in controls.items()]
    Path("reports/refresh-tracking.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:12]))


if __name__ == "__main__":
    main()
