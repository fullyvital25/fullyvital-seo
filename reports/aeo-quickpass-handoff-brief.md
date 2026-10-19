# Handoff brief: AEO quick pass on 128 older blog articles

You're picking up one bounded, repetitive task in an existing project. Read this whole brief before doing anything. `CLAUDE.md` in this folder loads automatically and its rules apply; the key ones are repeated here.

## Context

- **The site:** fullyvital.com, a Shopify store with a blog (`hair-care` and `hair-vitamins`). It sells hair-growth and anti-gray supplements and serums. The niche is health/YMYL.
- **What's already done:** the project has rebuilt 22 hub pages and refreshed 122 articles to an "answer engine" standard. Those pages open with a direct answer and carry FAQ schema, so Google's AI Overviews, "People also ask" and AI assistants can quote them.
- **What's left:** 128 older on-topic articles. They have no FAQ schema, and most don't open with a direct answer. They earn about 566,000 Google impressions over 16 months.
- **Your task:** a light, mechanical pass on those 128. **It is not a rewrite.**

## The page list

`data/processed/aeo_quickpass_pages.csv`, ordered by impressions. Columns:
- `path`, `title`, `impressions_16m`;
- `has_faq_section`, `faq_questions` (questions found in the FAQ section);
- `question_headings`, `answer_first_now`.

Of the 128, 121 have an FAQ section with 2 or more questions. 7 don't: 5 have no FAQ section and 2 have a single question.

**Before you start, re-check each page live.** Skip a page and list it in your report if any of these is true:
- it's no longer published;
- it already has `"@type": "FAQPage"` in its body;
- it's a refresh-test page: any URL in `data/processed/refresh_controls.json`, **both the keys (treated) and the values (control)**.

## What to change on each page

Two additions, and nothing else.

### 1. A short answer at the very top

Insert this as the first element of the article body:

```html
<p class="fv-keyfact"><strong>Short answer:</strong> SENTENCE ONE. SENTENCE TWO.</p>
```

- **Exactly 2 sentences, 30–60 words in total.** They answer the question the page's title asks, directly. For example, for "Protein Overload: Causes, Symptoms, And Solutions For Hair": what protein overload is, and the main sign or fix.
- **Base it only on the article's own text.** Don't add facts, numbers, doses, study results or percentages that aren't already on the page. If the page doesn't support a clear answer, write a plain, general definition and flag the page in your report.
- **Plain, neutral wording.** Never use cure, treat, prevent, reverse, regrow, heal, stop (hair loss/graying), clinically proven, guarantee, miracle or "will grow".
  - On disease or drug pages, such as finasteride, alopecia, PCOS, scalp inflammation and dandruff, describe the condition or the drug factually.
- **No product names or links.**
- **If the page's own text makes a disease or unsupported claim,** don't repeat it. Flag the page in your report. Don't edit the claim; that's a separate pass the owner is doing.
- **Match the page's spelling** (gray/grey) and its subject.

### 2. FAQ schema from the questions already on the page

Append one block at the very end of the body:

```html
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
  {"@type": "Question", "name": "...", "acceptedAnswer": {"@type": "Answer", "text": "..."}}
]}
</script>
```

- **Where the questions come from:** use the article's FAQ section, the `h2`/`h3` whose text contains "Frequently Asked" or "FAQ". Each question is a heading inside it that ends in "?". Its answer is the text of the paragraphs (and list items) after that heading, up to the next heading.
- **Pages without an FAQ section** (or with only 1 question in it): use the question-style `h2`/`h3` headings in the body, up to 6, with the paragraph text that follows each one. If there are fewer than 2, skip the schema for that page and note it.
- **Copy the visible text exactly,** as plain text with HTML stripped and whitespace collapsed. Don't rephrase, shorten, add or merge. Google requires the schema to match what's visible on the page.
- **Leave out any Q&A whose answer is a product pitch,** for example one that mostly says "FullyVital's X is…", or contains claim words from the list above. Note how many you left out per page.
- **Limits:** at most 8 Q&As. Keep any one answer under about 1,200 characters; if it's longer, use its first paragraph only.
- **Validity:** the JSON must parse (`json.loads`). Escape quotes properly; build it with `json.dumps(..., ensure_ascii=False)`, never by hand.

