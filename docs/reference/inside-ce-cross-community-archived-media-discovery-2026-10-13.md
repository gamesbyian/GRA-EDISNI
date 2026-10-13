# INSIDE CE archived cross-community public photograph search, 2026-10-13

**Purpose:** extend the working CE photo-provenance pipeline outside the original Playdead subreddit and promotional storefronts to Reddit's public collector, resale and gaming communities. The existing [82 verified sticker originals](../../archive/stickers/README.md) and the [20 publisher/press negative controls](../../data/reference/inside-ce-visual-sources.json) remain the fixed photo baselines. **No owner outreach, no credentials, no serial inference from text alone.**

## Why broaden now?

The October 13 source-pilot sequence recovered an original January 2020 sticker photograph and six PS4 reverse-cover photographs from historical archived **comments**, demonstrating why searching only submission titles or publicity imagery misses media. The original #171 photograph was byte-identical to the canonical sticker, so no new number was added. To find real additional leads, search **independent collector communities** and **historical resale postings** rather than repeatedly revisiting known iam8bit photos.

The [October 12 native owner hunt](inside-ce-native-owner-hunt-2026-10-12.md) already names an [unreconciled July 2020 GameSale offer](https://www.reddit.com/r/GameSale/comments/i0vgml/) with a CE, figure and sealed PS4 game, and an already known [December 2020 GameSale offer](https://www.reddit.com/r/GameSale/comments/k4wyvu/) tracked as U32. Use those as positive and duplicate-control retrieval fixtures, not instant new owner observations. A sale may involve the same physical copy crossing multiple hands.

## Implemented

- [Arctic Shift](https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md) documented `/api/posts/search` and `/api/comments/search` provide scoped, bounded public historical search. Post title/selftext `query` and comment `body` are used **with subreddit constraints** as required by the API.
- [Search manifest](../../data/reference/inside-ce-public-reddit-cross-community-queries.json): 24 predetermined requests across `r/GameSale`, `r/gamecollecting`, `r/PlaydeadsInside`, `r/limitedprintgames` and `r/PS4`. Topics include first-party brand, Huddle/RealDoll, edition, sticker and unboxing. Per-query cap 30, absolute cap 32 queries and 40/request; hard 500-record unique review ceiling. This is not equivalent to exhaustively scanning Reddit or all resale listings.
- [Search and media extraction](../../scripts/external_evidence/search_public_reddit_ce_media.py): exact HTTPS archive host/redirect limitation, 7-MiB response cap, bounded network timeout, schema validation, query-by-query SHA-256, explicit failure records, relevance gates that reject vague uses of *inside*, deduplicated post/comment IDs, original public Reddit permalink, UTC timestamp, only 240 characters of source-context excerpt without full outbound URLs, media link inventory. No account-name enrichment or unsolicited messages.
- Extract directly fetchable public images from Reddit/Imgur/known media CDN, with eligible exact links forwarded to the existing allowlisted public image downloader only when manually enabled. Gallery URLs are **review leads** rather than automatically crawled or accepted. The known physical source ledger is checked by exact post/gallery identifier before ranking unknown URLs. **Exact URL absence is an unreconciled link, not proof of a previously unknown owner.**
- [Existing CE visual workflow](../../.github/workflows/ce-visual-provenance.yml) has opt-in `archived_cross_community_search` for bounded requests, and optional `download_page_images` to hash/download eligible original media. CI uses offline synthetic controls only, plus indexing/sha-verifying the existing 82 canonical source photos.
- Outputs in disposable `visual-evidence-work/archived-market-discovery/`: `search-report.json`, `review-queue.json`, `image-leads.json`, `gallery-leads.json`. Artifacts are not automatically promoted into the canonical ledger or committed.

## Ground rules for sorting search results

The record's `source_status` is **only** `post-id-present-in-known-ledger`, `imgur-gallery-present-in-known-ledger` or `unreconciled-by-exact-url`; full sticker provenance requires reconciling against the entire known U/L transfer graph. A relevant post with an image attached does not mean the image shows a CE; a relevant sale with a CE photograph does not mean the white numbered seal appears in it. Review original photo bytes and context, identify standalone PS4 versus full CE, then compare against known original sticker photographs before promoting a source as materially novel.

## Calibration targets

1. Rediscover the old GameSale `i0vgml` listing and/or identify search coverage failures. If an archive query misses it, query an exact post ID separately instead of counting it as an absent listing.
2. Measure source record counts, bounded API failures, image/gallery hits, source duplicates, and manual visual review yield separately.
3. Feed any retrieved reseller photos into the already shipping visual provenance index; don't use CLIP similarity or OCR to claim printed serials.
4. Broaden to site-specific national resale sites and native-language forums using the **existing 50-locale lexicon** only after this small archive pilot establishes which query and media routes are productive; avoid treating English translations as native query variants.
5. For pages unreachable by direct HTML retrieval, use already approved public archival APIs or documented historical listing mirrors. Keep archive URL and original published URL both visible.

**Status when authored:** implementation and synthetic test suite; first broad live campaign has not yet run. Report actual results and errors before declaring any new source or physical sticker.
