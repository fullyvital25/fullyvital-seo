"""Append FAQPage JSON-LD (no short answer) to pages that already have a key-fact box."""
import json, re, time
from aeo_quickpass import extract_qas, build_schema, schema_block
from shopify_client import Shopify, ARTICLE_FIELDS
HANDLES = ["do-anti-gray-supplements-work-honest-review", "gray-hair-research-studies", "gray-hair-science-glossary"]
s = Shopify(apply=True)
print("backup:", s.backup_articles())
for h in HANDLES:
    n = s.gql('query($q: String!) { articles(first: 50, query: $q) { nodes { id handle blog { handle } isPublished } } }', {"q": f"handle:{h}"})["articles"]["nodes"]
    n = [x for x in n if x["handle"] == h and x["blog"]["handle"] == "hair-care" and x["isPublished"]]
    assert len(n) == 1, h
    cur = s.gql("query($id: ID!) { article(id: $id) { " + ARTICLE_FIELDS + " } }", {"id": n[0]["id"]})["article"]
    b = cur["body"]
    if "FAQPage" in b: print("SKIP has FAQPage", h); continue
    items, dropped = build_schema(extract_qas(b)[0])
    assert len(items) >= 2
    new = b.rstrip("\n") + "\n" + schema_block(items)
    s.update_article(cur, {"body": new}); print("updated", h, len(items), "dropped", dropped); time.sleep(0.5)
