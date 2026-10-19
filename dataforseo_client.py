"""
Minimal DataForSEO v3 client for the FullyVital SEO pipeline.

- Auth: DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD from .env (API Access tab in your account).
- Caches every response in data/raw/dataforseo/ — identical requests are never re-billed.
- Logs the real `cost` DataForSEO returns on every call; enforces a per-session $ cap.
- Uses Live endpoints (one request = one result, no task polling).

IMPORTANT for Claude Code: endpoint paths, field paths and filter syntax below follow
https://docs.dataforseo.com/v3/. Before the first real run, check each against the docs
(DataForSEO has a free sandbox at https://sandbox.dataforseo.com that returns dummy data
at no cost — use it to validate request shapes). Fix names here, not around this client.

Usage:
    from dataforseo_client import DFS
    d = DFS()
    print(d.balance())
    kws = d.ranked_keywords("fullyvital.com", limit=1000)
"""

import base64
import hashlib
import json
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = os.environ.get("DATAFORSEO_BASE", "https://api.dataforseo.com")  # sandbox: https://sandbox.dataforseo.com
IS_SANDBOX = "sandbox" in BASE
# Sandbox returns dummy data — keep it out of the live cache so it is never reused as real data.
CACHE_DIR = Path("data/raw/dataforseo_sandbox" if IS_SANDBOX else "data/raw/dataforseo")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

LOCATION_US = 2840
LANGUAGE = "en"
MAX_ROWS_PER_CALL = 1000
SESSION_BUDGET_USD = float(os.environ.get("DFS_SESSION_BUDGET_USD", "25"))

TOPIC_TERMS = [
    "gray", "grey", "white hair", "hair color loss", "premature gray", "hair growth", "hair loss",
    "thinning hair", "hair thinning", "regrow", "shedding", "alopecia",
    "biotin", "catalase", "minoxidil", "hair vitamin", "hair supplement",
]
# DataForSEO allows up to 8 filters per request; 7 leaves room for the max_position condition.
MAX_FILTER_CONDITIONS = 7


def topic_filters(terms=TOPIC_TERMS, field="keyword_data.keyword"):
    """Yield OR-filter arrays of ≤7 'like' conditions each (run one call per chunk, then dedupe)."""
    for i in range(0, len(terms), MAX_FILTER_CONDITIONS):
        chunk = terms[i:i + MAX_FILTER_CONDITIONS]
        f = []
        for t in chunk:
            if f:
                f.append("or")
            f.append([field, "like", f"%{t}%"])
        yield f


