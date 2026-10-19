# Phase 1 — SEO Audit: fullyvital.com (gray hair + hair growth)

Audit date: 2026-10-12. Search Console property: `sc-domain:fullyvital.com`, 2025-06-10 to 2026-10-09. DataForSEO: US, English. All numbers are computed from the saved files in `data/`. "In scope" means the query or keyword contains one of the topic terms in `phase1-audit.md`; brand queries are excluded from in-scope figures.

## Executive summary

1. **Organic traffic has fallen by about two thirds in a year.** July–September clicks went from 6,599 in 2025 to 2,093 in 2026 (down 68%); impressions fell 84%. 94 of the 98 pages that had 10+ clicks in that window last year are down 30% or more.
2. **Half of the identifiable clicks are brand searches.** Of 8,687 clicks with a visible query, 4,351 are FullyVital brand queries. In-scope non-brand queries brought 1,341 clicks in 16 months; the gray cluster accounts for 303 of them.
3. **The site ranks for a lot but almost none of it is on page one.** DataForSEO finds 2,020 in-scope keywords, with 63 in the top 10 and 111 in the top 20. Only 3% of all ranked keywords are top 10, against 15%–35% for the eight competitors.
4. **Link authority is not the gap.** FullyVital's domain rank (317) is higher than 6 of the 8 competitors (arey.com, particleformen.com, mdhair.co, neofollics.com, kerotin.com, theradome.com), yet each of those has 2.5–20 times FullyVital's estimated organic traffic. The gap is in content performance, not links.
5. **A large share of the blog is dead weight.** 312 of 746 articles had under 50 impressions in the last 90 days (117 had none), and 315 had zero clicks in 16 months.
6. **Cannibalization is widespread.** 1,031 non-brand queries (200+ impressions) have two or more URLs each taking 10%+ of impressions; 431 are in scope. The two blogs (`hair-care`, `hair-vitamins`) often carry near-duplicate posts on the same ingredient.
7. **Keyword gap: 514 in-scope keywords** (618,690 monthly searches) where 2+ competitors rank top 20 and FullyVital is absent or below 50. 284 of them already have a lower-authority competitor in the top 10. Only 71 are gray-hair keywords (48,770 searches).
8. **Compliance risk sits on the product pages.** 8 of 61 product pages use "reverse" gray wording in the title, meta description or H1, and 15 use it somewhere in the copy (for example "Reverses Grays in 90 Days"). These need review before more traffic is sent to them.
9. **E-E-A-T is thin for a health topic.** Every article has a byline, but 733 of 746 carry the same one, only 14% link to a study, and none of a 60-article sample names a medical reviewer.
10. **Striking-distance upside is small.** Only 14 in-scope query–page pairs sit at positions 4–20 with 100+ impressions in 90 days. Quick ranking tweaks will not recover the decline.

## Current visibility in scope

### Search Console (16 months)

| Metric | Value |
|---|---|
| All clicks (site total) | 21,712 |
| All impressions (site total) | 5,475,834 |
| Clicks with a visible query | 8,687 |
| Share of clicks with no query shown (anonymized) | 60% |
| Share of impressions with no query shown | 41% |
| Brand clicks | 4,351 |
| In-scope non-brand queries | 17,744 |
| In-scope non-brand clicks | 1,341 |
| In-scope non-brand impressions | 755,007 |
| Gray cluster: clicks / impressions | 303 / 69,901 |
| Hair growth/loss cluster: clicks / impressions | 1,038 / 685,106 |
| In-scope queries with average position ≤3 / ≤10 / ≤20 | 1,108 / 2,717 / 4,345 |

The Search Console position counts include many queries with a handful of impressions, so they overstate real page-one presence. The DataForSEO counts below are the stricter view.

### DataForSEO (ranking snapshot)

| Metric | Value |
|---|---|
| All ranked keywords | 6,694 |
| In-scope keywords | 2,020 |
| In-scope top 3 / top 10 / top 20 | 11 / 63 / 111 |
| Gray keywords (all positions) | 279 |
| Gray keywords top 10 / top 20 | 10 / 20 |

### Monthly trend (all pages)

| Month | Clicks | Impressions |
|---|---|---|
| 2025-06 | 3,511 | 982,388 |
| 2025-07 | 2,776 | 949,440 |
| 2025-08 | 2,082 | 754,185 |
| 2025-09 | 1,741 | 504,259 |
| 2025-10 | 1,685 | 287,086 |
| 2025-11 | 1,642 | 230,510 |
| 2025-12 | 1,037 | 265,788 |
| 2026-01 | 929 | 210,552 |
| 2026-02 | 807 | 147,963 |
| 2026-03 | 813 | 190,832 |
| 2026-04 | 887 | 204,007 |
| 2026-05 | 890 | 214,841 |
| 2026-06 | 628 | 147,949 |
| 2026-07 | 638 | 140,089 |
| 2026-08 | 693 | 129,854 |
| 2026-09 | 762 | 89,115 |
| 2026-10 | 191 | 26,976 |

June 2025 and October 2026 are partial months.

### Clicks by page type (16 months)

| Page type | Clicks | Impressions |
|---|---|---|
| blog | 12,845 | 5,467,907 |
| product | 4,234 | 455,641 |
| home | 3,059 | 38,691 |
| page | 1,421 | 59,890 |
| collection | 457 | 57,517 |
| other | 32 | 17,191 |

## Content inventory

