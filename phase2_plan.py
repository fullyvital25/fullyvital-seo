"""
Phase 2C: score clusters, inventory the pages serving each cluster, and propose decisions for the
132 held posts and 69 brand-comparison posts. Cached data only (no API calls).

Outputs:
    data/processed/phase2_cluster_scores.csv
    data/processed/phase2_page_cluster_map.csv
    data/processed/phase2_held_decisions.csv
    data/processed/phase2_comparison_decisions.csv

Usage:
    python phase2_plan.py
"""

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

import phase2_keywords as p2

O = "data/processed/"
AVOID = {"Drugs: minoxidil, finasteride & Rx", "Medications that cause hair loss", "Gray: coverage, dye & styling",
         "Gray: care for gray hair", "Styling for thinning hair", "Off-scope: beard, brows, lashes, body, pets"}
COMMERCIAL = {"Gray: supplements & products", "Gray: competitor brands", "Hair vitamins & supplements (commercial)",
              "Growth products: serums, shampoos, kits", "Collagen", "Hair, skin & nails vitamins", "Competitor brands (growth)"}
# exact brand terms -> (brand family, line). Only brands that compete with FullyVital's products.
BRANDS = {"nutrafol": ("Nutrafol", "growth"), "viviscal": ("Viviscal", "growth"), "vegamour": ("Vegamour", "growth"),
          "arey": ("Arey", "gray"), "particle": ("Particle", "gray"), "mayraki": ("Mayraki", "gray"), "heyhair": ("Heyhair", "gray"),
          "pura d": ("Pura d'or", "growth"), "nioxin": ("Nioxin", "growth"), "olly": ("Olly", "growth"), "hairmax": ("HairMax", "growth"),
          "keranique": ("Keranique", "growth"), "sugar bear": ("Sugar Bear", "growth"), "hairburst": ("Hairburst", "growth"),
          "hum nutrition": ("HUM", "growth"), "wellbel": ("Wellbel", "growth"), "hairtamin": ("Hairtamin", "growth"),
          "mielle": ("Mielle", "growth"), "divi": ("Divi", "growth"), "act+acre": ("Act+Acre", "growth"), "act acre": ("Act+Acre", "growth"),
          "for hers": ("Hers", "growth"), "forhers": ("Hers", "growth"), "kerastase": ("Kérastase", "growth"),
          "revitalash": ("RevitaLash", "growth"), "shapiro": ("Shapiro MD", "growth"), "bosley": ("Bosley", "growth")}


# Direct competitors: supplement/serum brands a FullyVital shopper would weigh up.
DIRECT = {"Nutrafol", "Viviscal", "Vegamour", "Pura d'or", "Arey", "Particle", "Mayraki", "Heyhair"}


