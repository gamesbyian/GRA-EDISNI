# INSIDE CE: full-size public photographs and cursor-followthrough verification

**Date:** 2026-10-16. **Mode:** VALIDATE source-image inspection and source-native query evidence, with DISCOVER followthrough for previously incomplete searches. See the [exact one-time GitHub Actions run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38885283710) and its original three-image / native-source artifact **12038842963** (14-day retention), along with the persistent [SHA-pinned machine-readable findings](../../data/reference/inside-ce-bluesky-visual-followthrough-2026-10-16.json) and [frozen original image URLs](../../data/reference/inside-ce-bluesky-visual-source-pins-2026-10-16.json).

## The actual images, not alt text or promotional image search

All three public source URL images downloaded correctly as **WebP** with strict size bounds and SHA-256 preservation, and were directly reviewed at their native fullsize CDN resolutions. The two posters are art-card prints, not physical sticker evidence. **None of these images shows a numbered sticker or packaging wrap.** This is a negative result restricted to **these three inspected frames**, not a claim that the subjects never received, retained or photographed stickers elsewhere.

| Exact public source | Photo dimensions | SHA-256 | Observed visual content | Evidential ceiling |
|---|---|---|---|---|
| [Tom Caswell, Aug 16 2026](https://bsky.app/profile/tomcaswell.games/post/3mta6ecjbvk2i) | 3000 x 3999 | a5f703eeed6d561631cb31535ccf65b31e266f92036fb0582ba15f975e28d191 | An orange/flesh-toned Huddle statue being held in a hand, with ordinary room furnishings behind it. **No box, seal, number or sticker visible.** | Real Huddle object; no sticker observed. Already forwarded to Raezores, no repeat contact. |
| [Telemon, June 29 2025](https://bsky.app/profile/telemon.bsky.social/post/3lsqjezdwgc2z), image 1 | 1023 x 1023 | c407b74916ae4278f2524f625f6ad450bb722b045b38de93d86837137f37f59f | Game screenshot of Huddle in a dark, wintry scene. | Does not show CE packaging. |
| [Same Telemon post](https://bsky.app/profile/telemon.bsky.social/post/3lsqjezdwgc2z), image 2 | 1429 x 2000 | b5b521f371e1ad9aa56a84e93450aab7f40e2ca80a1ff08a5dd0a8db59a46157 | Two INSIDE Huddle concept-art prints laid out on a wooden table. | CE art-card presentation only, no sticker or owner-identifying serial. |

Prior community source context still stands: Discord **Telemon** furnished physical sticker **/449, background H**, in August 2024. We have not independently matched that Discord identity to the June 2025 Bluesky account. One person's publicly posted art cards should not be promoted to a second owner without further evidence.

## Retrying two timeouts and following first-page cursors

The earlier [16-expression Bluesky native recapture](inside-ce-bluesky-media-recapture-2026-10-16.md) returned 14 valid queries, had **two timeouts**, and left **two first-page cursors** unexplored. Before this followthrough, a frozen four-key task manifest specified precisely those omissions, with **at most six** official public search requests and a hard stop for HTTP 401/402/403/429. No owner names, IDs or serial numbers were added to the queries.

| Intended check | Actually attempted? | Source outcome | Interpretation |
|---|---|---|---|
| Retry playdead + inside + edition | Yes | 200-equivalent parse, **3 posts** | Molonara's already known community ARG appeal, a Playdead games comment and a tabletop RPG comment. No new owner or CE serial. |
| Retry inside + numbered + sticker | Yes | Valid **15-post** first page | General sticker/collector conversations about other merchandise, not new INSIDE CE owner evidence. |
| Refetch inside + sticker first page to obtain native cursor | Yes | Valid **49-post** first page with cursor | Returned previously seen generic sticker references, no new relevant sticker observation. |
| Use that source cursor for the next page | Yes | **HTTP 403 Forbidden** | Provider refused this exact cursor request. This is *not* a negative result for page two and is not grounds to change endpoint or bypass access. |
| Refetch inside + cipher and follow its cursor | **No** | Explicit `not_attempted_after_provider_block` | Not searched. Earlier first page remained unexhausted. |

Exactly **four** native search requests were made rather than the six-request ceiling. The 403 stopped all remaining public native search calls. Three successful query responses returned **3 + 15 + 49 = 67** post appearances; 18 source AT URIs were not in the preceding 133-post pilot because their two queries had timed out previously. None of these 18 is a new verified INSIDE CE owner/sticker.

These four executed requests and three photograph retrievals are independent steps. No second page was successfully obtained. The 403 affects the particular cursor request, **not** a proven platform-wide search ban. All response metadata and original JPEG/PNG/WebP bytes are in the 14-day artifact; source photos are not copied into the repository.

## Methodology and future work

The image-caption regression from [PR #296](https://github.com/gamesbyian/GRA-EDISNI/pull/296) remains valuable even though original photographs reveal no sticker: text-only review failed to recover Telemon's CE concept-art provenance, and image alt text did recover it. Direct photographic inspection now closes these **individual** visual leads.

The remaining Bluesky blind spots are: additional pages of `inside_sticker` and `inside_cipher`, source-native platform rank/date behavior, truly uncaptained photographs in less noisy CE-specific queries, and queries that do not use ordinary ambiguous words. Preserve the 403 as a provider-boundary observation. Better next work at modest budgets is independent known-positive recall and targeted source images on Reddit, eBay and YouTube, not repeated attempts at the forbidden cursor URL.

**No new physical sticker observation; no new CE owner confirmed; no decoded sticker result.** Only three source images were actually inspected. No outreach took place.
