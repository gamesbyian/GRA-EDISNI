# INSIDE CE: public Reddit comment photo recovery

**Research mode:** DISCOVER only, public archived comments; do not count text or links as newly seen physical stickers. **Added:** 2026-10-13, after [second image pilot](inside-ce-visual-second-live-pilot-2026-10-13.md). **Source docs:** [Arctic Shift API docs](https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md), [PullPush API docs](https://pullpush.io/).

## Why this lane exists

Original Reddit submission pages for three CE owner/sticker threads are HTTP 403 in GitHub Actions, but Arctic Shift successfully recovered metadata by post ID and a genuine image from 2019. That recovered image is **only a screenshot of iam8bit's public NOW SHIPPING marketing post, no sticker**. Reddit conversations can contain original photo links in comments that are *not part of the submission image metadata*. Finding those requires a separate, bounded archive query.

### Implementation

- `scripts/external_evidence/recover_reddit_comment_images.py`: for exact IDs from the existing six-source [public pilot manifest](../../data/reference/inside-ce-visual-historical-pages.json), call `/api/comments/tree?link_id=t3_<postID>` with explicit node limit/depth. If unavailable or no comments, fallback to the PullPush `/reddit/search/comment/?link_id=<postID>&size=100` **first page**. Never imply archived comments are complete: report `possible_partial_tree` whenever archive uses collapsed nodes or first-page fallback.
- Extract HTTPS links only from public, nondeleted comment bodies; preserve the post ID, original comment ID, comment permalink, archived timestamp if present, source archive SHA-256, whether the link is a directly permitted image host or a gallery/manual lead. No author identity or contact details are stored, and no outreach occurs.
- `scripts/external_evidence/fetch_html_images.py` accepts multiple optional `--additional-leads` JSON files and retains exact *per-image comment permalink*, rather than attributing all recovered images to the thread's top-level page.
- `scripts/external_evidence/visual_index.py` attaches that exact per-image page URL and original media URL to future candidate visual matching.
- The optional [CE visual workflow](../../.github/workflows/ce-visual-provenance.yml) has a new `archived_reddit_comment_images` flag; pair with `download_page_images` for bounded original-image retrieval. Neither runs on PR checks; CI checks only deterministic offline tests.

## Caveats and acceptance gates

Archives can be stale, incomplete, unavailable or inaccurate; a deleted comment does not imply present availability. Archived media URLs may point to expired/deleted hosts; never invent replacements. A photo belonging to one Reddit comment does not establish that every commenter in the whole thread owned a copy. If the body says “my sticker,” record that specific claim with its direct permalink and independently reconcile against known serials and lost `L`/unknown `U` cases before proposing a new lead.

Real-world discovery requires **media URL + retrievable original bytes + visual review + original comment context + canonical sticker-ledger reconciliation**. Absent those, queue a manual or archival lead, not a sticker observation.

A later run must explicitly report every source thread’s actual retrieved comment count, archive provider, incomplete-tree status and direct versus gallery link counts, even when zero.
