# Refresh batch 5: 8 drafts for review (plus 2 held)

Nothing is published. Open each `preview.html`; `review.md` lists what changed, the 3 sources and anything for you to decide. Every draft follows the citation style rule: 3 studies, each linked once, all links in the second half.

| Article | Type | New title | Words | Study links | Preview | Review |
|---|---|---|---|---|---|---|
| /blogs/hair-vitamins/wheat-germ-oil | refresh | Wheat Germ Oil for Hair: What the Research Shows | 2,049 → 696 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__wheat-germ-oil/preview.html) | [review](../data/refresh_drafts/hair-vitamins__wheat-germ-oil/review.md) |
| /blogs/hair-vitamins/l-arginine | refresh | L-Arginine for Hair: What the Research Shows | 2,064 → 932 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__l-arginine/preview.html) | [review](../data/refresh_drafts/hair-vitamins__l-arginine/review.md) |
| /blogs/hair-care/caprylhydroxamic-acid | refresh | Caprylhydroxamic Acid in Hair and Skin Products: What It Is and Safety | 2,456 → 750 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__caprylhydroxamic-acid/preview.html) | [review](../data/refresh_drafts/hair-care__caprylhydroxamic-acid/review.md) |
| /blogs/hair-care/normal-hair-part-vs-thinning | merge target | Normal Hair Part vs Thinning: How to Tell the Difference | 1,629 → 645 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__normal-hair-part-vs-thinning/preview.html) | [review](../data/refresh_drafts/hair-care__normal-hair-part-vs-thinning/review.md) |
| /blogs/hair-vitamins/l-methionine | merge target | Methionine for Hair: What the Research Shows | 1,993 → 830 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__l-methionine/preview.html) | [review](../data/refresh_drafts/hair-vitamins__l-methionine/review.md) |
| /blogs/hair-vitamins/dmae | refresh | DMAE for Hair: What the Research Shows | 2,036 → 729 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__dmae/preview.html) | [review](../data/refresh_drafts/hair-vitamins__dmae/review.md) |
| /blogs/hair-vitamins/niacin | merge target | Niacin for Hair: What the Research Shows | 2,638 → 857 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__niacin/preview.html) | [review](../data/refresh_drafts/hair-vitamins__niacin/review.md) |
| /blogs/hair-care/nettle-leaf | merge target | Stinging Nettle for Hair: What the Research Shows | 2,665 → 826 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__nettle-leaf/preview.html) | [review](../data/refresh_drafts/hair-care__nettle-leaf/review.md) |

## Held back (2): `brush-scalp-for-hair-growth` and `how-to-use-derma-roller-for-hair`

Same issue as `clogged-hair-follicles` in batch 3: these short posts have no testimonial, product widget or closing table at all, and their only images are product-linked images (a hair-brush image and a serum-pack image, each wrapped in a product link). The builder can't place them, and the rule is not to paste product HTML by hand. Options: (1) extend `refresh_build.py` to copy those linked images by position, then draft the three held posts; (2) draft them without the images, which drops FullyVital product links from the page; (3) leave all three live posts as they are. Decision needed.

## Checks run

- **AI-chat links / pasted-chat markup in live bodies:** none in the 10 batch posts or the 6 redirected sources (`does-brushing-hair-cause-hair-loss`, `normal-hair-vs-thinning-hair`, `methionine`, `niacin` x2, `nettle-extract`, `how-to-use-a-derma-roller`).
- **Citation style:** every draft has exactly 3 distinct PubMed studies, each linked once, first link at 60–64% of the text.
- **Claims scan:** no cure/prevent/reverse language. Hits are neutral phrasing.
- **Builder checks:** PMIDs verified; blocks match the live articles (the normal-part post has no closing table or images, so none were added); no stray `**`; no reviewer line.

## Flags that need your decision

- **Most interesting finding:** `l-arginine` (a 2025 study: low serum arginine in people with androgenetic alopecia, arginine rescued hair growth in mice and cultured human follicles). It is lab/animal work; the article says no trial shows oral arginine works.
- **Mixed:** `niacin` (a topical niacin-derivative pilot was positive; topical niacinamide was not supported), `l-methionine` (mouse study + a multi-ingredient trial taken with drug treatment).
- **No hair evidence (honest, shorter):** `wheat-germ-oil`, `caprylhydroxamic-acid` (a safety/allergy explainer), `dmae` (skin-wrinkle research; note the EU 'unauthorized ingredient' line), `nettle-leaf` (review + one cell study). You may prefer to hold or merge some.
- **Compliance flags:** `caprylhydroxamic-acid` discusses a contact-allergy outbreak; if any FullyVital product uses it, check you're comfortable with the page. `dmae` says DMAE is listed as an unauthorized supplement ingredient by the European Commission; check against your products and markets.
- **Title-only citation:** the caprylhydroxamic acid 2025 allergen paper has no PubMed abstract.
- **Closing product box** still says products "Promote Hair Regrowth". Unchanged and flagged on every draft.

## Not yet done

Nothing is published. On approval: fresh backup, rebuild, dry run, publish one, check it live, then the rest.