def main():
    u = pd.read_csv(O + "phase2_keyword_universe.csv")
    cl = pd.read_csv(O + "phase2_clusters.csv")
    rev = pd.read_csv(O + "blog_cleanup_review.csv")
    rev["url"] = "https://fullyvital.com" + rev.path
    queue = set(pd.read_csv(O + "refresh_queue.csv").path)
    done = {"/blogs/" + d.name.replace("__", "/") for d in Path("data/refresh_drafts").iterdir() if (d / "published.json").exists()}
    idx = pd.read_csv(O + "index_status_all.csv") if Path(O + "index_status_all.csv").exists() else None

    # ---------- cluster scores ----------
    fit = np.where(cl.cluster.isin(AVOID) | (cl.product_fit == "none"), 0.0, 1.0)
    risk = cl.compliance.map({"disease topic": 0.6, "drug topic": 0.0, "treat/prevent wording": 0.8, "reverse/prevent wording": 0.8}).fillna(1.0)
    ability = 0.5 + 0.5 * np.minimum(1, cl.winnable_volume / cl.volume.replace(0, np.nan)).fillna(0)
    visible = np.where(cl.fv_top20 > 0, 1.15, 1.0)
    cl["score"] = (cl.volume_dedup * fit * risk * ability * visible * (1 + cl.commercial_share)).round(0)
    cl["line_rank"] = cl.groupby("line").score.rank(ascending=False, method="first").astype(int)

    def action(r):
        if r.cluster in AVOID:
            return "Avoid (no product fit, or drug/styling topic)"
        if r.cluster in COMMERCIAL:
            return "Commercial: optimise product/collection page + compliant comparison/guide content"
        if r.compliance == "disease topic":
            return "Informational, careful: one sourced hub, no product claims near disease content"
        if r.fv_top10 > 0:
            return "Strengthen: existing pages already rank top 10; refresh and interlink"
        return "Build: hub page + supporting articles (reuse existing posts where they fit)"
    cl["action"] = cl.apply(action, axis=1)

    # ---------- page inventory per cluster ----------
    live = rev[~rev.decision.str.startswith(("MERGE:", "REMOVE"))].copy()
    live["kw"] = live.primary_keyword_guess.fillna(live.title).astype(str)
    live[["line", "cluster", "product_fit", "compliance"]] = live.kw.apply(lambda k: pd.Series(p2.classify(k)))
    live["status"] = np.select([live.path.isin(done), live.path.isin(queue), live.decision.str.startswith("HOLD: brand"),
                                live.decision.str.startswith("HOLD: in scope"), live.decision.str.startswith("LEAVE")],
                               ["refreshed", "in refresh queue", "comparison (held)", "held (Phase 2)", "new in 2026"], "kept")
    if idx is not None:
        live = live.merge(idx[["url", "coverage"]], on="url", how="left")
    live = live.merge(cl[["cluster", "line_rank", "action"]], on="cluster", how="left")
    hub = (live[live.status.isin(["refreshed", "in refresh queue", "kept", "new in 2026"])]
           .sort_values(["clicks_90d", "clicks_16m", "impressions_90d"], ascending=False).drop_duplicates("cluster").set_index("cluster").path)
    live["cluster_hub"] = live.cluster.map(hub)
    cols = ["path", "status", "line", "cluster", "line_rank", "action", "cluster_hub", "title", "primary_keyword_guess",
            "clicks_16m", "clicks_90d", "impressions_90d", "referring_domains", "word_count"] + (["coverage"] if idx is not None else [])
    live[cols].sort_values(["line", "line_rank", "clicks_90d"], ascending=[True, True, False]).to_csv(O + "phase2_page_cluster_map.csv", index=False)
    # current best page by Search Console impressions on the cluster's keywords (fact) ...
    livep = set(live.url)
    x = u[u.current_url.isin(livep) & u.current_url.str.contains("/blogs/", na=False)]
    top_by_impr = (x.groupby(["cluster", "current_url"]).gsc_impressions_16m.sum().reset_index()
                   .sort_values(["cluster", "gsc_impressions_16m"], ascending=[True, False]).drop_duplicates("cluster")
                   .set_index("cluster").current_url.str.replace("https://fullyvital.com", "", regex=False))
    # ... and a suggested hub: the live (non-held, non-comparison) page whose URL best matches the head term
    GEN = set("for the and of to in a is with on does do can how what your my are it be hair growth grow supplement loss men man women woman best top".split())
    norm_t = lambda t: {x for x in (("gray" if w in ("grey", "greying", "graying", "white") else re.sub(r"(ies|es|s)$", "", w))
                                    for w in re.findall(r"[a-z0-9]+", str(t).lower())) if x not in GEN}
    cand = live[live.status.isin(["refreshed", "in refresh queue", "kept", "new in 2026"])]
    cand_t = [(r.path, r.line, norm_t(r.path.rsplit("/", 1)[-1].replace("-", " "))) for r in cand.itertuples()]

    def suggest(r):
        h = norm_t(r.head_term)
        if not (h - {"gray"}):
            return None
        score = lambda t: len(h & t) / max(1, len(h | t)) if (h & t) - {"gray"} else 0
        best = max(((p, score(t)) for p, ln, t in cand_t if ln == r.line), key=lambda z: z[1], default=(None, 0))
        return best[0] if best[1] >= 0.5 else None
    pages_per = live.groupby("cluster").agg(live_pages=("path", "size"), held_pages=("status", lambda s: int((s == "held (Phase 2)").sum())))
    cl = cl.merge(pages_per, on="cluster", how="left").fillna({"live_pages": 0, "held_pages": 0})
    cl["top_page_by_impressions"] = cl.cluster.map(top_by_impr)
    cl["hub_page"] = cl.apply(suggest, axis=1)
    cl.sort_values(["line", "line_rank"]).to_csv(O + "phase2_cluster_scores.csv", index=False)

    # ---------- held posts (132) ----------
    held = live[live.status == "held (Phase 2)"].copy()
    not_indexed = (held.coverage.fillna("").str.contains("not indexed|unknown", case=False)) if "coverage" in held else False

    STOP = set(("for the and of to in a is with on does do can how what your my are it be from at by an you i hair growth loss "
                "before after best top guide good help use vs or fully vital benefit secret unlock power ultimate why which "
                "cause your everything need know natural healthy stimulat women men tip").split())
    w_ok = lambda x: x != "nan"
    stem = lambda t: {x for x in (re.sub(r"(ies|es|s|ing)$", "", w) for w in re.findall(r"[a-z0-9]+", "" if pd.isna(t) else str(t).lower())) if x and x not in STOP and w_ok(x)}
    keepers = live[live.status.isin(["refreshed", "in refresh queue", "kept", "new in 2026"])]
    slug = lambda p: p.rsplit("/", 1)[-1].replace("-", " ")
    keep_stems = [(r.path, r.cluster, stem(slug(r.path))) for r in keepers.itertuples() if not re.search(r"\bor fully|fully vital or|vs", r.path.replace("-", " "))]
    from collections import Counter
    df = Counter(t for _, _, ks in keep_stems for t in ks)
    uk = u.dropna(subset=["volume"])[["keyword", "volume"]].copy()
    uk["st"] = uk.keyword.map(stem)

    def topic_demand(st):
        """Largest volume among universe keywords that share most of this post's topic words."""
        if not st:
            return 0
        m = uk[uk.st.map(lambda k: len(st & k) / max(1, len(st)) >= 0.67 and len(st & k) >= 1)]
        return m.volume.max() if len(m) else 0

    def held_decision(r):
        if r.cluster in AVOID:
            return ("Remove (off-strategy topic)", None)
        if re.search(r"\bor fully|fully vital or|vs fully|fully vital vs", slug(r.path)):
            return ("Remove (indirect brand comparison, no demand)", None)
        st = stem(slug(r.path))
        # same subtopic as a live page -> merge into it (prefer same cluster)
        def match(k):
            shared = st & k[2]
            specific = [t for t in shared if df.get(t, 0) <= 4]   # a rare topic word, not "oil" or "benefit"
            return (len(shared) / max(1, len(st | k[2])) if specific and len(shared) >= 1 else 0) + (0.05 if k[1] == r.cluster else 0)
        best = max(keep_stems, key=match, default=None)
        if best and match(best) >= 0.5:
            return ("Merge into existing page on the same subtopic", best[0])
        demand = topic_demand(st | stem(r.primary_keyword_guess))
        if demand >= 1000:
            return ("Rewrite as supporting article (distinct subtopic with demand)", None)
        if demand >= 100:
            return ("Fold into the planned hub for this cluster", None)
        return ("Remove (no demand, no clear home)", None)
    held[["decision_p2", "target"]] = held.apply(lambda r: pd.Series(held_decision(r)), axis=1)
    held["topic_demand"] = held.apply(lambda r: topic_demand(stem(slug(r.path)) | stem(r.primary_keyword_guess)), axis=1)
    # one rewrite per topic: rewrite candidates on the same topic (same matched demand + shared rare word) merge into the strongest
    rw = held[held.decision_p2.str.startswith("Rewrite")].sort_values(["impressions_90d", "word_count"], ascending=False)
    seen = []
    for i, r in rw.iterrows():
        st = stem(slug(r.path))
        twin = next((p for p, d, ks in seen if d == r.topic_demand and ((st & ks) - {"oil", "vitamin", "extract", "acid"})), None)
        if twin:
            held.loc[i, ["decision_p2", "target"]] = ["Merge into the rewrite of the same topic", twin]
        else:
            seen.append((r.path, r.topic_demand, st))
    held["not_indexed"] = not_indexed
    held.to_csv(O + "phase2_held_decisions.csv", index=False)

    # ---------- comparison posts (69) ----------
    comp = live[live.status == "comparison (held)"].copy()

    def brand_of(r):
        t = (r.path + " " + str(r.title)).lower().replace("-", " ")
        for k, (b, line) in BRANDS.items():
            if k in t:
                return b, line
        # otherwise take the brand from the URL handle: the part that isn't "fully vital"/"vs"
        h = r.path.rsplit("/", 1)[-1]
        h = re.sub(r"(-anti-gray-comparison|-1|-choosing.*|-premium.*|-hair-serum)$", "", h)
        h = re.sub(r"fully-?vital|-?vs-?|-?versus-?|-?or-?", " ", h).replace("-", " ").strip()
        return (h.title() or None), "growth"
    comp[["brand", "brand_line"]] = comp.apply(lambda r: pd.Series(brand_of(r)), axis=1)
    bvol = {}
    for k, (b, _) in BRANDS.items():
        x = u[u.keyword.str.contains(rf"\b{re.escape(k)}", case=False, na=False)]
        bvol[b] = bvol.get(b, 0) + x.volume.sum()
    def vol(b):
        if b in bvol:
            return bvol[b]
        x = u[u.keyword.str.contains(rf"\b{re.escape(str(b).lower())}\b", case=False, na=False)]
        return x.volume.sum()
    comp["brand_keyword_volume"] = comp.brand.map(vol).fillna(0)
    real = comp.title.str.contains(r"(?:\bvs\.?|versus|\bor)\s+fully\s?vital|fully\s?vital\s+(?:vs\.?|versus|or)\b", case=False)

    def comp_decision(r):
        if not r.real:
            return "Not a brand comparison: treat as a normal post (keep)"
        if r.brand in DIRECT and (r.brand_keyword_volume >= 3000 or r.clicks_16m >= 10):
            return "Keep and refresh (brand has search demand): honest, sourced comparison, no claims about the competitor you can't support"
        return "Remove (no demand for this brand); fold any useful content into a 'FullyVital alternatives' guide"
    comp["real"] = real
    comp["decision_p2"] = comp.apply(comp_decision, axis=1)
    comp.to_csv(O + "phase2_comparison_decisions.csv", index=False)

    pd.set_option("display.width", 260, "display.max_colwidth", 70)
    print(cl.sort_values(["line", "line_rank"])[["line", "line_rank", "cluster", "volume_dedup", "winnable_volume", "fv_top10", "score", "live_pages", "held_pages", "action"]].to_string())
    print("\nheld:", held.decision_p2.value_counts().to_dict(), "| not indexed:", int(held.not_indexed.sum()) if idx is not None else "n/a")
    print("comparison:", comp.decision_p2.str[:40].value_counts().to_dict())
    print(comp[comp.decision_p2.str.startswith("Keep")][["path", "brand", "brand_keyword_volume", "clicks_16m"]].to_string())


if __name__ == "__main__":
    main()
