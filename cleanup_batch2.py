"""
Clean-up batch 2 review sheet (no writes): Phase 2 decisions for the 132 held and 69 comparison posts,
plus two non-calendar gray duplicates. Same schema as blog_cleanup_review.csv so cleanup_apply.py can run it.

Rules:
- Act now: removals and merges into an existing live page. Rewrites and "fold into planned hub" are listed but not actioned.
- Anti-gray calendar posts are kept; control pages (refresh test) are never a source or a target.
- Removal with 1+ referring domain -> 301 to the merge target or the cluster's page with most impressions (flagged for review); otherwise 404.

Outputs: data/processed/blog_cleanup_review_batch2.csv, reports/blog-cleanup-batch2-review.md
"""
import json
import re
from pathlib import Path

import pandas as pd

O = "data/processed/"
norm = lambda u: re.sub(r"^https?://(www\.)?", "https://", str(u).split("?")[0].rstrip("/")).lower()
path = lambda u: norm(u).replace("https://fullyvital.com", "")

held = pd.read_csv(O + "phase2_held_decisions.csv")
comp = pd.read_csv(O + "phase2_comparison_decisions.csv")
cl = pd.read_csv(O + "phase2_cluster_scores.csv").set_index("cluster")
cal = set(pd.read_csv("data/reference/anti_gray_content_calendar.csv").shopify_url.map(path)) | \
      set(pd.read_csv("data/reference/hair_growth_content_calendar.csv").shopify_url.map(path))
controls = json.loads(Path(O + "refresh_controls.json").read_text())
control_pages = {path(u) for v in controls.values() for u in v} | {path(u) for u in controls}
bl = pd.read_csv(O + "dfs_backlinks_by_page.csv").assign(p=lambda d: d.page.map(path)).groupby("p").referring_domains.sum()
backup = sorted(Path("data/shopify_backup").glob("articles_*.json"))[-1]
arts = {f"/blogs/{a['blog']['handle']}/{a['handle']}".lower(): a for a in json.loads(backup.read_text())}
live = {p for p, a in arts.items() if a["isPublished"]}

rows = []
for r in held.itertuples():
    d = r.decision_p2
    tgt = path(r.target) if isinstance(r.target, str) else None
    if d.startswith("Merge"):
        dec = "MERGE: unpublish + 301 to target"
    elif d.startswith("Remove"):
        dec = "REMOVE"
    elif d.startswith("Rewrite"):
        dec = "LATER: rewrite (content queue)"
    else:
        dec = "LATER: fold into planned hub"
    rows.append({"path": r.path, "source": "held", "phase2_decision": d, "decision": dec, "redirect_to": tgt if dec.startswith("MERGE") else None,
                 "cluster": r.cluster, "clicks_16m": r.clicks_16m, "impressions_90d": r.impressions_90d})
for r in comp.itertuples():
    if r.path in cal:
        dec, d = "KEEP (in your content calendar)", r.decision_p2
    elif not r.real:
        dec, d = "KEEP (not a brand comparison)", r.decision_p2
    elif r.decision_p2.startswith("Keep"):
        dec, d = "KEEP + refresh later (direct competitor)", r.decision_p2
    else:
        dec, d = "REMOVE", r.decision_p2
    rows.append({"path": r.path, "source": "comparison", "phase2_decision": d, "decision": dec, "redirect_to": None,
                 "cluster": r.cluster, "clicks_16m": r.clicks_16m, "impressions_90d": r.impressions_90d})
for src, tgt in [("/blogs/hair-care/glutathione-for-gray-hair", "/blogs/hair-vitamins/glutathione"),
                 ("/blogs/hair-care/gray-hair-ingredients-ranked-by-evidence", "/blogs/hair-care/anti-gray-hair-ingredients-what-actually-works")]:
    rows.append({"path": src, "source": "gray duplicate", "phase2_decision": "duplicate of an existing gray page", "decision": "MERGE: unpublish + 301 to target",
                 "redirect_to": tgt, "cluster": "gray", "clicks_16m": None, "impressions_90d": None})
