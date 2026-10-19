# Brief: finish the FullyVital blog article refreshes

You are continuing work on the FullyVital SEO project in `/Users/farazk/CodingProjects/fullyvital-seo`. Ten articles have already been refreshed and published with the method below. Your job is to refresh the remaining **111 articles** in `data/processed/refresh_queue.csv` with the same method, in batches of 10. Each batch goes to the user for approval before anything is published.

Read this whole brief before starting. Then read `CLAUDE.md` (project rules, which override anything here if they conflict) and the project memory files.

---

## 1. Background you need

- **The site.** fullyvital.com is a Shopify store selling hair supplements and serums for gray hair and for hair growth and hair loss. The blog has two blogs: `hair-care` and `hair-vitamins`.
- **Why we're doing this.** Organic blog traffic fell about 95% from mid-2025 in two sitewide drops. The working hypothesis is that Google sees the blog as mass-produced: about 600 template posts from 2023–24, each about 2,000 words, almost no citations, and lots of overlap. Full diagnosis: `reports/phase1-audit.md` and `data/processed/decline_*.csv`.
- **What's already done:**
  - 159 duplicate or off-topic posts were unpublished and redirected on 2026-10-17. Log: `data/shopify_changes/2026-10-17.jsonl`.
  - 10 articles were refreshed and published: boron, manganese, baby-hairs, choline, glucosamine, n-acetyl-cysteine, copper, chlorophyll, quercetin and glutathione. Each folder in `data/refresh_drafts/` has a `published.json` marker.
- **What you're doing.** The other refresh candidates (62 "refresh" posts) and duplicate-group survivors (49 "merge target" posts), all listed in `data/processed/refresh_queue.csv`.
- **Out of scope:**
  - The 132 "HOLD: in scope, no traffic" posts (reserved for Phase 2).
  - The 69 brand comparison posts ("X vs Fully Vital").
  - Product pages.
  - Starting the "pages that used to rank" review.

## 2. Non-negotiable rules

1. **Never invent a fact, number, study, author or year.** Every specific claim (a statistic, a dose, a food source, a study result, a safety caution) must come from a source you retrieved and read in this session. If you can't source a specific, write around it in general terms or cut it. Don't fill gaps from memory.
2. **All citations go through `pubmed.py`.** Search, read the abstract, and cite only what the abstract actually says. The builder generates the reference list from PubMed records, so you never type references by hand. In-text citations look like `(<a href="https://pubmed.ncbi.nlm.nih.gov/PMID/" target="_blank" rel="noopener">Surname et al., YEAR</a>)`. Use `Surname &amp; Surname` for two authors and `Surname` for one, and check the authors and year against `summaries()` before writing the citation.
3. **Stay within structure/function claims (YMYL).** No text may say an ingredient or product diagnoses, treats, cures or prevents a disease. Nothing may promise to reverse gray hair. Research on diseases (alopecia areata, pattern hair loss) can be described as research, in neutral wording, never as a product benefit. Run the claims scan in section 5 before handing over a batch.
4. **No AI-chat links or pasted-chat leftovers, ever.** The live baby-hairs article contained six `chat.openai.com` links and the user was rightly unhappy. Before drafting each article:
   - read its **current** body and list any `chat.openai.com`, `chatgpt.com`, `utm_source=chatgpt`, `user-content-fn`, `data-footnote-backref`, `oaicite` or similar;
   - report any you find to the user in the batch summary.

   The builder and publisher both block these patterns. Never weaken that check.
5. **No medical reviewer line.** FullyVital has no named reviewer yet. Don't add "medically reviewed by", "fact-checked by" or similar.
6. **Leave product claims alone.** Copy the product widgets, testimonial block, images and the closing FullyVital product box exactly as they are. The closing box says products "Promote Hair Regrowth". The user handles product claims, so flag it but don't edit it.
7. **Shopify writes only after approval.** Prepare drafts locally. Publish a batch only after the user approves it. Always run a dry run first, publish one article and check it live, then publish the rest of the batch.
8. **Keep URLs.** Never change handles, blogs or publish dates.
9. **Don't touch the control pages.** `data/processed/refresh_controls.json` lists 20 untouched articles used to measure whether refreshes work. They aren't in your queue; never edit them, even if they look like good candidates. Don't edit `refresh_tracker.py` or its outputs either. After publishing each batch, run `.venv/bin/python refresh_tracker.py` once: it adds the new batch to the measurement automatically and picks matched controls for it.

