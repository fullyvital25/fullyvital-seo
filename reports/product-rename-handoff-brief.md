# Handoff brief: rename old "Enhance Hair" product names on the FullyVital blog

You're picking up one bounded, repetitive task in an existing project. Read this whole brief before doing anything. `CLAUDE.md` in this folder loads automatically and its rules apply. The key ones are repeated here.

## Context

- **The site:** fullyvital.com is a Shopify store with a blog (blogs `hair-care` and `hair-vitamins`). It sells hair-growth and anti-gray supplements and serums.
- **The project:** an SEO clean-up of the blog that has been running for weeks. Hubs, refreshes, merges and redirects are done. You're doing one small part.
- **Product names:** the current names are in `data/reference/fullyvital_products.csv`. The hair-growth line is:

| Current name | Product URL |
|---|---|
| Hair Revival Serum | `/products/hair-growth-serum` |
| Hair Revival Supplements | `/products/vitamins-for-hair-growth` |
| Hair Revival Kit 30-Day | `/products/hair-growth-kit` |
| Hair Revival System 90-Day | `/products/womens-hair-growth-products` |
| Hair Skin Gut Collagen | `/products/collagen-for-hair-and-skin` |

- **What's already renamed:** "Density Scalp Treatment", "Enhance Hair Density Serum", "Density Renewal System 30-Day" and "Density Renewal Complex" on non-test pages. Don't redo those.
- **What's left:** older posts still name the products "Enhance Hair Serum", "Enhance Hair Vitamins" and variants. About 464 mentions sit on about 196 live articles, mostly in old "Our Best Sellers" product widgets and in image alt/title attributes.

## Your task

Replace the old product names with the current ones in live blog articles, then verify. Nothing else.

### Name mapping (case-sensitive, longest first)

| Old (product name only) | New |
|---|---|
| `Enhance Hair Density Serum` | `Hair Revival Serum` |
| `Enhance Hair Growth Serum` | `Hair Revival Serum` |
| `Enhance Hair Growth Supplements` | `Hair Revival Supplements` |
| `Enhance Hair Growth Supplement` | `Hair Revival Supplements` |
| `Enhance Hair Supplement` | `Hair Revival Supplements` |
| `Enhance Hair Vitamins` | `Hair Revival Supplements` |
| `Enhance Hair Serum` (but **not** when followed by ` 3-Pack`) | `Hair Revival Serum` |

- **Brand words:** replace only the product part. "Fully Vital's Enhance Hair Serum" becomes "Fully Vital's Hair Revival Serum". Don't change how "Fully Vital" / "FullyVital" is written.
- **Mixed-case variants** inside `alt="..."` or `title="..."` attributes, or as the text of a link to `/products/...`, are product names: rename them too. Examples: "Enhance hair serum", "Fully vital enhance hair supplement", "Enhance hair growth supplements".
- **Lowercase in running text** ("to enhance hair growth", "enhance hair density") is ordinary English. Leave it alone.
- **Ambiguous cases:** "Enhance Hair" on its own, "Enhance Hair Growth" with no Serum/Supplement after it, "Enhance hair wellness", or a capitalized "Enhance hair …" at the start of a sentence in body text. Print each one with about 100 characters of context. Rename it only if it clearly names a product (inside a widget, a link to /products/ or an alt/title). Otherwise leave it and list it in your report.
- **"Enhance Hair Serum 3-Pack":** this links to `/products/enhance-hair-serum-3-pack`, a product that isn't in the product sheet. Don't rename it. List every occurrence for the user. If the Admin API lets you read that product's current title (a read-only query), include it in the report, but still don't change anything.

### Do not touch

