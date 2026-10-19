"""
Publish approved refresh drafts to Shopify (body, title, summary, SEO title + meta description).

Each draft is re-checked right before writing: built from the latest backup, no AI-chat links,
every PubMed link present in its reference list. Handles, URLs and publish dates are not changed.

Usage:
    python publish_refresh.py                       # dry run for all drafts
    python publish_refresh.py --apply --only hair-vitamins__boron
    python publish_refresh.py --apply            # all drafts not yet published (published.json marks done ones)
    python publish_refresh.py --root data/hub_drafts --apply --only hair-care__what-causes-gray-hair   # hub drafts
"""

import json
import re
import sys
from pathlib import Path

from shopify_client import Shopify

APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
AI_PAT = re.compile(r"chat\.openai\.com|chatgpt\.com|openai\.com|utm_source=(chatgpt|openai)|perplexity\.ai|gemini\.google|"
                    r"claude\.ai|copilot\.microsoft|user-content-fn|data-footnote-backref|oaicite|contentReference|turn0search", re.I)

s = Shopify(apply=APPLY)
live = {(a["blog"]["handle"], a["handle"]): a for a in s.articles()}
ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path("data/refresh_drafts")  # data/hub_drafts for hubs
dirs = sorted(d for d in ROOT.iterdir() if d.is_dir() and (d / "draft.html").exists())
if ONLY:
    dirs = [d for d in dirs if d.name == ONLY]
# Already-published drafts are skipped unless named with --only (re-publishing must be deliberate).
if not ONLY:
    dirs = [d for d in dirs if not (d / "published.json").exists()]

for d in dirs:
    blog, handle = d.name.split("__")
    a = live[(blog, handle)]
    body = (d / "draft.html").read_text()
    meta = json.loads((d / "meta.json").read_text())
    if AI_PAT.search(body):
        sys.exit(f"{d.name}: AI artifact in draft, not publishing")
    cited = set(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", body))
    refs = body[body.find("References"):]
    if not cited or any(f"/{p}/" not in refs for p in cited):
        sys.exit(f"{d.name}: reference list incomplete, not publishing")
    if not a["isPublished"]:
        sys.exit(f"{d.name}: live article is unpublished, not publishing")
    changes = {
        "title": meta["title"],
        "body": body,
        "summary": f"<p>{meta['seo_description']}</p>",
        "metafields": [
            {"namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": meta["seo_title"]},
            {"namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": meta["seo_description"]},
        ],
    }
    res = s.update_article(a, changes)
    if APPLY and res:
        from datetime import datetime, timezone
        (d / "published.json").write_text(json.dumps({"published_at": datetime.now(timezone.utc).isoformat(),
                                                      "article_id": a["id"], "title": meta["title"]}))
    print(f"{'PUBLISHED' if APPLY else 'dry run'}: /blogs/{blog}/{handle} -> {meta['title']} | {len(cited)} citations | {res}")
