# SEO / AEO pass on the 121 refreshed articles (2026-10-17)

## Done and verified (all 121 live)
- **FAQPage JSON-LD** added to every article, built from the visible FAQ (3 Q&As each, plain text, no links). Shopify keeps the script in the article body; the live page renders it next to the theme's Article, BlogPosting, Person, Organization and BreadcrumbList schema (checked on 6 live pages; all 121 checked via the Admin API).
- **Alt text** set to the article title on every image that lacked it: 474 images across 120 pages. Images that already had alt text were left alone. 0 images now lack alt.
- Nothing else in the bodies changed (verified by comparing each rebuilt draft to the previously published one, ignoring alt and the script). Titles, meta descriptions, citations (3 each) and publish dates are unchanged.
- Builder now does this automatically (`enhance()` in `refresh_build.py`), so future rebuilds keep it.

## Still open
1. **Duplicate Article + BlogPosting schema** on 101 pages is from the theme (not edited by us).
2. **Internal links** are proposed, not applied:
   - `data/processed/related_reading_proposal_2026-10-17.csv`: 3 related articles per page (TF-IDF similarity on our own text), max 7 inbound per target, as a "Related reading" list at the end.
   - `data/processed/internal_linking_proposal_2026-10-17.csv`: in-text anchors; only 22 natural matches exist, because the articles rarely name other ingredients outside the old marketing blocks.
3. **Carried-over marketing blocks (compliance):** the product widgets / CTA paragraphs copied unchanged from the old posts contain claims such as "stop and reverse the aging process" of hair (72 pages), "scientifically proven/backed" (58 pages), "promote regrowth" (13 pages) and a 120-day refund guarantee (2 pages). 83 pages have at least one. These blocks are not our new text and were not edited. They are different from the closing "Promote Hair Regrowth" box, which was left out of scope as instructed.
4. `hair-care/vitamin-c` ("Vitamin C: Stimulating Hair Growth For Women...") is a separate published post that is not in the refresh queue.
