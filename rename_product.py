"""
Rename product mentions in blog articles (exact string swaps only; nothing else in the text changes).
Covers body, summary and SEO title/description. Pairs run in order, so put longer names first.
Skips unpublished articles and refresh-test pages (treated and control). Dry run unless --apply; --limit N for a live test.
Usage: python rename_product.py "Old A=>New A" ["Old B=>New B" ...] [--apply] [--limit 1] [--regex]
--regex: each pair is re.sub(pattern, replacement), repeated until nothing more matches; use (?i) for case-insensitive.
"""
import json
import re
import sys

from shopify_client import ARTICLE_FIELDS, Shopify

args = [a for a in sys.argv[1:] if not a.startswith("--")]
apply = "--apply" in sys.argv
regex = "--regex" in sys.argv
limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
if limit is not None:
    args = [a for a in args if a != str(limit)]
pairs = [tuple(p.split("=>")) for p in args]
ctrl = json.load(open("data/processed/refresh_controls.json"))
test_urls = set(ctrl) | {u for v in ctrl.values() for u in v}
SEO = {"seoTitle": "title_tag", "seoDescription": "description_tag"}


def swap(text):
    for old, new in pairs:
        if not regex:
            text = text.replace(old, new)
            continue
        while (nxt := re.sub(old, new, text)) != text:
            text = nxt
    return text


def plan(a):
    fields = {"body": a["body"] or "", "summary": a["summary"] or ""}
    fields.update({k: (a.get(k) or {}).get("value") or "" for k in SEO})
    return {k: swap(v) for k, v in fields.items() if swap(v) != v}


s = Shopify(apply=apply)
todo, skipped = [], []
for a in s.articles():
    if a["isPublished"] and plan(a):
        (skipped if f'https://fullyvital.com/blogs/{a["blog"]["handle"]}/{a["handle"]}' in test_urls else todo).append(a)
done = 0
for a in todo:
    if done == limit:
        break
    a = s.gql("query($id: ID!) { node(id: $id) { ... on Article { %s } } }" % ARTICLE_FIELDS, {"id": a["id"]})["node"]  # re-read right before writing
    ch = plan(a) if a["isPublished"] else {}
    if not ch:
        print("skipped (changed since list) " + a["handle"])
        continue
    upd = {k: v for k, v in ch.items() if k in ("body", "summary")}
    meta = [{"namespace": "global", "key": SEO[k], "type": "single_line_text_field", "value": v} for k, v in ch.items() if k in SEO]
    if meta:
        upd["metafields"] = meta
    s.update_article(a, upd)
    done += 1
    print(("updated " if apply else "would update ") + a["handle"], sorted(ch))
print(f"{done} of {len(todo)} articles", "applied" if apply else "(dry run)",
      "| control pages left for after the refresh test:", [a["handle"] for a in skipped])