## 2b. Citation style (user rule, 2026-10-17; replaces anything below that implies more)

- **3 studies per article**, the ones that carry the claims. Drop background and safety-only citations.
- **Cite each study once.** Key Takeaways and FAQ stay link-free.
- **All study links in the second half** of the article. Intro, takeaways and "What Is X?" have no links.
- Cut or generalise any claim whose source you dropped. Check before building: first link at 50% or more of the text, 3 distinct PMIDs, each once.
- This overrides "3 or more PubMed citations", "FAQ answers each citing its source" and the 4-8 searches guidance as to what is cited (still research widely, cite 3).

## 3. Tone and content standard

The user asked for this explicitly: **err on the side of being a little promotional, but not too much.**

- **Lead with the strongest real evidence and frame it positively.** For example: "Copper powers tyrosinase, the enzyme that makes hair pigment", or "In a 2023 study, quercetin woke up resting follicles."
- **Label each study type once, plainly, and don't dwell on it.** For example: "These are laboratory results; clinical trials in people are still needed." Lab, animal and small pilot studies all get this one line.
- **Be honest when evidence is thin.** Say direct hair studies haven't been done, then explain the real mechanism or nutrient link that makes the ingredient relevant. The boron article is more cautious than the user wants; match the other nine instead.
- **Answer the page's main search query directly.** It's in the `primary_keyword_guess` column. If the query is "does X cause hair loss", answer it in the FAQ and early in the body.
- **Write plainly.** Short sentences, everyday words, no hype words ("miracle", "game-changer", "unlock the secrets"), no filler.
- **Length:** usually about 950–1,600 words. Don't pad to match the old length. The old posts are full of unsourced filler.

### Standard article structure

