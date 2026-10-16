# INSIDE CE discovery: gold-control readiness, scoreability and measured native-source recall

**16 October 2026. Mode:** VALIDATE for structural defects in cold-search controls, with existing genuine source-provider evidence distinguished from local synthetic tests. **Inputs:** frozen 12-row [gold sources](../../data/reference/inside-ce-discovery-gold-controls.tsv), [community source-control register](../../data/reference/inside-ce-owner-source-recall-controls-2026-10-13.tsv), and [seven-kind search execution health tool](../../scripts/audit_ce_search_run_health.py). **Control data revision:** Only G08's known sticker number is removed from its query expression. Physical evidence, community statuses and URLs are unchanged.

## The metric we actually need

The target is: **Would an investigator, armed only with the game/edition's general public vocabulary, retrieve an original-source post, comment or photo using the specified *executed* search surface and finite budget?** That is different from (a) the source being known to exist, (b) a search plan being generated, (c) a search provider responding, (d) a nearby topic/thread being indexed, or (e) a crawler fetching a known URL supplied directly. All of these stages must be distinguishable.

The corrected index-gold evaluator counts every task's status as one of:
- **Never attempted** (including a planned task or explicit post-block skip). This is **zero** real provider attempts, not a failed search.
- **Attempted, provider unavailable** (network error, timeout, 401/403/429, invalid index response).
- **Attempted, valid index response**, returning only that response page's URLs. A returned URL can be exact, same thread only, or unrelated. There is no original HTML/comment/photo confirmation from this stage.
- **Incomplete response coverage**: one of two queries not executed, failed, or its result artifact is missing. Do not classify this as all queries exhausted.
- **Unscoreable control locator**: where the supposed gold source is a redirect shortener or a public account profile rather than the original post or image. It cannot pass a source-level photograph recall benchmark until a primary locator is independently resolved.

The source-specific 12-control dataset presently contains **10 controls with original-source-level locators and 2 requiring replacement before exact-scoring**:

| Gold control | Surface | Failure in prior benchmark | Correction / status |
|---|---|---|---|
| G05, sticker /043 | eBay | Target URL is `https://ebay.io/m/aK07BU`, a share redirect. `site:ebay.io` searches the *shortener*, not indexed eBay sale pages; finding the short URL is not original photo retrieval | Plan `site:ebay.com` and classify `short_redirect_requires_original_listing`. Must obtain original listing permalink/ID for true exact recall. Preserve lead history. |
| G10, lost L40 | Instagram | Target URL is the `bigdaffymonster` public *account profile*, not an identified original image/post URL | `profile_not_original_image_post` and unscoreable until an original post locator is provided. The **separate** tested 2019 Instagram post was login-blocked; this does not prove whether the particular 2024 bigdaffymonster source is accessible. |
| G02/G07 | X/Twitter | `twitter.com` and `x.com` can identify the **same status ID** but the generic exact-URL matcher treated them as different | Compare verified status IDs across recognized X/Twitter hosts; split query variants between source-era Twitter domain and current X domain. |
| G08, sticker -328 | Reddit | Query B literally contained the known physical serial `328`; the "blind" premise was contaminated by the withheld answer | Removed `328`; the planner now rejects any future three-digit known sticker serial leaked into an exact-token search query. |
| G10 query A | Russian / multilingual | The word for Huddle was `хaдл`, mixing Cyrillic `хдл` with Latin `a` inside one word, potentially defeating literal native search | Corrected to all-Cyrillic `хаддл`; planner now rejects Latin-Cyrillic mixed-script tokens as a confusable-query warning. |
| All 12 | multi-platform index | An explicit `not_attempted` results row was counted as a provider attempt, and one returned query page could imply exhaustive recall | Count statuses independently, preserve missing task slots, and mark a full 10-result Brave response as potentially truncated. |

**No alternative original eBay listing ID or Instagram post URL is invented.** URL aliases and account-level hits remain legitimate *lead* evidence but not scoreable exact-photo controls.

## What actual provider execution has already established