- 746 articles (600 in `hair-care`, 146 in `hair-vitamins`) and 34 content pages. Median article length is 1,968 words.
- Published by year: 2021: 10, 2022: 22, 2023: 432, 2024: 186, 2026: 96. The sitemap shows 715 articles modified in 2026, so last-modified dates do not indicate real content refreshes.
- 741 articles link to a product page. 115 have any external link; 102 link to a study or scientific source.
- The top 10 articles bring 27% of all article clicks.
- Full data: `data/processed/content_inventory.csv`.

## 1. Page scorecard (top 20 by clicks)

| URL | Clicks 16m | Impr. 16m | Avg pos. | Clicks 90d | Clicks Jul–Sep 2025 | Clicks Jul–Sep 2026 | Primary keyword (guess) | Words |
|---|---|---|---|---|---|---|---|---|
| /pages/faraz-khan | 479 | 6,156 | 5.0 | 37 | 259 | 38 | faraz khan | 242 |
| /blogs/hair-care/widows-peak-hair | 415 | 57,025 | 20.2 | 11 | 170 | 10 | widows peak hairstyles ladies | 2,653 |
| /blogs/hair-care/baby-hairs | 409 | 143,371 | 10.5 | 31 | 136 | 30 | are baby hairs a sign of balding | 2,136 |
| /blogs/hair-vitamins/boron | 380 | 31,344 | 6.7 | 64 | 78 | 65 | boron benefits for hair | 2,103 |
| /blogs/hair-care/isopropyl-alcohol | 312 | 102,434 | 10.1 | 1 | 130 | 1 | effects of rubbing alcohol on hair | 2,418 |
| /blogs/hair-vitamins/manganese | 280 | 13,307 | 5.2 | 23 | 97 | 25 | manganese benefits for hair | 2,097 |
| /blogs/hair-care/batana-oil-for-hair-growth | 277 | 107,912 | 15.8 | 0 | 133 | 0 | batana | 1,913 |
| /pages/shopify-collabs | 228 | 735 | 13.1 | 53 | 16 | 57 | cbd vital affiliate | 65 |
| /blogs/hair-care/biotin-vs-prenatal-vitamins-for-hair-growth | 217 | 33,136 | 30.8 | 13 | 62 | 13 | biotin vs prenatal vitamins for hair growth | 2,547 |
| /blogs/hair-vitamins/n-acetyl-cysteine | 177 | 18,959 | 9.7 | 2 | 80 | 2 | nac supplement | 1,954 |
| /blogs/hair-care/clogged-hair-follicles | 169 | 163,589 | 9.4 | 3 | 47 | 3 | clogged hair follicles | 2,609 |
| /blogs/hair-care/korean-perm-hair | 168 | 27,276 | 34.3 | 5 | 64 | 6 | korean perm | 2,320 |
| /blogs/hair-care/hair-relaxer | 166 | 32,276 | 19.5 | 0 | 62 | 0 | how to repair hair after relaxer damage | 2,489 |
| /blogs/hair-vitamins/chlorophyll | 164 | 32,420 | 8.0 | 12 | 61 | 12 | chlorophyll benefits for hair | 1,923 |
| /blogs/hair-vitamins/glutathione | 155 | 23,331 | 9.7 | 3 | 78 | 4 | glutathione grey hair | 1,969 |
| /blogs/hair-vitamins/glucosamine | 151 | 12,716 | 7.8 | 15 | 34 | 17 | does glucosamine cause hair loss | 1,964 |
| /pages/fully-vital-hair-reviews-results | 149 | 15,958 | 6.7 | 0 | 46 | 0 | fully hair | 1,449 |
| /blogs/hair-care/pumpkin-seed | 145 | 28,524 | 18.6 | 0 | 80 | 0 | how to eat pumpkin seeds for hair growth | 2,817 |
| /blogs/hair-care/how-to-get-rid-of-cowlicks | 140 | 32,141 | 23.1 | 2 | 46 | 3 | how to get rid of a cowlick | 2,193 |
| /blogs/hair-vitamins/choline | 139 | 14,508 | 6.5 | 29 | 42 | 27 | choline for hair growth | 1,951 |

Primary keyword is the non-brand query with the most impressions for the page. Full data, including top 5 queries and the 12-month click series: `page_scorecard.csv`.

## 2. Striking distance (last 90 days, in scope)

| Query | Page | Clicks | Impr. | Avg pos. | Expected click gain (90d) | Volume |
|---|---|---|---|---|---|---|
| hair loss treatment | /products/hair-growth-serum | 0 | 2,845 | 7.4 | 15.6 | — |
| hair loss treatment | /products/hair-growth-kit | 0 | 1,044 | 8.7 | 5.7 | — |
| best prenatal vitamins for hair growth | /blogs/hair-care/the-ultimate-guide-to-prenatal-vitamins-and-hair-growth-are-they-worth-the-hype | 0 | 849 | 10.2 | 4.6 | — |
| baby hair regrowth | /blogs/hair-care/baby-hairs | 0 | 213 | 5.2 | 1.2 | — |
| hair loss treatment | /products/womens-hair-growth-products | 0 | 198 | 7.3 | 1.1 | — |
| are baby hairs a sign of balding or regrowth | /blogs/hair-care/baby-hairs | 0 | 168 | 10.6 | 0.9 | — |
| does chlorophyll help with hair growth | /blogs/hair-vitamins/chlorophyll | 0 | 138 | 10.3 | 0.8 | 90.0 |
| boron hair loss | /blogs/hair-vitamins/boron | 0 | 140 | 9.7 | 0.8 | 90.0 |
| new baby hair growth in adults | /blogs/hair-care/baby-hairs | 0 | 102 | 7.6 | 0.6 | — |
| choline for hair growth | /blogs/hair-vitamins/choline | 0 | 118 | 6.0 | 0.6 | — |
| anti gray hair serum | /products/anti-gray-serum | 1 | 118 | 13.8 | 0.0 | 880 |
| boron hair growth | /blogs/hair-vitamins/boron | 6 | 131 | 7.0 | 0.0 | 70.0 |
| boron for hair growth | /blogs/hair-vitamins/boron | 3 | 113 | 6.7 | 0.0 | 70.0 |
| biotin vs prenatal vitamins for hair growth | /blogs/hair-care/biotin-vs-prenatal-vitamins-for-hair-growth | 8 | 600 | 5.1 | 0.0 | 320 |

