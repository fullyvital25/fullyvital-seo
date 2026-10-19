# Enhance Hair rename: report (2026-10-18)

## What changed
- **172 live blog articles** were updated (body only; one summary/SEO field was not needed). Old product names were replaced with the current ones:
  - Enhance Hair (Density/Growth) Serum, Enhance Hair Serum -> **Hair Revival Serum**
  - Enhance Hair Vitamins / Supplement(s) / Growth Supplement(s) -> **Hair Revival Supplements**
  - Mixed-case versions inside image alt/title attributes and product-link text were renamed too.
- Per your decisions: "Enhance Hair Serum (3-Pack)" links now read **Hair Revival Serum (3-Pack)**, and the supplement 3-pack link text now reads **Hair Revival Supplements**.
- Every article was re-read from Shopify right before it was written, so nothing edited elsewhere was overwritten.
- Backup taken just before the first write: `data/shopify_backup/articles_2026-10-18_164155.json`. Every write is logged in `data/shopify_changes/2026-10-18.jsonl`.

## Checks
- A 1-article live test ran first and passed, then the other 171 were applied.
- All 173 changed articles were compared with the backup (names swapped for a placeholder): only product names changed. Links, prices and FAQ JSON-LD are unchanged and all JSON-LD parses.
- **One flag, a false alarm:** `female-pattern-baldness` tripped the check only because my checker also masked the untouched sentence "Enhance hair growth vitamins can help..." on the before side. A line-by-line diff shows the only edits are the two widget names.
- No refresh-test page was edited.

## Deferred: refresh-test pages
52 old-name mentions on 18 test pages (treated and control) were left alone until the December readout: best-shampoo-and-conditioner-for-hair-growth, beta-carotene, club-hair, does-saw-palmetto-fight-hair-thinning, does-wearing-hats-cause-hair-loss, ethoxydiglycol, ginseng, glucosamine, how-much-biotin-for-hair-growth, humectant, keravis-protein, natural-hair-growth-products, pcos-hair-loss, pituitary-gland, resveratrol, telogen-effluvium, understanding-crown-balding-causes-treatments-and-solutions, white-tea-extract.

## "Enhance Hair Serum 3-Pack" left as is
6 plain-text mentions on 4 pages (not renamed, as instructed): almond-oil, argan-oil, ashwagandha, black-seed-oil. This product (`/products/enhance-hair-serum-3-pack`) is not in the product sheet. I did not query its current title; say if you want that read.

## Prices (not touched)
Widget prices, with the number of live non-test pages each appears on: $269.00: 148, $44.25: 118, $47.20: 148. Other dollar figures are ordinary body text, on 1 to 9 pages each: $1 (1), $10 (1), $105 (2), $120 (1), $138 (1), $150 (3), $2 (1), $200 (9), $2000 (1), $21 (1), $240 (1), $250 (2), $269 (2), $3 (1), $480 (1), $50 (1), $55 (3), $59 (2), $79 (1), $86 (1), $97 (1). Please check the three widget prices ($47.20, $44.25, $269.00) are current.

## Ambiguous cases left unchanged
- `female-pattern-baldness`: sentence starts "Enhance hair growth vitamins can help provide the nutrition..." (body text).
- `inulin`: image alt text "Fully vital enhance hair" (no product word after it).
- `dandruff-cause-hair-thinning`, `hair-texture-chart`: link titles/anchors "enhance hair growth (products)" that point at product pages but read as ordinary phrases.
- 33 other uses are ordinary English ("enhance hair health", "Enhance Hair Strength:" list headings and similar), for example in glycerin, formaldehyde, saw-palmetto, melatonin, l-glutamine, prebiotics, ceramides.

## Failures
None. Nothing needed the stop-and-ask rules after your two decisions.
