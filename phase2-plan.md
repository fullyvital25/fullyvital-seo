# Phase 2: Keyword research and content plan (gray hair and hair growth)

Follow CLAUDE.md rules: read-only APIs, cache raw pulls, DataForSEO budget, numbers in code, compliance. Use the product map in `data/reference/fullyvital_products.csv`. Stop at the end for review. Phase 2 makes no changes to the site.

## Inputs
- Phase 1 data: Search Console queries and page-query pairs (16 months), FullyVital in-scope keywords (2,020), competitor in-scope keywords (5,613 rows, 8 brands), keyword gap (514, enriched).
- Clean-up state: `data/processed/blog_cleanup_review.csv` (keep, merge, removed, held) and `data/processed/refresh_queue.csv` (being refreshed by another agent).
- Index status of every published article: `data/processed/index_status_all.csv`, from `index_audit.py`.
- Refresh measurement: `reports/refresh-tracking.md` (no results until about December 2026).

## Step 2A: Keyword universe (free, cached data)
1. Combine the in-scope keywords from FullyVital, the competitors and the gap list (with DataForSEO volume, keyword difficulty, intent and top-10 domain strength) with in-scope Search Console queries (impressions, position; volume missing unless DataForSEO has it).
2. Sort every keyword into a topic taxonomy for the two product lines. Also mark intent (informational, commercial, transactional) and compliance risk (disease or drug topics, "reverse gray" wording).
3. Map each cluster to:
   - the product it serves, from the product map;
   - FullyVital's current best page and position;
   - the clean-up decision for that page (refresh queue, held, removed).

## Step 2B: Expansion (paid; estimate first)
For clusters where Phase 1 data is thin, pull keyword ideas from DataForSEO Labs (`keyword_suggestions` / `related_keywords`, with in-scope filters, limit ≤200 per seed), then pull top-10 results for the head term of each priority cluster. Validate any new client method in the sandbox first.

## Step 2C: Content plan (free)
1. **Cluster scorecard:** total volume, FullyVital visibility, competitor visibility, winnability (a lower-authority competitor ranks top 10), commercial value (product fit and intent), compliance risk.
2. **Action per cluster:** maintain, strengthen an existing page, consolidate, build a new hub or article, build or fix a commercial landing page, or avoid (YMYL or drug topics with no product fit).
3. **Fate of the 132 held posts:** fold into a cluster page, rewrite as a cluster article, or remove.
4. **Fate of the 69 brand comparison posts:** keep a few high-value comparisons for commercial "X alternative" and "X vs" demand, merge, or remove.
5. **Prioritised calendar:** quick wins first (existing pages close to ranking); new hub pages for the biggest winnable clusters; landing-page fixes for commercial terms after the product-page claims are fixed.
6. **Decision point:** when the refresh test reads out (about 6–8 weeks after each batch), reweight between refreshing and building new.

## Deliverable
Write `reports/phase2-content-plan.md`:
- summary;
- cluster table;
- page-to-cluster map;
- decisions on held and comparison posts;
- calendar;
- compliance notes;
- DataForSEO spend.

Full data goes in `data/processed/phase2_*.csv`. Then stop.