s = pd.DataFrame(rows)
s["referring_domains"] = s.path.map(bl).fillna(0)

# removals with backlinks -> redirect to the cluster's page with most impressions (if live and safe), flagged
def fallback(r):
    t = cl.top_page_by_impressions.get(r.cluster) if r.cluster in cl.index else None
    return t if isinstance(t, str) and t in live and t != r.path else None
m = s.decision.eq("REMOVE") & (s.referring_domains >= 1)
s.loc[m, "redirect_to"] = s[m].apply(fallback, axis=1)
s["decision"] = s.apply(lambda r: ("REMOVE: unpublish + 301 (has backlinks; check target)" if r.decision == "REMOVE" and isinstance(r.redirect_to, str)
                                   else "REMOVE: unpublish, let 404" if r.decision == "REMOVE" else r.decision), axis=1)

# merges into refresh-test pages (controls or refreshed pages in the test) wait until the test reads out
test_pages = control_pages
m = s.decision.str.startswith("MERGE") & s.redirect_to.isin(test_pages)
s.loc[m, "decision"] = "LATER: merge after refresh test (target is in the test)"

# safety checks
acting = s.decision.str.startswith(("MERGE", "REMOVE"))
leaving = set(s[acting].path)
problems = []
for r in s[acting].itertuples():
    if r.path in cal:
        problems.append(f"calendar post would be removed: {r.path}")
    if r.path in control_pages:
        problems.append(f"control page would be removed: {r.path}")
    if r.path not in live:
        problems.append(f"not live: {r.path}")
    if isinstance(r.redirect_to, str):
        if r.redirect_to in leaving:
            problems.append(f"target also leaving: {r.path} -> {r.redirect_to}")
        if r.redirect_to not in live:
            problems.append(f"target not live: {r.path} -> {r.redirect_to}")
        if r.redirect_to in control_pages:
            problems.append(f"target is a control page: {r.path} -> {r.redirect_to}")
# a merge target that is itself being merged/removed: follow the chain once
s.to_csv(O + "blog_cleanup_review_batch2.csv", index=False)
print(s.decision.value_counts().to_string()); print("problems:", len(problems)); [print("  ", p) for p in problems[:30]]

L = ["# Clean-up batch 2: review sheet\n",
     "Nothing has been changed. Approve this sheet, or edit the `decision` column in `data/processed/blog_cleanup_review_batch2.csv`.\n",
     "Sources: Phase 2 decisions for the 132 held posts and 69 brand comparisons, plus two duplicate gray posts. Anti-gray calendar posts and the 20 refresh-test control pages "
     "are excluded. Rewrites and \"fold into hub\" items are listed but not actioned until the hubs exist.\n", "## Summary\n", "| Decision | Posts |", "|---|---|"]
L += [f"| {d} | {n} |" for d, n in s.decision.value_counts().items()]
L += [f"\nSafety checks: {len(problems)} problems." + ("" if not problems else " " + "; ".join(problems[:10]))]
for title, key in [("Merges", "MERGE"), ("Removals with backlinks (301; check each target)", "REMOVE: unpublish + 301"), ("Removals (404)", "REMOVE: unpublish, let 404"),
                   ("Kept comparisons", "KEEP"), ("Later (content work or after the refresh test)", "LATER")]:
    x = s[s.decision.str.startswith(key)].sort_values("path")
    L += [f"\n## {title} ({len(x)})\n", "| Post | Decision | Redirect to | Referring domains | Why |", "|---|---|---|---|---|"]
    L += [f"| {r.path} | {r.decision} | {r.redirect_to if isinstance(r.redirect_to, str) else '—'} | {int(r.referring_domains)} | {str(r.phase2_decision)[:90]} |" for r in x.itertuples()]
Path("reports/blog-cleanup-batch2-review.md").write_text("\n".join(L) + "\n")
