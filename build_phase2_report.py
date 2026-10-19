"""Phase 2 deliverable: reports/phase2-content-plan.md, built from data/processed/phase2_* files."""
import glob
from pathlib import Path

import pandas as pd

O = "data/processed/"
cl = pd.read_csv(O + "phase2_cluster_scores.csv")
pm = pd.read_csv(O + "phase2_page_cluster_map.csv")
held = pd.read_csv(O + "phase2_held_decisions.csv")
comp = pd.read_csv(O + "phase2_comparison_decisions.csv")
serp = pd.read_csv(O + "phase2_serp_summary.csv")
uni = pd.read_csv(O + "phase2_keyword_universe.csv")
idx = pd.read_csv(O + "index_status_all.csv") if Path(O + "index_status_all.csv").exists() else None
spend = sum(pd.read_csv(f).cost_usd.sum() for f in [O + "dfs_spend_phase2_suggestions.csv", O + "dfs_spend_phase2_serp.csv"])


def fmt(v):
    if isinstance(v, float):
        return "—" if pd.isna(v) else f"{v:,.0f}"
    return "—" if v is None else str(v).replace("|", "/")


def table(df, cols, names):
    out = ["| " + " | ".join(names) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    out += ["| " + " | ".join(fmt(v) for v in r) + " |" for r in df[cols].itertuples(index=False)]
    return "\n".join(out)


short = lambda p: p if not isinstance(p, str) else p.replace("https://fullyvital.com", "")
cl["hub_page"] = cl.hub_page.map(short)
act = cl[(cl.score > 0) & ~cl.cluster.str.endswith("general")]
pri_g = act[(act.line == "gray")].sort_values("line_rank").head(8)
pri_h = act[(act.line == "growth")].sort_values("line_rank").head(12)
avoid = cl[cl.score == 0]
sv = serp.set_index("cluster")

L = ["# Phase 2: Keyword research and content plan\n",
     "Scope: gray/grey hair and hair growth/hair loss, mapped to the 10 FullyVital products in `data/reference/fullyvital_products.csv`. "
     "No changes were made to the site. Everything here is a recommendation for you to approve.\n"]

# ---------- summary ----------
gray_dem = act[act.line == "gray"].volume_dedup.sum()
growth_dem = act[act.line == "growth"].volume_dedup.sum()
A = L.append
A("## Summary\n")
A(f"1. **Keyword universe:** {len(uni):,} in-scope keywords ({(uni.source == 'dataforseo').sum():,} with search volume from DataForSEO, "
  f"{(uni.source == 'gsc_only').sum():,} from Search Console only), grouped into {len(cl)} topic clusters across the two product lines.")
A(f"2. **Where the demand is that FullyVital can serve:** about {growth_dem:,.0f} monthly searches across hair growth/loss clusters and "
  f"{gray_dem:,.0f} across gray-hair clusters (de-duplicated; clusters with no product fit excluded).")
A(f"3. **Gray hair is the smaller market but the better fit.** The largest gray cluster by raw volume is coverage, dye and styling ({cl.loc[cl.cluster == 'Gray: coverage, dye & styling', 'volume_dedup'].iat[0]:,.0f}), "
  "which FullyVital's products don't serve. The clusters that do fit (causes, early graying, nutrients, myths, products) are informational, "
  "and results pages for them are led by medical sites (AAD, Harvard, Cleveland Clinic) plus a few brands, notably neofollics.com.")
A("4. **FullyVital barely ranks in either line.** It has top-10 positions in only a handful of clusters, mostly long-tail ingredient pages in hair growth; "
  "no gray cluster has more than 5 top-10 keywords.")
top3 = ", ".join(pri_h.cluster.head(3))
A(f"5. **Highest-scoring hair-growth clusters (excluding the catch-all):** {top3}. These combine demand, product fit and commercial intent.")
A(f"6. **Biggest demand to avoid:** prescription drugs ({cl.loc[cl.cluster.str.startswith('Drugs'), 'volume_dedup'].iat[0]:,.0f} searches) and "
  "medications that cause hair loss. They have no product fit and carry compliance risk.")
hd = held.decision_p2.value_counts()
A(f"7. **The 132 held posts:** {int(hd.filter(like='Rewrite').sum())} rewrite (one per distinct topic with demand), "
  f"{int(hd.filter(like='Merge').sum() + hd.filter(like='Fold').sum())} merge or fold into another page, "
  f"{int(hd.filter(like='Remove').sum())} remove.")
cd = comp.decision_p2.str[:4].value_counts()
A(f"8. **The 69 brand comparison posts:** keep and refresh {int(cd.get('Keep', 0))} (direct competitors with search demand: "
  f"{', '.join(comp[comp.decision_p2.str.startswith('Keep')].brand)}), remove {int(cd.get('Remo', 0))}, "
  f"and {int(cd.get('Not ', 0))} aren't brand comparisons.")
if idx is not None:
    ix = idx.coverage.value_counts()
    A(f"9. **Indexing:** of {len(idx)} published articles inspected, {int(ix.get('Submitted and indexed', 0))} are indexed; "
      f"{int(ix.filter(like='not indexed').sum())} are crawled or discovered but not indexed, and {int(ix.get('URL is unknown to Google', 0))} are unknown to Google.")
A(f"10. **DataForSEO spend for Phase 2:** ${spend:.2f}.\n")

# ---------- method ----------
A("## How this was built\n")
A("- **Keywords:** Phase 1 data (FullyVital and 8 competitors' in-scope rankings, the 514-keyword gap list, 16 months of Search Console queries) "
  "plus DataForSEO keyword suggestions for 22 seed terms, 12 of them gray-hair, because Phase 1 had little gray-hair data.")
A("- **Clusters:** rule-based topic taxonomy, see `phase2_keywords.py`. Each keyword is mapped to the product it serves, FullyVital's best current page, and that page's clean-up status.")
A("- **De-duplicated demand:** DataForSEO gives every variant of a search family the same volume (for example, 25 \"haircuts for thinning hair women\" variants at 18,100 each). "
  "Variants with the same volume and mostly the same words are counted once. Raw sums are in the CSV for reference.")
A("- **Winnability:** a lower-authority competitor already ranks top 10, or the top 10's average domain rank is at or below FullyVital's (317).")
A("- **Score:** de-duplicated demand × product fit × compliance factor × winnability × commercial intent. A ranking aid, not a forecast.")
A("- **Results-page check:** live top 10 for the head term of each priority cluster (30 searches).\n")

# ---------- clusters ----------
for line, title, pri in [("gray", "Gray hair clusters", pri_g), ("growth", "Hair growth and hair loss clusters", pri_h)]:
    A(f"## {title}\n")
    x = cl[cl.line == line].sort_values("line_rank")
    A(table(x, ["line_rank", "cluster", "volume_dedup", "head_term", "fv_top10", "winnable_volume", "product_fit", "live_pages", "action"],
            ["Rank", "Cluster", "Demand (de-duplicated)", "Head term", "FullyVital top-10 keywords", "Winnable volume", "Product", "Live posts", "Recommended action"]))
    A("")

# ---------- priority cluster plans ----------
A("## Priority clusters: what to do\n")
A("For each priority cluster: the existing page to build around (the hub), what the results page looks like, and the next step. "
  "\"Hub\" means the page that should own the head term; other posts on the topic link to it or are merged into it. "
  "Suggested hubs are matched by URL to the head term, so confirm each one editorially. Where none fits, a new hub page is needed.\n")
for line, pri in [("gray", pri_g), ("growth", pri_h)]:
    A(f"### {'Gray hair' if line == 'gray' else 'Hair growth and hair loss'}\n")
    for r in pri.itertuples():
        s = sv.loc[r.cluster] if r.cluster in sv.index else None
        if isinstance(s, pd.DataFrame):
            s = s.iloc[0]
        pages = pm[pm.cluster == r.cluster]
        held_n = int((pages.status == "held (Phase 2)").sum())
        serp_note = (f"Top 10 for \"{s.keyword}\": {int(s.publishers)} publishers/medical, {int(s.brands)} brands or clinics, "
                     f"{int(s.ugc)} forums or video, {int(s.marketplace)} marketplaces; {int(s.product_pages)} product pages. Leaders: {s.top3}."
                     if s is not None else "No results-page check.")
        tp = r.top_page_by_impressions if isinstance(r.top_page_by_impressions, str) else "none"
        A(f"**{r.cluster}.** {fmt(r.volume_dedup)} searches/month (head term \"{r.head_term}\", {fmt(r.head_volume)}). "
          f"Product: {r.product_fit}. Suggested hub: `{r.hub_page if isinstance(r.hub_page, str) else 'none: a new hub page is needed'}`; "
          f"page with most impressions today: `{tp}`. "
          f"{int(r.live_pages)} live posts, {held_n} held. {serp_note} **Next:** {r.action}.\n")

# ---------- commercial ----------
A("The two \"general\" clusters are catch-alls for keywords that fit no specific topic. They're kept in the tables but aren't priorities on their own.\n")
A("## Commercial pages\n")
A("Commercial searches (\"hair growth supplements\", \"hair serum for hair growth\", \"products for gray hair\", \"arey grey\") show product pages, "
  "marketplaces and brand sites, not blog posts. These need product or collection pages, which are outside what this project may edit. Recommendations:\n")
for r in cl[cl.action.str.startswith("Commercial")].sort_values("score", ascending=False).itertuples():
    top = uni[(uni.cluster == r.cluster) & uni.intent.isin(["commercial", "transactional"])].sort_values("volume", ascending=False).keyword.head(4)
    A(f"- **{r.cluster}** ({fmt(r.volume_dedup)}/month; product: {r.product_fit}). Target terms: {', '.join(top) if len(top) else r.head_term}.")
A("\nFix the product-page \"reverse gray\" wording (Phase 1 list) before pointing any new content or internal links at those pages.\n")

# ---------- held / comparison ----------
A("## Decisions: the 132 held posts\n")
A(table(held.decision_p2.value_counts().rename_axis("Decision").reset_index(name="Posts"), ["Decision", "Posts"], ["Decision", "Posts"]))
A("\nRewrites (one per topic):\n")
A(table(held[held.decision_p2.str.startswith("Rewrite")].sort_values("topic_demand", ascending=False), ["path", "cluster", "topic_demand"],
        ["Post", "Cluster", "Demand for the topic"]))
A("\nFull list with merge targets: `data/processed/phase2_held_decisions.csv`.\n")
A("## Decisions: the 69 brand comparison posts\n")
A(table(comp[comp.decision_p2.str.startswith("Keep")].sort_values("brand_keyword_volume", ascending=False),
        ["path", "brand", "brand_keyword_volume", "clicks_16m"], ["Keep and refresh", "Brand", "Brand search volume (in-scope)", "Clicks 16m"]))
A("\nKept comparisons must be honest and sourced: no claims about a competitor's product that you can't support, no \"reverse gray\" wording "
  "(three current comparison posts say FullyVital products \"delay and reverse gray hairs\"). The other "
  f"{int(cd.get('Remo', 0))} have no meaningful brand demand; remove them and fold anything useful into one \"FullyVital alternatives\" guide. "
  "Full list: `data/processed/phase2_comparison_decisions.csv`.\n")

# ---------- index ----------
if idx is not None:
    A("## Index status of published articles\n")
    ix = idx.coverage.value_counts().rename_axis("Coverage").reset_index(name="Articles")
    A(table(ix, ["Coverage", "Articles"], ["Google's status", "Articles"]))
    ni = idx[~idx.coverage.eq("Submitted and indexed")]
    by = ni.groupby(ni.pub_year.fillna("?").astype(str).str[:4]).size().rename_axis("Published").reset_index(name="Not indexed")
    A("\n" + table(by, ["Published", "Not indexed"], ["Published", "Articles not indexed"]))
    cm = int(idx.canonical_mismatch.sum())
    idx["indexed"] = idx.coverage.eq("Submitted and indexed")
    held_ix = idx[idx.decision.fillna("").str.startswith("HOLD: in scope")]
    zero = idx[idx.impressions_90d.fillna(0) == 0]
    A(f"\n- **Google is skipping the weakest posts.** {int((~held_ix.indexed).sum())} of the {len(held_ix)} held posts aren't indexed, and only "
      f"{zero.indexed.mean():.0%} of articles with no impressions in 90 days are. Every refreshed, merge-target and kept article that earns traffic is indexed.")
    A(f"- **Crawling is slow.** {int((idx.coverage == 'URL is unknown to Google').sum())} published articles have never been seen by Google, and two posts published in July "
      "were last crawled before they went live. Removing low-value posts should help Google spend its crawl on the pages that matter.")
    A(f"- **No technical blockers:** robots.txt allows every crawled page, and Google chose a different canonical for {cm} articles.")
    new = idx[idx.decision.isna()]
    if len(new):
        A(f"- **New posts are still being published outside this work:** {', '.join('`' + short(u) + '`' for u in new.url)} went live after the clean-up sheet was made. "
          "One is a new brand comparison. Agree on who publishes what, so new posts follow the plan and the claims rules.")
    A("\nFull data: `data/processed/index_status_all.csv`.\n")

# ---------- calendar ----------
A("## Proposed sequence (hypotheses, for you to approve)\n")
A("1. **Weeks 1–4: finish consolidating.** The other session completes the 111 refreshes. In parallel, apply the held and comparison decisions as one clean-up batch, "
  "using the same safeguards as the first one (backlink check, redirects for merges, logged and reversible). You fix the product-page claims.")
A("2. **Weeks 3–8: build the gray-hair hubs.** Gray is the core product line and has little competition from brands. Start with the causes cluster (hub plus spokes "
  "on early graying, stress, B12 and copper, and myths). Reuse the 2026 gray posts already written as spokes and interlink them.")
A("3. **Weeks 5–10: strengthen the hair-growth clusters where FullyVital already has pages:** remedies and how to stop hair loss, topical oils (rosemary), "
  "vitamins and supplements, and protein and food. Pick one hub per cluster from the existing posts and merge the duplicates into it.")
A("4. **About 6–8 weeks after each refresh batch: read the refresh test** (`refresh_tracker.py`). If refreshed pages gain impressions against the controls, "
  "keep refreshing and consolidating before writing new posts. If they don't, shift effort to fewer, deeper hub pages and to the commercial pages.")
A("5. **Not before then: new articles for clusters with no page at all.** Adding volume to a site Google may already rate as low-quality risks repeating the problem.\n")

A("## Compliance notes\n")
A("- **Avoid entirely:** prescription drugs and medications that cause hair loss. Gray coverage, dye and styling clusters have no product fit, so skip them unless you want top-of-funnel traffic.")
A("- **Conditions** (alopecia, telogen effluvium, PCOS, thyroid): at most one sourced informational hub, with no product claims near disease content.")
A("- **\"Hair loss treatment\" and similar searches** (the remedies cluster) are worth targeting with how-to and support content. FullyVital pages must not present a supplement or serum as a treatment for hair loss; describe what ingredients support, and point to a doctor for diagnosis.")
A("- **\"Reverse\", \"stop\" and \"prevent\" gray-hair searches** are high-intent but sensitive. Answer them honestly (\"no study has shown…\") and never promise reversal.")
A("- **New articles** follow the citation style in CLAUDE.md (3 studies, each linked once, all in the second half).\n")
A("## Caveats\n")
A("- **Volumes** are DataForSEO estimates, and the de-duplication is a heuristic. Use them to rank, not forecast.")
A("- **Clusters** come from keyword rules. A few keywords will be misfiled; the CSV has every keyword with its cluster.")
A("- **Winnability** relies on domain rank, not page-level link data. DataForSEO keyword difficulty is unreliable (Phase 1) and isn't used.")
A("- **Held-post decisions** are rule-based drafts, like the first clean-up sheet. Review them before anything is applied.")
A(f"- **DataForSEO spend:** Phase 2 cost ${spend:.2f}. The balance is about $48.")
Path("reports/phase2-content-plan.md").write_text("\n".join(L) + "\n")
print("\n".join(L[:20]))