class DFS:
    def __init__(self, location_code: int = LOCATION_US, language_code: str = LANGUAGE):
        token = base64.b64encode(
            f"{os.environ['DATAFORSEO_LOGIN']}:{os.environ['DATAFORSEO_PASSWORD']}".encode()
        ).decode()
        self.headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}
        self.loc = location_code
        self.lang = language_code
        self.spent = 0.0
        self.log = []  # (endpoint, rows, cost, cached)

    # ---------- core ----------
    def _post(self, endpoint: str, task: dict, refresh: bool = False) -> dict:
        limit = int(task.get("limit", 0) or 0)
        if limit > MAX_ROWS_PER_CALL:
            raise ValueError(f"limit {limit} exceeds MAX_ROWS_PER_CALL={MAX_ROWS_PER_CALL}")

        cache_key = hashlib.sha1(
            json.dumps({"e": endpoint, **task}, sort_keys=True).encode()
        ).hexdigest()[:16]
        label = task.get("target") or task.get("target1") or task.get("keyword") or "batch"
        label = "".join(c if c.isalnum() or c in "._-" else "_" for c in str(label))[:60]
        path = CACHE_DIR / f"{endpoint.strip('/').replace('/', '_')}_{label}_{cache_key}.json"

        if path.exists() and not refresh:
            data = json.loads(path.read_text())
            self.log.append((endpoint, _rows(data), 0.0, True))
            return data

        if self.spent >= SESSION_BUDGET_USD:
            raise RuntimeError(
                f"Session budget ${SESSION_BUDGET_USD} reached (spent ${self.spent:.2f}). "
                "Ask the user before raising DFS_SESSION_BUDGET_USD."
            )

        r = requests.post(f"{BASE}{endpoint}", headers=self.headers, json=[task], timeout=120)
        data = _json_or_raise(r, endpoint)
        task_res = (data.get("tasks") or [{}])[0]
        if task_res.get("status_code") not in (20000, None):
            raise RuntimeError(f"{endpoint}: {task_res.get('status_code')} {task_res.get('status_message')}")

        cost = float(data.get("cost") or 0)
        self.spent += cost
        path.write_text(json.dumps(data))
        self.log.append((endpoint, _rows(data), cost, False))
        return data

    def balance(self) -> dict:
        r = requests.get(f"{BASE}/v3/appendix/user_data", headers=self.headers, timeout=30)
        res = _json_or_raise(r, "/v3/appendix/user_data")["tasks"][0]["result"][0]
        return {"balance_usd": res.get("money", {}).get("balance"), "raw": res.get("money")}

    def summary(self) -> pd.DataFrame:
        df = pd.DataFrame([{"endpoint": e, "rows": n, "cost_usd": c, "cached": k}
                           for e, n, c, k in self.log])
        return df

    def _base(self, **kw) -> dict:
        return {"location_code": self.loc, "language_code": self.lang, **kw}

    # ---------- Phase 1 reports ----------
    def ranked_keywords(self, target: str, limit: int = 1000, filters=None,
                        max_position: int | None = None, offset: int = 0) -> pd.DataFrame:
        """Keywords a domain ranks for, with volume, KD and intent included (Labs)."""
        f = filters
        if max_position:
            pos = ["ranked_serp_element.serp_item.rank_group", "<=", max_position]
            f = [pos] if not f else [f, "and", pos]
        task = self._base(target=target, limit=limit, item_types=["organic"],
                          order_by=["keyword_data.keyword_info.search_volume,desc"])
        if f:
            task["filters"] = f
        if offset:
            task["offset"] = offset
        data = self._post("/v3/dataforseo_labs/google/ranked_keywords/live", task)
        return pd.DataFrame([_flatten_ranked(i) for i in _items(data)])

    def ranked_keywords_in_scope(self, target: str, limit_per_chunk: int = 500,
                                 max_position: int | None = None) -> pd.DataFrame:
        frames = [self.ranked_keywords(target, limit_per_chunk, f, max_position)
                  for f in topic_filters()]
        df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
        return df.drop_duplicates(subset=["keyword", "url"]) if not df.empty else df

    def competitors_domain(self, target: str, limit: int = 20) -> pd.DataFrame:
        data = self._post("/v3/dataforseo_labs/google/competitors_domain/live",
                          self._base(target=target, limit=limit))
        return pd.json_normalize(_items(data))

    def relevant_pages(self, target: str, limit: int = 100) -> pd.DataFrame:
        """Top pages by organic traffic."""
        data = self._post("/v3/dataforseo_labs/google/relevant_pages/live",
                          self._base(target=target, limit=limit,
                                     order_by=["metrics.organic.etv,desc"]))
        return pd.json_normalize(_items(data))

    def domain_rank_overview(self, target: str) -> pd.DataFrame:
        data = self._post("/v3/dataforseo_labs/google/domain_rank_overview/live",
                          self._base(target=target))
        return pd.json_normalize(_items(data))

    def serp(self, keyword: str, depth: int = 10) -> pd.DataFrame:
        data = self._post("/v3/serp/google/organic/live/advanced",
                          self._base(keyword=keyword, depth=depth))
        rows = [i for i in _items(data) if i.get("type") == "organic"]
        return pd.DataFrame([{"keyword": keyword, "position": i.get("rank_group"),
                              "domain": i.get("domain"), "url": i.get("url"),
                              "title": i.get("title")} for i in rows])

    def serp_features(self, keyword: str, depth: int = 10, refresh: bool = False) -> dict:
        """Live Google SERP with AEO features: AI Overview citations, People Also Ask, featured snippet, organic top 10."""
        data = self._post("/v3/serp/google/organic/live/advanced", self._base(keyword=keyword, depth=depth), refresh=refresh)
        return {**parse_serp_features(data, keyword), "_raw": data}

    def keyword_overview(self, keywords: list[str]) -> pd.DataFrame:
        if len(keywords) > 700:
            raise ValueError("keyword_overview accepts ≤700 keywords per call.")
        data = self._post("/v3/dataforseo_labs/google/keyword_overview/live",
                          self._base(keywords=keywords))
        return pd.json_normalize(_items(data))

    def keyword_suggestions(self, keyword: str, limit: int = 300, filters=None) -> pd.DataFrame:
        """Labs: long-tail keywords that contain the seed, with volume, KD and intent."""
        task = self._base(keyword=keyword, limit=limit, include_seed_keyword=True,
                          order_by=["keyword_info.search_volume,desc"])
        if filters:
            task["filters"] = filters
        data = self._post("/v3/dataforseo_labs/google/keyword_suggestions/live", task)
        return pd.DataFrame([{
            "seed": keyword, "keyword": i.get("keyword"),
            "volume": (i.get("keyword_info") or {}).get("search_volume"),
            "cpc": (i.get("keyword_info") or {}).get("cpc"),
            "kd": (i.get("keyword_properties") or {}).get("keyword_difficulty"),
            "intent": (i.get("search_intent_info") or {}).get("main_intent"),
            "top10_avg_domain_rank": (i.get("avg_backlinks_info") or {}).get("main_domain_rank"),
        } for i in _items(data)])

    def domain_pages(self, target: str, limit: int = 1000, offset: int = 0) -> pd.DataFrame:
        """Backlinks API — every page of the target that has backlinks, with referring-domain counts."""
        task = {"target": target, "limit": limit, "include_subdomains": True,
                "order_by": ["page_summary.referring_domains,desc"]}
        if offset:
            task["offset"] = offset
        data = self._post("/v3/backlinks/domain_pages/live", task)
        return pd.DataFrame([{"page": i.get("page"),
                              **{k: (i.get("page_summary") or {}).get(k)
                                 for k in ("referring_domains", "referring_main_domains", "backlinks")}}
                             for i in _items(data)])

    def backlinks_summary(self, target: str) -> dict:
        """Backlinks API — may need to be enabled separately on your account."""
        data = self._post("/v3/backlinks/summary/live",
                          {"target": target, "include_subdomains": True})
        res = (data["tasks"][0].get("result") or [{}])[0]
        return {k: res.get(k) for k in ("target", "rank", "backlinks", "referring_domains",
                                         "referring_main_domains")}


