"""Build the clean-up review sheet: fixed merge directions, off-topic groups, brand-comparison carve-out,
backlink-based redirect decisions, Shopify article IDs and internal-link counts. No writes."""
import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd

O = "data/processed/"
norm = lambda u: re.sub(r"^https?://(www\.)?", "https://", str(u).split("#")[0].split("?")[0].rstrip("/")).lower()
path_of = lambda u: norm(u).replace("https://fullyvital.com", "")
COMPARISON = re.compile(r"\bvs\.?\b|versus|alternative", re.I)
STOP = set("a an the and or of for to in on with your you is are how what why does do can best hair blogs care vitamins".split())

plan = pd.read_csv(O + "blog_cleanup_plan.csv")
plan["url_n"] = plan.url.map(norm)
plan["is_comparison"] = plan.title.fillna("").str.contains(COMPARISON) & plan.title.fillna("").str.contains("fully ?vital", case=False)
bl = pd.read_csv(O + "dfs_backlinks_by_page.csv")
bl["url_n"] = bl.page.map(norm)
bl = bl.groupby("url_n")[["referring_domains", "backlinks"]].sum()
plan = plan.join(bl, on="url_n").fillna({"referring_domains": 0, "backlinks": 0})

# Shopify IDs + internal links (from the backup taken before any change)
backup = sorted(Path("data/shopify_backup").glob("articles_*.json"))[-1]
arts = json.loads(backup.read_text())
by_url = {f"https://fullyvital.com/blogs/{a['blog']['handle']}/{a['handle']}".lower(): a for a in arts}
plan["shopify_id"] = plan.url_n.map(lambda u: (by_url.get(u) or {}).get("id"))
plan["shopify_published"] = plan.url_n.map(lambda u: (by_url.get(u) or {}).get("isPublished"))
links = Counter()
for a in arts:
    if not a["isPublished"]:
        continue
    for h in set(re.findall(r'href="([^"]+)"', a["body"] or "")):
        if "/blogs/" in h:
            links[path_of(h if h.startswith("http") else "https://fullyvital.com" + h)] += 1
plan["internal_links_in"] = plan.url_n.map(lambda u: links.get(path_of(u), 0))

# ---------- regroup duplicates with fixed rules ----------
pairs = pd.read_csv(O + "blog_duplicate_pairs.csv")
groups = plan[plan.action.str.startswith(("1", "2"))].copy()
groups["gid"] = groups.merge_target  # old group key = old target
rank = lambda df: df.sort_values(["clicks_90d", "clicks_16m", "impressions_90d"], ascending=False)
rows = []
for gid, g in groups.groupby("gid"):
    in_scope = g.in_scope.any()
    if in_scope:
        best = g.sort_values(["clicks_90d", "clicks_16m", "in_scope", "impressions_90d"], ascending=False).iloc[0]
        for r in g.itertuples():
            rows.append((r.url, "MERGE TARGET (keep, refresh)" if r.url == best.url else "MERGE: unpublish + 301 to target", best.url, gid, "in scope"))
    else:
        best = rank(g).iloc[0]
        earns = best.clicks_16m >= 20 or best.clicks_last3 >= 10
        for r in g.itertuples():
            if earns and r.url == best.url:
                rows.append((r.url, "KEEP AS IS (off-topic, earns clicks)", None, gid, "off-topic"))
            elif earns:
                rows.append((r.url, "REMOVE: unpublish + 301 to kept sibling", best.url, gid, "off-topic"))
            else:
                rows.append((r.url, "REMOVE (off-topic group, no clicks)", None, gid, "off-topic"))
g2 = pd.DataFrame(rows, columns=["url", "decision", "redirect_to", "group", "group_topic"])
plan = plan.merge(g2, on="url", how="left")

# ---------- off-topic removals: backlinks -> redirect to the closest in-scope kept article ----------
kept = plan[(plan.decision.isna() & ~plan.action.str.startswith(("2", "4b"))) | plan.decision.isin(["MERGE TARGET (keep, refresh)"])]
kept = kept[kept.in_scope]
def toks(r):
    return {w for w in re.findall(r"[a-z]+", (str(r.title) + " " + r.url.split("/")[-1].replace("-", " ")).lower()) if w not in STOP and len(w) > 2}
