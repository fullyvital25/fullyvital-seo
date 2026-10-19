"""
Create a new article from data/hub_drafts/<blog>__<handle>/ as an UNPUBLISHED Shopify draft (or publish it later).

Usage:
    python create_new_article.py hair-care__gray-hair-in-men            # dry run
    python create_new_article.py hair-care__gray-hair-in-men --apply    # create unpublished draft
    python create_new_article.py hair-care__gray-hair-in-men --publish --apply   # publish the existing draft (after approval)
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from shopify_client import Shopify

folder = sys.argv[1]
APPLY, PUBLISH = "--apply" in sys.argv, "--publish" in sys.argv
D = Path("data/hub_drafts") / folder
blog, handle = folder.split("__")
meta, body = json.loads((D / "meta.json").read_text()), (D / "draft.html").read_text()
AI = re.compile(r"chat\.openai\.com|chatgpt\.com|openai\.com|utm_source=(chatgpt|openai)|user-content-fn|data-footnote-backref|oaicite", re.I)
if AI.search(body):
    sys.exit("AI artifact in draft")
s = Shopify(apply=APPLY)
arts = s.articles()
existing = next((a for a in arts if a["handle"] == handle and a["blog"]["handle"] == blog), None)
if PUBLISH:
    if not existing:
        sys.exit("no draft to publish; create it first")
    print(s.update_article(existing, {"isPublished": True}))
    if APPLY:
        (D / "published.json").write_text(json.dumps({"published_at": datetime.now(timezone.utc).isoformat(), "article_id": existing["id"]}))
    sys.exit(0)
if existing:
    sys.exit(f"/blogs/{blog}/{handle} already exists ({'published' if existing['isPublished'] else 'draft'}); use publish_refresh.py to update it")
blog_id = next(a["blog"]["id"] for a in arts if a["blog"]["handle"] == blog)
fields = {"title": meta["title"], "handle": handle, "body": body, "summary": meta.get("summary_html", f"<p>{meta['seo_description']}</p>"),
          "author": {"name": "Faraz Khan, MSC"},
          "metafields": [{"namespace": "global", "key": "title_tag", "type": "single_line_text_field", "value": meta["seo_title"]},
                         {"namespace": "global", "key": "description_tag", "type": "single_line_text_field", "value": meta["seo_description"]}]}
res = s.create_article(blog_id, fields)
print(("CREATED (unpublished): " if APPLY else "dry run: ") + f"/blogs/{blog}/{handle}", res)
if APPLY and res:
    (D / "created.json").write_text(json.dumps({"created_at": datetime.now(timezone.utc).isoformat(), "article_id": res["id"]}))
