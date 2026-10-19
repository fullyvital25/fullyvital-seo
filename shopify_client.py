"""
Shopify Admin API client for the FullyVital blog clean-up.

- Auth: client credentials grant (SHOPIFY_STORE_DOMAIN, SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET in .env).
  Tokens last ~24h and are kept in memory only.
- Scope of writes: blog articles (update / unpublish) and URL redirects. Nothing else.
- Every write is a dry run unless the client is created with apply=True.
- Every write (dry run or real) is logged with before/after to data/shopify_changes/<date>.jsonl.
- backup_articles() saves every article (body included) to data/shopify_backup/ before changes.

Usage:
    from shopify_client import Shopify
    s = Shopify()                 # dry run
    s = Shopify(apply=True)       # real writes, only for an approved batch
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-07")
BACKUP_DIR, LOG_DIR = Path("data/shopify_backup"), Path("data/shopify_changes")

ARTICLE_FIELDS = """
  id handle title body summary isPublished publishedAt createdAt updatedAt tags templateSuffix
  author { name }
  blog { id handle title }
  seoTitle: metafield(namespace: "global", key: "title_tag") { value }
  seoDescription: metafield(namespace: "global", key: "description_tag") { value }
  authorPageUrl: metafield(namespace: "custom", key: "author_page_url") { id value }
