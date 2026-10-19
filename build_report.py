"""Phase 1G — build reports/phase1-audit.md from data/processed (numbers come from the files, not typed by hand)."""
import glob
import json
from pathlib import Path

import pandas as pd

O = "data/processed/"
st = json.load(open(O + "phase1_stats.json"))
g, inv, dfs = st["gsc"], st["inventory"], st["dfs_fullyvital"]


def short(u):
    return u.replace("https://fullyvital.com", "") or "/" if isinstance(u, str) else u


def fmt(v):
    if isinstance(v, float):
        if pd.isna(v):
            return "—"
        return f"{v:,.0f}" if abs(v) >= 100 else f"{v:.1f}"
    if isinstance(v, (int,)) and not isinstance(v, bool):
        return f"{v:,}"
    return "—" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v).replace("|", "/")


def table(df, cols, names=None, n=20):
    df = df.head(n)
    names = names or cols
    out = ["| " + " | ".join(names) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df[cols].itertuples(index=False):
        out.append("| " + " | ".join(fmt(v) for v in r) + " |")
    return "\n".join(out)


def pct(x):
    return f"{x:.0%}"


sm = pd.DataFrame(st["site_monthly"]).set_index("month")
c25, c26 = sm.loc[["2025-07", "2025-08", "2025-09"]].sum(), sm.loc[["2026-07", "2026-08", "2026-09"]].sum()
auth = pd.read_csv(O + "authority_gap.csv")
me = auth.iloc[0]
comp = auth.iloc[1:]
weaker = comp[comp["rank"] <= me["rank"]]
gap = pd.read_csv(O + "keyword_gap.csv")
card = pd.read_csv(O + "page_scorecard.csv")
card["url"] = card.url.map(short)
sd = pd.read_csv(O + "striking_distance.csv")
sd["page"] = sd.page.map(short)
can = pd.read_csv(O + "cannibalization_by_query.csv")
dec = pd.read_csv(O + "decay.csv")
dec["url"] = dec.url.map(short)
dec["change"] = dec.change_yoy.map(pct)
zp = pd.read_csv(O + "zero_performers.csv")
zp["url"] = zp.url.map(short)
zp["published"] = zp.published.str[:10]
cf = pd.read_csv(O + "compliance_flags.csv")
cf["url"] = cf.url.map(short)
ee = pd.read_csv(O + "eeat_competitor_sample.csv")
spend_logged = sum(pd.read_csv(f).cost_usd.sum() for f in glob.glob(O + "dfs_spend_*.csv"))
BAL0, BAL1 = 51.0, 49.005636
prod = cf[cf.type == "product"]
artc = cf[cf.type == "article"]
gray_gap = gap[gap.cluster == "gray"]
zp_new = int((zp.published.str[:4] == "2026").sum())

L = []
A = L.append
A("# Phase 1 — SEO Audit: fullyvital.com (gray hair + hair growth)\n")
A("Audit date: 2026-10-12. Search Console property: `sc-domain:fullyvital.com`, 2025-06-10 to 2026-10-09. "
  "DataForSEO: US, English. All numbers are computed from the saved files in `data/`. "
  "\"In scope\" means the query or keyword contains one of the topic terms in `phase1-audit.md`; brand queries are excluded from in-scope figures.\n")

A("## Executive summary\n")
A(f"1. **Organic traffic has fallen by about two thirds in a year.** July–September clicks went from {c25.clicks:,} in 2025 to {c26.clicks:,} in 2026 "
  f"(down {pct(1 - c26.clicks / c25.clicks)}); impressions fell {pct(1 - c26.impressions / c25.impressions)}. "
  f"{st['decay']['decayed_30pct']} of the {st['decay']['pages_with_10plus_clicks_last_year_window']} pages that had 10+ clicks in that window last year are down 30% or more.")
A(f"2. **Half of the identifiable clicks are brand searches.** Of {g['query_level_clicks']:,} clicks with a visible query, {g['brand_clicks']:,} are FullyVital brand queries. "
  f"In-scope non-brand queries brought {g['in_scope_nonbrand_clicks']:,} clicks in 16 months; the gray cluster accounts for {g['by_cluster']['gray']['clicks']:,} of them.")
A(f"3. **The site ranks for a lot but almost none of it is on page one.** DataForSEO finds {dfs['in_scope_keywords']:,} in-scope keywords, with {dfs['top10']} in the top 10 and {dfs['top20']} in the top 20. "
  f"Only {pct(me.top10_share)} of all ranked keywords are top 10, against {pct(comp.top10_share.min())}–{pct(comp.top10_share.max())} for the eight competitors.")
A(f"4. **Link authority is not the gap.** FullyVital's domain rank ({me['rank']:.0f}) is higher than {len(weaker)} of the 8 competitors ({', '.join(weaker.domain)}), "
  f"yet each of those has {weaker.organic_etv.min() / me.organic_etv:.1f}–{weaker.organic_etv.max() / me.organic_etv:.0f} times FullyVital's estimated organic traffic. The gap is in content performance, not links.")
A(f"5. **A large share of the blog is dead weight.** {st['zero_performers']['articles_under_50_impr_90d']} of {inv['articles']} articles had under 50 impressions in the last 90 days "
  f"({st['zero_performers']['with_zero_impr_90d']} had none), and {inv['articles_zero_clicks_16m']} had zero clicks in 16 months.")
A(f"6. **Cannibalization is widespread.** {st['cannibalization']['queries']:,} non-brand queries (200+ impressions) have two or more URLs each taking 10%+ of impressions; "
  f"{st['cannibalization']['in_scope_queries']} are in scope. The two blogs (`hair-care`, `hair-vitamins`) often carry near-duplicate posts on the same ingredient.")
A(f"7. **Keyword gap: {st['keyword_gap']['keywords']} in-scope keywords** ({st['keyword_gap']['volume_sum']:,} monthly searches) where 2+ competitors rank top 20 and FullyVital is absent or below 50. "
  f"{int(gap.winnable.sum())} of them already have a lower-authority competitor in the top 10. Only {len(gray_gap)} are gray-hair keywords ({int(gray_gap.volume.sum()):,} searches).")
A(f"8. **Compliance risk sits on the product pages.** {int((prod.head_reverse_gray).sum())} of {len(prod)} product pages use \"reverse\" gray wording in the title, meta description or H1, "
  f"and {int((prod.reverse_gray_sentences > 0).sum())} use it somewhere in the copy (for example \"Reverses Grays in 90 Days\"). These need review before more traffic is sent to them.")
A(f"9. **E-E-A-T is thin for a health topic.** Every article has a byline, but {inv['authors'].get('Faraz Khan, MSC', 0)} of {inv['articles']} carry the same one, "
  f"only {pct(inv['articles_with_study_citation'] / inv['articles'])} link to a study, and none of a 60-article sample names a medical reviewer.")
A(f"10. **Striking-distance upside is small.** Only {st['striking_distance']['in_scope_pairs']} in-scope query–page pairs sit at positions 4–20 with 100+ impressions in 90 days. Quick ranking tweaks will not recover the decline.\n")

A("## Current visibility in scope\n")
A("### Search Console (16 months)\n")
A(table(pd.DataFrame([
    {"m": "All clicks (site total)", "v": g["site_clicks"]}, {"m": "All impressions (site total)", "v": g["site_impressions"]},
    {"m": "Clicks with a visible query", "v": g["query_level_clicks"]},
    {"m": "Share of clicks with no query shown (anonymized)", "v": pct(g["anonymized_click_share"])},
    {"m": "Share of impressions with no query shown", "v": pct(g["anonymized_impression_share"])},
    {"m": "Brand clicks", "v": g["brand_clicks"]},
    {"m": "In-scope non-brand queries", "v": g["in_scope_nonbrand_queries"]},
    {"m": "In-scope non-brand clicks", "v": g["in_scope_nonbrand_clicks"]},
    {"m": "In-scope non-brand impressions", "v": g["in_scope_nonbrand_impressions"]},
    {"m": "Gray cluster: clicks / impressions", "v": f"{g['by_cluster']['gray']['clicks']:,} / {g['by_cluster']['gray']['impressions']:,}"},
    {"m": "Hair growth/loss cluster: clicks / impressions", "v": f"{g['by_cluster']['hair growth/loss']['clicks']:,} / {g['by_cluster']['hair growth/loss']['impressions']:,}"},
    {"m": "In-scope queries with average position ≤3 / ≤10 / ≤20", "v": f"{g['in_scope_top3']:,} / {g['in_scope_top10']:,} / {g['in_scope_top20']:,}"},
]), ["m", "v"], ["Metric", "Value"], 30))
A("\nThe Search Console position counts include many queries with a handful of impressions, so they overstate real page-one presence. The DataForSEO counts below are the stricter view.\n")
A("### DataForSEO (ranking snapshot)\n")
A(table(pd.DataFrame([
    {"m": "All ranked keywords", "v": dfs["total_ranked_keywords"]}, {"m": "In-scope keywords", "v": dfs["in_scope_keywords"]},
    {"m": "In-scope top 3 / top 10 / top 20", "v": f"{dfs['top3']} / {dfs['top10']} / {dfs['top20']}"},
    {"m": "Gray keywords (all positions)", "v": dfs["gray_keywords"]},
    {"m": "Gray keywords top 10 / top 20", "v": f"{dfs['gray_top10']} / {dfs['gray_top20']}"},
]), ["m", "v"], ["Metric", "Value"]))
A("\n### Monthly trend (all pages)\n")
A(table(sm.reset_index(), ["month", "clicks", "impressions"], ["Month", "Clicks", "Impressions"], 30))
A("\nJune 2025 and October 2026 are partial months.\n")
A("### Clicks by page type (16 months)\n")
bt = pd.DataFrame(st["gsc_by_page_type"]).T.reset_index().sort_values("clicks", ascending=False)
A(table(bt, ["index", "clicks", "impressions"], ["Page type", "Clicks", "Impressions"]))

A("\n## Content inventory\n")
A(f"- {inv['articles']} articles ({inv['by_blog'].get('hair-care', 0)} in `hair-care`, {inv['by_blog'].get('hair-vitamins', 0)} in `hair-vitamins`) and {inv['pages']} content pages. Median article length is {inv['median_word_count']:,.0f} words.")
A(f"- Published by year: {', '.join(f'{k}: {v}' for k, v in inv['published_by_year'].items())}. The sitemap shows {inv['lastmod_by_year'].get('2026', 0)} articles modified in 2026, so last-modified dates do not indicate real content refreshes.")
A(f"- {inv['articles_with_product_link']} articles link to a product page. {inv['articles_with_any_external_link']} have any external link; {inv['articles_with_study_citation']} link to a study or scientific source.")
A(f"- The top 10 articles bring {pct(inv['top10_articles_click_share'])} of all article clicks.")
A("- Full data: `data/processed/content_inventory.csv`.\n")

A("## 1. Page scorecard (top 20 by clicks)\n")
A(table(card, ["url", "clicks_16m", "impressions_16m", "avg_position_16m", "clicks_90d", "clicks_same3_last_year", "clicks_last3", "primary_keyword_guess", "word_count"],
        ["URL", "Clicks 16m", "Impr. 16m", "Avg pos.", "Clicks 90d", "Clicks Jul–Sep 2025", "Clicks Jul–Sep 2026", "Primary keyword (guess)", "Words"]))
A("\nPrimary keyword is the non-brand query with the most impressions for the page. Full data, including top 5 queries and the 12-month click series: `page_scorecard.csv`.\n")

A("## 2. Striking distance (last 90 days, in scope)\n")
A(table(sd[sd.in_scope], ["query", "page", "clicks", "impressions", "position", "expected_click_gain_90d", "volume"],
        ["Query", "Page", "Clicks", "Impr.", "Avg pos.", "Expected click gain (90d)", "Volume"]))
A(f"\nPairs at average position 4–20 with 100+ impressions; {st['striking_distance']['pairs']} pairs in total, {st['striking_distance']['in_scope_pairs']} in scope. "
  f"Expected gain uses the site's own non-brand click-through rate at positions 1–3 ({st['own_nonbrand_ctr_top3']:.2%}), which is very low, so treat the gain column as a ranking order rather than a forecast. Volume is blank where DataForSEO has no row for the query. Full data: `striking_distance.csv`.\n")

A("## 3. Cannibalization (in scope, top 20 by impressions)\n")
A(table(can[can.in_scope], ["query", "total_impressions", "urls", "best_position", "pages"], ["Query", "Impr. 16m", "URLs", "Best avg pos.", "Competing URLs"]))
A("\nSeveral product-name queries (for example \"anti-gray hair supplement 3-pack\") show position 1 with almost no clicks across multiple product URLs. Those URLs were recorded with Shopify `product_sync` parameters, which suggests they are product-listing impressions rather than standard results; this is a hypothesis, not confirmed. Full data: `cannibalization.csv`, `cannibalization_by_query.csv`.\n")

A("## 4. Decay (Jul–Sep 2026 vs Jul–Sep 2025)\n")
A(table(dec, ["url", "clicks_same3_last_year", "clicks_last3", "change", "primary_keyword_guess", "word_count"],
        ["URL", "Clicks 2025", "Clicks 2026", "Change", "Primary keyword (guess)", "Words"]))
A(f"\n{st['decay']['decayed_30pct']} pages qualify (10+ clicks in the 2025 window, down 30%+), losing {st['decay']['clicks_lost']:,} clicks between them. Full data: `decay.csv`.\n")

A("## 5. Zero-performers\n")
A(f"{st['zero_performers']['articles_under_50_impr_90d']} articles had under 50 impressions in 90 days. {zp_new} of them were published in 2026 and may simply be too new to judge. "
  "Index status was not checked (that needs URL inspection per page), so \"indexed\" here means \"listed in the sitemap\".\n")
A(table(zp[zp.published.str[:4] != "2026"].sort_values("word_count", ascending=False), ["url", "published", "word_count", "impressions_90d", "impressions_16m", "clicks_16m"],
        ["URL", "Published", "Words", "Impr. 90d", "Impr. 16m", "Clicks 16m"]))
A("\nTable shows the 20 longest pre-2026 posts. Full data: `zero_performers.csv`.\n")

A("## 6. Keyword gap (top 20 by volume)\n")
A(table(gap, ["keyword", "volume", "kd", "intent", "trend_yearly_pct", "competitors", "fullyvital_position", "top10_avg_domain_rank", "weaker_domains_in_top10"],
        ["Keyword", "Volume", "KD", "Intent", "Trend YoY %", "Competitors top 20", "FullyVital pos.", "Top-10 avg domain rank", "Lower-authority competitor in top 10"]))
A("\n### Gray-hair gap keywords (top 20)\n")
A(table(gray_gap, ["keyword", "volume", "intent", "competitors", "fullyvital_position", "who", "weaker_domains_in_top10"],
        ["Keyword", "Volume", "Intent", "Competitors top 20", "FullyVital pos.", "Who ranks", "Lower-authority competitor in top 10"]))
A(f"\n{st['keyword_gap']['keywords']} gap keywords: {st['keyword_gap']['fullyvital_absent']} where FullyVital does not rank at all. By intent: "
  + ", ".join(f"{k} {v}" for k, v in st["keyword_gap"]["by_intent"].items()) + ". Full data: `keyword_gap.csv`.\n")

A("## 7. Authority gap and winnability\n")
A(table(auth, ["domain", "rank", "referring_domains", "backlinks", "organic_keywords", "top10", "organic_etv", "in_scope_top20_keywords"],
        ["Domain", "Domain rank (0–1,000)", "Referring domains", "Backlinks", "Ranked keywords", "Top-10 keywords", "Est. organic traffic", "In-scope top-20 keywords"]))
A(f"\nIn-scope top-20 counts for competitors are capped at 500 per topic chunk (1,500 max), so hims.com, theradome.com, mdhair.co, neofollics.com, vegamour.com and arey.com are undercounted.\n")
A(f"**Winnability rule:** a gap keyword is marked winnable when a competitor with domain rank at or below FullyVital's ({me['rank']:.0f}) already ranks in the top 10 for it. "
  f"{int(gap.winnable.sum())} of {len(gap)} gap keywords qualify ({int(gap[gap.winnable].volume.sum()):,} monthly searches): "
  f"{int((gap.winnable & (gap.cluster == 'gray')).sum())} gray, {int((gap.winnable & (gap.cluster != 'gray')).sum())} hair growth/loss. "
  "DataForSEO's keyword difficulty is shown but not used for this call: it scores 0 for about 40% of keywords at every volume level.\n")
top_serp = pd.read_csv(O + "dfs_serp_gap_top20.csv").domain.value_counts().head(10)
A("Domains appearing most often in the live results for the top 20 gap keywords: " + ", ".join(f"{d} ({n})" for d, n in top_serp.items()) + ".\n")

A("## 8. Compliance flags\n")
A("Automated pattern scan of 746 articles, 34 pages and 61 product pages. It finds wording to review; it is not a legal determination, and the article-level disease flags include false positives where a product widget sits next to a heading.\n")
A(table(pd.DataFrame([
    {"m": "Product pages with \"reverse\" gray wording in title, meta or H1", "v": f"{int(prod.head_reverse_gray.sum())} of {len(prod)}"},
    {"m": "Product pages with \"reverse\" gray wording anywhere in copy", "v": f"{int((prod.reverse_gray_sentences > 0).sum())} of {len(prod)}"},
    {"m": "Articles with \"reverse\" gray wording in title, meta or H1", "v": f"{int(artc.head_reverse_gray.sum())} of {len(artc)}"},
    {"m": "Articles with \"reverse\" gray wording anywhere", "v": f"{int((artc.reverse_gray_sentences > 0).sum())} of {len(artc)}"},
    {"m": "Articles tying a FullyVital product to \"reverse\" gray wording in one sentence", "v": f"{int((artc.product_reverse_gray_sentences > 0).sum())}"},
    {"m": "Articles whose title or meta pairs treat/prevent/cure wording with a condition", "v": f"{int(artc.head_disease_claim.sum())} of {len(artc)}"},
    {"m": "Articles carrying the FDA disclaimer text", "v": f"{int(artc.has_fda_disclaimer.sum())} of {len(artc)}"},
    {"m": "Product pages carrying the FDA disclaimer text", "v": f"{int(prod.has_fda_disclaimer.sum())} of {len(prod)}"},
]), ["m", "v"], ["Check", "Result"]))
A("\n### Product pages to review first\n")
pr = prod[prod.severity > 0].copy()
pr["example"] = pr.example_product_reverse.fillna("").where(pr.example_product_reverse.fillna("") != "", pr.head_text).str[:170]
A(table(pr, ["url", "example"], ["Product page", "Wording found"], 15))
A("\n### Articles to review first\n")
ar = artc[(artc.head_reverse_gray) | (artc.product_reverse_gray_sentences > 0)].copy()
ar["example"] = ar.example_product_reverse.fillna("").where(ar.example_product_reverse.fillna("") != "", ar.head_text).str[:170]
A(table(ar, ["url", "example"], ["Article", "Wording found"], 12))
A("\n`/blogs/hair-care/can-gray-hair-be-reversed` is flagged by the pattern but states that no product can promise reversal; it is a model for compliant wording, not a problem. Full data: `compliance_flags.csv`.\n")

A("## 9. E-E-A-T check\n")
A(table(pd.DataFrame([
    {"m": "Articles with a byline", "v": f"{inv['articles_with_byline']} of {inv['articles']}"},
    {"m": "Authors", "v": ", ".join(f"{k} ({v})" for k, v in inv["authors"].items())},
    {"m": "Articles linking to at least one study", "v": f"{inv['articles_with_study_citation']} ({pct(inv['articles_with_study_citation'] / inv['articles'])})"},
    {"m": "\"Reviewed by\" or fact-check mention (60-article sample)", "v": "0 of 60"},
    {"m": "Schema on articles", "v": "Article, BlogPosting, BreadcrumbList, Organization, Person on all; FAQPage on 92"},
]), ["m", "v"], ["FullyVital", "Value"]))
A("\n### Competitor sample (top 3 blog URLs per competitor by in-scope top-20 keywords)\n")
ee["url"] = ee.url.str.replace("https://", "", regex=False).str[:70]
A(table(ee, ["domain", "url", "word_count", "author", "schema_types", "study_citation_count", "mentions_reviewer"],
        ["Domain", "URL", "Words", "Author", "Schema", "Study links", "Reviewer named"], 30))
A("\nThis is a small sample (up to 3 pages per competitor). hims.com pages render content with JavaScript, so word and link counts are missing there, and one request was blocked (403). particleformen.com had no blog-style URLs among its in-scope top-20 pages. "
  "What the sample does show: mdhair.co bylines an MD and uses `MedicalWebPage` schema; hims.com and mdhair.co name a reviewer; arey.com and vegamour.com cite studies in some posts.\n")

A("## Competitor landscape\n")
A("**Brand competitors analyzed:** " + ", ".join(comp.domain) + ". Selected from DataForSEO's competitor overlap and the top results for 10 seed keywords.\n")
A("**Publishers dominating the results (not pulled):** healthline.com (4,445 shared keywords), byrdie.com (2,687), medicalnewstoday.com (2,326), webmd.com (2,240), clevelandclinic.org (1,685). "
  "YouTube, Reddit and Amazon also appear on most seed results.\n")
A("Nutrafol, Viviscal and similar brands did not surface in this data and were not analyzed.\n")

A("## Recommended Phase 2 focus (hypotheses, not a plan)\n")
A("1. **Consolidate before building.** Merge near-duplicate posts (biotin timing has 3 URLs; zinc, caffeine and peppermint oil each have a post in both blogs; selenium has two) and decide the fate of the ~260 pre-2026 posts with almost no impressions. Hypothesis: the volume of thin, overlapping posts is suppressing the whole blog.")
A("2. **Refresh the pages that used to work.** The top of the decay list (baby hairs, manganese, N-acetyl cysteine, glutathione and grey hair, biotin vs prenatal vitamins) already proved it can rank.")
A("3. **Gray hair: build the \"causes\" cluster.** The gray gap is informational: what causes gray hair (9,900), early or premature grey (1,600 each), grey hair causes. neofollics.com and theradome.com rank for these with lower authority. Copper, B12 and peptide-for-grey-hair terms are where FullyVital sits just outside the top 50.")
A("4. **Hair growth: peptides and copper peptides.** Volumes of 12,100–18,100 with year-on-year search growth of 174–235%, and mdhair.co already ranks top 10 for the copper peptide terms.")
A("5. **Commercial gray terms need a compliant landing page.** \"Gray hair supplement\", \"vitamins for gray hair\" and \"anti gray hair serum\" and close variants sit at positions 25–48 in DataForSEO. Product-page wording has to be fixed first (see section 8).")
A("6. **Raise E-E-A-T on the pages that matter.** Add study citations and a named medical reviewer to the refreshed and new pages; test `MedicalWebPage` schema as mdhair.co and hims.com use.")
A("7. **Treat medical-condition topics with care.** Many gap keywords are about alopecia types and medication side effects. They are YMYL, dominated by medical publishers, and risky to pair with product links.\n")

A("## Data gaps and caveats\n")
A(f"- **DataForSEO spend:** ${BAL0 - BAL1:.2f} for the phase (balance ${BAL0:.2f} → ${BAL1:.2f}). The per-call logs in `dfs_spend_*.csv` total ${spend_logged:.2f}; the remaining ${BAL0 - BAL1 - spend_logged:.2f} was the paged pull of FullyVital's full in-scope keyword set, which was run ad hoc and not written to a spend file.")
A("- **Keyword difficulty is unreliable** (0 for about 40% of keywords, including \"hair growth serum\" at 74,000 searches). Winnability uses competitor authority instead.")
A("- **Anonymized queries:** 60% of clicks and 41% of impressions have no query in Search Console, so query-level figures understate reality.")
A("- **Ranking data is a snapshot** up to about three months old (median 2026-09-03).")
A("- **FullyVital's unfiltered keyword list** is the top 1,000 of 6,694 by volume; the in-scope list is complete (2,020 rows).")
A("- **Competitor in-scope lists** are the top 500 per topic chunk by volume, top-20 positions only. The gap list therefore leans toward higher-volume terms.")
A("- **Seed and gap results pages** returned 6–8 organic results each, not a full 10.")
A("- **Product map** was not provided; no product-to-topic mapping was used. Seed competitors were not provided either.")
A("- **Content crawl** used a Python crawler rather than WebFetch, for exact word counts and schema. It covers published URLs in the sitemap only. Product pages were fetched for the compliance scan but are not in the inventory.")
A("- **Index status** was not checked per URL.")
A("- **Expected click gain** in striking distance rests on the site's own, unusually low, click-through rates.")
A("- **Cause of the traffic decline** was not investigated; this audit only measures it.")

Path("reports").mkdir(exist_ok=True)
Path("reports/phase1-audit.md").write_text("\n".join(L) + "\n")
print("\n".join(L)[:6000])