kt = [(r.url, toks(r)) for r in kept.itertuples()]
def closest(r):
    t = toks(r)
    best = max(kt, key=lambda k: len(t & k[1]) / max(1, len(t | k[1])))
    score = len(t & best[1]) / max(1, len(t | best[1]))
    return (best[0], round(score, 2)) if score >= 0.15 else ("https://fullyvital.com/blogs/hair-care", round(score, 2))

def final(r):
    if r.is_comparison and not isinstance(r.decision, str):
        return "HOLD: brand comparison post, decide separately", None
    if isinstance(r.decision, str):
        if r.decision == "REMOVE (off-topic group, no clicks)":
            return ("REMOVE: unpublish + 301 (has backlinks)", closest(r)[0]) if r.referring_domains >= 1 else ("REMOVE: unpublish, let 404", None)
        return r.decision, r.redirect_to
    if r.action.startswith("4b"):
        return ("REMOVE: unpublish + 301 (has backlinks)", closest(r)[0]) if r.referring_domains >= 1 else ("REMOVE: unpublish, let 404", None)
    if r.action.startswith("3"):
        return "REFRESH", None
    if r.action.startswith("4a"):
        return "HOLD: in scope, no traffic (Phase 2)", None
    if r.action.startswith("5"):
        return "KEEP AS IS (off-topic, earns clicks)", None
    if r.action.startswith("6"):
        return "LEAVE (new in 2026)", None
    return "KEEP, MONITOR", None
fx = plan.apply(lambda r: pd.Series(final(r), index=["decision", "redirect_to"]), axis=1)
plan[["decision", "redirect_to"]] = fx
plan["redirect_match_score"] = plan.apply(lambda r: closest(r)[1] if str(r.decision).startswith("REMOVE: unpublish + 301 (has") else None, axis=1)
plan["redirect_to"] = plan.redirect_to.map(lambda u: path_of(u) if isinstance(u, str) else None)
plan["path"] = plan.url.map(path_of)
cols = ["path", "decision", "redirect_to", "redirect_match_score", "group", "group_topic", "in_scope", "is_comparison", "title", "blog", "pub_year",
        "clicks_16m", "clicks_90d", "impressions_90d", "referring_domains", "backlinks", "internal_links_in", "word_count", "study_citation_count",
        "primary_keyword_guess", "shopify_id", "shopify_published"]
plan["group"] = plan.group.map(lambda u: path_of(u) if isinstance(u, str) else None)
out = plan[cols].sort_values(["decision", "group", "clicks_90d"], ascending=[True, True, False])
out.to_csv(O + "blog_cleanup_review.csv", index=False)

print("backup:", backup, "| unmatched to Shopify:", int(plan.shopify_id.isna().sum()), "| not published in Shopify:", int((plan.shopify_published == False).sum()))
print(out.groupby("decision").agg(posts=("path", "size"), clicks_16m=("clicks_16m", "sum"), clicks_90d=("clicks_90d", "sum"),
                                  with_backlinks=("referring_domains", lambda s: int((s > 0).sum())), internal_links_in=("internal_links_in", "sum")).to_string())
moving = out[out.decision.str.startswith(("MERGE:", "REMOVE"))]
print("posts leaving:", len(moving), "| internal links pointing at them (articles):", int(moving.internal_links_in.sum()),
      "| articles containing such links:", "n/a")
print("in-scope groups:", out[out.group_topic == "in scope"].group.nunique(), "off-topic groups:", out[out.group_topic == "off-topic"].group.nunique())
print("blog-home fallbacks:", int((out.redirect_to == "/blogs/hair-care").sum()))
pd.set_option("display.width", 250, "display.max_colwidth", 70)
print(out[out.decision.str.startswith("REMOVE: unpublish + 301 (has")][["path", "redirect_to", "redirect_match_score", "referring_domains"]].head(15).to_string())
print(out[out.decision.str.startswith("HOLD: brand")][["path", "clicks_16m"]].to_string())