"""


class Shopify:
    def __init__(self, apply: bool = False):
        self.domain = os.environ["SHOPIFY_STORE_DOMAIN"].replace("https://", "").strip("/")
        self.apply = apply
        self._token, self._token_exp = None, 0.0
        self.scopes = None
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    # ---------- core ----------
    def _get_token(self) -> str:
        if self._token and time.time() < self._token_exp - 300:
            return self._token
        r = requests.post(f"https://{self.domain}/admin/oauth/access_token", timeout=30, data={
            "grant_type": "client_credentials",
            "client_id": os.environ["SHOPIFY_CLIENT_ID"],
            "client_secret": os.environ["SHOPIFY_CLIENT_SECRET"],
        })
        if r.status_code != 200:
            raise RuntimeError(f"token request failed: HTTP {r.status_code} {r.text[:300]}")
        d = r.json()
        self._token, self._token_exp, self.scopes = d["access_token"], time.time() + int(d.get("expires_in", 86399)), d.get("scope")
        return self._token

    def gql(self, query: str, variables: dict | None = None) -> dict:
        for attempt in range(6):
            r = requests.post(f"https://{self.domain}/admin/api/{API_VERSION}/graphql.json", timeout=60,
                              headers={"X-Shopify-Access-Token": self._get_token(), "Content-Type": "application/json"},
                              json={"query": query, "variables": variables or {}})
            if r.status_code in (429, 502, 503):
                time.sleep(2 * (attempt + 1))
                continue
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:500]}")
            data = r.json()
            errs = data.get("errors")
            if errs and any((e.get("extensions") or {}).get("code") == "THROTTLED" for e in errs):
                time.sleep(2 * (attempt + 1))
                continue
            if errs:
                raise RuntimeError(f"GraphQL errors: {json.dumps(errs)[:800]}")
            self.api_version = r.headers.get("X-Shopify-API-Version")
            return data["data"]
        raise RuntimeError("throttled too many times")

    def _log(self, action: str, target: str, before, after, result=None):
        rec = {"ts": datetime.now(timezone.utc).isoformat(), "applied": self.apply, "action": action,
               "target": target, "before": before, "after": after, "result": result}
        with open(LOG_DIR / f"{datetime.now().date()}.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")

    @staticmethod
    def _check(payload: dict, key: str) -> dict:
        errs = payload[key].get("userErrors") or []
        if errs:
            raise RuntimeError(f"{key}: {errs}")
        return payload[key]

    # ---------- reads ----------
    def shop(self) -> dict:
        return self.gql("{ shop { name myshopifyDomain primaryDomain { url } } }")["shop"]

    def articles(self, page_size: int = 100) -> list[dict]:
        out, cursor = [], None
        while True:
            d = self.gql(f"""query($c: String) {{ articles(first: {page_size}, after: $c) {{
                pageInfo {{ hasNextPage endCursor }} nodes {{ {ARTICLE_FIELDS} }} }} }}""", {"c": cursor})["articles"]
            out += d["nodes"]
            if not d["pageInfo"]["hasNextPage"]:
                return out
            cursor = d["pageInfo"]["endCursor"]

    def redirects(self) -> list[dict]:
        out, cursor = [], None
        while True:
            d = self.gql("""query($c: String) { urlRedirects(first: 250, after: $c) {
                pageInfo { hasNextPage endCursor } nodes { id path target } } }""", {"c": cursor})["urlRedirects"]
            out += d["nodes"]
            if not d["pageInfo"]["hasNextPage"]:
                return out
            cursor = d["pageInfo"]["endCursor"]

    def backup_articles(self) -> Path:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        arts = self.articles()
        path = BACKUP_DIR / f"articles_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
        path.write_text(json.dumps(arts))
        return path

    # ---------- writes (dry run unless apply=True) ----------
    def update_article(self, article: dict, changes: dict) -> dict | None:
        """changes: ArticleUpdateInput fields, e.g. {"body": ..., "title": ..., "isPublished": False}."""
        before = {k: article.get(k) for k in changes}
        if not self.apply:
            self._log("articleUpdate", article["id"], before, changes, "dry-run")
            return None
        res = self._check(self.gql("""mutation($id: ID!, $a: ArticleUpdateInput!) {
            articleUpdate(id: $id, article: $a) { article { id handle isPublished } userErrors { field message } } }""",
                                   {"id": article["id"], "a": changes}), "articleUpdate")
        self._log("articleUpdate", article["id"], before, changes, res["article"])
        return res["article"]

    def create_article(self, blog_id: str, fields: dict) -> dict | None:
        """Create a NEW article, always unpublished (publishing is a separate, approved step)."""
        fields = {**fields, "blogId": blog_id, "isPublished": False}
        if not self.apply:
            self._log("articleCreate", fields.get("handle"), None, {k: v for k, v in fields.items() if k != "body"}, "dry-run")
            return None
        res = self._check(self.gql("""mutation($a: ArticleCreateInput!) {
            articleCreate(article: $a) { article { id handle isPublished blog { handle } } userErrors { field message } } }""",
                                   {"a": fields}), "articleCreate")
        self._log("articleCreate", res["article"]["handle"], None, {k: v for k, v in fields.items() if k != "body"}, res["article"])
        return res["article"]

    def unpublish_article(self, article: dict) -> dict | None:
        return self.update_article(article, {"isPublished": False})

    def set_article_metafield(self, article: dict, namespace: str, key: str, value: str, type_: str = "single_line_text_field") -> dict | None:
        """Set one article metafield (create or overwrite). Logs before/after like the other writes."""
        before = (article.get("authorPageUrl") or {}).get("value") if key == "author_page_url" else None
        change = {"namespace": namespace, "key": key, "type": type_, "value": value}
        if not self.apply:
            self._log("metafieldsSet", article["id"], before, value, "dry-run")
            return None
        res = self._check(self.gql("""mutation($m: [MetafieldsSetInput!]!) {
            metafieldsSet(metafields: $m) { metafields { id namespace key value } userErrors { field message } } }""",
                                   {"m": [{"ownerId": article["id"], **change}]}), "metafieldsSet")
        self._log("metafieldsSet", article["id"], before, value, res["metafields"])
        return res["metafields"]

    def create_redirect(self, path: str, target: str) -> dict | None:
        if not self.apply:
            self._log("urlRedirectCreate", path, None, target, "dry-run")
            return None
        res = self._check(self.gql("""mutation($r: UrlRedirectInput!) {
            urlRedirectCreate(urlRedirect: $r) { urlRedirect { id path target } userErrors { field message } } }""",
                                   {"r": {"path": path, "target": target}}), "urlRedirectCreate")
        self._log("urlRedirectCreate", path, None, target, res["urlRedirect"])
        return res["urlRedirect"]

    def update_redirect(self, redirect: dict, target: str) -> dict | None:
        """Repoint an existing redirect (used to avoid redirect chains)."""
        if not self.apply:
            self._log("urlRedirectUpdate", redirect["path"], redirect["target"], target, "dry-run")
            return None
        res = self._check(self.gql("""mutation($id: ID!, $r: UrlRedirectInput!) {
            urlRedirectUpdate(id: $id, urlRedirect: $r) { urlRedirect { id path target } userErrors { field message } } }""",
                                   {"id": redirect["id"], "r": {"target": target}}), "urlRedirectUpdate")
        self._log("urlRedirectUpdate", redirect["path"], redirect["target"], target, res["urlRedirect"])
        return res["urlRedirect"]


if __name__ == "__main__":
    s = Shopify()
    print(s.shop())
    print("scopes:", s.scopes)
