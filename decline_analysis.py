"""Traffic-decline diagnosis over saved GSC files. Writes data/processed/decline_*.csv."""
import json
import re

import numpy as np
import pandas as pd

RAW, O, D = "data/raw/", "data/processed/", "2026-10-12"
pd.set_option("display.width", 250, "display.max_colwidth", 70)
W = {  # comparison windows
    "A pre (Jun 10-29 2025)": ("2025-06-10", "2025-06-29"),
    "B after Jun-25 core (Jul 20-Aug 24)": ("2025-07-20", "2025-08-24"),
    "C autumn (Oct 1-Nov 15)": ("2025-10-01", "2025-11-15"),
    "D winter (Dec 7-Jan 31)": ("2025-12-07", "2026-01-31"),
    "E spring (Apr 9-May 20)": ("2026-04-09", "2026-05-20"),
    "F latest (Jul 1-Sep 23)": ("2026-07-01", "2026-09-23"),
}


def norm(u):
    u = u.split("#")[0].split("?")[0].rstrip("/")
    return re.sub(r"^https?://(www\.)?", "https://", u).lower()


def kind(u):
    for k, pat in [("blog", "/blogs/"), ("product", "/products/"), ("collection", "/collections/"), ("page", "/pages/")]:
        if pat in u:
            return k
    return "home" if u == "https://fullyvital.com" else "other"


def per_day(df, col="clicks"):
    out = {}
    for name, (a, b) in W.items():
        days = (pd.Timestamp(b) - pd.Timestamp(a)).days + 1
        out[name] = df[(df.date >= a) & (df.date <= b)].groupby(level=0)[col].sum() / days if df.index.name else df[(df.date >= a) & (df.date <= b)][col].sum() / days
    return out


tot = pd.read_csv(RAW + f"gsc_date_{D}.csv")
brand = pd.read_csv(RAW + f"gsc_date_brand_{D}.csv")
dev = pd.read_csv(RAW + f"gsc_date_device_{D}.csv")
ctry = pd.read_csv(RAW + f"gsc_date_country_{D}.csv")
pdte = pd.read_csv(RAW + f"gsc_page_date_{D}.csv")
pdte["url_n"] = pdte.page.map(norm)
pdte["kind"] = pdte.url_n.map(kind)

rows = []
for name, (a, b) in W.items():
    days = (pd.Timestamp(b) - pd.Timestamp(a)).days + 1
    t, br = tot[(tot.date >= a) & (tot.date <= b)], brand[(brand.date >= a) & (brand.date <= b)]
    p = pdte[(pdte.date >= a) & (pdte.date <= b)]
    r = {"window": name, "clicks/day": t.clicks.sum() / days, "impr/day": t.impressions.sum() / days,
         "avg_pos": (t.position * t.impressions).sum() / t.impressions.sum(), "ctr%": 100 * t.clicks.sum() / t.impressions.sum(),
         "brand clicks/day": br.clicks.sum() / days, "non-brand+hidden clicks/day": (t.clicks.sum() - br.clicks.sum()) / days}
    for k in ["blog", "product", "home", "page", "collection"]:
        r[f"{k} clicks/day"] = p[p.kind == k].clicks.sum() / days
    r["blog pages with a click"] = p[(p.kind == "blog") & (p.clicks > 0)].url_n.nunique()
    r["blog pages with impressions"] = p[p.kind == "blog"].url_n.nunique()
    for d_ in ["MOBILE", "DESKTOP"]:
        x = dev[(dev.date >= a) & (dev.date <= b) & (dev.device == d_)]
        r[f"{d_.lower()} clicks/day"] = x.clicks.sum() / days
    c = ctry[(ctry.date >= a) & (ctry.date <= b)]
    r["US clicks/day"] = c[c.country == "usa"].clicks.sum() / days
    r["non-US clicks/day"] = c[c.country != "usa"].clicks.sum() / days
    rows.append(r)
win = pd.DataFrame(rows).set_index("window")
win.to_csv(O + "decline_windows.csv")
print(win.T.round(2).to_string())

# daily detail around each break
tot["d"] = pd.to_datetime(tot.date)
for a, b in [("2025-06-26", "2025-07-22"), ("2025-09-06", "2025-09-22"), ("2025-11-12", "2025-12-14")]:
    x = tot[(tot.date >= a) & (tot.date <= b)]
    print(a, "clicks:", x.clicks.astype(int).tolist())
    print(" " * 10, "impr k:", (x.impressions / 1000).round(0).astype(int).tolist())
    print(" " * 10, "pos:", x.position.round(0).astype(int).tolist())

