"""Inventory of old 'Enhance Hair' product-name mentions on live articles (read-only). Output: data/processed/enhance_rename_inventory_<date>.csv"""
import csv, glob, json, re, sys
from collections import Counter

backup = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob("data/shopify_backup/articles_*.json"))[-1]
ctrl = json.load(open("data/processed/refresh_controls.json"))
test_urls = set(ctrl) | {u for v in ctrl.values() for u in v}
FIELDS = {"body": lambda a: a["body"], "summary": lambda a: a["summary"],
          "seoTitle": lambda a: (a.get("seoTitle") or {}).get("value"), "seoDescription": lambda a: (a.get("seoDescription") or {}).get("value")}
PAT = re.compile(r"enhance\s+hair", re.I)
rows = []
for a in json.load(open(backup)):
    if not a["isPublished"]:
        continue
    url = f'https://fullyvital.com/blogs/{a["blog"]["handle"]}/{a["handle"]}'
    for f, get in FIELDS.items():
        t = get(a) or ""
        for m in PAT.finditer(t):
            tail = t[m.start():m.start() + 60]
            nm = re.match(r"[Ee]nhance\s+[Hh]air(?:\s+(?:[Dd]ensity|[Gg]rowth))?(?:\s+(?:[Ss]erum|[Ss]upplements?|[Vv]itamins))?", tail)
            variant = nm.group(0) if nm else tail[:20]
            pre = t[max(0, m.start() - 300):m.start()]
            if re.search(r'(?:alt|title)="[^"]*$', pre):
                ctx = "attribute"
            elif re.search(r'<a [^>]*href="[^"]*/products/[^"]*"[^>]*>[^<]*$', pre):
                ctx = "product_link_text"
            else:
                ctx = "text"
            rows.append(dict(url=url, handle=a["handle"], field=f, variant=variant, context=ctx,
                             three_pack=bool(re.match(r"[Ee]nhance Hair Serum 3-Pack", tail)),
                             refresh_test=url in test_urls,
                             snippet=re.sub(r"\s+", " ", t[max(0, m.start() - 50):m.start() + 60])))
out = "data/processed/enhance_rename_inventory_2026-10-18.csv"
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(backup, len(rows), "mentions on", len({r["url"] for r in rows}), "pages;", sum(r["refresh_test"] for r in rows), "on test pages,", len({r["url"] for r in rows if r["refresh_test"]}), "pages")
for k, v in sorted(Counter((r["variant"], r["context"]) for r in rows).items(), key=lambda x: -x[1]): print(v, k)