# ---------- helpers ----------
def parse_serp_features(data: dict, keyword: str) -> dict:
    items = _items(data)
    aio = [i for i in items if i.get("type") == "ai_overview"]
    refs = [{"domain": r.get("domain"), "url": r.get("url"), "title": r.get("title")}
            for a in aio for r in (a.get("references") or [])]
    paa = [q.get("title") for i in items if i.get("type") == "people_also_ask" for q in (i.get("items") or [])]
    org = [{"position": i.get("rank_group"), "domain": i.get("domain"), "url": i.get("url")} for i in items if i.get("type") == "organic"]
    return {"keyword": keyword, "has_ai_overview": bool(aio), "ai_overview_refs": refs, "people_also_ask": paa,
            "has_featured_snippet": any(i.get("type") == "featured_snippet" for i in items), "organic": org,
            "checked": ((data.get("tasks") or [{}])[0].get("result") or [{}])[0].get("datetime")}


def _json_or_raise(r: requests.Response, endpoint: str) -> dict:
    """DataForSEO puts the real reason in the JSON body even on HTTP 4xx/5xx — surface it."""
    try:
        data = r.json()
    except ValueError:
        r.raise_for_status()
        raise
    if r.status_code >= 400 or data.get("status_code") != 20000:
        raise RuntimeError(f"{endpoint}: HTTP {r.status_code} / "
                           f"{data.get('status_code')} {data.get('status_message')}")
    return data


def _items(data: dict) -> list:
    try:
        res = data["tasks"][0]["result"] or []
        return (res[0].get("items") or []) if res else []
    except (KeyError, IndexError, TypeError):
        return []


def _rows(data: dict) -> int:
    return len(_items(data))


def _flatten_ranked(i: dict) -> dict:
    kd = i.get("keyword_data") or {}
    info = kd.get("keyword_info") or {}
    props = kd.get("keyword_properties") or {}
    intent = kd.get("search_intent_info") or {}
    serp = (i.get("ranked_serp_element") or {}).get("serp_item") or {}
    return {
        "keyword": kd.get("keyword"),
        "volume": info.get("search_volume"),
        "cpc": info.get("cpc"),
        "kd": props.get("keyword_difficulty"),
        "intent": intent.get("main_intent"),
        "position": serp.get("rank_group"),
        "url": serp.get("url"),
        "etv": serp.get("etv"),
    }


if __name__ == "__main__":
    print(json.dumps(DFS().balance(), indent=2))