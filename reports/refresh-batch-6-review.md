# Refresh batch 6: 10 drafts for review, plus 3 held posts now built

Nothing is published. Open each `preview.html`; `review.md` lists what changed, the 3 sources and anything for you to decide. Every draft follows the citation style rule: 3 studies, each linked once, all links in the second half.

| Article | Type | New title | Words | Study links | Preview | Review |
|---|---|---|---|---|---|---|
| /blogs/hair-vitamins/pantothenic-acid | merge target | Pantothenic Acid (Vitamin B5) for Hair: What the Research Shows | 1,810 → 821 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__pantothenic-acid/preview.html) | [review](../data/refresh_drafts/hair-vitamins__pantothenic-acid/review.md) |
| /blogs/hair-care/pumpkin-seed-oil-for-hair | merge target | Pumpkin Seed Oil for Hair: What the Research Shows | 2,159 → 924 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__pumpkin-seed-oil-for-hair/preview.html) | [review](../data/refresh_drafts/hair-care__pumpkin-seed-oil-for-hair/review.md) |
| /blogs/hair-care/hair-growth-products-that-work | merge target | Hair Growth Products: What the Research Supports | 2,322 → 852 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__hair-growth-products-that-work/preview.html) | [review](../data/refresh_drafts/hair-care__hair-growth-products-that-work/review.md) |
| /blogs/hair-care/vitamin-a | merge target | Vitamin A and Hair: Too Little, Too Much & What the Research Shows | 2,625 → 797 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__vitamin-a/preview.html) | [review](../data/refresh_drafts/hair-care__vitamin-a/review.md) |
| /blogs/hair-care/batana-oil-for-hair-growth | merge target | Batana Oil for Hair: What the Research Shows | 1,913 → 615 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__batana-oil-for-hair-growth/preview.html) | [review](../data/refresh_drafts/hair-care__batana-oil-for-hair-growth/review.md) |
| /blogs/hair-vitamins/vitamin-f-linoleic-acid | refresh | Vitamin F (Linoleic Acid) for Hair: What the Research Shows | 2,258 → 827 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__vitamin-f-linoleic-acid/preview.html) | [review](../data/refresh_drafts/hair-vitamins__vitamin-f-linoleic-acid/review.md) |
| /blogs/hair-care/best-hair-growth-serum-for-gray-hair | refresh | Serums for Gray Hair: What the Research Says About Care, Color & Sun | 2,380 → 837 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__best-hair-growth-serum-for-gray-hair/preview.html) | [review](../data/refresh_drafts/hair-care__best-hair-growth-serum-for-gray-hair/review.md) |
| /blogs/hair-care/centella-asiatica-extract | refresh | Centella Asiatica (Gotu Kola) for Hair: What the Research Shows | 2,253 → 636 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__centella-asiatica-extract/preview.html) | [review](../data/refresh_drafts/hair-care__centella-asiatica-extract/review.md) |
| /blogs/hair-care/pygeum-bark | refresh | Pygeum Bark for Hair: What the Research Shows | 1,913 → 763 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__pygeum-bark/preview.html) | [review](../data/refresh_drafts/hair-care__pygeum-bark/review.md) |
| /blogs/hair-vitamins/taurine | refresh | Taurine and Hair: Does It Cause Hair Loss? What the Research Shows | 2,029 → 821 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__taurine/preview.html) | [review](../data/refresh_drafts/hair-vitamins__taurine/review.md) |

### Held posts from batches 3 and 5, now drafted with the extended builder

| Article | Type | New title | Words | Study links | Preview | Review |
|---|---|---|---|---|---|---|
| /blogs/hair-care/clogged-hair-follicles | merge target | Clogged Hair Follicles: What the Research Really Says About Your Scalp | 2,609 → 930 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__clogged-hair-follicles/preview.html) | [review](../data/refresh_drafts/hair-care__clogged-hair-follicles/review.md) |
| /blogs/hair-care/brush-scalp-for-hair-growth | merge target | Does Brushing Your Scalp Make Hair Grow? What the Research Shows | 632 → 696 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__brush-scalp-for-hair-growth/preview.html) | [review](../data/refresh_drafts/hair-care__brush-scalp-for-hair-growth/review.md) |
| /blogs/hair-care/how-to-use-derma-roller-for-hair | merge target | How to Use a Derma Roller for Hair: What the Research Says About Technique & Safety | 578 → 606 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__how-to-use-derma-roller-for-hair/preview.html) | [review](../data/refresh_drafts/hair-care__how-to-use-derma-roller-for-hair/review.md) |

## Builder extension

`refresh_build.py` now also copies, by position and unchanged: product-linked image paragraphs (`{{LINKIMG_n}}`), short product-recommendation lines (`{{CTA_n}}`), and falls back to unclassed testimonial and 'Our Best Sellers' blocks and plain centred images. Rebuilding an already-published article produced an identical draft, so existing drafts are unaffected. Block-parity check: every product/image/table block in the three held posts appears verbatim in their drafts.

## Checks run

- **AI-chat links / pasted-chat markup in live bodies:** none in the 13 posts or their redirected sources.
- **Citation style:** every draft has exactly 3 distinct PubMed studies, each linked once, first link at 61–65% of the text.
- **Claims scan:** no cure/prevent/reverse/heal language. Hits are neutral ("treat as unproven", lab findings, "can a serum reverse gray hair? No").
- **Builder checks:** PMIDs verified; blocks match the live posts; no stray `**`; no reviewer line.

## Flags that need your decision

- **Gray hair (compliance):** `best-hair-growth-serum-for-gray-hair` states that no serum has been shown to restore color and that greying becomes largely irreversible (the review's wording). Check it against how your product pages describe gray-hair benefits. The title no longer says 'Best Hair Growth Serum'.
- **Ranking page rewrite:** `hair-growth-products-that-work` was a product roundup (including competitor brands). It is now a category-level evidence overview with no products ranked or named; it reports minoxidil trial results from abstracts. No FullyVital product is compared to a drug. Search rankings for 'hair growth products that work' may change.
- **Strongest hair evidence:** `pumpkin-seed-oil` (placebo-controlled trial in men: +40% vs +10% hair count), `hair-growth-products-that-work` (minoxidil, supplements), `pygeum-bark` (a multi-ingredient placebo-controlled trial; pygeum alone untested).
- **No hair evidence (honest, shorter):** `batana-oil` (no study exists; the article reports other oils), `taurine` (no link to hair loss found), `vitamin-a` (leads with the too-much-is-harmful point), `centella` (one cell study), `vitamin-f-linoleic-acid` (cell studies only), `pantothenic-acid` (animal cells + an uncontrolled combination study).
- **Overlap:** `how-to-use-derma-roller-for-hair` overlaps with the already-published `ultimate-guide-to-derma-roller`. You may want to consolidate (redirect one) later.
- **Brush post:** it now contradicts the old advice to 'brush 200 times'; the combing-strokes study points the other way. Two product lines and two product images from the old post are kept unchanged.
- **Disease research mentioned neutrally:** BPH (pygeum), androgenetic alopecia and telogen effluvium (several), seborrheic dermatitis (clogged follicles).

## Not yet done

Nothing is published. On approval: fresh backup, rebuild, dry run, publish one, check it live, then the rest.
