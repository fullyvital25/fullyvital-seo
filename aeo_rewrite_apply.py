"""Replace only the text of the existing fv-keyfact 'Short answer' paragraph with the approved rewrites."""
import html, json, re, sys, time
from shopify_client import Shopify, ARTICLE_FIELDS
import os
R = json.load(open(os.environ.get("REWRITES", "data/processed/aeo_quickpass_rewrites.json")))
OLD = json.load(open("data/processed/aeo_quickpass_short_answers.json"))
ctrl = json.load(open("data/processed/refresh_controls.json"))
ctrl = {u.replace("https://fullyvital.com", "") for k, v in ctrl.items() for u in [k] + v}
import csv
PATHS = {r['path'] for r in csv.DictReader(open('data/processed/aeo_quickpass_pages.csv'))}
s = Shopify(apply=True)
print("backup:", s.backup_articles())
PAT = re.compile(r'(<p class="fv-keyfact"><strong>Short answer:</strong> )(.*?)(</p>)', re.S)
done = 0
for h, new in R.items():
    if len(sys.argv) > 1 and h not in sys.argv[1:]: continue
    nodes = s.gql('query($q: String!) { articles(first: 50, query: $q) { nodes { id handle blog { handle } } } }', {"q": f"handle:{h}"})["articles"]["nodes"]
    nodes = [n for n in nodes if n["handle"] == h and f"/blogs/{n['blog']['handle']}/{h}" in PATHS]
    if len(nodes) != 1: print("SKIP unresolved", h); continue
    cur = s.gql("query($id: ID!) { article(id: $id) { " + ARTICLE_FIELDS + " } }", {"id": nodes[0]["id"]})["article"]
    path = f"/blogs/{cur['blog']['handle']}/{h}"
    b = cur["body"]
    ms = PAT.findall(b)
    if path in ctrl or not cur["isPublished"] or len(ms) != 1 or html.unescape(ms[0][1]) != OLD[h]["answer"]:
        print("SKIP changed/unexpected", h); continue
    nb = PAT.sub(lambda m: m.group(1) + html.escape(new, quote=False) + m.group(3), b, count=1)
    s.update_article(cur, {"body": nb}); done += 1; print("updated", h); time.sleep(0.5)
print("done", done)
