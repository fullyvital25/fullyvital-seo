"""
Roll out the hair-growth hubs one a day (plan: data/processed/hub_rollout_plan.json). Safe to re-run.

Each run:
  1. Publishes every hub whose date has come and that isn't live yet (new articles: the unpublished draft is updated
     and published; rebuilt articles: title, body, summary and SEO fields are replaced).
  2. For a hub that just went live: runs its approved merges through cleanup_apply.py (301s + internal link rewrites),
     then adds one sentence linking up to the hub on each spoke (before the FAQ; skipped if the spoke already links there).
  3. Re-renders live hubs so links to hubs that are now live appear. Fragments marked <!--hub:KEY-->...<!--/hub-->
     are left out while hub KEY isn't live. A hub edited in Shopify since our last push is not overwritten.
Refresh-test pages (treated and control) are never edited. Every write goes through shopify_client (logged).

Usage:
    python hub_rollout.py                 # dry run for today
    python hub_rollout.py --apply         # real writes (the daily launchd job runs this)
    python hub_rollout.py --date 2026-10-19   # dry run as if it were that date
Log: data/processed/hub_rollout_log.jsonl
"""
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from shopify_client import Shopify

APPLY = "--apply" in sys.argv
TODAY = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else date.today().isoformat()
PLAN = json.loads(Path("data/processed/hub_rollout_plan.json").read_text())
D = Path("data/hub_drafts")
LOG = Path("data/processed/hub_rollout_log.jsonl")
_rc = json.loads(Path("data/processed/refresh_controls.json").read_text())
TEST = {re.sub(r"^https?://[^/]+", "", u) for k, v in _rc.items() for u in [k, *v]}
sha = lambda t: hashlib.sha256((t or "").encode()).hexdigest()[:16]
path = lambda a: f"/blogs/{a['blog']['handle']}/{a['handle']}"


def log(event, **kw):
    rec = {"ts": datetime.now(timezone.utc).isoformat(), "run_date": TODAY, "applied": APPLY, "event": event, **kw}
    print(json.dumps(rec))
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def render(folder, live_keys):
    """draft.html with fragments for not-yet-live hubs removed and all markers stripped."""
    body = (D / folder / "draft.html").read_text()
    body = re.sub(r"<!--hub:(\w+)-->(.*?)<!--/hub-->", lambda m: m.group(2) if m.group(1) in live_keys else "", body, flags=re.S)
    live_urls = {h["hub"] for h in PLAN if h["key"] in live_keys}
    for h in PLAN:  # unmarked links to a NEW hub that isn't live would 404: stop rather than publish them
        if h["new"] and h["key"] not in live_keys and f'https://fullyvital.com{h["hub"]}"' in body:
            raise SystemExit(f"{folder}: unmarked link to {h['hub']}, which is not live yet")
    return body


def changes_for(h, body):
    meta = json.loads((D / h["folder"] / "meta.json").read_text())
    return {"title": meta["title"], "body": body, "summary": meta.get("summary_html", f"<p>{meta['seo_description']}</p>"),
            "metafields": [{"namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": meta["seo_title"]},
                           {"namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": meta["seo_description"]}]}


def add_spoke_link(body, sentence):
    para = f'\n<p class="fv-hub-link">{sentence}</p>\n'
    m = re.search(r"<h[23][^>]*>(?:(?!</h[23]>).){0,80}?(frequently asked|faq)", body, re.I | re.S)
    if not m:
        m = re.search(r'<section class="fv-refs"|<h[23][^>]*>\s*(scientific )?(references|sources)', body, re.I)
    return body[:m.start()] + para + body[m.start():] if m else body + para


s = Shopify(apply=APPLY)
if APPLY:
    log("backup", file=str(s.backup_articles()))
arts = s.articles()
by_path = {path(a): a for a in arts}
pub = lambda h: json.loads((D / h["folder"] / "published.json").read_text()) if (D / h["folder"] / "published.json").exists() else None
due = [h for h in PLAN if h["date"] <= TODAY]
live_keys = {h["key"] for h in due}  # after this run
newly = [h for h in due if not pub(h)]
log("start", due=[h["key"] for h in due], to_publish=[h["key"] for h in newly])

