# Content queue: the next 25 articles

**For:** Claude (or anyone) continuing this project.
**Built:** 2026-10-19.
**The list:** `data/reference/content_queue.csv`. Each row has its order, type, URL, working title, keywords with verified volume and KD, the hub to link up to, sibling links, product bridge, compliance notes, redirects to add on publishing, and status.

## Why a queue, and why this pace

In 2023–24 the blog published 767 posts in a year, two to three a day. Impressions rose to about 980,000 a month, but at average positions of 24–43 and a click-through rate of about 0.3%. Two sitewide drops followed in July and November 2025: impressions fell 84% and clicks 68% year on year. Google demotes whole sites for mass-produced content.

So the rule is **quality and fit over volume: 2 articles a week.** Each one fills a real gap found in the keyword data and links into a hub. Volume alone is what got the site demoted.

## Schedule

- **Start the week of 2026-11-16.** That's four weeks after the hubs launched, and after the first hub tracking update on 8 Nov. The scheduler sends a reminder every Monday from then on.
- **Pace:** 2 a week, in the CSV's order (column `week`): usually one new page and one rewrite. 25 articles take about 13 weeks, to mid-February 2027.
- **Review the order first:** check `reports/hub-tracking.md`. If a hub's cluster is gaining, move its items up. If the claims pass (around 1 Nov) changed any wording rules, apply them.

## How to write and publish each article

1. **Read the row:** primary and secondary keywords, the hub, siblings, product bridge and compliance notes. Check that no live page already covers the topic, since hubs may have changed. Check that it's not a refresh-test page (`data/processed/refresh_controls.json`, keys and values) and not a calendar post. Calendar posts are extended, never rebuilt.
2. **Get Google's questions:** run `DFS().serp_features("<primary keyword>")` from `dataforseo_client.py` (about $0.002) and save the raw result to `data/raw/`. Use its "People also ask" questions for the FAQ. Skip celebrity, speculative or unverifiable questions.
3. **Find 3 PubMed studies** with `pubmed.py` (`search`, `summaries`, `abstract`). Read the abstracts and use only what they say. Never cite from memory.
4. **Write `data/hub_drafts/hair-care__<handle>/template.html` and `meta.json`,** in the same format as the existing hub drafts. Copy any recent one, such as `hair-care__hairstyles-for-thinning-hair`.
   - **Opening:** a 40–60-word direct answer first, then a "Key fact" box and "The Short Answer" box.
   - **Headings:** use question headings.
   - **Research section:** all 3 study links go in "What the Research Shows", in the second half of the page, each linked once.
   - **Product paragraph:** after the evidence. Structure/function wording only ("designed to support"). Ingredients come only from `data/reference/fullyvital_products.csv`. Product facts: the derma roller is 1 mm, and the 120-day guarantee covers every product.
   - **Links:** an FAQ from the Google questions, a Related Reading block with the hub plus 2–3 siblings, and a disclosure.
   - **Pages that skip the product paragraph:** disease, drug and pregnancy topics. Say plainly that FullyVital products aren't treatments.
5. **Build the draft:** `python hub_build.py hair-care <handle>`. Its guards check the 3 studies, link placement, years and authors, and AI-chat artifacts. Then check every internal link is live.
6. **Create it unpublished** for a new page: `python create_new_article.py hair-care__<handle> --apply`. For a rewrite, keep the URL and prepare the draft the same way.
7. **Get the user's approval** for the article or the week's batch. CLAUDE.md requires this. Then publish:
   - **New pages:** `create_new_article.py ... --publish --apply`.
   - **Rewrites:** add the item to `data/processed/hub_rollout_plan.json` and run `hub_rollout.py --apply`. It publishes, adds the spoke links and makes the redirects.
8. **Link it up and down:**
   - **Down from the hub:** add a link from the hub to the new page, as a new item in the hub's Related Reading block.
   - **Up from relevant spokes:** add one sentence linking up to the new page on related spokes where it fits. Never on refresh-test pages.
   - **Redirects:** add the redirects in `redirect_on_publish`, blog URLs only, after checking that the target is live.
9. **Record it:**
   - In the CSV, set `status` to `published YYYY-MM-DD` and fill in the URL if it changed.
   - Add the page to `hub_tracker.py` (HUBS) or to its hub's cluster in `data/processed/hub_clusters.json`.
   - Update `reports/project-status.md`.

## Waiting until after the refresh-test readout (early December)

- **Crown balding:** rewrite `/understanding-crown-balding-causes-treatments-and-solutions` for "crown hair loss" (6,600, KD 0) and "thinning crown hair loss" (6,600). It's a control page today.
- **Hairspray:** rewrite `/is-hairspray-bad-for-your-hair` (17,641 impressions). It's also a control page.
- **Copper peptides:** if the peptides article (#1) is live by then, `/copper-peptides-hair-thinning` should 301 to it, not to `/hair-vitamins/copper`. #1 already lists it under `redirect_on_publish`.

## Not in the queue on purpose

- **Big commercial terms** such as "minoxidil" (450,000), "hair growth supplements" (110,000) and "hair growth serum" (74,000) are won by product pages and shops; see `reports/product-page-brief.md`.
- **Off-topic beauty and styling posts** (bangs, bobs, perms, skincare) were removed on purpose in clean-up batch 1.
- **Celebrity questions,** and the "3:2:1 haircut rule", which has no reliable source.