- **Prices:** widgets show prices such as "$47.20" and "$44.25". Leave them, and list every distinct price with the number of pages it appears on, so the user can check them.
- **Links and URLs:** don't change any `href`. Old product URLs (`/products/enhance-hair-growth-serum` and so on) already 301 to the current products.
- **Claims:** many of these old widgets also contain marketing claims ("scientifically proven", "reverse the aging process", "promote regrowth"). The user has said to **skip these for now**. Don't edit, flag or reword them.
- **The closing "Promote Hair Regrowth" product box:** copy it unchanged and don't mention it (standing user instruction).
- **Refresh-test pages:** these are every URL in `data/processed/refresh_controls.json`, both the keys (treated pages) and the values (control pages). Don't edit them until the test reads out in early December. About 52 of the old-name mentions are on these pages. List them in your report as deferred.
- **Anything outside blog articles:** no products, collections, pages, themes, prices or orders. No GSC writes. Blog articles are the only thing you edit.

## Tools

- **`shopify_client.py`:** the only way to talk to Shopify. `Shopify()` is a dry run and `Shopify(apply=True)` makes real writes. Every write is logged to `data/shopify_changes/<date>.jsonl`. `backup_articles()` saves every article.
- **`rename_product.py`:** already does exact, case-sensitive string swaps across body, summary and SEO title/description. It skips refresh-test pages and runs pairs in order:

  ```
  python rename_product.py "Old=>New" ["Old2=>New2" ...] [--apply] [--limit 1]
  ```

  It has no regex support yet. You'll need it for the `(?! 3-Pack)` exclusion and for case-insensitive matching inside attributes. Add a `--regex` flag that treats each pair as `re.sub(pattern, replacement)`, keeping the existing behavior as the default. Match the existing code style: short, no new dependencies.
- **Python:** use `.venv/bin/python`. Do all counting and checking in code, not by eyeballing output.

## Steps

1. **Back up:** `Shopify().backup_articles()`. Note the backup filename.
2. **Inventory, read-only:**
   - Using the newest backup, count every old-name occurrence on live articles by variant.
   - Record each one's context (link target, attribute or plain text) and whether the page is a refresh-test page.
   - Save it to `data/processed/enhance_rename_inventory_<date>.csv`.
3. **Dry run** with your final pairs. Check the would-change count against the inventory. Print the ambiguous cases with context and decide each one.
4. **Live test on 1 article** (`--apply --limit 1`). Re-read that article through the API and confirm all of the following:
   - None of the old names you targeted remain.
   - Hrefs and prices are byte-identical to the backup.
   - Any FAQ JSON-LD (`<script type="application/ld+json">`) still parses.
5. **Apply to the rest** with `--apply`.
6. **Verify every changed article** against the backup:
   - In the *before* body, replace every targeted old name and every existing new name with a placeholder. In the *after* body, replace the new names with the same placeholder. The two must be identical, which proves only product names changed.
   - All hrefs are unchanged.
   - All JSON-LD parses.
   - No refresh-test page was edited.
   - Recount what's left of each old variant, and explain each remaining one (lowercase verb, 3-Pack, ambiguous or test page).
7. **Report** to `reports/enhance-rename-<date>.md` in plain language: what changed, counts, the backup file, deferred test pages, 3-Pack occurrences, the price list, ambiguous cases you left, and anything that failed. Keep it short; it's for the site owner.

## Stop and ask the user if

- More than 5% of articles fail the "only names changed" check.
- The pattern list would change a name that links to a product not in the product sheet, other than the 3-Pack you're already listing.
- Anything would require editing outside blog article body, summary or SEO fields.

## Background, if useful

- **Earlier work:** the same kind of rename was done on 2026-10-17/18. See `data/shopify_changes/2026-10-17.jsonl` and `2026-10-18.jsonl` for the log format, and `rename_product.py` for the approach.
- **Still deferred:** old names on the test pages `/hair-vitamins/ginseng` and `/beta-carotene` wait for the December test readout.
- **Compliance context:** the niche is YMYL. Content must stay within structure/function claims. You aren't changing any claims; you're only renaming products.
