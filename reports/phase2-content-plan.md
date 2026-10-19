# Phase 2: Keyword research and content plan

Scope: gray/grey hair and hair growth/hair loss, mapped to the 10 FullyVital products in `data/reference/fullyvital_products.csv`. No changes were made to the site. Everything here is a recommendation for you to approve.

## Summary

1. **Keyword universe:** 12,547 in-scope keywords (10,865 with search volume from DataForSEO, 1,682 from Search Console only), grouped into 43 topic clusters across the two product lines.
2. **Where the demand is that FullyVital can serve:** about 3,096,100 monthly searches across hair growth/loss clusters and 150,610 across gray-hair clusters (de-duplicated; clusters with no product fit excluded).
3. **Gray hair is the smaller market but the better fit.** The largest gray cluster by raw volume is coverage, dye and styling (271,840), which FullyVital's products don't serve. The clusters that do fit (causes, early graying, nutrients, myths, products) are informational, and results pages for them are led by medical sites (AAD, Harvard, Cleveland Clinic) plus a few brands, notably neofollics.com.
4. **FullyVital barely ranks in either line.** It has top-10 positions in only a handful of clusters, mostly long-tail ingredient pages in hair growth; no gray cluster has more than 5 top-10 keywords.
5. **Highest-scoring hair-growth clusters (excluding the catch-all):** Growth products: serums, shampoos, kits, Hair vitamins & supplements (commercial), Remedies & how to stop hair loss. These combine demand, product fit and commercial intent.
6. **Biggest demand to avoid:** prescription drugs (1,525,580 searches) and medications that cause hair loss. They have no product fit and carry compliance risk.
7. **The 132 held posts:** 22 rewrite (one per distinct topic with demand), 40 merge or fold into another page, 70 remove.
8. **The 69 brand comparison posts:** keep and refresh 6 (direct competitors with search demand: Arey, Nutrafol, Particle, Pura d'or, Vegamour, Viviscal), remove 61, and 2 aren't brand comparisons.
9. **Indexing:** of 589 published articles inspected, 480 are indexed; 63 are crawled or discovered but not indexed, and 44 are unknown to Google.
10. **DataForSEO spend for Phase 2:** $0.91.

## How this was built

- **Keywords:** Phase 1 data (FullyVital and 8 competitors' in-scope rankings, the 514-keyword gap list, 16 months of Search Console queries) plus DataForSEO keyword suggestions for 22 seed terms, 12 of them gray-hair, because Phase 1 had little gray-hair data.
- **Clusters:** rule-based topic taxonomy, see `phase2_keywords.py`. Each keyword is mapped to the product it serves, FullyVital's best current page, and that page's clean-up status.
- **De-duplicated demand:** DataForSEO gives every variant of a search family the same volume (for example, 25 "haircuts for thinning hair women" variants at 18,100 each). Variants with the same volume and mostly the same words are counted once. Raw sums are in the CSV for reference.
- **Winnability:** a lower-authority competitor already ranks top 10, or the top 10's average domain rank is at or below FullyVital's (317).
- **Score:** de-duplicated demand × product fit × compliance factor × winnability × commercial intent. A ranking aid, not a forecast.
- **Results-page check:** live top 10 for the head term of each priority cluster (30 searches).

## Gray hair clusters

| Rank | Cluster | Demand (de-duplicated) | Head term | FullyVital top-10 keywords | Winnable volume | Product | Live posts | Recommended action |
|---|---|---|---|---|---|---|---|---|
| 1 | Gray: general | 87,550 | grey in hair | 0 | 4,570 | Anti-Gray System | 9 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 2 | Gray: causes | 47,340 | what causes grey hair | 1 | 56,250 | Anti-Gray Supplements | 9 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 3 | Gray: supplements & products | 19,040 | products for gray hair | 5 | 18,380 | Anti-Gray System | 15 | Commercial: optimise product/collection page + compliant comparison/guide content |
| 4 | Gray: reversal, slowing & stopping | 26,770 | how to prevent gray hair | 1 | 6,120 | Anti-Gray System | 6 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 5 | Gray: competitor brands | 7,710 | arey grey | 2 | 8,570 | Anti-Gray System | 7 | Commercial: optimise product/collection page + compliant comparison/guide content |
| 6 | Gray: nutrients & deficiencies | 11,600 | vitamin b12 deficiency gray hair | 1 | 5,580 | Anti-Gray Supplements | 7 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 7 | Gray: men | 14,930 | greying men | 0 | 320 | Anti-Gray System | 1 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 8 | Gray: questions, myths & meaning | 9,830 | white vs gray hair | 0 | 480 | Anti-Gray System | 1 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 9 | Gray: by age & early graying | 9,850 | early grey hair | 0 | 400 | Anti-Gray System | 0 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 10 | Gray: natural remedies | 3,540 | natural white hair | 0 | 0 | Anti-Gray Serum | 0 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 11 | Gray: coverage, dye & styling | 271,840 | gray blending for dark hair | 0 | 7,840 | none | 8 | Avoid (no product fit, or drug/styling topic) |
| 12 | Gray: care for gray hair | 36,380 | for gray hair shampoo | 0 | 16,660 | none | 0 | Avoid (no product fit, or drug/styling topic) |
| 13 | Off-scope: beard, brows, lashes, body, pets | 31,040 | anime character with white hair | 0 | 460 | none | 2 | Avoid (no product fit, or drug/styling topic) |

## Hair growth and hair loss clusters

| Rank | Cluster | Demand (de-duplicated) | Head term | FullyVital top-10 keywords | Winnable volume | Product | Live posts | Recommended action |
|---|---|---|---|---|---|---|---|---|
| 1 | Growth products: serums, shampoos, kits | 322,970 | hair growth serum | 2 | 80,000 | Hair Revival Kit / System | 58 | Commercial: optimise product/collection page + compliant comparison/guide content |
| 2 | Hair vitamins & supplements (commercial) | 347,150 | hair growth supplements | 2 | 31,850 | Hair Revival Supplements | 35 | Commercial: optimise product/collection page + compliant comparison/guide content |
| 3 | Remedies & how to stop hair loss | 500,550 | hair loss treatment | 2 | 22,810 | Hair Revival System | 18 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 4 | Topical oils & natural ingredients | 298,990 | rosemary hair oil for growth | 0 | 38,470 | Hair Revival Serum | 44 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 5 | Hair growth: general | 219,940 | hair growth | 21 | 89,860 | Hair Revival System | 209 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 6 | Protein & food for hair | 218,790 | protein rich foods for hair growth | 0 | 17,770 | Hair Revival Supplements | 5 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 7 | Biotin | 154,850 | hair growth supplements biotin | 0 | 5,220 | Hair Revival Supplements | 13 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 8 | Procedures & devices | 139,110 | red light therapy for hair loss | 3 | 26,460 | Derma roller | 14 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 9 | Conditions: alopecia, TE, PCOS, thyroid… | 214,160 | hair loss androgenetic alopecia | 0 | 75,080 | Hair Revival System | 17 | Informational, careful: one sourced hub, no product claims near disease content |
| 10 | Competitor brands (growth) | 82,510 | nutrafol hair growth supplements | 0 | 2,360 | Hair Revival System | 11 | Commercial: optimise product/collection page + compliant comparison/guide content |
| 11 | Iron, vitamin D & deficiencies | 110,030 | iron supplement hair growth | 4 | 23,490 | Hair Revival Supplements | 17 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 12 | Peptides & copper peptides | 79,380 | hair growth peptides | 1 | 29,490 | Hair Revival Serum | 2 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 13 | Causes of hair loss & thinning | 83,990 | will wearing hats cause hair loss | 10 | 53,990 | Hair Revival System | 7 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 14 | Hairline, crown & bald spots | 89,520 | hair thinning and balding | 0 | 19,240 | Hair Revival System | 10 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 15 | Life stages: postpartum, pregnancy, menopause | 56,870 | postpartum hair loss | 1 | 23,150 | Hair Revival System | 12 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 16 | Supplement myths: creatine, protein shakes | 46,110 | does creatine cause hair loss | 0 | 3,640 | Hair Revival Supplements | 3 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 17 | Speed & regrowth timelines | 52,610 | hair to regrow | 1 | 10,170 | Hair Revival System | 4 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 18 | Hair, skin & nails vitamins | 40,580 | skin hair nail vitamins | 0 | 0 | Hair Skin Gut Collagen | 0 | Commercial: optimise product/collection page + compliant comparison/guide content |
| 19 | Shedding & how much is normal | 43,560 | shedding | 0 | 10,460 | Hair Revival System | 7 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 20 | Men's thinning & hair loss | 43,870 | regrow hair for men | 0 | 10,390 | Hair Revival System | 0 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 21 | Collagen | 40,530 | karseell collagen hair mask | 0 | 9,480 | Hair Skin Gut Collagen | 1 | Commercial: optimise product/collection page + compliant comparison/guide content |
| 22 | Saw palmetto & DHT blockers | 40,140 | saw palmetto extract hair loss | 3 | 5,690 | Hair Revival Supplements | 6 | Strengthen: existing pages already rank top 10; refresh and interlink |
| 23 | Women's thinning & hair loss | 39,200 | hair is thinning women | 0 | 2,110 | Hair Revival System | 1 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 24 | Signs & symptoms of thinning | 19,820 | is my hair thinning | 0 | 21,710 | Hair Revival System | 1 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 25 | Prenatal vitamins & hair | 16,420 | hair growth prenatal vitamins | 0 | 25,900 | Hair Revival Supplements | 1 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 26 | Hair growth cycle & biology | 14,390 | hair growth calculator | 0 | 4,640 | Hair Revival System | 8 | Build: hub page + supporting articles (reuse existing posts where they fit) |
| 27 | Drugs: minoxidil, finasteride & Rx | 1,525,580 | minoxidil | 3 | 33,750 | none | 12 | Avoid (no product fit, or drug/styling topic) |
| 28 | Styling for thinning hair | 166,800 | thinning hairline haircut | 0 | 1,040 | none | 5 | Avoid (no product fit, or drug/styling topic) |
| 29 | Off-scope: beard, brows, lashes, body, pets | 126,970 | growing a beard with minoxidil | 0 | 16,920 | none | 2 | Avoid (no product fit, or drug/styling topic) |
| 30 | Medications that cause hair loss | 52,760 | hair loss drugs | 0 | 42,710 | none | 2 | Avoid (no product fit, or drug/styling topic) |

## Priority clusters: what to do

For each priority cluster: the existing page to build around (the hub), what the results page looks like, and the next step. "Hub" means the page that should own the head term; other posts on the topic link to it or are merged into it. Suggested hubs are matched by URL to the head term, so confirm each one editorially. Where none fits, a new hub page is needed.

### Gray hair

**Gray: causes.** 47,340 searches/month (head term "what causes grey hair", 9,900). Product: Anti-Gray Supplements. Suggested hub: `/blogs/hair-care/what-causes-gray-hair`; page with most impressions today: `/blogs/hair-care/best-anti-gray-products-women-30s`. 9 live posts, 0 held. Top 10 for "what causes grey hair": 5 publishers/medical, 2 brands or clinics, 1 forums or video, 0 marketplaces; 0 product pages. Leaders: aad.org, health.harvard.edu, my.clevelandclinic.org. **Next:** Strengthen: existing pages already rank top 10; refresh and interlink.

**Gray: supplements & products.** 19,040 searches/month (head term "products for gray hair", 3,600). Product: Anti-Gray System. Suggested hub: `/blogs/hair-care/best-anti-gray-products-women-20s`; page with most impressions today: `/blogs/hair-care/best-hair-growth-serum-for-gray-hair`. 15 live posts, 0 held. Top 10 for "products for gray hair": 1 publishers/medical, 5 brands or clinics, 2 forums or video, 0 marketplaces; 1 product pages. Leaders: paigeditullio.com, arey.com, glamour.com. **Next:** Commercial: optimise product/collection page + compliant comparison/guide content.

**Gray: reversal, slowing & stopping.** 26,770 searches/month (head term "how to prevent gray hair", 3,600). Product: Anti-Gray System. Suggested hub: `/blogs/hair-care/foods-to-prevent-gray-hair`; page with most impressions today: `/blogs/hair-vitamins/glutathione`. 6 live posts, 2 held. Top 10 for "how to prevent gray hair": 5 publishers/medical, 2 brands or clinics, 1 forums or video, 0 marketplaces; 0 product pages. Leaders: aad.org, pmc.ncbi.nlm.nih.gov, reddit.com. **Next:** Strengthen: existing pages already rank top 10; refresh and interlink.

**Gray: competitor brands.** 7,710 searches/month (head term "arey grey", 2,900). Product: Anti-Gray System. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `/blogs/hair-care/fullyvital-vs-arey-anti-gray-comparison`. 7 live posts, 0 held. Top 10 for "arey grey": 1 publishers/medical, 5 brands or clinics, 1 forums or video, 0 marketplaces; 3 product pages. Leaders: credobeauty.com, thequalityedit.com, reddit.com. **Next:** Commercial: optimise product/collection page + compliant comparison/guide content.

**Gray: nutrients & deficiencies.** 11,600 searches/month (head term "vitamin b12 deficiency gray hair", 4,400). Product: Anti-Gray Supplements. Suggested hub: `/blogs/hair-care/vitamins-for-gray-hair`; page with most impressions today: `/blogs/hair-vitamins/copper`. 7 live posts, 0 held. Top 10 for "vitamin b12 deficiency gray hair": 1 publishers/medical, 5 brands or clinics, 2 forums or video, 0 marketplaces; 0 product pages. Leaders: tareendermatology.com, facebook.com, 1mg.com. **Next:** Strengthen: existing pages already rank top 10; refresh and interlink.

**Gray: men.** 14,930 searches/month (head term "greying men", 12,100). Product: Anti-Gray System. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `none`. 1 live posts, 0 held. Top 10 for "greying men": 0 publishers/medical, 3 brands or clinics, 3 forums or video, 0 marketplaces; 0 product pages. Leaders: pauledmonds.com, celebremagazine.world, reddit.com. **Next:** Build: hub page + supporting articles (reuse existing posts where they fit).

**Gray: questions, myths & meaning.** 9,830 searches/month (head term "white vs gray hair", 2,400). Product: Anti-Gray System. Suggested hub: `/blogs/hair-care/gray-hair-myths-vs-facts`; page with most impressions today: `none`. 1 live posts, 0 held. Top 10 for "what is the reason for gray hair": 2 publishers/medical, 4 brands or clinics, 2 forums or video, 0 marketplaces; 0 product pages. Leaders: neofollics.com, hairstory.com, reddit.com. **Next:** Build: hub page + supporting articles (reuse existing posts where they fit).

**Gray: by age & early graying.** 9,850 searches/month (head term "early grey hair", 1,600). Product: Anti-Gray System. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `none`. 0 live posts, 0 held. Top 10 for "what cause white hair at early age": 2 publishers/medical, 4 brands or clinics, 2 forums or video, 0 marketplaces; 0 product pages. Leaders: dermatology.ca, us.davines.com, hairlossclinic.com.au. **Next:** Build: hub page + supporting articles (reuse existing posts where they fit).

### Hair growth and hair loss

**Growth products: serums, shampoos, kits.** 322,970 searches/month (head term "hair growth serum", 74,000). Product: Hair Revival Kit / System. Suggested hub: `/blogs/hair-care/hair-growth-serum`; page with most impressions today: `/blogs/hair-care/hair-growth-products-that-work`. 58 live posts, 14 held. Top 10 for "hair serum for hair growth": 2 publishers/medical, 2 brands or clinics, 1 forums or video, 4 marketplaces; 2 product pages. Leaders: sephora.com, allure.com, reddit.com. **Next:** Commercial: optimise product/collection page + compliant comparison/guide content.

**Hair vitamins & supplements (commercial).** 347,150 searches/month (head term "hair growth supplements", 110,000). Product: Hair Revival Supplements. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `/blogs/hair-vitamins/silica`. 35 live posts, 9 held. Top 10 for "hair growth supplements": 1 publishers/medical, 5 brands or clinics, 0 forums or video, 3 marketplaces; 2 product pages. Leaders: vitaminshoppe.com, goodrx.com, sephora.com. **Next:** Commercial: optimise product/collection page + compliant comparison/guide content.

**Remedies & how to stop hair loss.** 500,550 searches/month (head term "hair loss treatment", 301,000). Product: Hair Revival System. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `/blogs/hair-care/regrow-hair-naturally-in-3-weeks`. 18 live posts, 8 held. Top 10 for "hair loss treatment": 2 publishers/medical, 6 brands or clinics, 0 forums or video, 0 marketplaces; 0 product pages. Leaders: mayoclinic.org, americanhairloss.org, vcuhealth.org. **Next:** Strengthen: existing pages already rank top 10; refresh and interlink.

**Topical oils & natural ingredients.** 298,990 searches/month (head term "rosemary hair oil for growth", 60,500). Product: Hair Revival Serum. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `/blogs/hair-vitamins/caffeine`. 44 live posts, 15 held. Top 10 for "rosemary hair oil for growth": 3 publishers/medical, 3 brands or clinics, 1 forums or video, 1 marketplaces; 1 product pages. Leaders: majesticpure.com, reddit.com, us.tangleteezer.com. **Next:** Build: hub page + supporting articles (reuse existing posts where they fit).

**Protein & food for hair.** 218,790 searches/month (head term "protein rich foods for hair growth", 60,500). Product: Hair Revival Supplements. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `/blogs/hair-care/pumpkin-seed-oil-for-hair`. 5 live posts, 1 held. Top 10 for "protein rich foods for hair growth": 4 publishers/medical, 4 brands or clinics, 1 forums or video, 0 marketplaces; 0 product pages. Leaders: health.clevelandclinic.org, healthline.com, pmc.ncbi.nlm.nih.gov. **Next:** Build: hub page + supporting articles (reuse existing posts where they fit).

**Biotin.** 154,850 searches/month (head term "hair growth supplements biotin", 22,200). Product: Hair Revival Supplements. Suggested hub: `/blogs/hair-care/how-much-biotin-for-hair-growth`; page with most impressions today: `/blogs/hair-care/how-long-does-it-take-for-biotin-to-work`. 13 live posts, 9 held. Top 10 for "hair growth supplements biotin": 3 publishers/medical, 3 brands or clinics, 0 forums or video, 1 marketplaces; 3 product pages. Leaders: pmc.ncbi.nlm.nih.gov, mayoclinic.org, amazon.com. **Next:** Build: hub page + supporting articles (reuse existing posts where they fit).

**Procedures & devices.** 139,110 searches/month (head term "red light therapy for hair loss", 18,100). Product: Derma roller. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `/blogs/hair-care/microneedling-before-and-after`. 14 live posts, 7 held. Top 10 for "red light therapy for hair loss": 2 publishers/medical, 4 brands or clinics, 1 forums or video, 1 marketplaces; 1 product pages. Leaders: med.stanford.edu, ishrs.org, amazon.com. **Next:** Strengthen: existing pages already rank top 10; refresh and interlink.

**Conditions: alopecia, TE, PCOS, thyroid….** 214,160 searches/month (head term "hair loss androgenetic alopecia", 33,100). Product: Hair Revival System. Suggested hub: `/blogs/hair-care/androgenetic-alopecia`; page with most impressions today: `/blogs/hair-care/pcos-hair-loss`. 17 live posts, 8 held. Top 10 for "hair loss androgenetic alopecia": 2 publishers/medical, 6 brands or clinics, 0 forums or video, 0 marketplaces; 0 product pages. Leaders: medlineplus.gov, pmc.ncbi.nlm.nih.gov, ishrs.org. **Next:** Informational, careful: one sourced hub, no product claims near disease content.

**Competitor brands (growth).** 82,510 searches/month (head term "nutrafol hair growth supplements", 14,800). Product: Hair Revival System. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `/blogs/hair-care/nutrafol-vs-fully-vital`. 11 live posts, 0 held. Top 10 for "nutrafol hair growth supplements": 0 publishers/medical, 5 brands or clinics, 1 forums or video, 2 marketplaces; 3 product pages. Leaders: amazon.com, nutrafol.com, nutrafol.com. **Next:** Commercial: optimise product/collection page + compliant comparison/guide content.

**Iron, vitamin D & deficiencies.** 110,030 searches/month (head term "iron supplement hair growth", 14,800). Product: Hair Revival Supplements. Suggested hub: `/blogs/hair-care/iron`; page with most impressions today: `/blogs/hair-care/zinc`. 17 live posts, 5 held. Top 10 for "iron supplement hair growth": 0 publishers/medical, 4 brands or clinics, 3 forums or video, 0 marketplaces; 0 product pages. Leaders: reddit.com, clinichunter.com, upgradedformulas.com. **Next:** Strengthen: existing pages already rank top 10; refresh and interlink.

**Peptides & copper peptides.** 79,380 searches/month (head term "hair growth peptides", 22,200). Product: Hair Revival Serum. Suggested hub: `none: a new hub page is needed`; page with most impressions today: `/blogs/hair-vitamins/copper`. 2 live posts, 1 held. Top 10 for "peptides hair growth": 2 publishers/medical, 4 brands or clinics, 1 forums or video, 1 marketplaces; 1 product pages. Leaders: pmc.ncbi.nlm.nih.gov, plasticsurgerykey.com, theordinary.com. **Next:** Strengthen: existing pages already rank top 10; refresh and interlink.

**Causes of hair loss & thinning.** 83,990 searches/month (head term "will wearing hats cause hair loss", 12,100). Product: Hair Revival System. Suggested hub: `/blogs/hair-care/does-wearing-hats-cause-hair-loss`; page with most impressions today: `/blogs/hair-care/does-wearing-hats-cause-hair-loss`. 7 live posts, 3 held. Top 10 for "will wearing hats cause hair loss": 3 publishers/medical, 2 brands or clinics, 1 forums or video, 0 marketplaces; 0 product pages. Leaders: reddit.com, health.clevelandclinic.org, onlinedoctor.lloydspharmacy.com. **Next:** Strengthen: existing pages already rank top 10; refresh and interlink.

The two "general" clusters are catch-alls for keywords that fit no specific topic. They're kept in the tables but aren't priorities on their own.

## Commercial pages

Commercial searches ("hair growth supplements", "hair serum for hair growth", "products for gray hair", "arey grey") show product pages, marketplaces and brand sites, not blog posts. These need product or collection pages, which are outside what this project may edit. Recommendations:

- **Growth products: serums, shampoos, kits** (322,970/month; product: Hair Revival Kit / System). Target terms: serum growth hair, hair serum for growth, growth hair serum, growth serum for hair.
- **Hair vitamins & supplements (commercial)** (347,150/month; product: Hair Revival Supplements). Target terms: hair growth supplements, women's hair growth supplements, supplements for hair growth for women, hair growth for women supplements.
- **Competitor brands (growth)** (82,510/month; product: Hair Revival System). Target terms: nutrafol hair growth supplements, viviscal hair growth supplements, viviscal supplements for hair growth, hair growth supplements viviscal.
- **Hair, skin & nails vitamins** (40,580/month; product: Hair Skin Gut Collagen). Target terms: nails hair and skin vitamins, nail skin hair vitamins, vitamins skin hair nails, vitamins nails hair skin.
- **Collagen** (40,530/month; product: Hair Skin Gut Collagen). Target terms: karseell collagen hair mask, collagen supplements and hair, collagen supplements for hair, collagen supplements hair.
- **Gray: supplements & products** (19,040/month; product: Anti-Gray System). Target terms: grey hair products, products for gray hair, gray hair product, gray hair products.
- **Gray: competitor brands** (7,710/month; product: Anti-Gray System). Target terms: particle anti-gray serum, particle anti gray serum, particle anti gray serum for men, arey grey hair products.

Fix the product-page "reverse gray" wording (Phase 1 list) before pointing any new content or internal links at those pages.

## Decisions: the 132 held posts

| Decision | Posts |
|---|---|
| Remove (no demand, no clear home) | 59 |
| Merge into existing page on the same subtopic | 28 |
| Rewrite as supporting article (distinct subtopic with demand) | 22 |
| Remove (off-strategy topic) | 8 |
| Merge into the rewrite of the same topic | 7 |
| Fold into the planned hub for this cluster | 5 |
| Remove (indirect brand comparison, no demand) | 3 |

Rewrites (one per topic):

| Post | Cluster | Demand for the topic |
|---|---|---|
| /blogs/hair-care/hair-thinning | Remedies & how to stop hair loss | 165,000 |
| /blogs/hair-care/best-hair-growth-serums | Growth products: serums, shampoos, kits | 74,000 |
| /blogs/hair-vitamins/protein | Protein & food for hair | 60,500 |
| /blogs/hair-care/rosemary-oil-for-hair-growth | Topical oils & natural ingredients | 60,500 |
| /blogs/hair-care/hair-loss-vitamins | Hair vitamins & supplements (commercial) | 14,800 |
| /blogs/hair-vitamins/vitamin-d | Iron, vitamin D & deficiencies | 12,100 |
| /blogs/hair-vitamins/coconut-oil | Topical oils & natural ingredients | 9,900 |
| /blogs/hair-care/derma-roller-for-hair | Procedures & devices | 9,900 |
| /blogs/hair-vitamins/collagen | Collagen | 8,100 |
| /blogs/hair-care/how-much-hair-loss-is-normal | Shedding & how much is normal | 5,400 |
| /blogs/hair-care/stem-cell-therapy | Procedures & devices | 4,400 |
| /blogs/hair-care/which-vitamin-deficiency-causes-hair-loss | Iron, vitamin D & deficiencies | 4,400 |
| /blogs/hair-care/hair-cycle | Hair growth cycle & biology | 2,900 |
| /blogs/hair-care/the-best-hair-growth-serum | Growth products: serums, shampoos, kits | 1,900 |
| /blogs/hair-care/can-hair-loss-be-reversed | Hair growth: general | 1,900 |
| /blogs/hair-care/dermatologist | Hair growth: general | 1,600 |
| /blogs/hair-vitamins/tea-tree-oil | Topical oils & natural ingredients | 1,600 |
| /blogs/hair-vitamins/argan-oil | Topical oils & natural ingredients | 1,600 |
| /blogs/hair-care/thyroid-hair-loss | Conditions: alopecia, TE, PCOS, thyroid… | 1,300 |
| /blogs/hair-care/folate | Iron, vitamin D & deficiencies | 1,300 |
| /blogs/hair-care/keratin | Hair growth: general | 1,000 |
| /blogs/hair-care/biotin-vs-collagen | Biotin | 1,000 |

Full list with merge targets: `data/processed/phase2_held_decisions.csv`.

## Decisions: the 69 brand comparison posts

| Keep and refresh | Brand | Brand search volume (in-scope) | Clicks 16m |
|---|---|---|---|
| /blogs/hair-care/viviscal-vs-fully-vital | Viviscal | 41,200 | 2 |
| /blogs/hair-care/pura-dor-vs-fully-vital | Pura d'or | 29,970 | 2 |
| /blogs/hair-care/nutrafol-vs-fully-vital | Nutrafol | 28,890 | 82 |
| /blogs/hair-care/vegamour-vs-fully-vital | Vegamour | 28,870 | 13 |
| /blogs/hair-care/fullyvital-vs-particle-anti-gray-comparison | Particle | 5,120 | 1 |
| /blogs/hair-care/fullyvital-vs-arey-anti-gray-comparison | Arey | 4,370 | 17 |

Kept comparisons must be honest and sourced: no claims about a competitor's product that you can't support, no "reverse gray" wording (three current comparison posts say FullyVital products "delay and reverse gray hairs"). The other 61 have no meaningful brand demand; remove them and fold anything useful into one "FullyVital alternatives" guide. Full list: `data/processed/phase2_comparison_decisions.csv`.

## Index status of published articles

| Google's status | Articles |
|---|---|
| Submitted and indexed | 480 |
| Crawled - currently not indexed | 61 |
| URL is unknown to Google | 44 |
| Not found (404) | 2 |
| Discovered - currently not indexed | 2 |

| Published | Articles not indexed |
|---|---|
| 2021 | 3 |
| 2022 | 6 |
| 2023 | 69 |
| 2024 | 19 |
| 2026 | 10 |
| ? | 2 |

- **Google is skipping the weakest posts.** 90 of the 132 held posts aren't indexed, and only 7% of articles with no impressions in 90 days are. Every refreshed, merge-target and kept article that earns traffic is indexed.
- **Crawling is slow.** 44 published articles have never been seen by Google, and two posts published in July were last crawled before they went live. Removing low-value posts should help Google spend its crawl on the pages that matter.
- **No technical blockers:** robots.txt allows every crawled page, and Google chose a different canonical for 0 articles.
- **New posts are still being published outside this work:** `/blogs/hair-care/is-fullyvital-hair-growth-proven`, `/blogs/hair-care/scandinavian-biolabs-vs-fullyvital` went live after the clean-up sheet was made. One is a new brand comparison. Agree on who publishes what, so new posts follow the plan and the claims rules.

Full data: `data/processed/index_status_all.csv`.

## Proposed sequence (hypotheses, for you to approve)

1. **Weeks 1–4: finish consolidating.** The other session completes the 111 refreshes. In parallel, apply the held and comparison decisions as one clean-up batch, using the same safeguards as the first one (backlink check, redirects for merges, logged and reversible). You fix the product-page claims.
2. **Weeks 3–8: build the gray-hair hubs.** Gray is the core product line and has little competition from brands. Start with the causes cluster (hub plus spokes on early graying, stress, B12 and copper, and myths). Reuse the 2026 gray posts already written as spokes and interlink them.
3. **Weeks 5–10: strengthen the hair-growth clusters where FullyVital already has pages:** remedies and how to stop hair loss, topical oils (rosemary), vitamins and supplements, and protein and food. Pick one hub per cluster from the existing posts and merge the duplicates into it.
4. **About 6–8 weeks after each refresh batch: read the refresh test** (`refresh_tracker.py`). If refreshed pages gain impressions against the controls, keep refreshing and consolidating before writing new posts. If they don't, shift effort to fewer, deeper hub pages and to the commercial pages.
5. **Not before then: new articles for clusters with no page at all.** Adding volume to a site Google may already rate as low-quality risks repeating the problem.

## Compliance notes

- **Avoid entirely:** prescription drugs and medications that cause hair loss. Gray coverage, dye and styling clusters have no product fit, so skip them unless you want top-of-funnel traffic.
- **Conditions** (alopecia, telogen effluvium, PCOS, thyroid): at most one sourced informational hub, with no product claims near disease content.
- **"Hair loss treatment" and similar searches** (the remedies cluster) are worth targeting with how-to and support content. FullyVital pages must not present a supplement or serum as a treatment for hair loss; describe what ingredients support, and point to a doctor for diagnosis.
- **"Reverse", "stop" and "prevent" gray-hair searches** are high-intent but sensitive. Answer them honestly ("no study has shown…") and never promise reversal.
- **New articles** follow the citation style in CLAUDE.md (3 studies, each linked once, all in the second half).

## Caveats

- **Volumes** are DataForSEO estimates, and the de-duplication is a heuristic. Use them to rank, not forecast.
- **Clusters** come from keyword rules. A few keywords will be misfiled; the CSV has every keyword with its cluster.
- **Winnability** relies on domain rank, not page-level link data. DataForSEO keyword difficulty is unreliable (Phase 1) and isn't used.
- **Held-post decisions** are rule-based drafts, like the first clean-up sheet. Review them before anything is applied.
- **DataForSEO spend:** Phase 2 cost $0.91. The balance is about $48.