Pairs at average position 4–20 with 100+ impressions; 66 pairs in total, 14 in scope. Expected gain uses the site's own non-brand click-through rate at positions 1–3 (0.55%), which is very low, so treat the gain column as a ranking order rather than a forecast. Volume is blank where DataForSEO has no row for the query. Full data: `striking_distance.csv`.

## 3. Cannibalization (in scope, top 20 by impressions)

| Query | Impr. 16m | URLs | Best avg pos. | Competing URLs |
|---|---|---|---|---|
| regrow hair naturally in 3 weeks | 8,126 | 2 | 39.5 | /blogs/hair-care/how-to-grow-your-hair-in-3-weeks / /blogs/hair-care/regrow-hair-naturally-in-3-weeks |
| anti-gray hair supplement 3-pack | 5,818 | 2 | 1.0 | /products/anti-gray-vitamins / /products/anti-gray-supplement-3-pack |
| ashwagandha hair loss | 4,302 | 2 | 49.0 | /blogs/hair-care/does-ashwagandha-cause-hair-loss / /blogs/hair-care/ashwagandha |
| hair loss treatment | 4,133 | 2 | 7.4 | /products/hair-growth-serum / /products/hair-growth-kit |
| how long does biotin take to work | 4,011 | 3 | 39.8 | /blogs/hair-care/how-long-does-it-take-biotin-to-work / /blogs/hair-care/how-long-does-it-take-for-biotin-to-start-working / /blogs/hair-care/how-long-does-it-take-for-biotin-to-work |
| selenium hair loss | 3,658 | 2 | 61.3 | /blogs/hair-vitamins/what-is-selenium-used-for / /blogs/hair-vitamins/selenium |
| prenatal vitamins for hair growth | 3,624 | 2 | 45.0 | /blogs/hair-care/the-ultimate-guide-to-prenatal-vitamins-and-hair-growth-are-they-worth-the-hype / /blogs/hair-care/biotin-vs-prenatal-vitamins-for-hair-growth |
| particle anti-gray serum | 3,217 | 4 | 1.0 | /products/anti-gray-serum-supplement / /products/gray-repigment-serum / /products/anti-gray-serum / /products/gray-hair-v4 |
| biotin results after 1 week | 3,022 | 3 | 58.4 | /blogs/hair-care/how-long-does-it-take-for-biotin-to-start-working / /blogs/hair-care/how-long-does-it-take-biotin-to-work / /blogs/hair-care/how-long-does-it-take-for-biotin-to-work |
| zinc for hair growth | 2,966 | 2 | 33.8 | /blogs/hair-care/zinc / /blogs/hair-vitamins/zinc |
| peppermint oil for hair growth | 2,792 | 2 | 57.2 | /blogs/hair-care/peppermint-oil-for-hair / /blogs/hair-vitamins/peppermint-oil |
| how long does it take for biotin to work | 2,629 | 3 | 40.4 | /blogs/hair-care/how-long-does-it-take-for-biotin-to-work / /blogs/hair-care/how-long-does-it-take-biotin-to-work / /blogs/hair-care/how-long-does-it-take-for-biotin-to-start-working |
| caffeine hair growth | 2,627 | 2 | 61.4 | /blogs/hair-vitamins/caffeine / /blogs/hair-care/caffeine-hair-growth |
| meta anti-gray supplement 3-pack | 2,610 | 3 | 1.0 | /products/anti-gray-vitamins / /products/anti-gray-supplement-3-pack / /products/anti-gray-vitamins-3-pk |
| vital hair growth | 2,432 | 4 | 8.5 | /products/vitamins-for-hair-growth / /collections/all /  / /products/womens-hair-growth-products |
| vitamin a for hair growth | 2,271 | 2 | 59.0 | /blogs/hair-vitamins/vitamin-a / /blogs/hair-care/vitamin-a |
| iron deficiency hair loss | 2,223 | 2 | 81.3 | /blogs/hair-care/iron-deficiency-hair-loss / /blogs/hair-care/iron-deficiency-hair-thinning |
| iodine for hair growth | 2,132 | 2 | 15.0 | /blogs/hair-care/iodine / /blogs/hair-vitamins/iodine-and-your-hair |
| turmeric for hair growth | 2,125 | 2 | 43.0 | /blogs/hair-care/turmeric / /blogs/hair-vitamins/turmeric |
| are baby hairs a sign of regrowth | 2,095 | 2 | 11.8 | /blogs/hair-care/baby-hairs / /products/enhance-hair-serum-supplement-2 |

Several product-name queries (for example "anti-gray hair supplement 3-pack") show position 1 with almost no clicks across multiple product URLs. Those URLs were recorded with Shopify `product_sync` parameters, which suggests they are product-listing impressions rather than standard results; this is a hypothesis, not confirmed. Full data: `cannibalization.csv`, `cannibalization_by_query.csv`.

## 4. Decay (Jul–Sep 2026 vs Jul–Sep 2025)

