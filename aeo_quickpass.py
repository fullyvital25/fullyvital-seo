"""AEO quick pass: add a 'Short answer' paragraph at the top and FAQPage JSON-LD at the end of older articles.

Stage 1 (default): fetch, build FAQ schema, merge short answers (data/processed/aeo_quickpass_short_answers.json),
  write data/processed/aeo_quickpass_drafts.csv and reports/aeo-quickpass-review.md. Read-only.
Stage 2 (--apply [--limit N]): back up, re-read each article, insert the approved drafts, write, log.
  `--dump` writes a text digest of each page for writing the short answers.
"""
import argparse, csv, html, json, re, sys, time
from pathlib import Path
from bs4 import BeautifulSoup
from shopify_client import Shopify, ARTICLE_FIELDS

PAGES = Path("data/processed/aeo_quickpass_pages.csv")
CONTROLS = Path("data/processed/refresh_controls.json")
ANSWERS = Path("data/processed/aeo_quickpass_short_answers.json")
DRAFTS = Path("data/processed/aeo_quickpass_drafts.csv")
REVIEW = Path("reports/aeo-quickpass-review.md")
DIGEST = Path("data/processed/aeo_quickpass_digest.txt")
SITE = "https://fullyvital.com"
CLAIM = re.compile(r"\b(cure[sd]?|curing|treat(?:s|ed|ing)?|prevent(?:s|ed|ing|ion)?|revers(?:e|es|ed|ing)|regrow\w*|"
                   r"heal(?:s|ed|ing)?|stop(?:s|ped|ping)?|clinically proven|guarantee\w*|miracle\w*|will grow)\b", re.I)
HEAD = ["h1", "h2", "h3", "h4", "h5", "h6"]
MAX_QA, MAX_ANS = 8, 1200


def norm(t): return re.sub(r"\s+", " ", t).strip()


def blocks(soup):
    """Document-order list of ('h', level, text) / ('t', text); li kept, p inside li skipped."""
    out = []
    for el in soup.find_all(HEAD + ["p", "li"]):
        if el.name in HEAD:
            out.append(("h", int(el.name[1]), norm(el.get_text(" "))))
        elif el.name == "p" and el.find_parent("li"):
            continue
        elif el.name == "li" and el.find_parent("li") and False:
            continue
        else:
            t = norm(el.get_text(" "))
            if t:
                out.append(("t", t))
    return out


def qa_from(bl, start, stop_level):
    """Question headings ending in ? after index start; stop at a non-question heading of level <= stop_level."""
    qas, i = [], start
    while i < len(bl):
        b = bl[i]
        if b[0] == "h":
            if b[2].endswith("?"):
                paras, j = [], i + 1
                while j < len(bl) and bl[j][0] == "t":
                    paras.append(bl[j][1]); j += 1
                qas.append((b[2], paras))
                i = j
                continue
            if b[1] <= stop_level:
                break
        i += 1
    return qas


def extract_qas(body):
    soup = BeautifulSoup(body, "html.parser")
    bl = blocks(soup)
    faq_idx = next((i for i, b in enumerate(bl) if b[0] == "h" and re.search(r"frequently asked|\bfaqs?\b", b[2], re.I)), None)
    qas, source = [], "none"
    if faq_idx is not None:
        qas = qa_from(bl, faq_idx + 1, bl[faq_idx][1])
        source = "faq_section"
    if len(qas) < 2:
        qas = [(h[2], [])for h in []]
        allq, i = [], 0
        while i < len(bl):
            if bl[i][0] == "h" and bl[i][2].endswith("?") and bl[i][1] in (2, 3):
                paras, j = [], i + 1
                while j < len(bl) and bl[j][0] == "t":
                    paras.append(bl[j][1]); j += 1
                allq.append((bl[i][2], paras)); i = j
            else:
                i += 1
        qas, source = allq[:6], "body_headings"
    return qas, source


def build_schema(qas):
    items, dropped = [], 0
    for q, paras in qas:
        if not paras:
            dropped += 1; continue
        ans = " ".join(paras)
        if len(ans) > MAX_ANS:
            ans = paras[0]
        if len(ans) > 1500 or CLAIM.search(ans) or re.search(r"fullyvital", ans, re.I):
            dropped += 1; continue
        items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}})
        if len(items) == MAX_QA:
            break
    return items, dropped


def schema_block(items):
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False) + "\n</script>"


def controls():
    c = json.loads(CONTROLS.read_text())
    s = set(c.keys())
    for v in c.values():
        s |= set(v)
    return {u.replace(SITE, "") for u in s}


def fetch_all(s):
    return {f"/blogs/{a['blog']['handle']}/{a['handle']}": a for a in s.articles()}


