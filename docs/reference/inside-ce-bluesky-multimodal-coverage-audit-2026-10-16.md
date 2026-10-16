# Bluesky source retrieval: multimodal coverage and date semantics audit

**Date:** 2026-10-16. **Mode:** VALIDATE for search and parsing reliability, not sticker decoding. **Original source:** [16-query cross-year native Bluesky run 38869121304](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38869121304), archived artifact **12032825947**. The completed pilot returned **153 post appearances / 140 distinct AT URIs**, **14 valid responses / 2 failed search requests**. These are bounded returned results, not platform completeness.

## Confirmed provenance omission

The original `scripts/audit_bluesky_ce_recall.py` reduced each AppView post to AT URI, handle, source-author `record.createdAt`, text (capped to 450 characters), and known-control indicator. It **discarded** original AppView `embed.images` view metadata, `record.embed` image declarations, alt text, external embedded URLs, and `indexedAt`. Therefore a text-negative image-bearing post, or a relevant linked media source, could be **successfully retrieved from the source** yet be unrecoverable from the saved API artifact and its text-only lead queue. Such records were not proved absent.

An additional actual source date discrepancy was observed: one returned original post from `skywilly.bsky.social`, AT URI `at://did:plc:jqqb3pdkybmwhashro4mc4rl/app.bsky.feed.post/3lztdlwep3z2a`, carried `record.createdAt` in **July 2016**, despite the all-time discovery pilot applying `since=2023-01-01`. This is not proof Bluesky search implemented the range incorrectly: the source may filter or index by a different timestamp or return syndicated/imported records. The old artifact did **not** preserve `indexedAt`, so an honest retrospective judgment is unavailable.

## Fix and evidence ceiling

- Post extractor now retains `record.embed` media-declaration count and type, AppView visible image thumbnail/fullsize URLs restricted to unchanged `https://cdn.bsky.app` URLs, bounded alt text, original `indexedAt`, and public external embed URLs. These are **unverified hints**: no downloads, OCR, owner contacting or sticker claims.
- Each valid search response now records how many returned posts advertised public images, how many declared images without returned view URLs, and how many source-author timestamps lay outside the requested range. The last count explicitly does **not** claim a search-provider bug.
- Text lead triage remains separately conservative. An independent **image-led public metadata review queue** preserves media-bearing posts even when there is no relevant textual cue. It deduplicates on original AT URI, preserves search-match provenance, and marks `owner_verified=false`, `sticker_verified=false`, `original_image_retrieved=false`.
- A retained pre-fix raw-result artifact with no image metadata cannot be used to infer `0` image-bearing posts; its coverage report explicitly counts `posts_without_captured_media_metadata`. A **new user-authorized bounded native run** is necessary to reconstruct media fields lost by the old parsing step. Recapture is opt-in, not secretly scheduled.
- Source filters never attempt to resolve blocked posts or scrape additional account metadata. No new physical sticker was confirmed.

## Positive and negative regressions

Source-derived synthetic records now test a native post with `record.embed.images`, `embed.images` fullsize/thumb/alt, and distinct `indexedAt` vs `record.createdAt`. Tests require the metadata survives, the date outlier is flagged and original bytes remain unacquired. A separate image-only post, with unrelated or blank body, must appear in the **visual** review queue but **not** the confirmed-owner or ordinary text lead queue. Dedup across two query pages preserves its original AT URI and both query matches. Malformed CDN host/lookalike or HTTP URLs are refused; old text-only records are explicitly counted as uninspectable.

## Next measured action

After code/tests are integrated, dispatch one small, source-compliant Bluesky native search whose new original post responses include these media fields; compare the resulting visual metadata queue and text queue without conflating either with verified sticker imagery. In parallel continue blind native positive-recall work on other surfaces (as indexed by [the gold-control audit](inside-ce-cold-recall-controls-audit-2026-10-16.md)). Stop and record platform access refusals.

**Status:** pipeline capability correction, not a new CE owner, sticker number or original source photograph.