| URL | Clicks 2025 | Clicks 2026 | Change | Primary keyword (guess) | Words |
|---|---|---|---|---|---|
| /pages/faraz-khan | 259 | 38 | -85% | faraz khan | 242 |
| /blogs/hair-care/widows-peak-hair | 170 | 10 | -94% | widows peak hairstyles ladies | 2,653 |
| /blogs/hair-care/baby-hairs | 136 | 30 | -78% | are baby hairs a sign of balding | 2,136 |
| /blogs/hair-care/batana-oil-for-hair-growth | 133 | 0 | -100% | batana | 1,913 |
| /blogs/hair-care/isopropyl-alcohol | 130 | 1 | -99% | effects of rubbing alcohol on hair | 2,418 |
| /blogs/hair-vitamins/manganese | 97 | 25 | -74% | manganese benefits for hair | 2,097 |
| /blogs/hair-vitamins/n-acetyl-cysteine | 80 | 2 | -98% | nac supplement | 1,954 |
| /blogs/hair-care/pumpkin-seed | 80 | 0 | -100% | how to eat pumpkin seeds for hair growth | 2,817 |
| /blogs/hair-vitamins/glutathione | 78 | 4 | -95% | glutathione grey hair | 1,969 |
| /blogs/hair-care/korean-perm-hair | 64 | 6 | -91% | korean perm | 2,320 |
| /blogs/hair-care/biotin-vs-prenatal-vitamins-for-hair-growth | 62 | 13 | -79% | biotin vs prenatal vitamins for hair growth | 2,547 |
| /blogs/hair-care/hair-relaxer | 62 | 0 | -100% | how to repair hair after relaxer damage | 2,489 |
| /blogs/hair-vitamins/chlorophyll | 61 | 12 | -80% | chlorophyll benefits for hair | 1,923 |
| /blogs/hair-care/pygeum-bark | 49 | 0 | -100% | pygeum bark hair loss | 1,913 |
| /blogs/hair-vitamins/lecithin | 47 | 5 | -89% | lecithin benefits for hair | 1,804 |
| /blogs/hair-care/clogged-hair-follicles | 47 | 3 | -94% | clogged hair follicles | 2,609 |
| /blogs/hair-care/how-to-get-rid-of-cowlicks | 46 | 3 | -93% | how to get rid of a cowlick | 2,193 |
| /pages/fully-vital-hair-reviews-results | 46 | 0 | -100% | fully hair | 1,449 |
| /blogs/hair-vitamins/milk-thistle | 45 | 2 | -96% | milk thistle for hair growth | 1,970 |
| /blogs/hair-care/best-hair-growth-serum-for-gray-hair | 43 | 0 | -100% | shine serum for gray hair | 2,380 |

94 pages qualify (10+ clicks in the 2025 window, down 30%+), losing 2,911 clicks between them. Full data: `decay.csv`.

## 5. Zero-performers

312 articles had under 50 impressions in 90 days. 49 of them were published in 2026 and may simply be too new to judge. Index status was not checked (that needs URL inspection per page), so "indexed" here means "listed in the sitemap".

| URL | Published | Words | Impr. 90d | Impr. 16m | Clicks 16m |
|---|---|---|---|---|---|
| /blogs/hair-care/folate | 2023-07-18 | 3,220 | 17 | 657 | 1 |
| /blogs/hair-care/hair-extensions | 2023-07-05 | 3,123 | 0 | 24 | 0 |
| /blogs/hair-care/tonic | 2023-07-04 | 3,080 | 14 | 10,025 | 3 |
| /blogs/hair-care/hair-doctor-specialist | 2024-01-10 | 3,075 | 0 | 40 | 0 |
| /blogs/hair-care/keratin-treatment | 2023-07-04 | 3,071 | 0 | 906 | 2 |
| /blogs/hair-care/best-shampoo-for-dry-hair | 2024-01-09 | 3,053 | 0 | 1,302 | 0 |
| /blogs/hair-care/dermaroller-for-face | 2023-07-03 | 3,045 | 0 | 619 | 0 |
| /blogs/hair-care/biotin-for-hair | 2023-07-05 | 2,982 | 2 | 45 | 0 |
| /blogs/hair-care/derma-roller-for-hair | 2023-06-29 | 2,981 | 0 | 0 | 0 |
| /blogs/hair-care/conditioning | 2023-07-04 | 2,965 | 16 | 919 | 1 |
| /blogs/hair-care/keratin | 2023-07-10 | 2,960 | 7 | 201 | 0 |
| /blogs/hair-care/gray-highlights | 2024-01-11 | 2,885 | 47 | 920 | 0 |
| /blogs/hair-care/microneedling-at-home | 2023-07-03 | 2,809 | 0 | 542 | 0 |
| /blogs/hair-care/clarifying-shampoo | 2023-06-27 | 2,783 | 0 | 0 | 0 |
| /blogs/hair-care/hair-doctor | 2024-01-03 | 2,775 | 2 | 34 | 0 |
| /blogs/hair-vitamins/keratin | 2024-01-15 | 2,747 | 0 | 12 | 0 |
| /blogs/hair-care/dermaroller | 2023-06-29 | 2,742 | 0 | 23 | 0 |
| /blogs/hair-care/phthalates | 2023-07-12 | 2,721 | 0 | 52 | 0 |
| /blogs/hair-care/dermatologist | 2023-08-13 | 2,720 | 6 | 1,112 | 0 |
| /blogs/hair-care/hyaluronic-acid | 2023-07-13 | 2,706 | 21 | 701 | 0 |

