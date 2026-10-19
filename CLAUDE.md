# FullyVital SEO Pipeline

## Context
- Site: fullyvital.com (Shopify store + blog), DTC supplements.
- Topic scope: gray / grey hair (prevention, reversal, causes) and hair growth / hair loss.
- This project runs in phases. Only run the phase you're asked to run, then stop for review.
  - Phase 1: Audit (see phase1-audit.md)
  - Phase 2: Keyword research & content plan (later)
  - Phase 3+: SERP reverse-engineering, outlines (later)

## Data sources
- Google Search Console via the Composio MCP server.
- DataForSEO v3 via `dataforseo_client.py` ONLY (US, location_code 2840, English). No Semrush, no Ahrefs, no DataForSEO MCP or Composio for DataForSEO. Do not call DataForSEO outside this client — it handles caching, row caps and the session $ cap. If an endpoint path, field path or filter is wrong, fix it in the client.
- Before the first real call, validate request shapes against the free sandbox (set `DATAFORSEO_BASE=https://sandbox.dataforseo.com`), then switch back.
- Check `balance()` at the start and end of every phase; report spend from `summary()` (it logs the real `cost` DataForSEO returns per call).
- DataForSEO bills per request + per row returned. Keep `limit` as low as the analysis needs. Labs keyword results already include volume, KD and intent — no separate difficulty pull needed.
- For topic scope use `ranked_keywords_in_scope()` (chunked OR filters, ≤8 conditions each) instead of unfiltered pulls.
- Backlinks API may not be enabled on the account. If `backlinks_summary()` errors on access, say so and continue without it.
- WebFetch for fullyvital.com pages and competitor sitemaps/blog indexes.

## Product map
- `data/reference/fullyvital_products.csv` (from the user, 2026-10-17): the 10 products with type, key ingredients, persona, primary concern, claims, attributes, format and product URL. Use it to map keywords and articles to products. Use only ingredients listed there when saying what a product contains.
- Two lines: hair growth/loss (Hair Revival Serum, Supplements, 30-Day Kit, 90-Day System, Hair Skin Gut Collagen, Derma roller) and anti-gray (Anti-Gray Serum, Supplements, 30-Day Kit, 90-Day System).

## Hard rules
- **Read-only.** Never call any GSC action that writes or deletes: submit sitemap, delete sitemap, add site, delete site, URL inspection requests are fine to read only. Never use DataForSEO endpoints that create, change or delete anything (e.g. rank-tracking or on-page tasks) in Phase 1.
- **Cache everything.** Save every raw API pull to `data/raw/` as CSV or JSON, named `<source>_<what>_<YYYY-MM-DD>`. Before pulling, check whether a file for that pull already exists and reuse it unless I say to refresh.
- **DataForSEO budget.** Before any batch of calls, estimate the $ cost from DataForSEO's pricing pages (per request + per row) and tell me. The client stops at $25 per session (`DFS_SESSION_BUDGET_USD`); never raise it without my approval. Report actual spend at the end of each phase.
- **Run numbers in code.** Do all aggregation, filtering and scoring in Python over the saved files, not by eyeballing tool output.
- **No fabricated data.** If a metric isn't available, mark it missing. Never estimate volume, position or traffic from memory.
- **Spelling variants.** Always include both "gray" and "grey" in keyword filters.

## Shopify writes (blog clean-up and refreshes only)
- Shopify Admin API via `shopify_client.py` ONLY (credentials in `.env`). The read-only rule above still applies to GSC and DataForSEO.
- Allowed writes: blog articles (create, update, unpublish) and URL redirects. Never touch products, collections, pages, themes, prices or orders.
- Link direction (user rule 2026-10-17): links go from blog pages to product pages, never from product pages to blog pages. Don't propose or add blog links on product or collection pages.
- New articles (approved 2026-10-17): create them **unpublished**, review locally and in the Shopify draft, and publish only after the user approves that article or batch.
- Recent hair-growth content plan: `data/reference/hair_growth_content_calendar.csv` lists 26 hair-growth articles published September–October 2026 (perimenopause, telogen effluvium, postpartum, comparisons, evidence hub). There are many older hair-growth posts besides these. Treat calendar posts like the anti-gray ones: extend, don't duplicate or remove without asking.
- Survey claim (user decision 2026-10-17): the "April 2025 FullyVital customer survey, 85%/88%" statistic in the anti-gray articles stays. Don't remove or rewrite it, and don't re-flag it on those pages. Don't add it to new pages unless the user asks.
- Existing anti-gray content plan: `data/reference/anti_gray_content_calendar.csv` lists the 66 anti-gray articles published June–September 2026 as pillar/spoke clusters. Review it before planning new gray-hair content, and extend those clusters rather than duplicating them.
- Dry run is the default. Real writes only for a batch the user has approved, with `--apply`.
- Back up every article (`data/shopify_backup/`) before the first write of a session. Log every write with before/after to `data/shopify_changes/`.
- Removal = unpublish, not delete. Permanent deletion only after 90 days and with the user's approval.
- Refreshed article content is prepared locally and reviewed by the user before it is published. No medical reviewer is listed until the user names one.

