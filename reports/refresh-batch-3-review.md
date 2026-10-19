# Refresh batch 3: 9 drafts for review (plus 1 held: clogged-hair-follicles)

Nothing is published. Open each `preview.html`; `review.md` lists what changed, the 3 sources and anything for you to decide. Every draft follows the citation style rule: 3 studies, each linked once, all links in the second half.

| Article | Type | New title | Words | Study links | Preview | Review |
|---|---|---|---|---|---|---|
| /blogs/hair-vitamins/lutein | refresh | Lutein for Hair: What the Research Shows | 1,833 → 790 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__lutein/preview.html) | [review](../data/refresh_drafts/hair-vitamins__lutein/review.md) |
| /blogs/hair-vitamins/goji-berry-extract | refresh | Goji Berry Extract for Hair: What the Research Shows | 1,915 → 883 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__goji-berry-extract/preview.html) | [review](../data/refresh_drafts/hair-vitamins__goji-berry-extract/review.md) |
| /blogs/hair-vitamins/paba | refresh | PABA for Hair: Gray Hair Claims & What the Research Shows | 1,950 → 754 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__paba/preview.html) | [review](../data/refresh_drafts/hair-vitamins__paba/review.md) |
| /blogs/hair-vitamins/uva-ursi-extract | refresh | Uva Ursi Extract: Skin, Scalp & What the Research Shows | 1,984 → 793 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__uva-ursi-extract/preview.html) | [review](../data/refresh_drafts/hair-vitamins__uva-ursi-extract/review.md) |
| /blogs/hair-vitamins/soy-isoflavones | merge target | Soy Isoflavones for Hair: What the Research Shows | 1,783 → 770 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__soy-isoflavones/preview.html) | [review](../data/refresh_drafts/hair-vitamins__soy-isoflavones/review.md) |
| /blogs/hair-vitamins/squalane | refresh | Squalane for Hair: What It Is and What the Research Shows | 1,808 → 796 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__squalane/preview.html) | [review](../data/refresh_drafts/hair-vitamins__squalane/review.md) |
| /blogs/hair-vitamins/nickel | refresh | Nickel and Hair: Allergy, Diet & Hair Analysis | 1,729 → 704 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__nickel/preview.html) | [review](../data/refresh_drafts/hair-vitamins__nickel/review.md) |
| /blogs/hair-vitamins/milk-thistle | refresh | Milk Thistle for Hair: What the Research Shows | 1,970 → 823 | 0 → 3 | [preview](../data/refresh_drafts/hair-vitamins__milk-thistle/preview.html) | [review](../data/refresh_drafts/hair-vitamins__milk-thistle/review.md) |
| /blogs/hair-care/understanding-hair-whorl-a-key-to-hair-growth | refresh | Hair Whorl: What It Is and What Research Shows | 1,760 → 768 | 0 → 3 | [preview](../data/refresh_drafts/hair-care__understanding-hair-whorl-a-key-to-hair-growth/preview.html) | [review](../data/refresh_drafts/hair-care__understanding-hair-whorl-a-key-to-hair-growth/review.md) |

## Held back: `/blogs/hair-care/clogged-hair-follicles` (merge target)

This post has a hand-edited layout the builder can't fill: its testimonial, "Our Best Sellers" block and closing table aren't in the standard `fv-blog-proof` / `fv-blog-product-wrap` markup, and it has 11 images. The rule is never to paste widget HTML by hand, so I did not draft it. Options: (1) I extend `refresh_build.py` to copy those blocks by position, then draft it; (2) skip it and leave the live post as is. Its two redirected sources (`follicle`, `hair-follicles`) are unsourced anatomy posts with no AI-chat markup.

## Checks run

- **AI-chat links / pasted-chat markup in live bodies:** none in any of the 10 batch posts or the 3 redirected sources (`follicle`, `hair-follicles`, `soy-protein`). The live clogged-hair-follicles post cites Healthline, CDC and familydoctor.org in a plain reference list (no AI links).
- **Citation style:** every draft has exactly 3 distinct PubMed studies, each linked once, first link at 58–66% of the text.
- **Claims scan:** no cure/prevent/reverse/heal/guarantee language. Hits are neutral phrasing ("treat X as unproven", "not a test of squalane as a treatment").
- **Builder checks:** PMIDs verified; product, testimonial and footer blocks match the live articles; no stray `**`; no reviewer line.

## Flags that need your decision

- **Compliance, PABA:** a gray-hair article. It reports only a 1950 report (title only, no abstract) and a 1992 review saying the effect awaits confirmation, and says plainly nothing shows PABA can restore hair color. It also names the prescription drug Potaba and its liver-injury reports.
- **No hair evidence at all (honest, shorter articles):** `lutein`, `squalane`, `nickel` (reframed as allergy/diet/hair test), `uva-ursi-extract`, `hair-whorl`. You may prefer to hold or merge some.
- **Thin or mixed:** `goji-berry-extract` (one mouse study of a bergamot + boxthorn mix; boxthorn was treated as goji), `soy-isoflavones` (a multi-ingredient pilot with no control group, a mouse study, a broad review).
- **Best evidence this batch:** `milk-thistle` (a clinical shampoo study of flower extract plus lab work; not the same as silymarin capsules, and the article says so).
- **Hair whorl:** the cited review says abnormal or absent whorls have been associated with abnormal brain development. The article reports it neutrally; check you're comfortable with that line.
- **Disease research mentioned neutrally:** androgenetic alopecia and alopecia areata (soy), acne (uva ursi), Peyronie's disease (PABA).
- **Truncated abstracts:** the uva ursi safety review and the acne study abstracts are cut off on PubMed; the article states only what is visible.
- **Closing product box** still says products "Promote Hair Regrowth". Unchanged and flagged on every draft.

## Not yet done

Nothing is published. On approval: fresh backup, rebuild, dry run, publish one, check it live, then the rest.