Table shows the 20 longest pre-2026 posts. Full data: `zero_performers.csv`.

## 6. Keyword gap (top 20 by volume)

| Keyword | Volume | KD | Intent | Trend YoY % | Competitors top 20 | FullyVital pos. | Top-10 avg domain rank | Lower-authority competitor in top 10 |
|---|---|---|---|---|---|---|---|---|
| protein for hair growth | 27,100 | 25 | informational | 82.0 | 2 | — | 545 | — |
| peptide for hair growth | 18,100 | 0 | informational | 235 | 2 | — | 530 | — |
| peptides for hair growth | 18,100 | 0 | informational | 235 | 2 | — | 552 | — |
| copper peptides for hair loss | 12,100 | 0 | informational | 174 | 2 | — | 491 | mdhair.co #6 |
| hair growth supplements for men | 12,100 | 12 | commercial | -64.0 | 2 | — | 379 | — |
| copper peptides for hair growth | 12,100 | 0 | informational | 174 | 2 | — | 422 | mdhair.co #4 |
| hair to regrow | 9,900 | 41 | informational | 50.0 | 2 | — | 556 | — |
| what is the cause of graying hair | 9,900 | 46 | informational | 0.0 | 2 | — | 526 | neofollics.com #8 |
| what is the cause of grey hair | 9,900 | 46 | informational | 0.0 | 2 | — | 599 | — |
| protein supplements for hair growth | 6,600 | 19 | commercial | -84.0 | 2 | — | 534 | — |
| onion juice for hair growth | 5,400 | 13 | informational | 0.0 | 2 | — | 663 | — |
| hair growth tablets | 5,400 | 19 | transactional | 0.0 | 2 | — | 538 | mdhair.co #6 |
| prenatals and hair growth | 5,400 | 0 | informational | 10,700 | 3 | 55.0 | 562 | — |
| prenatal pills hair growth | 5,400 | 0 | informational | 23.0 | 2 | 54.0 | 619 | — |
| prenatal pills for hair growth | 5,400 | 2 | transactional | 23.0 | 2 | 55.0 | 618 | — |
| how long for hair growth | 5,400 | 33 | informational | 86.0 | 2 | 63.0 | 588 | — |
| beard hair growth products | 5,400 | 0 | transactional | -56.0 | 2 | — | 469 | — |
| does prenatal help with hair growth | 4,400 | 0 | informational | 23.0 | 2 | 55.0 | 528 | — |
| does prenatal pills help hair growth | 4,400 | 0 | informational | 23.0 | 3 | 59.0 | 589 | theradome.com #9 |
| peptides for hair loss | 4,400 | 0 | informational | 247 | 3 | — | 530 | — |

### Gray-hair gap keywords (top 20)

| Keyword | Volume | Intent | Competitors top 20 | FullyVital pos. | Who ranks | Lower-authority competitor in top 10 |
|---|---|---|---|---|---|---|
| what is the cause of graying hair | 9,900 | informational | 2 | — | neofollics.com, theradome.com | neofollics.com #8 |
| what is the cause of grey hair | 9,900 | informational | 2 | — | neofollics.com, theradome.com | — |
| naturally white hair | 2,400 | informational | 2 | — | kerotin.com, hims.com | — |
| dying hair gray men | 2,400 | commercial | 2 | — | hims.com, arey.com | — |
| early grey hair | 1,600 | informational | 2 | — | neofollics.com, theradome.com | — |
| early grey hairs | 1,600 | informational | 2 | — | hims.com, neofollics.com | — |
| grey hair causes | 1,600 | informational | 3 | — | hims.com, neofollics.com, theradome.com | — |
| grey hair reasons | 1,600 | informational | 2 | — | theradome.com, neofollics.com | — |
| reason of gray hair | 1,600 | informational | 2 | — | neofollics.com, theradome.com | neofollics.com #10 |
| how to stop grey hair naturally | 880 | informational | 2 | — | arey.com, neofollics.com | — |
| prematurely grey | 880 | informational | 2 | — | theradome.com, neofollics.com | — |
| what cause grey hair at young age | 720 | informational | 2 | — | neofollics.com, theradome.com | neofollics.com #10 |
| what causes gray hair at young age | 720 | informational | 2 | — | theradome.com, neofollics.com | — |
| copper supplement for grey hair | 590 | informational | 2 | 52.0 | neofollics.com, mdhair.co | — |
| gray hair in young age | 590 | informational | 2 | — | theradome.com, neofollics.com | — |
| what causes premature grey hair | 480 | informational | 2 | — | neofollics.com, theradome.com | — |
| is grey hair genetic | 480 | informational | 2 | — | theradome.com, neofollics.com | theradome.com #7 |
| gray hair vitamin b12 | 480 | informational | 2 | 55.0 | mdhair.co, arey.com | — |
| medicine for white hair | 390 | informational | 2 | 55.0 | neofollics.com, mdhair.co | — |
| grey hairs meaning | 390 | informational | 2 | — | neofollics.com, vegamour.com | — |

514 gap keywords: 437 where FullyVital does not rank at all. By intent: informational 423, transactional 66, commercial 25. Full data: `keyword_gap.csv`.

## 7. Authority gap and winnability

