# INSIDE CE cross-community archive pilot: two 2020 resale reposts, degraded keyword coverage

**Observed:** 2026-10-13. **Original completed public-GitHub-Actions run:** [38467083410](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38467083410), [source artifact 11849605186](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38467083410/artifacts/11849605186) (30-day retention). **Code baseline:** merged PR [#245](https://github.com/gamesbyian/GRA-EDISNI/pull/245). **Mode:** source DISCOVER only: do not promote any new owner, physical copy, symbol or serial.

## Direct observations

The first 24 bounded public Arctic Shift Reddit collector/resale queries returned **1 successful query**, **9 HTTP 422 query rejections** and **14 HTTP 429 rate-limit failures**. (The individual status and error details, along with the SHA-256 of successful archive JSON, are preserved in `search-report.json` in the Actions artifact.) Zero direct image/gallery URLs were returned by the successful query, and therefore zero candidate photos were downloaded. It would be materially incorrect to call this an exhaustive search or to claim that 23 source slices contain no evidence. Initial runner erroneously continued after 429, which is now corrected.

The one successful archived query was `r/GameSale` / posts / `realdoll`, dated 2018-01-01 through 2026-10-14, `limit=25`; it returned two relevant archived posts, archive response SHA-256 **`0d3ef592e5604b69dddadd7bd7e8c7b6e079b0de2a8250062295f279752bc012`**.

### Unreconciled public **resale postings**, not yet new owners

| Original Reddit URL | Original timestamp (UTC) | Archived post title and description | Reconciliation |
|---|---|---|---|
| [`iuutfq`](https://www.reddit.com/comments/iuutfq/) | 2020-09-17 23:23:06 | `[US - CA] [H] Inside iam8bit Collector's Edition [W] Paypal, LRG Trades`. Excerpt: includes RealDoll Huddle, new sealed components, unsealed presentation box as originally released. | Absent by exact post ID from captured canonical `stickers.md` and prior native-owner hunt. No picture or numbered seal acquired. |
| [`izs23a`](https://www.reddit.com/comments/izs23a/) | 2020-09-25 21:06:44 | Identical title and near-identical beginning of archived description to Sept 17 post. | Treat as likely **relist of same physical CE**, NOT an independent copy. No picture or numbered seal acquired. |

Source-finding does not establish either a new copy or a new owner; full description and historical commentary must be fetched, then checked for the possibility the seller/CE was already counted under a canonical `U`/lost sticker or the earlier GameSale resale case. Original archived text `context_excerpt` is deliberately capped at 240 characters and does not include personal account or contact details.

**Older comparison:** [July 2020 GameSale `i0vgml`](https://www.reddit.com/r/GameSale/comments/i0vgml/) was already listed as an *unreconciled* CE resale lead in [October 12 native-owner hunt](inside-ce-native-owner-hunt-2026-10-12.md). The September posts are **not presumed** related to the July offer. [December 2020 GameSale `k4wyvu`](https://www.reddit.com/r/GameSale/comments/k4wyvu/) is already the known U32 case. These four exact IDs and a known shipping-thread control are now stored in [public resale post target registry](../../data/reference/inside-ce-public-archived-resale-posts.json) for a *single API posts/ids request*, independent of unreliable full-text search.

**Actual eBay cross-check:** public [item 257753799919](https://www.ebay.com/itm/257753799919) is a plausible current CE listing, but already documented in the original [community sticker ledger](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) as sticker **/047** in a known transfer chain, so it is **not a novel CE owner/sticker lead**.

## Required API behavior correction

The initial 24-request run did not respect an initial HTTP 429, continuing with 13 further destined-to-fail requests. The response code is a *real source-provider access limit*, not a negative result. The corrected [cross-community search utility](../../scripts/external_evidence/search_public_reddit_ce_media.py):

- captures up to 1,200 bytes of HTTP error body and records `Retry-After` (if present), without storing credentials;
- stops immediately on 429 and marks later queries `not-attempted`;
- stops after three consecutive 422 responses so unsupported/broken text-search syntax cannot trigger a flood;
- sleeps 1.5 seconds between live requests, runs **at most eight query slices by default**, and permits explicit `--start-query N` so a later run can resume a different finite slice without restarting already-run queries;
- retains per-query status, source responses and individual media links separately; `not-attempted` entries never become 'no leads found';
- adds an exact public post-ID lookup route for five preidentified cases, using `/api/posts/ids?ids=...`; known archive errors and missing records have distinct statuses.

These changes are backed by deterministic mock regressions for 429, successive 422, successful intervening queries, direct CLI invocation and missing exact IDs. No newly extracted number or sticker is promoted.

## Next practical step

Run the one-request *exact post ID* lookup on a fresh bounded Actions job, **without** keyword searches in the same run. Review returned full original descriptions, source media fields and comment references for those September reposts, July resale and U32 known control. Use a 30-day artifact; classify whether the listings are copies, sales, repeat postings or already-known objects before proposing raezores a genuine new lead. Delay further Arctic Shift keyword campaigns until 429 retry/reset information permits respectful use; prefer source-specific archived page or seller photo mirrors during the cooldown.

**Communication boundary:** two 2020 historical resale URLs can be investigated, but they are **not yet two new CE owners, and not evidence that either has a readable sticker**.
