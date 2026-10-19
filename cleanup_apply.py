"""
Apply the approved blog clean-up (data/processed/blog_cleanup_review.csv).

Order: fresh backup -> checks -> new redirects -> repoint existing redirects that would chain ->
unpublish leaving posts -> rewrite internal links in remaining published articles.

Usage:
    python cleanup_apply.py              # preview only (dry run, writes plan files)
    python cleanup_apply.py --apply      # real writes
    python cleanup_apply.py --apply --limit 1   # first leaving post only (smoke test)
    python cleanup_apply.py --sheet data/processed/blog_cleanup_review_batch2.csv   # batch 2 preview
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd

from shopify_client import Shopify

APPLY = "--apply" in sys.argv
LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
OUT = Path("data/shopify_changes")
# Approved 2026-10-17: the 4 off-topic posts with weak redirect matches return 404 instead.
FORCE_404 = {"/blogs/hair-care/benefits-of-almond-oil-for-hair", "/blogs/hair-care/female-receding-hairline",
             "/blogs/hair-care/porosity", "/blogs/hair-care/frizz"}

s = Shopify(apply=APPLY)
backup = s.backup_articles()
arts = json.loads(backup.read_text())
by_path = {f"/blogs/{a['blog']['handle']}/{a['handle']}".lower(): a for a in arts}

SHEET = sys.argv[sys.argv.index("--sheet") + 1] if "--sheet" in sys.argv else "data/processed/blog_cleanup_review.csv"
r = pd.read_csv(SHEET)
leave = r[r.decision.str.startswith(("MERGE:", "REMOVE"))].copy()
leave.loc[leave.path.isin(FORCE_404), "redirect_to"] = None
leaving = {p: (t if isinstance(t, str) and t else None) for p, t in zip(leave.path, leave.redirect_to)}

# ---------- checks ----------
problems = []
for p, t in leaving.items():
    a = by_path.get(p)
    if not a:
        problems.append(f"not found in Shopify: {p}")
    elif not a["isPublished"] and not APPLY:
        problems.append(f"already unpublished: {p}")
    if t:
        if t in leaving:
            problems.append(f"redirect target is itself leaving: {p} -> {t}")
        elif not (by_path.get(t) or {}).get("isPublished"):
            problems.append(f"redirect target not a published article: {p} -> {t}")
existing = s.redirects()
ex_by_path = {x["path"].lower(): x for x in existing}
# A redirect on a live article's path is inactive until the article goes; repoint it to our target.
stale = {p: ex_by_path[p] for p in leaving if p in ex_by_path}
for p, x in stale.items():
    if not leaving[p]:
        problems.append(f"existing redirect would fire for a post meant to 404: {p} -> {x['target']}")
chains = [(x, leaving[x["target"].lower().rstrip("/")]) for x in existing
          if x["target"].lower().rstrip("/") in leaving and leaving[x["target"].lower().rstrip("/")]]
dead = [x for x in existing if x["target"].lower().rstrip("/") in leaving and not leaving[x["target"].lower().rstrip("/")]]

# ---------- internal links ----------
HREF = re.compile(r'(<a\b[^>]*?\bhref=")([^"]+)("[^>]*>)(.*?)(</a>)', re.I | re.S)


def norm_href(h):
    h = re.sub(r"^https?://(www\.)?fullyvital\.com", "", h.strip(), flags=re.I)
    return h.split("#")[0].split("?")[0].rstrip("/").lower()


def rewrite(body):
    n_re, n_un = 0, 0

    def sub(m):
        nonlocal n_re, n_un
        h = norm_href(m.group(2))
        if h not in leaving:
            return m.group(0)
        if leaving[h]:
            n_re += 1
            return m.group(1) + leaving[h] + m.group(3) + m.group(4) + m.group(5)
        n_un += 1
        return m.group(4)
    return HREF.sub(sub, body or ""), n_re, n_un


CONTROLS = {re.sub(r"^https?://(www\.)?fullyvital\.com", "", u).lower() for v in json.loads(Path("data/processed/refresh_controls.json").read_text()).values() for u in v} \
    if Path("data/processed/refresh_controls.json").exists() else set()
skipped_controls = []
link_edits = []
for p, a in by_path.items():
    if p in leaving or not a["isPublished"]:
        continue
    if p in CONTROLS:  # refresh-test controls stay untouched until the test ends
        if rewrite(a["body"])[1] or rewrite(a["body"])[2]:
            skipped_controls.append(p)
        continue
    new, n_re, n_un = rewrite(a["body"])
    if n_re or n_un:
        link_edits.append((a, new, n_re, n_un))

plan = {"backup": str(backup), "posts_leaving": len(leaving), "redirects_new": sum(1 for t in leaving.values() if t),
        "unpublish_404": sum(1 for t in leaving.values() if not t), "existing_redirects_repointed": len(chains) + len(stale),
        "stale_redirects_on_leaving_paths": {p: x["target"] for p, x in stale.items()},
        "existing_redirects_now_dead": [x["path"] for x in dead], "articles_with_link_edits": len(link_edits),
        "links_repointed": sum(e[2] for e in link_edits), "control_pages_with_links_left_for_later": skipped_controls, "links_unwrapped": sum(e[3] for e in link_edits), "problems": problems}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / f"cleanup_plan_preview_{Path(SHEET).stem}.json").write_text(json.dumps(plan, indent=1))
print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 15 else v[:15] + [f"... {len(v)} total"]) for k, v in plan.items()}, indent=1))
if problems:
    sys.exit("Stopping: fix the problems above first.")
if not APPLY:
    print("\nPreview only. Re-run with --apply to make these changes.")
    sys.exit(0)

# ---------- apply ----------
todo = list(leaving.items())[:LIMIT] if LIMIT else list(leaving.items())
done = 0
for p, t in todo:
    a = by_path[p]
    if t and p in stale:
        s.update_redirect(stale[p], t)
    elif t:
        s.create_redirect(p, t)
    if a["isPublished"]:
        s.unpublish_article(a)
    done += 1
print(f"redirects + unpublish done for {done} posts")
if LIMIT:
    sys.exit(0)
for x, t in chains:
    s.update_redirect(x, t)
print(f"repointed {len(chains)} existing redirects")
for a, new, n_re, n_un in link_edits:
    s.update_article(a, {"body": new})
print(f"rewrote links in {len(link_edits)} articles")