for h in newly:
    a = by_path.get(h["hub"])
    if not a:
        log("error", hub=h["hub"], msg="article not found (create the unpublished draft first)")
        continue
    if h["new"] and a["isPublished"]:
        log("error", hub=h["hub"], msg="new hub is already published outside the rollout; skipping")
        continue
    body = render(h["folder"], live_keys)
    ch = changes_for(h, body)
    if h["new"] or not a["isPublished"]:  # new article, or an unpublished one being brought back as a hub
        ch["isPublished"] = True
    res = s.update_article(a, ch)
    log("hub_published", hub=h["hub"], result=res)
    if not APPLY:
        continue
    saved = next(x for x in s.articles() if x["id"] == a["id"])["body"]  # Shopify may normalise HTML on save
    (D / h["folder"] / "published.json").write_text(json.dumps({"published_at": datetime.now(timezone.utc).isoformat(),
                                                               "article_id": a["id"], "body_sha": sha(body), "live_sha": sha(saved),
                                                               "live_keys": sorted(live_keys)}))
    # merges (approved only)
    ms = [m for m in h["merges"] if m["approved"]]
    if ms:
        sheet = Path(f"data/processed/hub_merges_{h['key']}.csv")
        sheet.write_text("path,decision,redirect_to\n" + "".join(f'{m["path"]},MERGE: unpublish + 301 to target,{m["redirect_to"]}\n' for m in ms))
        r = subprocess.run([sys.executable, "cleanup_apply.py", "--sheet", str(sheet), "--apply"], capture_output=True, text=True)
        log("merges", hub=h["hub"], paths=[m["path"] for m in ms], returncode=r.returncode, out=r.stdout[-1500:], err=r.stderr[-500:])
    # redirects for posts removed earlier (already unpublished, returning 404): straight 301s, no unpublish step
    rds = h.get("redirects", [])
    if rds:
        existing = {x["path"].lower() for x in s.redirects()}
        now = {path(x): x for x in s.articles()}
        made = []
        for r in rds:
            src, tgt = r["path"], r["redirect_to"]
            if src.lower() in existing or (now.get(src) or {}).get("isPublished") or not (now.get(tgt) or {}).get("isPublished") or tgt in TEST:
                log("redirect_skipped", path=src, target=tgt)
                continue
            s.create_redirect(src, tgt)
            made.append(src)
        log("redirects", hub=h["hub"], created=made)
    # spoke links (fresh read: merges rewrote some bodies)
    fresh = {path(a): a for a in s.articles()}
    added = []
    for p in h["spokes"]:
        a2 = fresh.get(p)
        if not a2 or not a2["isPublished"] or p in TEST or h["hub"] in (a2["body"] or ""):
            continue
        s.update_article(a2, {"body": add_spoke_link(a2["body"] or "", h["spoke_sentence"])})
        added.append(p)
    log("spoke_links", hub=h["hub"], added=len(added), pages=added)

# re-render earlier hubs so links to newly live hubs appear
if newly:
    fresh = {path(a): a for a in s.articles()} if APPLY else by_path
    for h in due:
        if h in newly:
            continue
        p = pub(h)
        if not p:
            continue
        body = render(h["folder"], live_keys)
        live_body = fresh[h["hub"]]["body"]
        if sha(body) == p.get("body_sha"):
            continue
        if sha(live_body) != p.get("live_sha"):
            log("skip_rerender", hub=h["hub"], msg="edited in Shopify since our last push; not overwriting")
            continue
        s.update_article(fresh[h["hub"]], {"body": body})
        if APPLY:
            saved = next(x for x in s.articles() if x["id"] == fresh[h["hub"]]["id"])["body"]
            p.update(body_sha=sha(body), live_sha=sha(saved), live_keys=sorted(live_keys))
            (D / h["folder"] / "published.json").write_text(json.dumps(p))
        log("hub_rerendered", hub=h["hub"], live_keys=sorted(live_keys))
log("done")
