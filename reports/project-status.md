# Project status (read this first in a new session)

Last updated: 2026-10-19 (project paused by the user; resume with "continue"). Keep this file current at the end of each work session.

## Where things stand

**Done**
- Phase 1 audit and Phase 2 plan.
- Clean-up batches 1 and 2.
- 121 article refreshes.
- The refresh test, with 9 treated and 20 control pages.
- AEO quick pass (2026-10-19): 125 older articles got a short answer and FAQ schema; 3 skipped. All 125 short answers were then rewritten so they answer directly, never "the article says". See `reports/aeo-quickpass-2026-10-19.md`.
- /finasteride safety fix (2026-10-19): the short answer and a body safety note now cover sexual side effects and the pregnancy warning. A full rewrite is #1 in the content queue.
- About 80 dead URLs redirected to topic-matched pages, and 27 redirect chains collapsed (2026-10-18/19).
- Product renames to the "Hair Revival" names (blog only; refresh-test pages wait).
- The product-page brief and FAQs. The user edits product pages themselves; there is no Shopify product write access.

**Hubs live (all published or rebuilt on 2026-10-18).** Tracked in `reports/hub-tracking.md`; plan in `data/processed/hub_rollout_plan.json`.

| Line | Hubs |
|---|---|
| Hair growth | `/how-to-stop-hair-loss`, `/best-hair-growth-vitamins`, `/rosemary-oil-for-hair-growth`, `/foods-for-hair-growth`, `/is-biotin-good-for-hair`, `/receding-hairlines`, `/hair-cycle`, `/types-of-alopecia` (conditions; no product links), `/alopecia-areata` (no product links), `/best-hair-growth-serums`, `/thinning-hair-shampoo`, `/hairstyles-for-thinning-hair`, `/minoxidil` (drug hub; informational, says FullyVital is not a substitute) |
| Gray | `/what-causes-gray-hair`, `/why-am-i-going-gray-causes-explained`, `/gray-hair-in-men`, `/vitamin-b12-deficiency-gray-hair`, `/vitamins-for-gray-hair`, `/can-stress-cause-gray-hair`, `/how-to-prevent-gray-hair-naturally`, `/gray-hair-myths-vs-facts`, `/best-anti-gray-hair-supplements-2026` |

Background: `reports/hair-growth-corpus-review.md` and `reports/anti-gray-review.md`.

**In progress:** nothing. Minoxidil/finasteride hub went live 2026-10-19.

**Next, in order**
1. From the week of 2026-11-16: the content queue (#1 is the /finasteride safety rewrite), 2 articles a week. Instructions in `reports/content-queue.md`, list in `data/reference/content_queue.csv`. A weekly reminder comes from the scheduler.
2. Until then, nothing urgent. Let measurement run (hubs launched 2026-10-18/19). The remaining 404s with history are off-topic beauty posts, removed on purpose; leave them (`data/processed/unredirected_404s_2026-10-19.csv`). `/copper-peptides-hair-thinning` will 301 to the new peptides article (queue #2) when it's published.

## Dated items

These are run by the daily scheduler (`fv_scheduler.py`, launch agent `com.fullyvital.scheduler`, schedule in `data/processed/schedule.json`). Check `reports/scheduler-status.md`, or run `python fv_scheduler.py --list`.

| Date | What | Who |
|---|---|---|
| 2026-10-25 | Hub indexing check (`hub_tracker.py --inspect`) | Automatic. Read the indexing section of `reports/hub-tracking.md`. |
| 2026-11-01 | Standardize survey numbers and claims: product pages (85–95%) vs. the blog (85%/88%); old widget claims on 83 refreshed pages; derma-roller posts' needle advice (the product is 1 mm) | Reminder, needs the user |
| every 14 days from 2026-11-08 | Hub tracking update | Automatic |
| 2026-11-15 | Interim refresh-test numbers | Automatic |
| every Monday from 2026-11-16 | Content queue reminder: write this week's 2 articles | Reminder; needs Claude plus the user's approval to publish |
| every 30 days from 2026-11-17 | AEO tracker (52 searches, about $0.10) | Automatic |
| 2026-12-03 | Refresh-test readout, then the deferred test-page items (see the memory note "pending-in-scope-no-traffic-posts") | Automatic run plus a reminder |

## Standing decisions (also in CLAUDE.md and memory)

- **Survey statistic:** the anti-gray survey line stays on the calendar posts. The user will standardize the numbers around 2026-11-01.
- **Old marketing claims:** skip them in blog widgets for now. Leave the "Promote Hair Regrowth" box unchanged and don't flag it.
- **Widget prices:** leave them alone.
- **Link direction:** links go blog → product only.
- **Calendar posts:** extend them, never rebuild.
- **New articles:** create them unpublished; publish only once the user approves.
- **Refresh-test pages:** never edit until the readout.
- **Medical reviewer:** none named yet, so don't add a reviewer line.
- **Product facts:** the derma roller is 1 mm, used once a week. The 120-day guarantee covers every product.