### Do not touch

- **Any existing text, headings, links, images, product widgets, prices or claims.** The old marketing blocks with claims are being handled separately by the owner, so don't edit, flag or reword them. The only exception is the flag-only rule in section 1.
- **The closing "Promote Hair Regrowth" product box.** Leave it unchanged and don't mention it.
- **Titles, SEO title/description, summary, author, publish date and URL.**
- **Refresh-test pages,** unpublished pages, and anything outside blog articles: no products, pages, themes or redirects. Make no Google Search Console writes.

## Tools

- **`shopify_client.py`:** the only way to talk to Shopify.
  - `Shopify()` is a dry run; `Shopify(apply=True)` makes real writes.
  - `backup_articles()` saves every article.
  - `update_article(article, {"body": new})` writes and logs to `data/shopify_changes/<date>.jsonl`.
  - To re-read one article right before writing it:

    ```python
    s.gql("query($id: ID!) { article(id: $id) { " + ARTICLE_FIELDS + " } }", {"id": ...})["article"]
    ```

    `ARTICLE_FIELDS` comes from `shopify_client`.
- **Python:** use `.venv/bin/python`. BeautifulSoup is installed. Do all extraction, counting and checks in code.

**Write one script, `aeo_quickpass.py`.** It works in two stages:

1. **Draft** (default):
   - Read the list and fetch each article.
   - Build the FAQ schema in code.
   - Write each page's short answer. You write these; base each one on the page's text, which you pass in.
   - Save everything to `data/processed/aeo_quickpass_drafts.csv`, with columns: path, short_answer, word_count, faq_count, faq_questions, skipped_reason, flags.
   - Write a review file, `reports/aeo-quickpass-review.md`, listing each page's title, its short answer, and the FAQ questions it will use.
2. **Apply** (`--apply`, optional `--limit N`):
   - Back up all articles first.
   - For each page, **re-read the article from the API immediately before writing**, so you never overwrite a newer edit made by someone else.
   - Insert the short answer and the schema from the approved drafts CSV.
   - Write the change, and log it.

## Steps

1. **Draft all pages** and save the review file.
2. **Stop and ask the owner to review** `reports/aeo-quickpass-review.md`. CLAUDE.md requires article content to be reviewed before it's published. Apply any edits they ask for.
3. **Check that no other session is writing to the store.** Look at the latest entries in `data/shopify_changes/<today>.jsonl`. If you see recent writes from another session, ask the owner before continuing.
4. **Back up**, then run `--apply --limit 1`. Re-read that article from the API and check:
   - the body is the old body with exactly two additions: the short-answer paragraph at the start and the script at the end;
   - the JSON-LD parses;
   - every FAQ question in the schema appears in the visible text.
5. **Apply to the rest.**
6. **Verify every changed article against the backup:**
   - the only differences are the two additions, so after removing them the before and after bodies must be identical;
   - all hrefs are unchanged;
   - every JSON-LD block on the page parses;
   - no refresh-test page was edited.
   - Then load 5 pages live on fullyvital.com, with pauses so you don't get rate-limited, and confirm the short answer shows and the FAQPage script is in the HTML.
7. **Report** to `reports/aeo-quickpass-<date>.md`, in plain language for the site owner. Keep it short. Include:
   - the pages updated, and the pages skipped with reasons;
   - the pages flagged for claims, or for having no clear answer in the text;
   - the backup file;
   - anything that failed.
8. **Add one line** to the "Done" section of `reports/project-status.md`.

## Stop and ask the owner if

- more than 5% of pages fail the "only two additions" check;
- a page's FAQ answers are mostly product pitches, so the schema would be mostly product claims;
- anything would need editing beyond the body's start and end.
