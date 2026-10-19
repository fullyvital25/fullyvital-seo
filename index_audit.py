"""
Index-status audit: URL Inspection (read-only) for every published blog article.

Resumable: results accumulate in data/raw/gsc_url_inspection_all_<date>.json, keyed by URL.
Run analyze() (or `python index_audit.py analyze`) to write data/processed/index_status_all.csv.

Usage:
    python index_audit.py            # inspect anything not yet inspected
    python index_audit.py analyze
"""

import json
import re
import sys
from pathlib import Path

import pandas as pd

import gsc_pull as g

D = "2026-10-17"
OUT = Path(f"data/raw/gsc_url_inspection_all_{D}.json")


def published_urls() -> list[str]:
    backup = sorted(Path("data/shopify_backup").glob("articles_*.json"))[-1]
    arts = json.loads(backup.read_text())
    return sorted(f"https://fullyvital.com/blogs/{a['blog']['handle']}/{a['handle']}" for a in arts if a["isPublished"])


def inspect_all():
    done = json.loads(OUT.read_text()) if OUT.exists() else {}
    todo = [u for u in published_urls() if u not in done or "error" in done[u]]
    print(f"{len(done)} done, {len(todo)} to inspect", flush=True)
    for n, u in enumerate(todo, 1):
        try:
            done[u] = g.execute("GOOGLE_SEARCH_CONSOLE_INSPECT_URL",
                                {"site_url": g.SITE, "inspection_url": u, "language_code": "en-US"})
        except Exception as e:
            done[u] = {"error": str(e)[:300]}
        if n % 25 == 0:
            OUT.write_text(json.dumps(done))
            print(f"{n}/{len(todo)}", flush=True)
    OUT.write_text(json.dumps(done))


def analyze():
    raw = json.loads(OUT.read_text())
    rows = []
    for u, v in raw.items():
        s = (v.get("inspectionResult") or {}).get("indexStatusResult") or {}
        rows.append({"url": u, "coverage": s.get("coverageState") or v.get("error", "?")[:80], "verdict": s.get("verdict"),
                     "indexing_state": s.get("indexingState"), "fetch": s.get("pageFetchState"), "robots": s.get("robotsTxtState"),
                     "last_crawl": (s.get("lastCrawlTime") or "")[:10], "crawled_as": s.get("crawledAs"),
                     "google_canonical": s.get("googleCanonical"), "user_canonical": s.get("userCanonical"),
                     "referring_urls": len(s.get("referringUrls") or []), "in_sitemap": bool(s.get("sitemap"))})
    df = pd.DataFrame(rows)
    norm = lambda x: re.sub(r"^https?://(www\.)?", "https://", str(x).rstrip("/")).lower()
    df["canonical_mismatch"] = df.google_canonical.notna() & (df.google_canonical.map(norm) != df.url.map(norm))
    card = pd.read_csv("data/processed/page_scorecard.csv")[["url", "clicks_16m", "clicks_90d", "impressions_90d", "word_count", "published"]]
    rev = pd.read_csv("data/processed/blog_cleanup_review.csv")[["path", "decision", "in_scope", "is_comparison"]]
    rev["url"] = "https://fullyvital.com" + rev.path
    df = df.merge(card, on="url", how="left").merge(rev.drop(columns="path"), on="url", how="left")
    df["pub_year"] = df.published.str[:4]
    df.to_csv("data/processed/index_status_all.csv", index=False)
    return df


if __name__ == "__main__":
    if sys.argv[1:] == ["analyze"]:
        analyze()
    else:
        inspect_all()
