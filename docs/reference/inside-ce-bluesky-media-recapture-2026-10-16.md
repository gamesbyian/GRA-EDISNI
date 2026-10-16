# INSIDE Collector's Edition: native Bluesky image-led recapture, October 16 2026

**Mode:** DISCOVER using a *previously frozen* 16-query source-native search manifest, interpreted with VALIDATE evidence discipline. **Execution:** [source-pinned GitHub Actions run 38882275551](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38882275551), with original API responses, text- and media-review queues in artifact 12038316873 (30-day retention). Persistent [machine-readable source crosswalk](../../data/reference/inside-ce-bluesky-media-recapture-2026-10-16.json). No physical sticker observations or owner outreach.

## Design and measured coverage

Before [PR #293](https://github.com/gamesbyian/GRA-EDISNI/pull/293), the source extractor discarded public image captions, image/CDN preview URLs, external embeds, and indexedAt while retaining only 450 characters of post text. This repeat uses the exact prior 2023–2026 query expressions, official primary AppView, a one-page limit of 50 and 1-second request spacing. No source username, post key or known sticker number was used in discovery.

| Measurement | Result |
|---|---:|
| Executed public search requests | 16/16 |
| Valid source-native replies | 14 |
| Provider timed-out queries, not empty results | 2 |
| Post-result appearances | 147 |
| Unique original post AT URIs | 133 |
| Appearances with image metadata | 67 |
| Unique posts with image previews | 61 |
| Unique posts with external-link embeds | 40 |
| Distinct media/link review candidates | 101 |
| Image-preview posts with blank original captions | 8 |
| Distinct posts passing text relevance filter | 5 |
| Additional INSIDE CE-specific source revealed by original image captions | 1 |
| Original photograph bytes downloaded or visually decoded | 0 |
| Newly confirmed owners, symbols or sticker numbers | 0 |

Timed-out expression labels: **playdead_inside_edition** and **inside_numbered**. The valid first pages of **inside_sticker** (49 returned) and **inside_cipher** (48 returned) retained further-page cursors; those pages were not followed. Neither provider errors nor first-page-only coverage may be used as evidence that no other posts exist. The 101 media candidates comprise 61 image-preview posts plus 40 external-link posts, not 101 distinct photographs.

The prior cross-year run had 140 distinct post URIs, while this replay had 133. The provider errors affected different queries. This is two bounded snapshots with different failed queries, not a measured change in platform-wide recall.

## Source-reconciled references

- **[Tom Caswell, August 16 2026](https://bsky.app/profile/tomcaswell.games/post/3mta6ecjbvk2i).** His original question about still needing the Collector's Edition statue now has one preserved image preview, but **blank alt text**, and source indexedAt 2026-08-16T21:53:16.966Z. The lead was previously sent by the user to Raezores. The image has not been visually verified as showing a sticker or intact packaging.
- **[Telemon, June 29 2025](https://bsky.app/profile/telemon.bsky.social/post/3lsqjezdwgc2z).** The body describes a work inspired by “The Huddle” without naming INSIDE or Collector's Edition, so the old text gate discarded it. The original image caption expressly says **“Concept art cards of The Huddle, from INSIDE Collector's Edition.”** Two original media descriptions and two public image previews survived. This is the sole high-specificity image-caption rescue in 128 text-rejected results. Importantly, [the community sticker register](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) already identifies a **Discord member named Telemon** as provider of sticker **/449, image H**, on August 2 2024. That suggests an existing-owner cross-platform lead, not a new owner or new sticker. We have **not** independently established that both accounts belong to the same person, and a picture of the art cards is not a sticker photograph.
- **[iam8bit.com, June 29 2026](https://bsky.app/profile/iam8bit.com/post/3mphksb3pku2h).** Anniversary publisher post linking [video gqlQaHgRaHg](https://youtu.be/gqlQaHgRaHg), already known to the community as U01 (IGN). Publisher-origin crosslink, not a fresh object.
- **[StrayCatalyst, September 24 2026](https://bsky.app/profile/straycatalyst.bsky.social/post/3mwagj42at22f)** and **[Fedorasaurus, September 22 2026](https://bsky.app/profile/fedorasaurus.bsky.social/post/3mw3b352tsc2v).** Existing puzzle discussions and an appeal for owners, respectively. Neither asserts possession.
- **[GiantBombForever, March 30 2026](https://bsky.app/profile/giantbombforever.bsky.social/post/3miaqe4kjop2h).** Repost of already documented Giant Bomb 2019 original unboxing video U02 / L35.

## Reproducible improvements after inspecting source evidence

The media queue now prioritizes original image captions containing the INSIDE Collector's Edition title **and** a distinctive Huddle/Playdead context, independent of unrelated post text. It does not promote media relevance into owner verification. An executable regression uses Telemon's exact two captions as the positive, and a Terminator 2D: No Fate product image whose alt text says “Inside Collector's Edition tin” as a negative. Caswell's blank-caption photograph stays unknown rather than excluded. The original 101 media/link records, including unrelated results, stay preserved.

Eight original image-bearing posts had no meaningful alt text, so a text/alt-only search cannot inspect their contents. The image retrieval, media-recognition and code-readability stages would be a *different* experiment; this run did **not** acquire or decode image bytes. The source-author creation date of a French post is July 2016 but its native indexedAt is September 2025, within the requested search window. This is a plausible explanation for the discrepancy without proving how the provider's date filter works.

A temporary **PR-opened-only** workflow issued this single bound-edition replay because the available connector cannot dispatch manual GitHub Actions. It must be deleted before integration. Future searches remain manual opt-in; PR updates must not repeat the 16 live queries.

## Next source-specific gates

1. Retain both media positive controls, Telemon with descriptive captions and Caswell with empty captions, but withhold their identities from blind discovery queries.
2. If investigating original photographs, limit acquisition to candidate-specific, permitted public CDN images, recording success and original bytes, not treating a stock art-card picture as a numbered sticker.
3. Cross-validate native Reddit, YouTube, eBay and Wayback gold-control recall using the existing cross-platform audit and exact source URLs. Preserve timeouts and untraversed result pages as censoring.
4. Do not contact Telemon, Caswell or any other owner from the automated pipeline. Reconcile with canonical owner/sticker records before offering any human lead.

**Evidence ceiling:** one previously missed *image-caption retrieval path*, no newly confirmed owner or sticker, and no decoding advancement.
