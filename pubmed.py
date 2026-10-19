"""
PubMed lookups for article refreshes (NCBI E-utilities, free, no key needed at low volume).

Every citation used in a refresh must come through here so its title, journal, year and abstract
are verified, not recalled. Responses are cached in data/raw/pubmed/.

Usage:
    from pubmed import search, summaries, abstract
    ids = search("boron supplementation steroid hormones", n=10)
    for s in summaries(ids): print(s)
    print(abstract(ids[0]))
"""

import hashlib
import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CACHE = Path("data/raw/pubmed")
CACHE.mkdir(parents=True, exist_ok=True)


def _get(endpoint: str, params: dict) -> str:
    key = hashlib.sha1(json.dumps({"e": endpoint, **params}, sort_keys=True).encode()).hexdigest()[:16]
    path = CACHE / f"{endpoint}_{key}.txt"
    if path.exists():
        return path.read_text()
    for attempt in range(4):
        r = requests.get(f"{EUTILS}/{endpoint}.fcgi", params={**params, "tool": "fullyvital-seo"}, timeout=60)
        if r.status_code == 429:
            time.sleep(2 * (attempt + 1))
            continue
        r.raise_for_status()
        break
    time.sleep(0.4)  # stay under 3 requests/second
    path.write_text(r.text)
    return r.text


def search(term: str, n: int = 10, sort: str = "relevance") -> list[str]:
    d = json.loads(_get("esearch", {"db": "pubmed", "term": term, "retmax": n, "sort": sort, "retmode": "json"}))
    return d["esearchresult"]["idlist"]


def summaries(pmids: list[str]) -> list[dict]:
    if not pmids:
        return []
    d = json.loads(_get("esummary", {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"}))["result"]
    out = []
    for p in pmids:
        x = d.get(p) or {}
        out.append({"pmid": p, "title": x.get("title"), "journal": x.get("fulljournalname") or x.get("source"),
                    "year": (x.get("pubdate") or "")[:4], "authors": ", ".join(a["name"] for a in (x.get("authors") or [])[:3]),
                    "pubtype": ", ".join(x.get("pubtype") or []), "url": f"https://pubmed.ncbi.nlm.nih.gov/{p}/"})
    return out


def abstract(pmid: str) -> str:
    root = ET.fromstring(_get("efetch", {"db": "pubmed", "id": pmid, "retmode": "xml"}))
    parts = []
    for t in root.iter("AbstractText"):
        label = t.get("Label")
        parts.append((f"{label}: " if label else "") + "".join(t.itertext()))
    return "\n".join(parts)
