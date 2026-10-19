# Refresh batch 7: 10 drafts for review

Nothing is published. Open each `preview.html`; `review.md` lists what changed, the 3 sources and anything for you to decide. Every draft follows the citation style rule: 3 studies, each linked once, all links in the second half.

| Article | Type | New title | Words | Study links | Preview | Review |
|---|---|---|---|---|---|---|
| /blogs/hair-care/hair-crimping | refresh | Hair Crimping: Heat Damage & What the Research Shows | 2,031 → 822 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__hair-crimping/preview.html) | [review](../data/refresh_drafts/hair-care__hair-crimping/review.md) |
| /blogs/hair-care/what-causes-greasy-hair | refresh | What Causes Greasy Hair? What the Research Shows | 2,221 → 922 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__what-causes-greasy-hair/preview.html) | [review](../data/refresh_drafts/hair-care__what-causes-greasy-hair/review.md) |
| /blogs/hair-care/pineapple | refresh | Pineapple for Hair: What the Research Shows | 2,876 → 793 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__pineapple/preview.html) | [review](../data/refresh_drafts/hair-care__pineapple/review.md) |
| /blogs/hair-care/prostaglandin-analog | refresh | Prostaglandin Analogs for Hair: What the Research Shows | 2,103 → 784 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__prostaglandin-analog/preview.html) | [review](../data/refresh_drafts/hair-care__prostaglandin-analog/review.md) |
| /blogs/hair-vitamins/rhodiola-extract | refresh | Rhodiola for Hair: Stress, Evidence & What to Know | 1,827 → 835 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__rhodiola-extract/preview.html) | [review](../data/refresh_drafts/hair-vitamins__rhodiola-extract/review.md) |
| /blogs/hair-vitamins/kelp | refresh | Kelp for Hair: Iodine, the Thyroid & What the Research Shows | 1,923 → 793 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__kelp/preview.html) | [review](../data/refresh_drafts/hair-vitamins__kelp/review.md) |
| /blogs/hair-vitamins/phytoceramides | refresh | Phytoceramides for Hair: What They Are and What the Research Shows | 1,936 → 694 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__phytoceramides/preview.html) | [review](../data/refresh_drafts/hair-vitamins__phytoceramides/review.md) |
| /blogs/hair-vitamins/whey-protein | refresh | Whey Protein for Hair Growth: What the Research Shows | 2,255 → 807 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__whey-protein/preview.html) | [review](../data/refresh_drafts/hair-vitamins__whey-protein/review.md) |
| /blogs/hair-care/oily-hair-shampoo | refresh | Shampoo for Oily Hair: What the Research Shows About Ingredients | 2,045 → 787 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__oily-hair-shampoo/preview.html) | [review](../data/refresh_drafts/hair-care__oily-hair-shampoo/review.md) |
| /blogs/hair-vitamins/astaxanthin | refresh | Astaxanthin for Hair: What the Research Shows | 1,842 → 806 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__astaxanthin/preview.html) | [review](../data/refresh_drafts/hair-vitamins__astaxanthin/review.md) |

## Builder note

`refresh_build.py` now also treats a plain, unlinked image paragraph as an image block when a post has no centred images (needed for `hair-crimping`). Rebuilding an already-published article produced an identical draft.

## Checks run

- **AI-chat links / pasted-chat markup in live bodies:** none in the 10 posts.
- **Citation style:** every draft has exactly 3 distinct PubMed studies, each linked once, first link at 59–64% of the text.
- **Claims scan:** no cure/prevent/reverse/heal language beyond neutral phrasing.
- **Builder checks:** PMIDs verified; blocks match the live posts (including the unclassed blocks in `oily-hair-shampoo`); no stray `**`; no reviewer line.

## Flags that need your decision

- **Medicine topic:** `prostaglandin-analog` is now a neutral, doctor-referral article on drugs such as bimatoprost (a 2023 meta-analysis of six placebo-controlled trials; PGD2 works the other way; a safety review). If any FullyVital product contains a prostaglandin analog, check the page against it.
- **Strongest evidence:** `prostaglandin-analog` (meta-analysis of randomized trials), `oily-hair-shampoo` (shampoo/scalp microbiome study, one extract trial).
- **No hair evidence (honest, shorter):** `pineapple`, `rhodiola-extract`, `kelp` (leads with excess-iodine risk and links to the iodine article), `whey-protein` (safety-focused), `astaxanthin` (skin and safety), `phytoceramides` (skin trial + cell and breakage studies), `what-causes-greasy-hair` (answers 'is it a vitamin deficiency': no evidence), `hair-crimping` (heat-damage research; styling topic). You may prefer to hold or merge some.
- **Title-only citation:** the astaxanthin hair-dye allergy paper has no PubMed abstract.
- **Disease/medical mentions (neutral):** thyroid dysfunction (kelp), acne and kidney/liver effects (whey), botulinum toxin injection for oily scalp (greasy hair), androgenetic alopecia (PGA).

## Not yet done

Nothing is published. On approval: fresh backup, rebuild, dry run, publish one, check it live, then the rest.