def draft():
    s = Shopify()
    arts = fetch_all(s)
    ctrl = controls()
    rows = list(csv.DictReader(PAGES.open()))
    answers = json.loads(ANSWERS.read_text()) if ANSWERS.exists() else {}
    digest, out = [], []
    for r in rows:
        p = r["path"]
        a = arts.get(p)
        skip, flags = "", []
        if not a: skip = "not found"
        elif not a["isPublished"]: skip = "not published"
        elif p in ctrl: skip = "refresh-test page"
        elif '"@type": "FAQPage"' in a["body"] or '"@type":"FAQPage"' in a["body"]: skip = "already has FAQPage"
        qas, items, dropped, src = [], [], 0, ""
        if not skip:
            qas, src = extract_qas(a["body"])
            items, dropped = build_schema(qas)
            soup = BeautifulSoup(a["body"], "html.parser")
            txt = norm(soup.get_text(" "))
            digest.append(f"=== {p}\nTITLE: {a['title']}\nINTRO: {txt[:900]}\nHEADINGS: " +
                          " | ".join(norm(h.get_text(' ')) for h in soup.find_all(["h2", "h3"])[:14]) + "\n")
            if len(items) < 2:
                flags.append("no schema (fewer than 2 usable Q&As)"); items = []
            if src == "body_headings": flags.append("schema from body question headings")
            if dropped: flags.append(f"{dropped} Q&A left out (pitch/claim word/long/empty)")
            if "<script" in a["body"] and "ld+json" in a["body"]: flags.append("page has existing JSON-LD")
        sa = answers.get(p.rsplit("/", 1)[1], {})
        sa_text = sa.get("answer", "") if isinstance(sa, dict) else sa
        if isinstance(sa, dict) and sa.get("flag"): flags.append(sa["flag"])
        wc = len(sa_text.split())
        # "Short answer:" label not counted in the 30-60 words
        if not skip:
            if not sa_text: flags.append("MISSING short answer")
            elif not 30 <= wc <= 60: flags.append(f"word count {wc} out of range")
            elif len(re.findall(r"[.!?](?:\s|$)", sa_text)) != 2: flags.append("not exactly 2 sentences")
            elif CLAIM.search(sa_text): flags.append("claim word in short answer")
        out.append({"path": p, "short_answer": sa_text, "word_count": wc, "faq_count": len(items),
                    "faq_questions": " || ".join(i["name"] for i in items), "skipped_reason": skip,
                    "flags": "; ".join(flags), "_schema": json.dumps(items, ensure_ascii=False),
                    "title": a["title"] if a else r["title"]})
    cols = ["path", "short_answer", "word_count", "faq_count", "faq_questions", "skipped_reason", "flags"]
    with DRAFTS.open("w", newline="") as f:
        w = csv.DictWriter(f, cols + ["faq_json"]); w.writeheader()
        for o in out:
            w.writerow({**{c: o[c] for c in cols}, "faq_json": o["_schema"]})
    md = ["# AEO quick pass: drafts for review", "",
          f"{sum(1 for o in out if not o['skipped_reason'])} pages to update, {sum(1 for o in out if o['skipped_reason'])} skipped.", ""]
    for o in out:
        md += [f"## {o['title']}", f"`{o['path']}`", ""]
        if o["skipped_reason"]:
            md += [f"**Skipped:** {o['skipped_reason']}", ""]; continue
        md += [f"**Short answer ({o['word_count']} words):** {o['short_answer']}", ""]
        if o["faq_count"]:
            md += [f"**FAQ schema ({o['faq_count']}):**"] + [f"- {q}" for q in o["faq_questions"].split(" || ")] + [""]
        else:
            md += ["**FAQ schema:** none", ""]
        if o["flags"]: md += [f"**Flags:** {o['flags']}", ""]
    REVIEW.write_text("\n".join(md))
    print("pages", len(out), "skipped", sum(1 for o in out if o["skipped_reason"]),
          "flagged", sum(1 for o in out if o["flags"]), "no schema", sum(1 for o in out if not o["skipped_reason"] and not o["faq_count"]))


def apply(limit):
    s = Shopify(apply=True)
    ctrl = controls()
    rows = [r for r in csv.DictReader(DRAFTS.open()) if not r["skipped_reason"]]
    bad = [r["path"] for r in rows if "MISSING" in r["flags"] or "out of range" in r["flags"] or "not exactly" in r["flags"] or "claim word in short" in r["flags"]]
    if bad: sys.exit(f"drafts with problems: {bad}")
    print("backup:", s.backup_articles())
    done = 0
    for r in rows:
        if limit and done >= limit: break
        p = r["path"]
        if p in ctrl: continue
        handle = p.rsplit("/", 1)[1]
        # find id via listing handle is cheap enough: fetch by query
        a = s.gql('query($q: String!) { articles(first: 5, query: $q) { nodes { id handle blog { handle } } } }', {"q": f"handle:{handle}"})["articles"]["nodes"]
        a = [x for x in a if x["blog"]["handle"] == p.split("/")[2] and x["handle"] == handle]
        if len(a) != 1: print("SKIP cannot resolve", p); continue
        cur = s.gql("query($id: ID!) { article(id: $id) { " + ARTICLE_FIELDS + " } }", {"id": a[0]["id"]})["article"]
        body = cur["body"]
        if not cur["isPublished"] or "FAQPage" in body or "fv-keyfact" in body:
            print("SKIP changed since draft", p); continue
        items = json.loads(r["faq_json"])
        new = f'<p class="fv-keyfact"><strong>Short answer:</strong> {html.escape(r["short_answer"], quote=False)}</p>\n' + body
        if items: new = new.rstrip("\n") + "\n" + schema_block(items)
        s.update_article(cur, {"body": new})
        done += 1; print("updated", p); time.sleep(0.6)
    print("done", done)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true"); ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    apply(a.limit) if a.apply else draft()
