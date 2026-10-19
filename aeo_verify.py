import json, sys, csv, re
from bs4 import BeautifulSoup
from shopify_client import Shopify
bk = json.load(open(sys.argv[1]))
old = {f"/blogs/{a['blog']['handle']}/{a['handle']}": a for a in bk}
drafts = {r["path"]: r for r in csv.DictReader(open("data/processed/aeo_quickpass_drafts.csv"))}
new = {f"/blogs/{a['blog']['handle']}/{a['handle']}": a for a in Shopify().articles()}
ctrl = json.load(open("data/processed/refresh_controls.json"))
ctrl = {u.replace("https://fullyvital.com", "") for k, v in ctrl.items() for u in [k] + v}
done = bad = 0
for p, a in new.items():
    o = old[p]
    if a["body"] == o["body"]: 
        if p in drafts and "--all" in sys.argv: print("UNCHANGED", p)
        continue
    if p not in drafts: print("UNEXPECTED CHANGE", p); bad += 1; continue
    if p in ctrl: print("CONTROL EDITED", p); bad += 1
    d = drafts[p]; b = a["body"]
    m = re.match(r'<p class="fv-keyfact"><strong>Short answer:</strong> (.*?)</p>\n', b, re.S)
    ok = bool(m)
    rest = b[m.end():] if m else b
    items = json.loads(d["faq_json"])
    if items:
        i = rest.rfind('\n<script type="application/ld+json">')
        blk = rest[i:]; rest = rest[:i]
        ld = json.loads(re.search(r"<script[^>]*>(.*)</script>", blk, re.S).group(1))
        vis = re.sub(r"\s+", " ", BeautifulSoup(rest, "html.parser").get_text(" "))
        for q in ld["mainEntity"]:
            if q["name"] not in vis: ok = False; print("Q not visible", p, q["name"])
    if rest.rstrip("\n") != o["body"].rstrip("\n"): ok = False; print("BODY DIFF", p)
    hr = lambda x: re.findall(r'href="([^"]*)"', x)
    if hr(rest) != hr(o["body"]): ok = False
    for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', b, re.S): json.loads(s)
    if (a["title"], a["handle"], a["summary"]) != (o["title"], o["handle"], o["summary"]): ok = False; print("META DIFF", p)
    done += 1; bad += (not ok)
    print("OK " if ok else "BAD", p)
print("changed", done, "bad", bad)