| Domain | Domain rank (0–1,000) | Referring domains | Backlinks | Ranked keywords | Top-10 keywords | Est. organic traffic | In-scope top-20 keywords |
|---|---|---|---|---|---|---|---|
| fullyvital.com | 317 | 1,637 | 6,570 | 6,694 | 191 | 729 | 111 |
| arey.com | 255 | 1,474 | 6,209 | 2,537 | 437 | 1,809 | 503 |
| particleformen.com | 265 | 2,034 | 15,863 | 3,680 | 618 | 14,392 | 101 |
| vegamour.com | 328 | 3,440 | 17,318 | 18,897 | 2,847 | 18,508 | 757 |
| mdhair.co | 271 | 861 | 7,526 | 9,346 | 1,427 | 5,873 | 800 |
| hims.com | 401 | 12,873 | 178,139 | 152,147 | 45,101 | 339,021 | 1,465 |
| neofollics.com | 263 | 2,197 | 4,583 | 11,725 | 3,103 | 5,966 | 696 |
| kerotin.com | 197 | 1,366 | 1,877 | 1,628 | 337 | 1,894 | 135 |
| theradome.com | 285 | 2,141 | 7,480 | 18,532 | 6,474 | 11,686 | 1,029 |

In-scope top-20 counts for competitors are capped at 500 per topic chunk (1,500 max), so hims.com, theradome.com, mdhair.co, neofollics.com, vegamour.com and arey.com are undercounted.

**Winnability rule:** a gap keyword is marked winnable when a competitor with domain rank at or below FullyVital's (317) already ranks in the top 10 for it. 284 of 514 gap keywords qualify (275,060 monthly searches): 28 gray, 256 hair growth/loss. DataForSEO's keyword difficulty is shown but not used for this call: it scores 0 for about 40% of keywords at every volume level.

Domains appearing most often in the live results for the top 20 gap keywords: youtube.com (13), amazon.com (8), reddit.com (8), elle.com (6), healthline.com (5), health.com (5), santeclinics.com (3), idealofmed.com (3), instagram.com (3), health.harvard.edu (3).

## 8. Compliance flags

Automated pattern scan of 746 articles, 34 pages and 61 product pages. It finds wording to review; it is not a legal determination, and the article-level disease flags include false positives where a product widget sits next to a heading.

| Check | Result |
|---|---|
| Product pages with "reverse" gray wording in title, meta or H1 | 8 of 61 |
| Product pages with "reverse" gray wording anywhere in copy | 15 of 61 |
| Articles with "reverse" gray wording in title, meta or H1 | 6 of 746 |
| Articles with "reverse" gray wording anywhere | 62 of 746 |
| Articles tying a FullyVital product to "reverse" gray wording in one sentence | 5 |
| Articles whose title or meta pairs treat/prevent/cure wording with a condition | 35 of 746 |
| Articles carrying the FDA disclaimer text | 95 of 746 |
| Product pages carrying the FDA disclaimer text | 61 of 61 |

### Product pages to review first

| Product page | Wording found |
|---|---|
| /products/anti-gray-vitamins | FullyVital combines cutting-edge, clinically proven ingredients to target these pathways, helping to slow and even reverse the graying process naturally. |
| /products/anti-gray-serum-3-pack-free-silk-sleep-mask | Reverse Gray Serum (x3) + Sleep Mask Sale price $179.00 Add to cart HAIR WELLNESS Shop Bestsellers Join Membership Science Our Results Ingredients Blog FAQ Author My Acco |
| /products/gray-hair-v4 | BioMelanin Formula Reverses Grays FullyVital's advanced ingredients target all root causes of hair graying. |
| /products/graykit-intro | FullyVital ★★★★★ 4.6 stars from 21K happy customers Brealthrough BioMelanin System Reverses Grays in 90 Days 85% saw new pigment in 90 days Skip salon visits. |
| /products/anti-gray-serum-supplement | FullyVital is formulated with cutting-edge, scientific ingredients that target the major pathways to slow down and reverse the graying process. |
| /products/anti-gray-supplement-3-pack | FullyVital combines cutting-edge, clinically proven ingredients to target these pathways, helping to slow and even reverse the graying process naturally. |
| /products/anti-gray-serum-3-pack | FullyVital is formulated with cutting-edge, scientific ingredients that target the major pathways to slow down and reverse the graying process. |
| /products/anti-gray-90-day-system | Anti-Gray System 90 Day Sale price $259.00 Regular price $279.00 Add to cart Free Shipping on Autoship & Orders $35+ 120-Day Money Back Guarantee Vegan, Cruelty-Free, Dru |
| /products/anti-gray-vitamins-free-silk-sleep-mask | FullyVital combines cutting-edge, clinically proven ingredients to target these pathways, helping to slow and even reverse the graying process naturally. |
| /products/greysup | FullyVital combines clinically proven ingredients to target 5 graying pathways , helping to slow and reverse the graying process naturally. |
| /products/free-hair-revival-guide | Hair Revival Guide FREE Guide to Reverse Gray Hairs Naturally. Hair Revival Guide |
| /products/free-gray-reversal-guide | Gray Reversal Guide FREE Guide to Reverse Gray Hairs Naturally. Gray Reversal Guide |
| /products/gray-repigment-serum | Dr. Formulated BioMelanin Serum Reverses Grays in 90 Days Repigment grays with PTP-20 peptide + exosomes + 12 clinical extracts. 85% saw new pigment in 90 days 100% natur |
| /products/anti-gray-serum-men | Reverse Gray Serum Breakthrough serum with PTP-20 peptide and 12 clinical ingredients to reduce gray hairs - naturally. ✔ 90% saw new pigment in 90 days ✔ Targets 5 root  |
| /products/vitamins-for-hair-growth | Hair Growth Supplements - 27 Superfoods for Thicker, Fuller Hair Hair growth supplements with 27 superfoods to stop thinning and boost density. Targets hormonal hair loss |

### Articles to review first