## Compliance (applies to all recommendations)
- Health/YMYL niche. Supplement content must stay within structure/function claims: no claims to diagnose, treat, cure or prevent disease, and nothing promising to "reverse" gray hair without approved substantiation.
- Flag any existing FullyVital page that appears to make a disease or unsupported claim.

## Outputs
- Analysis files: `data/processed/`
- Reports: `reports/` as Markdown.
## Refresh citation style (set by user 2026-10-17; overrides the brief where they differ)
- Each refreshed article cites **3 studies**, the ones that carry the claims. No background or safety-only citations.
- **Each study is linked once**, never repeated in Key Takeaways or FAQ.
- **All study links sit in the second half** of the article. The top half has none.
- A claim whose source was cut is removed or made general. Never keep a specific (dose, figure, caution) without its source.
- Do not flag the closing product box ("Promote Hair Regrowth"); copy it unchanged and don't mention it (user instruction, 2026-10-17).

## Resuming this project (added 2026-10-19)
- **Start here:** if the user says "continue", read `reports/project-status.md` first. It has what's live, what's next, the dated items and the standing decisions. Then check `reports/scheduler-status.md` (what the scheduler ran) and `reports/hub-tracking.md` before proposing work. Update `project-status.md` at the end of every session.
- **Scheduler:** `fv_scheduler.py` runs daily at 9:00 (launch agent `com.fullyvital.scheduler`; tasks in `data/processed/schedule.json`; `python fv_scheduler.py --list`). It runs the read-only trackers itself and sends reminders for decisions. Add new dated tasks there, not in memory.
- **New content:** follow `reports/content-queue.md` and `data/reference/content_queue.csv` at 2 articles a week. Never publish in bulk: the 2023–24 mass publishing (767 posts) came before the 2025 sitewide drops. Build with `hub_build.py` (its guards check 3 PubMed studies, link placement, years, authors and AI artifacts). Create unpublished with `create_new_article.py`, and publish after the user approves. Use `hub_rollout.py` (plan in `data/processed/hub_rollout_plan.json`) for publishing, merges, redirects and spoke links.
- **Writing safely to Shopify:**
  - Back up first, and run a 1-article live test before any batch.
  - Re-read each article from the API immediately before writing it.
  - Never run writes while another Claude session is writing. Check today's `data/shopify_changes/*.jsonl` first.
  - Afterwards, verify against the backup that only the intended text changed.
- **Never edit refresh-test pages** until the readout (about 2026-12-03). That's both the keys and the values in `data/processed/refresh_controls.json`. The deferred test-page work is listed in `project-status.md`.
- **Redirects:** blog URLs only (`/blogs/...`). Redirect only to a live page on the same topic. Off-topic removed posts stay 404, because an unrelated redirect counts as a soft 404. Collapse chains when you find them.
- **Product pages:** the user edits these themselves; there's no product write access. Give them a brief instead (`reports/product-page-brief.md`, `reports/product-faqs.md`). Confirmed facts: the derma roller is 1 mm, used once a week; the 120-day guarantee covers every product.
- **Product names:** use "Hair Revival Serum / Supplements / Kit 30-Day / System 90-Day", "Hair Skin Gut Collagen" and "Hair Revival Serum (3-Pack)". Never the old "Enhance Hair" or "Density" names. The old names remain only on refresh-test pages, until December.
- **Claims and survey numbers:** the user will standardize these around 2026-11-01 (a scheduler reminder). Until then, leave the old widget claims and widget prices alone.
- **Disease, drug and pregnancy pages:** no product claims or product links. Say FullyVital products aren't treatments or substitutes, and keep side effects balanced.
- **Cheaper model:** for big repetitive batches, write a handoff brief for a cheaper model (examples: `reports/product-rename-handoff-brief.md`, `reports/aeo-quickpass-handoff-brief.md`), then spot-check its work against the backup.