# blog pages: step B (June core update) and step D (late Nov) — who lost
def blog_window(a, b):
    days = (pd.Timestamp(b) - pd.Timestamp(a)).days + 1
    p = pdte[(pdte.date >= a) & (pdte.date <= b) & (pdte.kind == "blog")]
    g = p.assign(pxi=p.position * p.impressions).groupby("url_n").agg(clicks=("clicks", "sum"), impressions=("impressions", "sum"), pxi=("pxi", "sum"))
    g["pos"] = g.pxi / g.impressions
    g[["clicks", "impressions"]] = g[["clicks", "impressions"]] / days
    return g.drop(columns="pxi")


inv = pd.read_csv(O + "content_inventory.csv")
inv["url_n"] = inv.url.map(norm)
for label, (w0, w1) in {"step1_june_core": ("A pre (Jun 10-29 2025)", "B after Jun-25 core (Jul 20-Aug 24)"),
                        "step2_late_nov": ("C autumn (Oct 1-Nov 15)", "D winter (Dec 7-Jan 31)")}.items():
    x = blog_window(*W[w0]).join(blog_window(*W[w1]), lsuffix="_before", rsuffix="_after", how="outer").fillna({"clicks_before": 0, "clicks_after": 0, "impressions_before": 0, "impressions_after": 0})
    x["click_loss_per_day"] = x.clicks_before - x.clicks_after
    x = x.sort_values("click_loss_per_day", ascending=False)
    x.to_csv(O + f"decline_{label}_pages.csv")
    lost = x[x.click_loss_per_day > 0]
    had = x[x.clicks_before > 0]
    print(f"\n{label}: blog clicks/day {x.clicks_before.sum():.1f} -> {x.clicks_after.sum():.1f}; pages with clicks before {len(had)}; "
          f"of those down>=50%: {int((had.clicks_after <= 0.5 * had.clicks_before).sum())}; went to zero: {int((had.clicks_after == 0).sum())}; "
          f"pages that gained: {int((x.click_loss_per_day < 0).sum())}; top-20 losers' share of gross loss: {lost.click_loss_per_day.head(20).sum() / lost.click_loss_per_day.sum():.0%}")
    both = x[(x.impressions_before > 5) & x.pos_after.notna() & x.pos_before.notna()]
    print(f"  median position before {both.pos_before.median():.1f} -> after {both.pos_after.median():.1f}; pages whose position worsened by 5+: {int((both.pos_after - both.pos_before >= 5).sum())} of {len(both)}")
    y = x.head(12).reset_index()
    y["url_n"] = y.url_n.str.replace("https://fullyvital.com", "")
    print(y[["url_n", "clicks_before", "clicks_after", "pos_before", "pos_after", "impressions_before", "impressions_after"]].round(1).to_string())
    m = x.reset_index().merge(inv[["url_n", "blog", "word_count", "published", "study_citation_count"]], on="url_n", how="left")
    m["topic"] = np.where(m.url_n.str.contains("gray|grey"), "gray", np.where(m.blog == "hair-vitamins", "hair-vitamins blog", "hair-care blog"))
    print(m.groupby("topic").agg(pages=("url_n", "size"), before=("clicks_before", "sum"), after=("clicks_after", "sum")).round(1).to_string())
    m["pub_year"] = m.published.str[:4]
    print(m.groupby("pub_year").agg(pages=("url_n", "size"), before=("clicks_before", "sum"), after=("clicks_after", "sum")).round(1).to_string())

# index status sample
ins = json.load(open(RAW + f"gsc_url_inspection_{D}.json"))
ir = []
for u, v in ins.items():
    s = (v.get("inspectionResult") or {}).get("indexStatusResult") or {}
    ir.append({"url": u, "coverage": s.get("coverageState", v.get("error", "?"))[:60], "verdict": s.get("verdict"), "last_crawl": (s.get("lastCrawlTime") or "")[:10],
               "google_canonical_differs": bool(s.get("googleCanonical")) and norm(s.get("googleCanonical")) != norm(u)})
ir = pd.DataFrame(ir)
ir.to_csv(O + "index_status_sample.csv", index=False)
print("\nindex sample:", len(ir), ir.coverage.value_counts().to_dict(), "| canonical differs:", int(ir.google_canonical_differs.sum()))
dec = set(pd.read_csv(O + "decay.csv").url.head(20))
ir["group"] = np.where(ir.url.isin(dec), "decayed top 20", "zero-performer")
print(ir.groupby(["group", "coverage"]).size().to_string())
print("last crawl by month:", ir.last_crawl.str[:7].value_counts().sort_index().to_dict())

# sitemap lastmod and publish dates
a = inv[inv.type == "article"]
print("\nsitemap lastmod by month:", a.sitemap_lastmod.str[:7].value_counts().sort_index().to_dict())
print("lastmod top days:", a.sitemap_lastmod.str[:10].value_counts().head(6).to_dict())
print("published by month (2025+):", a[a.published >= "2024-06"].published.str[:7].value_counts().sort_index().to_dict())
print("schema dateModified by month:", a.updated.str[:7].value_counts().sort_index().tail(8).to_dict())
