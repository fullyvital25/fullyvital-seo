# Refresh batch 1: 10 drafts for review

Nothing is published. Open each `preview.html` in a browser; `review.md` lists what changed, every source and anything for you to decide.

| Article | Type | New title | Words | Study links | Preview | Review |
|---|---|---|---|---|---|---|
| /blogs/hair-vitamins/chromium | refresh | Chromium for Hair: Blood Sugar, Insulin & What the Research Shows | 2,010 → 1,061 | 0 → 8 | [preview](../data/refresh_drafts/hair-vitamins__chromium/preview.html) | [review](../data/refresh_drafts/hair-vitamins__chromium/review.md) |
| /blogs/hair-care/hairline-receding-on-one-side | merge target | Hairline Receding on One Side: Causes, Warning Signs & When to See a Doctor | 2,381 → 1,224 | 0 → 8 | [preview](../data/refresh_drafts/hair-care__hairline-receding-on-one-side/preview.html) | [review](../data/refresh_drafts/hair-care__hairline-receding-on-one-side/review.md) |
| /blogs/hair-vitamins/rutin | refresh | Rutin for Hair: What the Research Shows | 1,784 → 1,058 | 0 → 7 | [preview](../data/refresh_drafts/hair-vitamins__rutin/preview.html) | [review](../data/refresh_drafts/hair-vitamins__rutin/review.md) |
| /blogs/hair-vitamins/molybdenum | refresh | Molybdenum for Hair: What It Does, How Much You Need & Safety | 2,082 → 1,132 | 0 → 5 | [preview](../data/refresh_drafts/hair-vitamins__molybdenum/preview.html) | [review](../data/refresh_drafts/hair-vitamins__molybdenum/review.md) |
| /blogs/hair-care/biotin-vs-prenatal-vitamins-for-hair-growth | merge target | Biotin vs Prenatal Vitamins for Hair Growth: What the Evidence Shows | 2,547 → 1,521 | 0 → 11 | [preview](../data/refresh_drafts/hair-care__biotin-vs-prenatal-vitamins-for-hair-growth/preview.html) | [review](../data/refresh_drafts/hair-care__biotin-vs-prenatal-vitamins-for-hair-growth/review.md) |
| /blogs/hair-care/widows-peak-hair | merge target | Widow's Peak Hairstyles for Women: What It Is & How to Style It | 2,653 → 981 | 0 → 5 | [preview](../data/refresh_drafts/hair-care__widows-peak-hair/preview.html) | [review](../data/refresh_drafts/hair-care__widows-peak-hair/review.md) |
| /blogs/hair-vitamins/l-glutamine | refresh | L-Glutamine for Hair: What the Research Shows | 1,864 → 1,052 | 0 → 6 | [preview](../data/refresh_drafts/hair-vitamins__l-glutamine/preview.html) | [review](../data/refresh_drafts/hair-vitamins__l-glutamine/review.md) |
| /blogs/hair-vitamins/coenzyme-q10 | refresh | Coenzyme Q10 (CoQ10) for Hair: What the Research Shows | 2,333 → 1,158 | 0 → 7 | [preview](../data/refresh_drafts/hair-vitamins__coenzyme-q10/preview.html) | [review](../data/refresh_drafts/hair-vitamins__coenzyme-q10/review.md) |
| /blogs/hair-vitamins/ferulic-acid | refresh | Ferulic Acid for Hair and Scalp: What the Research Shows | 2,054 → 944 | 0 → 5 | [preview](../data/refresh_drafts/hair-vitamins__ferulic-acid/preview.html) | [review](../data/refresh_drafts/hair-vitamins__ferulic-acid/review.md) |
| /blogs/hair-vitamins/poysorbate-80 | refresh | Polysorbate 80 in Hair Products: What It Is and What the Research Shows | 1,870 → 1,049 | 0 → 4 | [preview](../data/refresh_drafts/hair-vitamins__poysorbate-80/preview.html) | [review](../data/refresh_drafts/hair-vitamins__poysorbate-80/review.md) |

## Checks run

- **AI-chat links / pasted-chat markup in the current live bodies:** none found in any of the 10 articles, or in the 6 redirected posts folded into the merge targets (searched for chat.openai.com, chatgpt, utm_source, user-content-fn, data-footnote-backref, oaicite, contentReference, turn0search and similar). The builder's own guard also passed on every draft.
- **Claims scan:** no hits on cure/prevent/reverse/heal/guarantee/clinically proven. Hits are all neutral: 'treatment' and 'reversible' in the hairline article (describing clinical treatment and traction alopecia's early reversible stage, with sources), and 'mild, reversible side effects' in the rutin safety paragraph.
- **Builder checks:** every PMID verified through `pubmed.py`; reference lists generated from PubMed; testimonial, product widgets, images and footer block counts match the live article.
- **No reviewer line** in any draft.

## Flags that need your decision

- **Thin evidence (shorter, honest articles):** `poysorbate-80` (no hair research exists; 4 sources on what it is and safety), `chromium` (no direct hair research; leads with the metabolic-syndrome link), `molybdenum` (one mouse study of a nano form). You may prefer to merge or hold these.
- **Closing product box:** says products 'Promote Hair Regrowth'. Unchanged sitewide, flagged on every draft.
- **Disease-research mentions (neutral, research only):** alopecia areata in `l-glutamine` (genetic study) and `hairline-receding-on-one-side`; androgenic alopecia in `coenzyme-q10` and `chromium` (metabolic syndrome); frontal fibrosing alopecia in `hairline-receding-on-one-side` and `widows-peak-hair`; minoxidil, finasteride and hair transplants in `hairline-receding-on-one-side`, with no comparison to FullyVital products.
- **Removed unsupported product claims:** the old biotin-vs-prenatal post said biotin hair vitamins 'win' and recommended a 'purpose-built hair growth formula that targets DHT'; the old widow's peak post had a promo line ('wave goodbye to thinning'). Both removed.
- **Styling post:** `widows-peak-hair` styling tips are opinion, not sourced. Widgets kept as they were.
- **Rutin:** the 2026 Zhang abstract on PubMed is one sentence, so the article does not say whether it was done in cells or animals.
- **Length:** drafts are 944 to 1,521 words (builder count, including references), shorter than the old 1,900 to 2,650. Evidence for these ingredients is thin and I didn't pad.

## Not yet done

Nothing has been published and no Shopify writes were made. A fresh backup was taken this session (`data/shopify_backup/articles_2026-10-17_141630.json`). On approval: fresh backup, rebuild, dry run, publish one, check live, then the rest.
