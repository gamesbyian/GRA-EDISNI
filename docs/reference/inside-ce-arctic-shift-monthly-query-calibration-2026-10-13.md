# Arctic Shift query calibration: 422 responses are backend timeouts, not negative source searches

**Date:** October 13, 2026. **Research:** public historical CE sources, no owner outreach or sticker promotion.

## Verified root cause

The [first archive cross-community pilot](inside-ce-first-cross-community-archive-pilot-2026-10-13.md) returned 9 HTTP 422 plus 14 HTTP 429 and just one successful search. It was initially unclear if 422 meant unsupported query filters or server capacity problems.

A deliberately limited [four-query live calibration](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38491665222) asked for one multiword GameSale term plus three single-term source slices across `r/limitedprintgames`, `r/PlaydeadsInside` and `r/gamecollecting`, 15 results/request. **All three attempted requests returned HTTP 422 with the identical provider JSON: `{"data":null,"error":"Timeout. Maybe slow down a bit"}`.** The fourth request was automatically marked `not-attempted` after the safe 3-failure stop. Therefore no result records were retrieved. These are **provider-side timeouts**, neither invalid search terms nor evidence of zero CE posts.

The [Arctic Shift public API](https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md) documents `/api/posts/search` with `query`, `title` or `selftext` constrained by subreddit and `/api/comments/search` with `body` constrained similarly. It warns searches of large/active subreddits may time out. The original code used `after=2018-01-01` through `before=2026-10-14` for **every** query, forcing eight-year scans even when researching 2019 sticker launch.

## Corrected bounded retrieval method

[Public archive search](../../scripts/external_evidence/search_public_reddit_ce_media.py) now accepts explicit per-entry `after` and `before` ISO 8601 dates. Supplied windows must be positive and at most **366 days**; old manifests without date fields retain previous behavior for backward compatibility, but broad query campaigns remain discouraged.

HTTP 422 with provider body containing `timeout` is now explicitly classified `archive-backend-query-timeout`; subsequent queries in that run become `not-attempted` rather than another accidental request storm. Three consecutive other 422 errors still trigger the previous protective stop. HTTP 429 always stops immediately. The review log retains the actual searched dates on successful calls, raw provider error snippet and source response SHA when retrieval succeeds. All candidate evidence remains review-only.

[One-month pilot manifest](../../data/reference/inside-ce-public-monthly-reddit-calibration.json) tests a positive-control September 2020 GameSale `realdoll` query (known U32 reposts) and three December 2019/January 2020 release-period niche subreddit query slices. This will determine whether narrower date ranges actually improve execution. Success in one month **does not** establish comprehensive Reddit coverage; failed slices are `unavailable`, never empty-result claims.

## Independent source-first progress

While diagnosing backend searches, an independently indexed [March 8 2026 public CE split-sale](inside-ce-march2026-disc-separated-acquisition-2026-10-13.md) was found and preserved with verified original comment ID and author. The sticker-carrying game-wrapper component might have remained with the reseller, but this is not confirmed. It is a high-priority **textual lead**, not a new number or proven physical edition. This shows why non-archive web search and exact Reddit post/comment ID verification should remain independent of bulk archive search health.

**Current conclusion:** the API's full-range keyword search is not a reliable absence detector. Prefer source discovery by public web search, known-public-ID archival lookup, and narrowly scoped historical archive windows.