**Bluesky, narrow native Caswell known-positive:** [successful 17-request source run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38867696822), October 16. Native quoted `"inside collector's edition"` found Caswell **2/2**, without querying his handle. Generic `inside collector's edition` on an incompletely paginated first response did not find him in the first 49 of 55. Both V1/V2 APIs recovered the quoted control on the primary host. Prior cached public host returned HTTP 403 for keyword search. This is measured *native search recall* for **one** post and query variant, not a platform-wide completeness estimate.

**Bluesky, independent frozen 2023–2026 multi-query pilot:** [16-query run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38869121304) completed 16 request attempts, **14 valid search responses and 2 failures**, **153 post appearances** and **140 distinct public AT URIs**. Its first relevance gate selected seven: **one Caswell potential-owner statement already sent to Raezores**, three ARG-awareness posts, a known Giant Bomb CE-video repost from March 2026, and **two false-positive mentions of unrelated iam8bit merchandise/parcels that happen to use "inside"**. The raw 140-post source artifact remains available in the run. Therefore the original seven-row queue had at least **2/7 irrelevant** records; do not promote its generic `iam8bit + inside` rule to proof of Playdead product relevance. None is a new verified sticker.

**X/Twitter source extraction:** In live [source smoke 38873470697](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38873470697), the archived Kayd Hendricks post yielded an image payload. This is **known-URL retrieval**, not blind X search and not a newly identified CE owner. The same smoke found Instagram `login-required` and VK `no-media-found`; neither is negative content evidence. Strict provenance checks now distinguish payload acquisition from process exit status.

**Reddit archive, older evidence:** In [source pilot 38467083410](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38467083410), Arctic Shift returned **one** successful query, **nine HTTP 422** and **fourteen HTTP 429** among 24 planned requests. Those 23 failures are **not** 23 evidence-free slices. Subsequent scanner fixes stop on blocking status and report candidate caps separately. Exact-ID lookups can validate known URL availability but cannot be scored as cold discovery.

**Public web-index/Brave gold controls:** Workflows historically defaulted to offline planning. This current PR's CI deliberately publishes an **offline readiness report**, with zero provider calls and no falsely attributed recall; the licensed official API requires a separately authorized, explicit request. Until performed, no 12-source live index recall number exists.

## Acceptance matrix for the next *actual* finite test

For each distinct platform, freeze **at least one** known positive original source and **one** similarly worded negative control; ideally two historical positives with different dates. Record source creation, retrieval date, query syntax, endpoint, credentials/permission state (without secrets), request sent, HTTP status, response count, page size/cursor, known-positive rank or absence within the *observed* window, whether original post/comment/image was actually fetched, and whether it matched a known canonical object.

Priorities:
1. **Bluesky:** resolve two failed native searches and current generic-iam8bit false positives before wider expansion; add truly independent older positive controls, not Caswell-only recall.
2. **Public web index / Brave:** execute a *small* legally authorized portion of 24 blind gold tasks. Keep 10-result page cap explicit, and evaluate 10 scoreable controls separately from G05/G10 locator repairs. Preserve manifest SHA across resumptions.
3. **YouTube:** source-native discovery of G06 original unboxing should be measured separately from fetching its known URL; a video hit cannot stand in for G09's **comment**. Decode media/metadata status and comment extraction failures.
4. **Reddit:** do not hammer a backend that has recently returned 429; prefer explicit limited positive control after provider cooldown or source-preserving public archives, and record missing nested replies.
5. **eBay/Instagram:** first recover primary original source locators for G05 and G10; don't prematurely record provider search failures against invalid controls.
6. **Visual discovery:** use the merged HTML selection waterfall. Test source original pages, images skipped by CDN/policy/budget, original image bytes and legible sticker evidence independently.

All source contacts remain passive, publicly permitted and rate-limited; no owner outreach, account probing or private data gathering. No new physical sticker or decoded code has been added.

**Main next gate:** Exact-head CI must pass for this PR; then retain a versioned offline readiness artifact as the baseline to compare with all future *real executed* provider batches.