| Article | Wording found |
|---|---|
| /blogs/hair-care/can-gray-hair-be-reversed | The Short Answer No product, including FullyVital's, can promise full reversal of gray hair, and no peer-reviewed study has demonstrated it at scale. |
| /blogs/hair-care/nutrafol-vs-fully-vital | If you prefer to get products that delay and reverse gray hairs: you must go with FullyVital. |
| /blogs/hair-care/wellbel-vs-fully-vital | If you prefer to get products that delay and reverse gray hairs: you must go with FullyVital. |
| /blogs/hair-care/fully-vital-vs-wellbel | If you prefer to get products that delay and reverse gray hairs: you must go with FullyVital. |
| /blogs/hair-care/5-step-plan-to-delay-grays | 5-Step Plan To Reverse Grays As we age, it’s natural to see some graying, but for many, it’s an unwelcome change. Gray hair occurs when melanocytes, the pigment-producing |
| /blogs/hair-care/reverse-gray-hair-naturally-without-dye | Can You Reverse Gray Hair Naturally (Without Dye)? Tired of chasing roots with dye? Learn how nutritional and topical approaches can support your hair's natural color — a |
| /blogs/hair-care/how-long-to-see-less-gray-hair | How Long Does It Take to See Less Gray Hair? Wondering how long to reverse gray hair? Get the honest growth-cycle timeline — and what FullyVital's 30/60/90-day system is  |
| /blogs/hair-care/premature-gray-hair-reversal-early-action | Premature Gray Hair Reversal: Why Early Action Works Best Can premature gray hair be reversed? Learn why catching grays early gives your follicles the best chance — and h |
| /blogs/hair-care/gray-hair-research-studies | Gray Hair Research: What Peer-Reviewed Studies Show Every major peer-reviewed study on gray hair causes and reversal, from stress and oxidative stress to nutrient deficie |
| /blogs/hair-care/gray-hair-ingredients-ranked-by-evidence | FullyVital's Anti-Gray system combines ingredients across these tiers, including copper (Tier A) and Greyverse/PTP-20 (Tier B), because no single ingredient on this list, |

`/blogs/hair-care/can-gray-hair-be-reversed` is flagged by the pattern but states that no product can promise reversal; it is a model for compliant wording, not a problem. Full data: `compliance_flags.csv`.

## 9. E-E-A-T check

| FullyVital | Value |
|---|---|
| Articles with a byline | 746 of 746 |
| Authors | Faraz Khan, MSC (733), FullyVital Editorial Team (13) |
| Articles linking to at least one study | 102 (14%) |
| "Reviewed by" or fact-check mention (60-article sample) | 0 of 60 |
| Schema on articles | Article, BlogPosting, BreadcrumbList, Organization, Person on all; FAQPage on 92 |

### Competitor sample (top 3 blog URLs per competitor by in-scope top-20 keywords)

| Domain | URL | Words | Author | Schema | Study links | Reviewer named |
|---|---|---|---|---|---|---|
| arey.com | arey.com/blogs/grey-matter/can-you-reverse-grey-hair-naturally-here-s- | 1,345 | BY JAY SMALL, HAIRSTYLIST AND CO-FOUNDER OF AREY | Article, Organization | 7.0 | False |
| arey.com | arey.com/blogs/grey-matter/when-will-your-hair-go-grey-why-your-ethnic | 1,502 | BY JAY SMALL, HAIRSTYLIST AND CO-FOUNDER OF AREY | Article, Organization | 4.0 | False |
| arey.com | arey.com/blogs/grey-matter/why-men-s-hair-goes-grey-and-what-you-can-d | 1,089 | Amanda Mears | Article, Organization | 0.0 | False |
| hims.com | www.hims.com/blog/natural-hair-growth | 0.0 | Vanessa Gibbs | ItemList, MedicalWebPage, OpinionNewsArticle | 0.0 | True |
| hims.com | www.hims.com/blog/mens-hairstyles-for-thinning-hair | 0.0 | Grace Gallagher | ItemList, MedicalWebPage, OpinionNewsArticle, VideoObject | 0.0 | True |
| hims.com | www.hims.com/blog/minoxidil-for-beard | — | — | — | — | — |
| kerotin.com | kerotin.com/blogs/featured/hair-friendly-drinks-smoothies-for-hair-gro | 493 | marketing e-brands | BlogPosting, BreadcrumbList | 0.0 | False |
| kerotin.com | kerotin.com/blogs/featured/6-tips-for-turning-your-gray-hair-into-shin | 0.0 | — | — | 0.0 | False |
| kerotin.com | kerotin.com/blogs/featured/how-long-does-it-actually-take-to-regrow-ha | 973 | Kim Nguyen | BlogPosting, BreadcrumbList | 0.0 | False |
| mdhair.co | www.mdhair.co/article/premature-hair-graying | 2,742 | Yoram Harth, MD | BlogPosting, MedicalWebPage | 1.0 | True |
| mdhair.co | www.mdhair.co/article/spray-vs-dropper-for-minoxidil-is-there-a-differ | 1,392 | Yoram Harth, MD | BlogPosting, MedicalWebPage | 0.0 | True |
| mdhair.co | www.mdhair.co/article/best-hair-dyes-for-people-with-hair-loss | 1,804 | Yoram Harth, MD | BlogPosting, MedicalWebPage | 0.0 | True |
| neofollics.com | neofollics.com/blogs/articles/grey-hair | 1,632 | Neofollics Content Team | BlogPosting, BreadcrumbList, OnlineStore, Organization, WebSite | 2.0 | True |
| neofollics.com | neofollics.com/blogs/articles/diseases-and-conditions-that-cause-hair- | 1,181 | Neofollics Content Team | BlogPosting, BreadcrumbList, OnlineStore, Organization, WebSite | 0.0 | True |
| neofollics.com | neofollics.com/blogs/articles/shedding | 757 | — | BlogPosting, BreadcrumbList, OnlineStore, Organization, WebSite | 0.0 | False |
| theradome.com | theradome.com/blogs/blog/can-minoxidil-cause-hair-loss | 947 | Tamim Hamid | Article, BreadcrumbList, Organization, WebPage, WebSite | 0.0 | False |
| theradome.com | theradome.com/blogs/blog/how-to-regrow-hair-on-a-bald-spot | 2,300 | Tamim Hamid | Article, BreadcrumbList, Organization, WebPage, WebSite | 1.0 | False |
| theradome.com | theradome.com/blogs/blog/how-to-stop-hair-shedding | 3,161 | Tamim Hamid | Article, BreadcrumbList, Organization, WebPage, WebSite | 3.0 | False |
| vegamour.com | vegamour.com/blogs/blog/biotin-vs-keratin | 1,173 | — | — | 1.0 | False |
| vegamour.com | vegamour.com/blogs/blog/why-does-hair-turn-gray-at-the-temples-first | 1,299 | — | — | 1.0 | False |
| vegamour.com | vegamour.com/blogs/blog/foods-with-biotin | 1,358 | — | — | 19.0 | False |

