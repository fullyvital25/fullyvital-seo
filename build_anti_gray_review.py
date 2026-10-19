"""reports/anti-gray-review.md: review of the 66-article anti-gray calendar + gray-hub plan (numbers from data/processed)."""
import pandas as pd
O = "data/processed/"
rv = pd.read_csv(O + "anti_gray_review.csv"); pc = pd.read_csv(O + "anti_gray_product_claims.csv"); ov = pd.read_csv(O + "anti_gray_overlap.csv")
cl = pd.read_csv(O + "phase2_cluster_scores.csv"); aeo = pd.read_csv(O + "aeo_tracking.csv"); aeo = aeo[aeo.run == aeo.run.max()]
f = lambda v: "—" if pd.isna(v) else (f"{v:,.0f}" if isinstance(v, (int, float)) else str(v).replace("|", "/"))
def table(df, cols, names):
    return "\n".join(["| " + " | ".join(names) + " |", "|" + "|".join("---" for _ in cols) + "|"] +
                     ["| " + " | ".join(f(v) for v in r) + " |" for r in df[cols].itertuples(index=False)])
cal_claims = pc[pc.in_calendar]; out = pc[~pc.in_calendar]
g = cl[cl.line == "gray"].set_index("cluster")
L = []; A = L.append
A("# Anti-gray content review and gray-hair hub plan\n")
A(f"Reviewed the {len(rv)} articles in `data/reference/anti_gray_content_calendar.csv` plus {len(out)} other 2026 gray-hair posts, against Search Console, index status, "
  "Phase 2 keyword demand, the compliance rules and the October AI Overview baseline. Read-only: nothing was changed.\n")
A("## Summary\n")
A(f"1. **The structure is good.** {int(rv.live.sum())} of {len(rv)} are live; {int((rv['index'] == 'Submitted and indexed').sum())} are indexed. "
  f"{int(rv.links_to_pillar.fillna(False).sum())} of {int(rv.role.eq('spoke').sum())} supporting articles link to their pillar, every article cites studies, and none has AI-chat leftovers.")
A(f"2. **Traffic is still very small:** {int(rv.clicks_16m.sum())} clicks and {int(rv.impressions_16m.sum()):,} impressions in total since June. Some of that is age; most is demand (point 3).")
A("3. **Most clusters target searches almost nobody makes.** Comparisons, reviews, system and routine, product deep-dives, dating, texture, and the 8 age-and-gender "
  "listicles target queries with little or no measurable volume. The big gray searches sit mostly in clusters where FullyVital has no clear hub: "
  f"what causes gray hair (about {f(g.loc['Gray: causes','volume_dedup'])}/month), gray hair in men ({f(g.loc['Gray: men','head_volume'])} for \"greying men\" alone), "
  f"and B12 and gray hair ({f(g.loc['Gray: nutrients & deficiencies','head_volume'])}).")
A(f"4. **The biggest risk is a repeated survey claim.** {int((cal_claims.survey > 0).sum())} of the {len(cal_claims)} calendar articles "
  f"(and {int((out.survey > 0).sum())} of the other {len(out)}) carry a variant of \"In an April 2025 FullyVital customer survey, 85% of users reported noticing fewer grays "
  "after 90 days\" or \"88% saw new pigment at the roots within 60 days\". Repeated on almost every page, a self-reported customer survey is unlikely to substantiate an efficacy claim, "
  "and \"new pigment at the roots\" reads as a repigmentation claim. This is your call; I haven't edited it.")
A(f"5. **{int(rv.claim_in_title_meta.sum())} titles or meta descriptions use reverse, prevent or treatment wording.** Several are honest question formats (\"Can Gray Hair Be Reversed?\"), "
  "but \"Premature Gray Hair Reversal: Why Early Action Works Best\" and the reversal-study title read as promises next to product widgets.")
A("6. **Some pages duplicate each other:**")
A("   - three pages answer \"what causes gray hair\";")
A("   - two glutathione-for-gray-hair pages (one is the refreshed `/hair-vitamins/glutathione`);")
A("   - two \"which gray-hair ingredients work\" pages;")
A("   - three review pages that split \"does FullyVital work\" searches between them.")
aio_n = int(aeo.has_ai_overview.sum()); 
A(f"7. **AI Overviews already dominate these searches:** {aio_n} of {len(aeo)} priority searches show one, and FullyVital is cited in none. "
  "Arey is the only brand regularly cited.\n")
A("## The survey claim, by page\n")
A(table(pc[(pc.survey > 0) | (pc.product_claim_sentences > 0)].sort_values(["survey", "product_claim_sentences"], ascending=False),
        ["url", "survey", "product_claim_sentences", "example"], ["Page", "Survey statistics", "Product-tied reversal sentences", "Example"]))
A("\n**My recommendation:** before building hubs, ask whoever substantiates your claims whether the survey can be used at all. If yes, keep it on one methods page "
  "(sample size, who was asked, exact question, dates) and refer to it from the product pages only, not repeated on informational posts. If no, remove it everywhere. "
  "Either way, replace \"new pigment at the roots\" with wording that doesn't imply repigmentation. I can make the edits once you decide.\n")
