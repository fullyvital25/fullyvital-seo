# Hub tracking

Hubs published or rebuilt on 2026-10-18. Search Console data to 2026-10-16.
- **Before:** the 28 days 2026-09-20–2026-10-17.
- **After:** 2026-10-19–2026-10-16 (no data after the change yet).
- **Cluster:** the hub, every page that linked to it when tracking started, and old URLs that now redirect to it.
- Rerun every 2–4 weeks with `python hub_tracker.py --inspect`. Google usually needs 4–8 weeks to reflect changes.

| Hub | Linking / merged | Hub clicks before → after | Hub impressions before → after | Cluster clicks before → after | Cluster impressions before → after |
|---|---|---|---|---|---|
| Hair: how to stop hair loss (`how-to-stop-hair-loss`) | 55 / 5 | 0 → — | 0 → — | 10 → — | 7,521 → — |
| Hair: vitamins (`best-hair-growth-vitamins`) | 34 / 4 | 0 → — | 11 → — | 12 → — | 3,700 → — |
| Hair: rosemary & oils (`rosemary-oil-for-hair-growth`) | 37 / 1 | 0 → — | 0 → — | 1 → — | 2,063 → — |
| Hair: protein & foods (`foods-for-hair-growth`) | 16 / 2 | 0 → — | 0 → — | 2 → — | 634 → — |
| Hair: biotin (`is-biotin-good-for-hair`) | 12 / 9 | 0 → — | 2 → — | 6 → — | 924 → — |
| Hair: receding hairline (`receding-hairlines`) | 19 / 6 | 0 → — | 29 → — | 12 → — | 6,022 → — |
| Hair: growth cycle (`hair-cycle`) | 16 / 5 | 0 → — | 6 → — | 2 → — | 3,578 → — |
| Hair: types of alopecia (`types-of-alopecia`) | 13 / 10 | 0 → — | 0 → — | 0 → — | 453 → — |
| Hair: alopecia areata (`alopecia-areata`) | 4 / 3 | 0 → — | 0 → — | 1 → — | 343 → — |
| Gray: causes (`what-causes-gray-hair`) | 10 / 0 | 0 → — | 8 → — | 4 → — | 505 → — |
| Gray: premature (`why-am-i-going-gray-causes-explained`) | 12 / 0 | 0 → — | 11 → — | 8 → — | 416 → — |
| Gray: men (`gray-hair-in-men`) | 4 / 2 | 0 → — | 0 → — | 7 → — | 241 → — |
| Gray: B12 (`vitamin-b12-deficiency-gray-hair`) | 3 / 0 | 0 → — | 0 → — | 0 → — | 42 → — |
| Gray: vitamins (`vitamins-for-gray-hair`) | 7 / 0 | 0 → — | 0 → — | 0 → — | 159 → — |
| Gray: stress (`can-stress-cause-gray-hair`) | 17 / 0 | 0 → — | 4 → — | 7 → — | 1,030 → — |
| Gray: prevent (`how-to-prevent-gray-hair-naturally`) | 21 / 0 | 0 → — | 42 → — | 7 → — | 1,221 → — |
| Gray: myths & white vs gray (`gray-hair-myths-vs-facts`) | 10 / 0 | 1 → — | 18 → — | 4 → — | 688 → — |
| Gray: products (`best-anti-gray-hair-supplements-2026`) | 20 / 3 | 6 → — | 203 → — | 22 → — | 2,173 → — |
| Hair: serums (`best-hair-growth-serums`) | 14 / 7 | 0 → — | 25 → — | 9 → — | 2,481 → — |
| Hair: shampoo for thinning hair (`thinning-hair-shampoo`) | 18 / 1 | 0 → — | 31 → — | 4 → — | 1,908 → — |
| Hair: styling (`hairstyles-for-thinning-hair`) | 16 / 0 | 0 → — | 0 → — | 11 → — | 3,238 → — |
| Hair: minoxidil & finasteride (`minoxidil`) | 19 / 4 | 0 → — | 92 → — | 4 → — | 2,424 → — |

## Target searches (sitewide, 90 days)

Which page Google shows for each hub's head terms. The goal is for the hub page to take most of these impressions, at a better position.

| Hub | Window | Matching queries | Impressions | Clicks | Avg position | Impressions on the hub page | Hub page position |
|---|---|---|---|---|---|---|---|
| Hair: how to stop hair loss | baseline_90d | 135 | 4,743 | 0 | 14.1 | 0 | — |
| Hair: vitamins | baseline_90d | 361 | 5,051 | 9 | 40.2 | 184 | 72.1 |
| Hair: rosemary & oils | baseline_90d | 3 | 4 | 0 | 7.8 | 0 | — |
| Hair: protein & foods | baseline_90d | 206 | 1,367 | 0 | 36.6 | 0 | — |
| Hair: biotin | baseline_90d | 494 | 2,681 | 8 | 57.3 | 157 | 81.0 |
| Hair: receding hairline | baseline_90d | 1,161 | 13,755 | 18 | 41.0 | 78 | 66.0 |
| Hair: growth cycle | baseline_90d | 488 | 2,958 | 0 | 51.0 | 1 | 75.0 |
| Hair: types of alopecia | baseline_90d | 342 | 1,165 | 1 | 73.3 | 0 | — |
| Hair: alopecia areata | baseline_90d | 258 | 1,247 | 0 | 84.6 | 522 | 89.3 |
| Hair: serums | baseline_90d | 987 | 22,246 | 189 | 28.9 | 14 | 14.9 |
| Hair: shampoo for thinning hair | baseline_90d | 87 | 669 | 0 | 34.5 | 23 | 48.2 |
| Hair: styling | baseline_90d | 6 | 12 | 0 | 41.3 | 0 | — |
| Hair: minoxidil & finasteride | baseline_90d | 359 | 2,125 | 0 | 52.3 | 81 | 39.9 |
| Gray: causes | baseline_90d | 43 | 86 | 0 | 44.5 | 4 | 82.5 |
| Gray: premature | baseline_90d | 30 | 485 | 0 | 13.0 | 0 | — |
| Gray: men | baseline_90d | 19 | 73 | 0 | 41.7 | 0 | — |
| Gray: B12 | baseline_90d | 8 | 15 | 0 | 56.5 | 0 | — |
| Gray: vitamins | baseline_90d | 159 | 2,714 | 2 | 46.4 | 0 | — |
| Gray: stress | baseline_90d | 6 | 10 | 0 | 10.7 | 0 | — |
| Gray: prevent | baseline_90d | 71 | 1,333 | 2 | 61.7 | 13 | 71.9 |
| Gray: myths & white vs gray | baseline_90d | 19 | 94 | 0 | 39.9 | 0 | — |
| Gray: products | baseline_90d | 133 | 5,126 | 33 | 30.5 | 99 | 44.9 |
