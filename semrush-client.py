"""
Minimal Semrush API client for the FullyVital SEO pipeline.

- Reads SEMRUSH_API_KEY from .env (never hardcode it).
- Caches every response in data/raw/semrush/ — identical requests are never re-billed.
- Hard cap on rows per request (Semrush bills per row returned).
- Checks the unit balance before and after a run.

Usage from Claude Code:
    from semrush_client import Semrush
    s = Semrush()
    print(s.units_balance())
    df = s.domain_organic("fullyvital.com", limit=500)
"""

import hashlib
import io
import json
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.semrush.com/"
BACKLINKS_BASE = "https://api.semrush.com/analytics/v1/"
CACHE_DIR = Path("data/raw/semrush")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

MAX_ROWS_PER_CALL = 1000  # safety ceiling; raise deliberately, never by default


class Semrush:
    def __init__(self, database: str = "us"):
        self.key = os.environ["SEMRUSH_API_KEY"]
        self.database = database
        self.log = []  # (report, params, rows_returned, cached)

    # ---------- core ----------
    def _get(self, url: str, params: dict, refresh: bool = False) -> pd.DataFrame:
        limit = int(params.get("display_limit", 0) or 0)
        if limit > MAX_ROWS_PER_CALL:
            raise ValueError(f"display_limit {limit} exceeds MAX_ROWS_PER_CALL={MAX_ROWS_PER_CALL}")

        cache_key = hashlib.sha1(
            json.dumps({"url": url, **params}, sort_keys=True).encode()
        ).hexdigest()[:16]
        name = f"{params.get('type', 'x')}_{params.get('domain') or params.get('target') or params.get('phrase', '')}"
        name = "".join(c if c.isalnum() or c in "._-" else "_" for c in name)[:80]
        path = CACHE_DIR / f"{name}_{cache_key}.csv"

        if path.exists() and not refresh:
            df = pd.read_csv(path, sep=";")
            self.log.append((params.get("type"), params, len(df), True))
            return df

        r = requests.get(url, params={**params, "key": self.key}, timeout=60)
        r.raise_for_status()
        text = r.text
        if text.startswith("ERROR"):
            # e.g. "ERROR 50 :: NOTHING FOUND" — cache empty result too, so it isn't re-billed
            if "NOTHING FOUND" in text:
                pd.DataFrame().to_csv(path, sep=";", index=False)
                self.log.append((params.get("type"), params, 0, False))
                return pd.DataFrame()
            raise RuntimeError(text.strip())

        path.write_text(text)
        df = pd.read_csv(io.StringIO(text), sep=";")
        self.log.append((params.get("type"), params, len(df), False))
        return df

    def units_balance(self) -> int:
        r = requests.get(
            "https://www.semrush.com/users/countapiunits.html",
            params={"key": self.key},
            timeout=30,
        )
        r.raise_for_status()
        return int(r.text.strip())

    def summary(self) -> pd.DataFrame:
        return pd.DataFrame(
            [{"report": t, "rows": n, "cached": c} for t, _, n, c in self.log]
        )

    # ---------- reports used in Phase 1 ----------
    def domain_overview(self, domain: str):
        return self._get(BASE, {
            "type": "domain_rank", "domain": domain, "database": self.database,
            "export_columns": "Dn,Rk,Or,Ot,Oc",
        })

    def domain_organic(self, domain: str, limit: int = 500, filter_: str | None = None):
        """Keywords a domain ranks for. filter_ uses Semrush display_filter syntax,
        e.g. '+|Ph|Co|gray' (keyword contains 'gray'). Multiple filters are ANDed,
        so run one call per topic term for OR logic."""
        p = {
            "type": "domain_organic", "domain": domain, "database": self.database,
            "display_limit": limit, "display_sort": "tr_desc",
            "export_columns": "Ph,Po,Pp,Nq,Kd,Cp,Ur,Tr,Co,In,Fp",
        }
        if filter_:
            p["display_filter"] = filter_
        return self._get(BASE, p)

    def organic_competitors(self, domain: str, limit: int = 20):
        return self._get(BASE, {
            "type": "domain_organic_organic", "domain": domain, "database": self.database,
            "display_limit": limit, "export_columns": "Dn,Cr,Np,Or,Ot",
        })

    def serp(self, phrase: str, limit: int = 10):
        """Top organic results for one keyword."""
        return self._get(BASE, {
            "type": "phrase_organic", "phrase": phrase, "database": self.database,
            "display_limit": limit, "export_columns": "Dn,Ur,Fk,Fp",
        })

    def keyword_overview(self, phrase: str):
        return self._get(BASE, {
            "type": "phrase_this", "phrase": phrase, "database": self.database,
            "export_columns": "Ph,Nq,Cp,Co,Kd,In",
        })

    def backlinks_overview(self, domain: str):
        return self._get(BACKLINKS_BASE, {
            "type": "backlinks_overview", "target": domain, "target_type": "root_domain",
            "export_columns": "ascore,total,domains_num,follows_num",
        })


if __name__ == "__main__":
    s = Semrush()
    print("Units balance:", s.units_balance())