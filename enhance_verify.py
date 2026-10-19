"""Offline check of the rename: dry-run simulation on a backup (sim) or verify live articles vs backup (verify)."""
import json, re, subprocess, sys, glob
from collections import Counter
mode, backup = sys.argv[1], sys.argv[2]
pairs = [tuple(l.rsplit("=>", 1)) for l in re.findall(r"^'(.*)'$", open("data/reference/enhance_rename_pairs.sh").read(), re.M)]
ctrl = json.load(open("data/processed/refresh_controls.json"))
test = set(ctrl) | {u for v in ctrl.values() for u in v}
OLD = re.compile(r"Enhance Hair (?:(?:Density|Growth) )?(?:Serum|Supplements?|Vitamins)|(?i:enhance hair (?:(?:density|growth) )?(?:serum|supplements?|vitamins))")
def swap(t):
    for o, n in pairs:
        while (x := re.sub(o, n, t)) != t: t = x
    return t
url = lambda a: f'https://fullyvital.com/blogs/{a["blog"]["handle"]}/{a["handle"]}'
def fields(a): return {"body": a["body"] or "", "summary": a["summary"] or "", **{k: (a.get(k) or {}).get("value") or "" for k in ("seoTitle", "seoDescription")}}
old = {a["id"]: a for a in json.load(open(backup))}
if mode == "sim":
    n = Counter(); links = Counter()
    for a in old.values():
        f = fields(a); ch = {k: swap(v) for k, v in f.items() if swap(v) != v}
        if not ch: continue
        n["unpub" if not a["isPublished"] else "test" if url(a) in test else "live"] += 1
        for k, v in ch.items():
            for m in re.finditer(r'<a [^>]*href="([^"]*/products/[^"]*)"[^>]*>[^<]*Hair Revival', v): links[m.group(1)] += 1
    print(n); print(links)
if mode == "verify":
    from shopify_client import Shopify
    NEW = re.compile(r"Hair Revival (?:Serum|Supplements)")
    PH = lambda t: NEW.sub("@@", OLD_T.sub("@@", t))
    OLD_T = re.compile(r"Enhance Hair (?:(?:Density|Growth) )?(?:Serum|Supplements?|Vitamins)(?! 3-Pack)|(?i:enhance hair (?:(?:density|growth) )?(?:serum|supplements?|vitamins)(?! 3-pack))")
    price = lambda t: sorted(re.findall(r"\$\d+(?:\.\d\d)?", t))
    href = lambda t: re.findall(r'href="[^"]*"', t)
    def ld_ok(t):
        try: [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)]; return True
        except Exception: return False
    live = Shopify().articles(); changed = fails = tested = 0; fail_list = []; left = Counter(); prices = {}
    for a in live:
        o = old.get(a["id"])
        if not o or not a["isPublished"]: continue
        f_new = fields(a); f_old = fields(o)
        if f_new != f_old:
            changed += 1
            if url(a) in test: fail_list.append((a["handle"], "TEST PAGE EDITED")); continue
            b0, b1 = f_old["body"], f_new["body"]
            bad = [k for k in f_old if PH(f_old[k]) != NEW.sub("@@", f_new[k])] + (["href"] if href(b0) != href(b1) else []) + (["price"] if price(b0) != price(b1) else []) + (["jsonld"] if not ld_ok(b1) else [])
            if bad: fail_list.append((a["handle"], bad))
        for k, v in f_new.items():
            for m in OLD.finditer(v): left[(m.group(0), url(a) in test, bool(re.match(r"Enhance Hair Serum 3-Pack|Enhance Hair Serum \(3-Pack\)", v[m.start():m.start()+40], re.I)))] += 1
        if url(a) not in test:
            for p in set(price(f_new["body"])): prices.setdefault(p, set()).add(a["handle"])
    print("changed", changed, "failures", fail_list); print("remaining", left)
    print({p: len(h) for p, h in sorted(prices.items())})
