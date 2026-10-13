# 2019 first-person collector photograph: independent INSIDE CE packaging evidence

**Observed / reviewed:** October 13, 2026. **Original Reddit publication:** December 14, 2019. **Status:** real first-person CE photograph, no numbered sticker visible. **Owner case:** already known **L08** (canonical lost sticker; public account Knuckles316). No new physical owner or serial confirmed; no outreach.

## Resolved public source identity and case

Original public post `eaktdt` → archived public author `Knuckles316` → **existing community L08**. The sticker ledger tracks the account, not this exact photo-post ID. The first exact-URL search therefore produced a false 'new owner' impression, resolved by checking the original public account against canonical owner-case text. No account-profile crawling, messaging or other outreach occurred.

## Exact primary evidence

- Original [2019 r/gamecollecting post `eaktdt`](https://www.reddit.com/r/gamecollecting/comments/eaktdt/) titled **“The INSIDE collector's edition finally came in!”**. The author describes preordering, physically receiving and opening the set. In the comments, they say they deliberately kept the covered Huddle from appearing fully in the picture.
- Original [uncompressed public JPEG at Reddit CDN](https://i.redd.it/xat8isnm7m441.jpg) (4032×3024 pixels; **1,185,588 bytes**; SHA-256 **`cd095cdfcfc9179d632876cceb8a3744da46e3248c34f7ad1bc2e3d301a129df`**).
- Additional [Reddit WEBP preview](https://preview.redd.it/xat8isnm7m441.jpg?auto=webp&s=55586d4b53e9da18f2294b0345255fc0b40b9438) (948,278 bytes; SHA-256 `74f9872852d810dcc05cb715959dd2b65a12bb42547a84763a72b0118b9e18ea`); another rendering of **the same photograph**, not another owner.
- Original post archived and original photo bytes recovered in completed [GitHub Actions run 38472506860](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38472506860), original [artifact 11852601900](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38472506860/artifacts/11852601900) (30-day artifact retention). The public archived post metadata response SHA-256 is `d7dcfe8fd7206410983a0ba725dbc6c956dc6f06703ee015b8c7d89a685a4527`.
- The archived comment-tree query retrieved **11 comments** and zero directly linked image/gallery URLs. Original comment-index response SHA-256 `7c200574e38ca6eaffb4f4f2f5ded3227851cc486a62313df156885abac5116f`. An incomplete or removed historic comment cannot be excluded by this count alone.

## Direct visual review at the original 4032-pixel resolution

The photo is a **private indoor snapshot** of the premium INSIDE collector's edition box opened on someone's lap/sofa, not an iam8bit art-directed marketing scene. The distinctive red/black outer presentation box, inner `CONTENTS` card, left-side PS4 game case with visible blue spine, large dark plastic bag containing the covered Huddle, clear figure/stand mounting frame and tiny plastic-wrapped Boy figurine are visible. There is no readable white serialized seal on the box, game, packaging, or at the margin of the image. **The photographed game case is no longer enclosed in the original black numbered paper wrapping**, to the extent visible; do not conclude the sticker was discarded or irrecoverable from this photograph alone.

The internal contents card includes the wording “INSIDE FOR PS4” and “EXCLUSIVE PHYSICAL EDITION, LIMITED TO 2,000 COPIES.” The wording refers to the **physical PS4 release**, not necessarily the number of complete collector boxes and not a proven production limit for serialized CE stickers. This should **not** be fed into code-length/600-ish-edition assumptions without independently verifying Playdead's edition policy.

## Comparative result

The actual two retrieved image files were compared with **82 canonical original sticker photographs** plus **20 publisher/standalone/press controls** via `visual_index.py`. Both were unmatched: 0 reference matches. The subsequent public account reconciliation demonstrated they belong to **already-known lost-sticker case L08**; a novel image or post URL alone would have been an unreliable signal of a novel owner.

### New positive-control class

The SHA-locked full-resolution JPEG is now an image reference with `role=positive-control-public-owner-open-ce-no-visible-sticker` and explicit **`canonical_case=L08`**, mapped to `historical-owner-photo-no-visible-sticker`. Future exact/reencoded reposts should be classified `known-owner-photo-repost-review`, rather than promotional artwork, known numbered sticker, or a newly confirmed physical copy. A regression enforces this.

## Qualification and useful follow-up

This is new **photographic provenance for previously known case L08**, not a new CE owner or sticker. The original post's archived public author is **Knuckles316**, whose exact username occurs in the [canonical community ledger](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) as **L08, sticker confirmed lost**, recorded January 28, 2020. The [one-shot public post-ID source comparison](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38473137674) confirmed this exact name match and original 2019 photo's date. Do not forward this as a new owner to raezores. The picture offers a valuable earlier historical view of that same collector's copy, but cannot establish why or when its sticker was lost.

The original 2019 high-resolution photograph remains retrievable via its exact Reddit CDN URL and under the 30-day GHA evidence artifact. Preserve its known digest so subsequent retrieval cannot silently substitute a different photo.

**Sticker result:** no number, symbol or background read; no canonical sticker observation created.
