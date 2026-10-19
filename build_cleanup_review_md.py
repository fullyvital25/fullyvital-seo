"""Render data/processed/blog_cleanup_review.csv as reports/blog-cleanup-review.md for approval."""
import pandas as pd

r = pd.read_csv("data/processed/blog_cleanup_review.csv")
L = ["# Blog clean-up — review sheet\n",
     "Nothing has been changed on the store. Approve, or mark changes in `data/processed/blog_cleanup_review.csv` (column `decision`).\n",
     "Rules: in-scope duplicate groups keep the post with the most clicks in the last 90 days (in-scope posts first) and 301 the rest to it. "
     "Off-topic groups keep the post that still earns clicks and 301 its siblings to it; if none earns clicks, the group is removed. "
     "Off-topic posts with no traffic are unpublished; those with 1+ referring domain get a 301 to the closest in-scope article. "
     "Brand comparison posts are held for a separate decision.\n",
     "## Summary\n", "| Decision | Posts | Clicks 16m | Clicks 90d | With backlinks | Internal links pointing in |", "|---|---|---|---|---|---|"]
s = r.groupby("decision").agg(n=("path", "size"), c16=("clicks_16m", "sum"), c90=("clicks_90d", "sum"), bl=("referring_domains", lambda x: int((x > 0).sum())), il=("internal_links_in", "sum"))
L += [f"| {d} | {x.n} | {int(x.c16):,} | {int(x.c90):,} | {x.bl} | {int(x.il):,} |" for d, x in s.iterrows()]
L.append("\n## Duplicate groups\n")
for topic in ["in scope", "off-topic"]:
    g = r[r.group_topic == topic]
    L.append(f"### {topic.capitalize()} ({g.group.nunique()} groups)\n")
    L += ["| Keep | Clicks 90d | Redirect into it (clicks 90d, referring domains) |", "|---|---|---|"]
    for gid, x in g.groupby("group"):
        keep = x[x.decision.str.startswith(("MERGE TARGET", "KEEP AS IS"))]
        go = x[~x.index.isin(keep.index)]
        k = keep.iloc[0] if len(keep) else None
        L.append(f"| {k.path if k is not None else '— (remove all)'} | {int(k.clicks_90d) if k is not None else '—'} | "
                 + "<br>".join(f"{p} ({int(c)}, {int(b)})" for p, c, b in zip(go.path, go.clicks_90d, go.referring_domains)) + " |")
    L.append("")
for title, key in [("Off-topic removals with backlinks (301)", "REMOVE: unpublish + 301 (has"), ("Off-topic removals without backlinks (unpublish, 404)", "REMOVE: unpublish, let 404"),
                   ("Held: brand comparison posts", "HOLD: brand")]:
    x = r[r.decision.str.startswith(key)].sort_values("clicks_16m", ascending=False)
    L.append(f"## {title} ({len(x)})\n")
    L += ["| Post | Redirect to | Clicks 16m | Referring domains | Title |", "|---|---|---|---|---|"]
    L += [f"| {p} | {t if isinstance(t, str) else '—'} | {int(c)} | {int(b)} | {str(n)[:80].replace('|', '/')} |" for p, t, c, b, n in zip(x.path, x.redirect_to, x.clicks_16m, x.referring_domains, x.title)]
    L.append("")
x = r[r.decision == "REFRESH"].sort_values("clicks_16m", ascending=False)
L.append(f"## Refresh list ({len(x)}, plus the {int((r.decision == 'MERGE TARGET (keep, refresh)').sum())} merge targets)\n")
L += ["| Post | Clicks 16m | Clicks 90d | Study links | Main query |", "|---|---|---|---|---|"]
L += [f"| {p} | {int(c)} | {int(c9)} | {int(s_)} | {q} |" for p, c, c9, s_, q in zip(x.path, x.clicks_16m, x.clicks_90d, x.study_citation_count, x.primary_keyword_guess)]
open("reports/blog-cleanup-review.md", "w").write("\n".join(L) + "\n")
print(len(L), "lines")
