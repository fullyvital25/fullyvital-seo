# AEO quick pass: report (2026-10-19)

## Result
- **125 of 128 articles updated.** Each now opens with a 2-sentence "Short answer" and ends with FAQ schema built from the questions already on the page.
- **3 skipped:** do-anti-gray-supplements-work-honest-review, gray-hair-research-studies and gray-hair-science-glossary. They already had a "fv-keyfact" box from an earlier pass, so I left them alone. They still have no FAQ schema.
- No page was unpublished, and no refresh-test page was touched.
- **6 pages got a short answer but no schema** (fewer than 2 usable Q&As after removing claim-word and pitch answers): b-vitamins-hair-growth, how-to-use-fully-vital-products, is-good-circulation-important-for-healthy-hair-growth, dextran, folate, 7-daily-habits-that-damage-hair.
- Many pages lost a few Q&As from the schema for claim words, brand mentions or length. Counts per page are in `data/processed/aeo_quickpass_drafts.csv`.

## Checks
- Every changed article was compared with the backup: the only differences are the two additions, all links are unchanged, every JSON-LD block parses, and each schema question appears in the visible text. 125 changed, 0 failures.
- 5 pages loaded live (protein-overload-hair, black-seed-oil, hair-breakage, jojoba-oil, anagen-phase): short answer and FAQPage script both present.

## Flagged pages
Pages whose own text makes disease or unsupported claims (not edited, as instructed) or have no clear answer are listed with the reason in the `flags` column of the drafts CSV. Most serious: formaldehyde, dextran, fade, stem-cell-therapy, dandruff-cause-hair-thinning (cancer claim about shampoo chemicals), 7-daily-habits-that-damage-hair, finasteride, finasteride-results-timeline, bimatoprost. The brand-comparison, how-to and testimonial pages got answers without brand names.

## Files and issues
- Backup: `data/shopify_backup/articles_2026-10-19_094604.json` (further backups were also taken on each apply run).
- Log: `data/shopify_changes/2026-10-19.jsonl`.
- One failure: the bulk run stopped on a dropped connection partway through. I re-ran it; it skips pages already done, so nothing was written twice.
- Verification script: `aeo_verify.py`.

## Follow-up: short-answer rewrite (2026-10-19)
- 61 short answers that said "the article" or "the page" were rewritten as direct answers in our own voice. All 61 are applied; only the text inside the existing Short answer paragraph changed.
- Checked against a backup taken just before each run: the rest of each body, the title, handle, summary and publish state are identical. The 60 changed in the first run showed 0 failures, and the last page, keratin, was checked separately.
- The 66 flagged pages were skipped as instructed and keep their original wording, which still says "the article". Neutral definitions for them are still open.
- keratin was missed in the first run because another unpublished article in the hair-vitamins blog has the same handle. The script now matches on the full blog path.
- Script: `aeo_rewrite_apply.py`. Rewrites: `data/processed/aeo_quickpass_rewrites.json`.

## Follow-up: FAQ schema on the 3 skipped pages (2026-10-19)
- FAQ schema (no short answer) added to do-anti-gray-supplements-work-honest-review (3 Q&As), gray-hair-research-studies (3) and gray-hair-science-glossary (2). Each already had a key-fact box. Q&As with claim words in the answer were left out (2, 2 and 1).
- Checked against a backup taken just before: the old body is unchanged and the only addition is the script block; the JSON parses and every question appears in the visible text. Script: `aeo_faq_only.py`.

## Follow-up: flagged-page short-answer rewrite (2026-10-19)
- 64 flagged pages now have neutral short answers: a definition or direct answer, plus one safe detail from the page. No flagged claim is restated and there are no brand names.
- Checked against a backup taken just before: only the text inside the Short answer paragraph changed on each page; the rest of the body, title, handle, summary and publish state are identical.
- Rewrites: `data/processed/aeo_quickpass_rewrites_flagged.json`. Same script as before (`aeo_rewrite_apply.py`, now takes a REWRITES file).