A("## Article by article\n")
rv["claims"] = rv.url.map(pc.set_index("url").survey)
A(table(rv.sort_values(["cluster", "role"]), ["cluster", "role", "url", "primary_query", "query_volume", "clicks_16m", "impressions_90d", "index", "claims"],
        ["Cluster", "Role", "Article", "Target query", "Monthly searches", "Clicks since June", "Impr. 90d", "Index", "Survey statistics"]))
A("\nMonthly searches: exact match or closest variant in the Phase 2 keyword data; blank means no measurable volume.\n")
A("## Pages competing with each other\n")
A(table(ov, ["query", "impressions", "pages"], ["Search", "Impressions", "Pages splitting it"]))
A("\nPlus three pages that answer \"what causes gray hair\": `/what-causes-gray-hair`, `/why-am-i-going-gray-causes-explained` and `/what-causes-hair-to-turn-gray-melanocyte-story`; "
  "two glutathione pages (`/hair-care/glutathione-for-gray-hair` and the refreshed `/hair-vitamins/glutathione`); two ingredient-evidence pages "
  "(`/gray-hair-ingredients-ranked-by-evidence` and `/anti-gray-hair-ingredients-what-actually-works`).\n")
A("## Gray-hair hub plan\n")
A("These build on what you already have. Most hubs are existing articles that get upgraded and become the page that owns the head term; only two need a new page.\n")
plan = [
 ("1", "What causes gray hair", "Gray: causes", "`/what-causes-gray-hair` (upgrade into the hub)",
  "Merge `/why-am-i-going-gray-causes-explained` into it, or retarget that post to early graying (hub 3). Keep `/what-causes-hair-to-turn-gray-melanocyte-story` as the "
  "\"how hair pigment works\" spoke. Link stress, smoking, thyroid, medications, sudden gray and hydrogen peroxide posts as spokes."),
 ("2", "Gray hair in men", "Gray: men", "New hub page",
  "No page targets \"greying men\". Fold the two men's listicles (30s, 40s) into it and link dating, silver fox and confidence posts as spokes."),
 ("3", "Early and premature graying", "Gray: by age & early graying", "`/why-am-i-going-gray-causes-explained` (retargeted) or a new page",
  "Spokes: 20s, 30s, 40s–50s, premature-reversal (retitled), perimenopause. Fold the women's age listicles (20s, 30s, over 40) into one \"by age\" product guide."),
 ("4", "Vitamins, B12 and copper", "Gray: nutrients & deficiencies", "`/vitamins-for-gray-hair`",
  "Add one new spoke for \"vitamin B12 deficiency gray hair\" (about 4,400/month, no dedicated page). Link copper deficiency, nutrient depletion and foods posts, and the refreshed "
  "copper and glutathione articles. Merge `/glutathione-for-gray-hair` into `/hair-vitamins/glutathione`."),
 ("5", "Stress and gray hair", "Gray: causes", "`/can-stress-cause-gray-hair` (keep)",
  "Already a good cluster (6,600/month for the pillar query). Strengthen it and link it to the causes hub."),
 ("6", "Preventing and slowing gray", "Gray: reversal, slowing & stopping", "`/how-to-prevent-gray-hair-naturally`",
  "Keep the reversal-science posts honest (no promises). Merge `/gray-hair-ingredients-ranked-by-evidence` into `/anti-gray-hair-ingredients-what-actually-works`."),
 ("7", "Myths and questions", "Gray: questions, myths & meaning", "`/gray-hair-myths-vs-facts`",
  "Spokes on plucking gray hairs, white vs gray, and texture (link the texture post here)."),
 ("8", "Products and comparisons", "Gray: supplements & products", "`/best-anti-gray-hair-supplements-2026` (blog) + the anti-gray collection page",
  "Keep the Arey and Particle comparisons; consolidate the 8 age-and-gender listicles into 2 (women by age, men); merge the overlapping review pages "
  "(`/do-anti-gray-supplements-work-honest-review`, `/fullyvital-anti-gray-reviews`, `/is-fullyvital-worth-it`) into one."),
]
A("| # | Hub | Cluster (Phase 2) | Monthly searches | Hub page | What to do |"); A("|---|---|---|---|---|---|")
for n, h, c, page, what in plan:
    A(f"| {n} | {h} | {c} | {f(g.loc[c, 'volume_dedup'])} | {page} | {what} |")
A("\n## AEO/GEO standard for every hub\n")
A("- **Answer first:** a 40–60 word direct answer under each question heading, then the evidence.")
A("- **A short evidence table** where useful: cause or ingredient → what the research shows → study.")
A("- **Three studies, each linked once, all in the second half** (CLAUDE.md citation rule).")
A("- **A true \"last updated\" date** and the author byline.")
A("- **One FAQ** built from the \"People also ask\" questions recorded in `data/processed/aeo_tracking.csv`.")
A("- **No product claims inside the informational answer.** The product bridge sits after the evidence, within structure/function wording.")
A("\n## Order of work\n")
A("1. **You decide on the survey claim and the reversal titles.** Every hub links to these pages, so this comes first.")
A("2. **Clean-up batch 2** (approved; the review sheet is next). It now also covers the gray duplicates above.")
A("3. **Hubs 1–4** (causes, men, early graying, nutrients). These carry most of the demand.")
A("4. **Hubs 5–8,** then the hair-growth clusters.")
open("reports/anti-gray-review.md", "w").write("\n".join(L) + "\n")
print(len(L), "lines")