1. A two-sentence intro that names the ingredient's real relevance to hair.
2. `{{PROOF}}`
3. `Key Takeaways`: 4 bullets, each backed by a source in the body.
4. `What Is X?`: what it is, with a citation.
5. `{{IMAGE_1}}` (only if the live article has images; check the builder's block counts).
6. `How Does X Support Hair?` (or the page's own question): the evidence, in H3 subsections.
7. `{{PRODUCTS_1}}`
8. Food sources, how to take it, or practical steps, all sourced.
9. `{{IMAGE_2}}`, then `{{PRODUCTS_2}}`
10. `Is X Safe?`: sourced cautions, plus "check with your doctor if pregnant, breastfeeding, have a condition or take medication".
11. `Frequently Asked Questions`: 3 questions taken from real queries, each answer citing its source.
12. `<h2><strong>References</strong></h2>` followed by `{{REFERENCES}}`.
13. `{{FOOTER}}`

Use the same H2/H3 markup as the live posts: `<h2><strong>…</strong></h2>`.

**Gold-standard examples to copy.** Read at least two before writing:
- `data/refresh_drafts/hair-vitamins__copper/` (`template.html` and `meta.json`)
- `data/refresh_drafts/hair-vitamins__quercetin/`
- `data/refresh_drafts/hair-vitamins__glutathione/`
- `data/refresh_drafts/hair-care__baby-hairs/` (a non-ingredient topic)

## 4. Tools (all in the repo root; run with `.venv/bin/python`)

| File | What it does |
|---|---|
| `shopify_client.py` | Shopify Admin API. Dry run by default (`Shopify()`); real writes need `Shopify(apply=True)`. `articles()` reads all articles, including unpublished ones. `backup_articles()` saves all articles to `data/shopify_backup/`. Every write is logged to `data/shopify_changes/<date>.jsonl`. |
| `pubmed.py` | `search(query, n)`, `summaries(pmids)` (title, journal, year, first 3 authors), `abstract(pmid)`. Results are cached in `data/raw/pubmed/`. |
| `refresh_build.py <blog> <handle>` | Builds `draft.html`, `review.md`, `preview.html` and `current.html` from `data/refresh_drafts/<blog>__<handle>/template.html` and `meta.json`. Fills placeholders from the **latest backup**, generates the reference list from PubMed, and stops on unverified PMIDs, wrong years, a missing first author in the references, or AI artifacts. |
| `publish_refresh.py` | No flags is a dry run. `--apply --only <folder>` publishes one draft. `--apply` publishes every draft without a `published.json`. Writes title, body, summary, SEO title and meta description, then writes `published.json`. |

**Placeholders.** These are filled with blocks copied from the live article:
- `{{PROOF}}`: the testimonial block;
- `{{PRODUCTS_1}}` and `{{PRODUCTS_2}}`: the "Our Best Sellers" widgets;
- `{{IMAGE_1}}` and `{{IMAGE_2}}`: the centred images;
- `{{FOOTER}}`: the closing product table;
- `{{REFERENCES}}`: the generated reference list.

If the live post has fewer blocks than your template uses, the build stops. Remove the extra placeholder in that case. The baby-hairs post, for example, had no images.

**`meta.json` keys:**
- `title`: the H1 and article title.
- `seo_title`: about 60 characters, ending in `| FullyVital`.
- `seo_description`: about 150 characters.
- `notes`: a list of what changed and why, for the user.
- `sources`: `{pmid: what it supports}`; optional but helpful.
- `flags`: a list of things for the user to decide. (User update 2026-10-17: do NOT flag the closing box any more; copy it unchanged and say nothing.)

## 5. Workflow

### Once at the start
1. Read `CLAUDE.md`, this brief and the gold-standard drafts.
2. Take a fresh backup: `Shopify().backup_articles()`. The builder always uses the newest backup.
3. Load `data/processed/refresh_queue.csv`. Work in `batch` order (1–12, about 10 articles each, ordered by recent clicks).

### For each article
1. **Read the live article** from the latest backup: title, H2s, word count, block counts, internal links, and any existing "Sources" or "References" section.
2. **Scan the current body for AI-chat links and markup** (rule 4) and note anything you find. Also note weak or wrong old sources. For example, the boron post cited a lithium study as evidence for boron.
3. **For merge targets,** read the bodies of the posts in `merged_sources`. They're unpublished but still in the backup. Fold any genuinely useful, sourceable content into the target, and note which source posts you used in `notes`.
4. **Research.** Run 4–8 PubMed searches: the ingredient plus hair, alopecia, graying, follicle, dermal papilla, keratinocyte or melanocyte; then reviews on its function, intake, food sources and safety. Read the abstracts. Prefer human trials, systematic reviews and reviews, then lab or animal studies, which must be labelled as such. Note exact figures from abstracts only.
5. **Check authors and years** with `summaries()` for every PMID you'll cite. Write in-text citations to match.
6. **Write `template.html` and `meta.json`** following section 3.
7. **Build:** `.venv/bin/python refresh_build.py <blog> <handle>`. Fix whatever stops it.
8. **Self-review the draft** against this checklist:
   - Does each specific claim match its cited abstract?
   - Is any specific left unsourced?
   - Does any sentence imply that an ingredient or product treats, prevents or cures a disease?
   - Is the page's main query answered?
   - Does it say plainly, once, where evidence comes from lab or animal studies?

### Before handing a batch to the user
1. **Run the claims scan** over the new prose and fix anything that reads as a disease or reversal claim:
   ```python
   import re, glob
   from bs4 import BeautifulSoup
   PAT = r"\b(cur(e|es|ed)|treat(s|ed|ing|ment)?|prevent(s|ed|ing)?|revers\w*|heal(s|ed)?|guarantee\w*|clinically proven)\b"
   for t in glob.glob("data/refresh_drafts/*/template.html"):
       txt = BeautifulSoup(re.sub(r"\{\{[A-Z_0-9]+\}\}", "", open(t).read()), "html.parser").get_text(" ")
       for s in re.split(r"(?<=[.!?])\s+", txt):
           if re.search(PAT, s, re.I): print(t.split("/")[2], "|", s.strip()[:160])
   ```
   Hits in safety advice ("talk to your doctor if…") or in an honest "no study has shown X can reverse…" are fine.
2. **Write an index for the batch** at `reports/refresh-batch-<n>-review.md`. For each article give the path, new title, old → new word count, old → new study links, and links to its `preview.html` and `review.md`. Copy the format of `reports/refresh-pilot-review.md`.
3. **Give the user a short summary:** what you did, any AI-chat links or bad old sources you found, every flag that needs a decision, and the claims-scan result. Then **stop and wait for approval.**

### Publishing an approved batch
1. Take a fresh backup, then rebuild every draft in the batch so the copied blocks match the live store.
2. Dry run: `.venv/bin/python publish_refresh.py`. It lists only unpublished drafts. Make sure it lists exactly the approved batch.
3. Publish one article: `--apply --only <folder>`. Check it live (step 5).
4. Publish the rest one by one with `--only`, or with `--apply` if the dry run showed exactly this batch.
5. **Check every article live.** Fetch each page with a cache-busting query string (`?v=<timestamp>`) and a browser User-Agent. Confirm:
   - HTTP 200;
   - `<title>` equals `seo_title`;
   - the H1 equals `title`;
   - the meta description equals `seo_description`;
   - the number of PubMed links matches;
   - zero AI-chat links;
   - both product widgets are present.

   The storefront rate-limits (HTTP 429). Wait 20–60 seconds between retries and about 3 seconds between pages. Where you can, verify through the Admin API instead of loading pages.
6. Report the results to the user, then move to the next batch.

## 6. Special cases

- **Off-topic or styling merge targets.** Six rows have `topic_note` set: widows-peak-hair, micro-bangs-short-hair, fine-hair, normal-hair-part-vs-thinning and similar. Refresh them for accuracy, clarity and sources. Don't force supplements into styling topics; keep the existing widgets and stop there. Where the topic does touch hair loss (receding hairline, thinning), use the same evidence standard.
- **Medication and procedure topics** (finasteride, dutasteride, minoxidil, PRP and similar, if they appear). Describe the evidence neutrally. Don't compare FullyVital products to drugs. Point readers to a doctor.
- **"Does X cause hair loss?" posts.** Answer directly. If there's no evidence, say so. Don't invent mechanisms.
- **Gray-hair posts.** Never say an ingredient restores, repigments or reverses gray hair. "Supports normal pigment production" is fine when sourced, for example copper and tyrosinase.
- **No good PubMed evidence at all.** Write a shorter, honest article covering what the ingredient is, its known general function (sourced) and safety, and flag it. The user may prefer to merge it or hold it instead.
- **A build stops on a missing block.** Remove the unused placeholder. Never paste widget HTML by hand.

## 7. Known pitfalls from the first round

- **zsh doesn't split unquoted variables.** In loops, `for a in hair-vitamins:silica …; do .venv/bin/python refresh_build.py ${a%%:*} ${a##*:}; done` works; passing `"$a"` as one string doesn't.
- **Check abstracts for exact wording before stating a specific.** In round one, three drafted specifics had to be removed or corrected: named manganese foods, a vitamin K warning for chlorella, and a garbled boric-acid sentence.
- **Check author names every time.** A recalled author for one boron reference turned out to be wrong.
- **Abstract text is sometimes cut off in quick prints.** Read the full `abstract()` before quoting results.
- **The NIH Office of Dietary Supplements site blocks automated fetching.** Use PubMed sources instead.
- **Delete any `quickfix.html` or scratch files** you create in draft folders, or keep them out of the build.

- **template.html is raw HTML.** Use `<strong>`, never markdown `**bold**`: batch 1 went live with literal asterisks in bullet lists. After building, grep `draft.html` for `**` and fix before handing over.

## 8. Definition of done

- All 111 queue rows have a built draft. The user has approved each batch, and the batch is published and checked live, with `published.json` written.
- Every published article has exactly 3 PubMed citations (section 2b), zero AI-chat links and no disease or reversal claims, and its product blocks are unchanged.
- A final summary goes to the user covering: articles published, total citations, articles where evidence was too thin (flagged), AI-chat links or bad sources found in old posts, and anything left for them to decide.

Then stop. Don't start the "pages that used to rank" review or Phase 2 unless the user asks.