This is a small sample (up to 3 pages per competitor). hims.com pages render content with JavaScript, so word and link counts are missing there, and one request was blocked (403). particleformen.com had no blog-style URLs among its in-scope top-20 pages. What the sample does show: mdhair.co bylines an MD and uses `MedicalWebPage` schema; hims.com and mdhair.co name a reviewer; arey.com and vegamour.com cite studies in some posts.

## Competitor landscape

**Brand competitors analyzed:** arey.com, particleformen.com, vegamour.com, mdhair.co, hims.com, neofollics.com, kerotin.com, theradome.com. Selected from DataForSEO's competitor overlap and the top results for 10 seed keywords.

**Publishers dominating the results (not pulled):** healthline.com (4,445 shared keywords), byrdie.com (2,687), medicalnewstoday.com (2,326), webmd.com (2,240), clevelandclinic.org (1,685). YouTube, Reddit and Amazon also appear on most seed results.

Nutrafol, Viviscal and similar brands did not surface in this data and were not analyzed.

## Recommended Phase 2 focus (hypotheses, not a plan)

1. **Consolidate before building.** Merge near-duplicate posts (biotin timing has 3 URLs; zinc, caffeine and peppermint oil each have a post in both blogs; selenium has two) and decide the fate of the ~260 pre-2026 posts with almost no impressions. Hypothesis: the volume of thin, overlapping posts is suppressing the whole blog.
2. **Refresh the pages that used to work.** The top of the decay list (baby hairs, manganese, N-acetyl cysteine, glutathione and grey hair, biotin vs prenatal vitamins) already proved it can rank.
3. **Gray hair: build the "causes" cluster.** The gray gap is informational: what causes gray hair (9,900), early or premature grey (1,600 each), grey hair causes. neofollics.com and theradome.com rank for these with lower authority. Copper, B12 and peptide-for-grey-hair terms are where FullyVital sits just outside the top 50.
4. **Hair growth: peptides and copper peptides.** Volumes of 12,100–18,100 with year-on-year search growth of 174–235%, and mdhair.co already ranks top 10 for the copper peptide terms.
5. **Commercial gray terms need a compliant landing page.** "Gray hair supplement", "vitamins for gray hair" and "anti gray hair serum" and close variants sit at positions 25–48 in DataForSEO. Product-page wording has to be fixed first (see section 8).
6. **Raise E-E-A-T on the pages that matter.** Add study citations and a named medical reviewer to the refreshed and new pages; test `MedicalWebPage` schema as mdhair.co and hims.com use.
7. **Treat medical-condition topics with care.** Many gap keywords are about alopecia types and medication side effects. They are YMYL, dominated by medical publishers, and risky to pair with product links.

## Data gaps and caveats

- **DataForSEO spend:** $1.99 for the phase (balance $51.00 → $49.01). The per-call logs in `dfs_spend_*.csv` total $1.75; the remaining $0.24 was the paged pull of FullyVital's full in-scope keyword set, which was run ad hoc and not written to a spend file.
- **Keyword difficulty is unreliable** (0 for about 40% of keywords, including "hair growth serum" at 74,000 searches). Winnability uses competitor authority instead.
- **Anonymized queries:** 60% of clicks and 41% of impressions have no query in Search Console, so query-level figures understate reality.
- **Ranking data is a snapshot** up to about three months old (median 2026-09-03).
- **FullyVital's unfiltered keyword list** is the top 1,000 of 6,694 by volume; the in-scope list is complete (2,020 rows).
- **Competitor in-scope lists** are the top 500 per topic chunk by volume, top-20 positions only. The gap list therefore leans toward higher-volume terms.
- **Seed and gap results pages** returned 6–8 organic results each, not a full 10.
- **Product map** was not provided; no product-to-topic mapping was used. Seed competitors were not provided either.
- **Content crawl** used a Python crawler rather than WebFetch, for exact word counts and schema. It covers published URLs in the sitemap only. Product pages were fetched for the compliance scan but are not in the inventory.
- **Index status** was not checked per URL.
- **Expected click gain** in striking distance rests on the site's own, unusually low, click-through rates.
- **Cause of the traffic decline** was not investigated; this audit only measures it.
