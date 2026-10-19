# Phase 1 — SEO Audit: FullyVital (gray hair + hair growth)

Run this phase only. Follow CLAUDE.md rules (read-only, cache raw pulls, DataForSEO budget, numbers in code). Stop at the end and wait for my review. Do NOT produce a content plan yet.

## Inputs
- Domain: fullyvital.com
- GSC property: try `sc-domain:fullyvital.com` first, then `https://fullyvital.com/` / `https://www.fullyvital.com/`. Tell me which one worked.
- Topic filter terms (case-insensitive, match in query/keyword): gray, grey, white hair, hair color loss, premature gray, hair growth, hair loss, thinning hair, hair thinning, regrow, shedding, alopecia, biotin, catalase, minoxidil, hair vitamin, hair supplement.
  - Report the filter separately as "in scope" and keep the full unfiltered data too.
- Product map: [FILL IN — product name → URL → which topic it serves]
- Seed competitors (optional): [FILL IN or leave blank]

## Step 1A — Content inventory (WebFetch)
1. Fetch fullyvital.com/sitemap.xml and its child sitemaps (Shopify uses sitemap_blogs_*, sitemap_pages_*, sitemap_products_*).
2. For every blog article and content page, fetch and record: URL, title tag, meta description, H1, H2 list, word count, published date, updated date, author/byline (yes/no + name), schema types present, internal links to product pages (count + targets), outbound citations to studies (count).
3. Save `data/processed/content_inventory.csv`.

## Step 1B — Google Search Console
Pull with pagination (rowLimit 25000, page through startRow until empty):
1. Last 16 months, dimensions [page, query] → `data/raw/gsc_page_query_<date>.csv`
2. Last 16 months, dimensions [page, date] aggregated to month → `data/raw/gsc_page_monthly_<date>.csv`
3. Last 16 months, dimensions [query] → `data/raw/gsc_query_<date>.csv`
4. Sitemaps list (read only).
Note in the report how much of total impressions is anonymized/missing from query-level data.

## Step 1C — DataForSEO: FullyVital
1. `ranked_keywords("fullyvital.com", limit=1000)` — all keywords (volume, KD, intent, position, URL, estimated traffic). Also `ranked_keywords_in_scope("fullyvital.com")` for the topic view.
2. `domain_rank_overview` + `backlinks_summary` (if Backlinks API is enabled) — rank, referring domains.
3. `relevant_pages` (limit 100) — top pages by organic traffic.

## Step 1D — Competitor identification
1. `competitors_domain("fullyvital.com")`.
2. For 10 in-scope seed keywords (pick the highest-volume in-scope terms from 1B/1C plus core head terms like "gray hair supplement", "hair growth supplement"), pull the top 10 via `serp()`.
3. Classify each domain: **brand competitor** (sells a hair/gray supplement or product), **publisher** (Healthline, WebMD, etc.), **marketplace** (Amazon etc.), **forum/UGC**.
4. Pick 5–8 brand competitors to analyze, plus note the 2–3 publishers that dominate SERPs. Show me the list with reasoning and the estimated $ cost of Step 1E before running it.

## Step 1E — Competitor pulls (DataForSEO)
For each selected competitor: `domain_rank_overview`, `backlinks_summary` (if enabled), `ranked_keywords_in_scope(competitor, limit_per_chunk=500, max_position=20)`, `relevant_pages` limit 50.

## Step 1E2 — Shortlist enrichment
After 1F's keyword gap is computed, take the top ≤100 gap keywords by volume and call `keyword_overview()` for fresh volume, KD, trend and intent. Pull `serp()` for the top 20 of those only, to see who ranks and how strong they are.

## Step 1F — Analysis (Python over saved files)
1. **Page scorecard:** join inventory + GSC + DataForSEO per URL: clicks, impressions, avg position, top 5 queries, primary keyword guess, 12-month click trend, word count, last updated.
2. **Striking distance:** query–page pairs with avg position 4–20 and meaningful impressions, sorted by impressions × (expected CTR gain).
3. **Cannibalization:** queries where 2+ FullyVital URLs each get ≥10% of impressions.
4. **Decay:** pages whose clicks in the last 3 months are ≥30% below the same 3 months last year (or prior 3 months if no YoY).
5. **Zero-performers:** indexed blog posts with <50 impressions in 90 days.
6. **Keyword gap:** in-scope keywords where ≥2 brand competitors rank top 20 and FullyVital is absent or >50. Include volume, KD, intent.
7. **Authority gap:** FullyVital vs competitors on domain rank and referring domains (if Backlinks API is available); mark which shortlisted gap keywords are realistically winnable (KD and the strength of the current top-10 results from `serp()` vs ours).
8. **Compliance flags:** pages with possible disease/unsupported claims.
9. **E-E-A-T check:** bylines, credentials, citations, schema — vs top competitors.

## Step 1G — Deliverable
Write `reports/phase1-audit.md`:
- Executive summary (10 bullets max): where we stand, biggest opportunities, biggest risks.
- Current visibility in scope: clicks, impressions, # keywords top 3 / top 10 / top 20, trend.
- Tables for each analysis in 1F (top 20 rows each; full data in CSVs).
- Competitor landscape table.
- Recommended Phase 2 focus: which clusters to attack, what to refresh vs consolidate vs build — as hypotheses, not a plan.
- Data gaps and caveats; DataForSEO $ spent (from `summary()`).

Then stop.