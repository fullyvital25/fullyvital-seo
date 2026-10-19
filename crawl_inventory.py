"""
Phase 1A — content inventory for fullyvital.com (public crawl).

Reads data/raw/sitemap_fullyvital_<date>.json, fetches every blog article and content page,
caches raw HTML in data/raw/html/, and writes data/processed/content_inventory.csv.

Usage:
    python crawl_inventory.py [--limit N]
"""

import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

SITEMAP = sorted(Path("data/raw").glob("sitemap_fullyvital_*.json"))[-1]
HTML_DIR = Path("data/raw/html")
HTML_DIR.mkdir(parents=True, exist_ok=True)
OUT = Path("data/processed/content_inventory.csv")
UA = {"User-Agent": "Mozilla/5.0 (FullyVital SEO audit; owner crawl)"}
DELAY = 0.5

# Outbound links counted as study / scientific citations.
STUDY_HOSTS = re.compile(
    r"(pubmed|ncbi\.nlm\.nih|nih\.gov|doi\.org|sciencedirect|springer|wiley|nature\.com|"
    r"jamanetwork|thelancet|bmj\.com|nejm\.org|plos\.org|frontiersin|mdpi\.com|tandfonline|"
    r"cochrane|karger\.com|oup\.com|academic\.oup|cell\.com|liebertpub|sagepub|jaad\.org|"
    r"europepmc|researchgate|biomedcentral|\.gov(/|$)|\.edu(/|$))", re.I)
BODY_SELECTORS = [".fv-article-col .prose", ".prose", "[itemprop=articleBody]", ".article-template__content", ".article__content",
                  ".article-content", "article .rte", ".rte", "article", "main"]


def fetch(url: str) -> tuple[str, int]:
    path = HTML_DIR / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".html")
    if path.exists():
        return path.read_text(), 200
    for attempt in range(4):
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(5 * (attempt + 1))
            continue
        break
    time.sleep(DELAY)
    if r.status_code == 200:
        path.write_text(r.text)
    return r.text, r.status_code


def jsonld(soup) -> list[dict]:
    out = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(s.string or "")
        except (ValueError, TypeError):
            continue
        stack = [d]
        while stack:
            x = stack.pop()
            if isinstance(x, list):
                stack.extend(x)
            elif isinstance(x, dict):
                out.append(x)
                stack.extend(x.get("@graph") or [])
    return out


def meta(soup, **attrs):
    t = soup.find("meta", attrs=attrs)
    return (t.get("content") or "").strip() if t else None


def parse(url: str, html: str, lastmod: str | None) -> dict:
    soup = BeautifulSoup(html, "lxml")
    ld = jsonld(soup)
    types = sorted({t for d in ld for t in ([d.get("@type")] if isinstance(d.get("@type"), str)
                                            else d.get("@type") or [])})
    art = next((d for d in ld if "Article" in str(d.get("@type")) or "BlogPosting" in str(d.get("@type"))), {})
    author = art.get("author")
    if isinstance(author, list):
        author = author[0] if author else None
    author = author.get("name") if isinstance(author, dict) else author
    author = author or meta(soup, name="author")

    body, used = None, None
    for sel in BODY_SELECTORS:
        cands = soup.select(sel)
        if cands:
            body = max(cands, key=lambda c: len(c.get_text()))
            used = sel
            break
    for junk in (body.select("script,style,noscript,nav,form") if body else []):
        junk.decompose()
    text = body.get_text(" ", strip=True) if body else ""
    host = urlparse(url).netloc
    products, studies, external = [], [], 0
    for a in (body.find_all("a", href=True) if body else []):
        h = urljoin(url, a["href"])
        p = urlparse(h)
        if p.scheme not in ("http", "https"):
            continue
        if p.netloc.replace("www.", "") == host.replace("www.", ""):
            if "/products/" in p.path:
                products.append(p.path.split("/products/")[1].split("/")[0].split("?")[0])
        else:
            external += 1
            if STUDY_HOSTS.search(p.netloc + p.path[:1]):
                studies.append(p.netloc)
    h1 = soup.find_all("h1")
    return {
        "url": url,
        "type": "article" if "/blogs/" in url else "page",
        "blog": url.split("/blogs/")[1].split("/")[0] if "/blogs/" in url else None,
        "title": soup.title.get_text(strip=True) if soup.title else None,
        "meta_description": meta(soup, name="description"),
        "h1": h1[0].get_text(" ", strip=True) if h1 else None,
        "h1_count": len(h1),
        "h2_count": len(body.find_all("h2")) if body else 0,
        "h2_list": " | ".join(h.get_text(" ", strip=True) for h in body.find_all("h2")) if body else "",
        "word_count": len(text.split()),
        "body_selector": used,
        "published": art.get("datePublished") or meta(soup, property="article:published_time"),
        "updated": art.get("dateModified") or meta(soup, property="article:modified_time"),
        "sitemap_lastmod": lastmod,
        "has_byline": bool(author),
        "author": author,
        "schema_types": ", ".join(types),
        "product_link_count": len(products),
        "product_link_targets": ", ".join(sorted(set(products))),
        "external_link_count": external,
        "study_citation_count": len(studies),
        "study_citation_hosts": ", ".join(sorted(set(studies))),
        "canonical": (soup.find("link", rel="canonical") or {}).get("href"),
        "robots": meta(soup, name="robots"),
    }


def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    sm = json.loads(SITEMAP.read_text())
    targets = [(u, lm) for k, v in sm.items() if "sitemap_articles" in k or "sitemap_pages" in k
               for u, lm in v]
    if limit:
        targets = targets[:: max(1, len(targets) // limit)][:limit]
    rows, errors = [], []
    for n, (u, lm) in enumerate(targets, 1):
        try:
            html, status = fetch(u)
            if status != 200:
                errors.append((u, status))
                rows.append({"url": u, "http_status": status})
                continue
            rows.append({**parse(u, html, lm), "http_status": 200})
        except Exception as e:  # keep crawling; report at the end
            errors.append((u, repr(e)))
            rows.append({"url": u, "http_status": None})
        if n % 50 == 0:
            print(f"{n}/{len(targets)}", flush=True)
    df = pd.DataFrame(rows)
    if not limit:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(OUT, index=False)
    print(f"done: {len(df)} rows, {len(errors)} errors")
    for e in errors[:20]:
        print("  ERR", e)
    return df


if __name__ == "__main__":
    df = main()
    if "--limit" in sys.argv:
        pd.set_option("display.width", 250, "display.max_colwidth", 60)
        print(df.drop(columns=["h2_list"], errors="ignore").T.to_string())
