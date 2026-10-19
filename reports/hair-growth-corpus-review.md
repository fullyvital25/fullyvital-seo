# Hair-growth library review and hub rollout

Date: 18 October 2026. Reviewed all 355 live hair-growth articles (not only the 26 calendar posts) against Search Console (16 months to 9 October) and the Phase 2 clusters. Files: `data/processed/growth_corpus_review.csv` (one row per article), `data/processed/growth_hub_query_overlap.csv` (which pages already get impressions for each hub's searches). Script: `growth_corpus_review.py`.

## What the library looks like

| Topic | Live articles | Clicks (16 mo) | Impressions (16 mo) | Hub |
|---|---|---|---|---|
| Hair loss, thinning, hairline, treatments | 59 | 335 | 326,044 | How to stop hair loss (new) |
| Vitamins, minerals, supplements | 35 | 246 | 187,171 | Best vitamins for hair growth (rebuilt) |
| Oils | 29 | 254 | 202,195 | Rosemary oil for hair growth (rebuilt) |
| Protein and food | 15 | 172 | 46,838 | Protein-rich foods for hair growth (new) |
| Everything else (ingredients, hair care, styling, biology) | 217 | 1,788 | 1,298,613 | none yet, see "What's next" |

Findings that shaped the hubs:

1. **No page owned any of the four head terms.** The best existing page for each ranked between positions 35 and 90. The traffic sits on narrow spokes: batana oil (84,000 impressions), zinc (25,700), biotin vs prenatal (22,700), protein overload (23,000).
2. **There were duplicates of the hubs.** The library had older posts on the same question, most with little or no traffic. Approved ones are merged into the hubs; the rest are listed below for your decision.
3. **Spokes didn't link up.** Almost no older article linked to a central page for its topic. Every eligible spoke now gets one sentence linking to its hub on the day the hub goes live: 118 pages across the four hubs.
4. **Hub links went to weak pages in places.** Changed: the microneedling link now goes to the refreshed microneedling page, not the 0-impression `/micro-needling`. The vitamins hub links zinc, silica, vitamin A, selenium and the biotin-timing page, not the old "Biotin: the Miracle Vitamin" post. The rosemary hub adds black seed oil (13,500 impressions).
5. **Refresh-test pages are untouched.** The 9 treated and 20 control pages get no edits until the readout in early December.

## Rollout (one hub a day)

| Date | Hub | Merged into it | Spokes linked up |
|---|---|---|---|
| 18 Oct (done) | `/how-to-stop-hair-loss` | `/how-to-make-hair-grow-back-faster`, `/regrow-hair` (was 404), `/types-of-hair-loss`. Also `/micro-needling` → refreshed microneedling page | 48 |
| 19 Oct | `/best-hair-growth-vitamins` (rebuild) | `/hair-loss-vitamins` | 28 |
| 20 Oct | `/rosemary-oil-for-hair-growth` (rebuild) | none | 30 (2 already linked) |
| 21 Oct | `/foods-for-hair-growth` | `/5-best-foods-hair-growth` (was 404) | 12 |

- **Schedule:** `hub_rollout.py --apply` runs daily at 9:00 from the launch agent `com.fullyvital.hubrollout`. If the Mac is asleep it runs on wake; if it's off, the next run catches up.
- **Links between hubs:** links to a hub that isn't live yet are left out and added on the day it goes live, so nothing 404s.
- **Log:** `data/processed/hub_rollout_log.jsonl`.

## For you to decide: more merges

Each of these duplicates a hub or a stronger page. They're in the plan with `"approved": false` and will run on the hub's day once you say yes.

| Post | Into | Why |
|---|---|---|
| `/can-hair-loss-be-reversed` | How to stop hair loss | 5,858 impressions on "can I reverse hair loss", which the hub's FAQ answers; in the rewrite queue |
| `/which-vitamin-deficiency-causes-hair-loss` | Best vitamins | 0 impressions; the hub answers "what vitamin am I lacking" |
| `/hair-vitamins/vitamin-d` | `/vitamin-d3` | 0 impressions; title "Can Vitamin D Cure Baldness?" is a disease claim |
| `/hair-care/iron` | `/iron-deficiency-hair-loss` | 467 impressions vs 13,478 on the refreshed iron page |
| `/vitamin-a-gateway-to-vibrant-hair-growth` | `/hair-care/vitamin-a` | 163 impressions; duplicate of the refreshed page |
| `/hair-vitamins/protein` | Foods hub | 0 impressions in 16 months |

After the refresh test: `/folate` → `/folic-acid` (control page), `/telogen-effluvium` → the new pillar, and `/hair-vitamins/saw-palmetto` and `/does-wearing-a-hat-cause-hair-loss` (already queued).

## What's next, by demand

1. **Biotin hub** (cluster about 154,850 searches a month). There are 5 posts. The natural hub, `/how-much-biotin-for-hair-growth`, is a control page, so build after the test or as a new page.
2. **Hairline, crown and bald spots.** This is FullyVital's strongest existing hair-loss traffic: 194,000 impressions and 328 clicks, led by baby hairs, receding hairline on one side, crown balding and widow's peak. It needs a hub tying these together; two of the pages are test pages.
3. **Hair growth cycle and biology** (132,000 impressions: clogged follicles, anagen, catagen, club hair, hair cycle). This could be a "how hair grows" hub; `/hair-cycle` is in the rewrite queue.
4. **Ingredient pages** (most of the 217 "other" articles, many already refreshed). These should link to the evidence hub `/is-fullyvital-hair-growth-proven` and to the relevant product, rather than getting a new hub.
5. **Hair care and styling posts** (flyaway hair, bleaching wet hair, perms and similar) bring impressions but sit outside the product line. Leave them as they are; no hub.

## Other checks

- **Product links:** every product and collection URL linked from live posts resolves (some via 301). One broken link on `/burdock-root` (`/products/enhance-hair-serum-`) was fixed.
- **Lavender claim:** `/lavender-oil-for-hair` still says aromatherapy "could effectively treat alopecia areata", a disease claim on an older page. It's flagged for the next compliance pass.

## Update, 18 October (later): everything published

At your request all hubs went live on 18 October, and the daily schedule was removed. All six extra merges were applied, along with `/can-hair-loss-be-reversed` into the stop-hair-loss hub. Verified: 13 of 13 merges are in place, and no live page links to a merged post except the telogen-effluvium control page, whose link still works through the 301.

Three more hubs were published the same day, each built around URLs that already had search history:

| Hub | URL | Redirects added for removed pages | Spokes linked up |
|---|---|---|---|
| Biotin for hair growth | `/is-biotin-good-for-hair` (rebuilt; 5 old biotin URLs already pointed here) | `/does-biotin-work-hair-thinning` | 8 |
| Receding hairline | `/receding-hairlines` (republished and rebuilt) | `/female-receding-hairline` (26,174 impressions, backlinks), `/types-of-hairlines` (24,165), `/traction-alopecia` (9,679), `/normal-hairline`, `/uneven-hairline`, `/hairlines` | 17 |
| Hair growth cycle | `/hair-cycle` (rebuilt) | `/how-long-does-it-take-for-hair-to-grow` (25,376), `/how-many-hairs-on-a-human-head` (26,632), `/how-long-does-it-take-for-hair-to-grow-back` (13,145), `/hair-growth-cycle`, `/telogen-phase` | 13 |

Seven removed pages were also redirected to a live page on the same topic. The biggest is `/peppermint-oil-for-hair` (28,228 impressions) → `/hair-vitamins/peppermint-oil`. Full list in `data/shopify_changes/2026-10-18.jsonl`.

All seven hubs cite 3 PubMed studies and include FAQ schema; 156 older posts now link up to a hub.

**Still returning 404 (hair-growth):** the alopecia-areata and scarring-alopecia pages (about 40,000 impressions combined). They need a careful conditions hub first. `/copper-peptides-hair-thinning` would redirect to `/hair-vitamins/copper`, a refresh-test page, so it waits for the test readout. The full list is in `data/processed/unredirected_404s_2026-10-18.csv`.

## Update, 18 October: conditions hub and ingredient links

**Conditions hub: `/types-of-alopecia` (new).**
- Covers pattern hair loss, telogen effluvium, alopecia areata, traction alopecia, trichotillomania, scarring alopecias, and hair loss linked to thyroid, PCOS, iron and scalp conditions.
- 3 studies (2024 American Family Physician hair loss review, 2018 scarring alopecia review, 2022 review of lichen planopilaris and frontal fibrosing alopecia).
- No product claims or product links; a short note says FullyVital products aren't treatments for these conditions.
- Removed pages now 301 here: scarring alopecia, cicatricial alopecia, triangular alopecia, lichen planopilaris, frontal fibrosing alopecia, discoid lupus, systemic lupus, alopecia mucinosa, trichotillomania. `/alopecia` was repointed here from `/androgenetic-alopecia`.
- 12 related posts link up to it.

**Alopecia areata spoke: `/alopecia-areata` (republished and rebuilt).**
- Sources: Nature Reviews Disease Primers 2017, a 2015 epidemiology review and the 2022 NEJM baricitinib phase 3 trials.
- No product links.
- `/alopecia-areata-treatments` and `/how-to-stop-alopecia-areata-from-spreading` now 301 here. `/alopecia-universalis` was repointed here from the stop-hair-loss hub.

**Ingredient pages → evidence hub and product.**
- 36 live ingredient pages now carry one sentence naming the FullyVital product(s) that contain the ingredient, based on the product sheet, and linking to `/is-fullyvital-hair-growth-proven`.
- Excluded: pages whose ingredient isn't in a product, a different form of it (pyrithione zinc, tocotrienols), refresh-test pages, and pages queued to merge.
- The evidence hub's three tables now link 12 graded ingredients to their pages. Log: `data/processed/ingredient_links_applied_2026-10-18.json`.

## Update, 18 October: serums and shampoo hubs, and tracking

**Serum hub: `/best-hair-growth-serums` (rebuilt).**
- Targets "good hair growth serum" (9,900 a month, KD 1), "best hair growth serum" and "does hair growth serum work".
- 3 randomized trials, one per ingredient: rosemary oil vs. minoxidil 2%, caffeine 0.2% vs. minoxidil 5%, and topical adenosine. All three are in Hair Revival Serum. The page says the trials tested single ingredients, not the combined formula.
- Merged into it (301): `/the-best-hair-growth-serum`, `/hair-growth-serum`, `/best-hair-serum`, `/scalp-serum`. `/how-the-fullyvital-hair-serum-works…` (10 impressions) went to `/how-to-use-fully-vital-hair-serums`.
- 13 related posts link up to it.

**Shampoo page: `/thinning-hair-shampoo` (rebuilt).**
- Targets a low-difficulty set: "regrow hair shampoo" (22,200 a month, KD 2), "sulfate-free shampoo for thinning hair" (12,100, KD 1), and the women's (8,100) and men's (6,600) versions.
- Honest framing: shampoo can't regrow hair, and FullyVital doesn't sell one, so the page bridges to the leave-on serum.
- 13 related posts link up to it.

The products pillar `/hair-growth-products-that-work` now links to both.

**Tracking.** `hub_tracker.py` has recorded the baseline for all 20 hubs:
- 28 days before the change, for each hub page and its cluster;
- head-term impressions and positions;
- index status.

Results are in `reports/hub-tracking.md`. Rerun with `python hub_tracker.py --inspect` from about 25 October for indexing, then every 2–4 weeks. The AEO tracker now covers 52 searches, adding the new hub head terms.
