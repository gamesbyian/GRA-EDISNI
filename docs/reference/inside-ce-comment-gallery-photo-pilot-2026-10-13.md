# INSIDE CE historical comment-gallery photo pilot: verified sticker 171, no novel serial

**Date:** 2026-10-13. **Research:** public-source DISCOVER, then visual/source-hash adjudication against established physical originals. **Run:** successful [GitHub Actions 38462782091](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38462782091), original [artifact 11846242785](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38462782091/artifacts/11846242785) (30-day retention). **Sourced APIs:** [Arctic Shift comments tree documentation](https://github.com/ArthurHeitmann/arctic_shift/blob/master/api/README.md), [gallery-dl CLI](https://github.com/mikf/gallery-dl). **Canonical:** [twinysam INSIDE-ARG sticker ledger](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md).

## What the comment archive actually recovered

The previous source-page pilot could recover historical Reddit submission metadata but only the publisher's **NOW SHIPPING** screenshot. The new exact-ID public **comment-tree** retrieval recovered:

| Original thread | Archived comments | Complete per API? | Public gallery links | Direct standalone image URLs |
|---|---:|---|---:|---:|
| [2019 owner display](https://www.reddit.com/r/PlaydeadsInside/comments/eers0x/) | 5 | No collapsed nodes reported | 0 | 0 |
| [2019 shipping](https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/) | 34 | No collapsed nodes reported | 2 | 0 |
| [2026 PSA](https://www.reddit.com/r/PlaydeadsInside/comments/1wruv2d/) | 1 | No collapsed nodes reported | 0 | 0 |

All three returned via Arctic Shift comments-tree without needing the fallback. Response SHA-256:
- `eers0x`: `85db6efe1571400f66d5233016c637079de5f4c8754b2a3f0b38fdd8f787d68d`.
- `e9bteo`: `82d73cd289812fbbc3ec7be71504e89a999428557c8b417196d73259d74ccb29`.
- `1wruv2d`: `ca143d463599fa119aa0e40dd674e6883859dd4d5a7d391f01fdb90e30e432fb`.

**Caveat:** No tree collapse detected does not guarantee complete historical capture, intact deleted comments, complete edit histories or live-source parity. These are the numbers returned by this archive query.

### Gallery 1: reversible PS4 cover, historical positive control

- Exact owner-archive [Reddit comment](https://www.reddit.com/comments/e9bteo/_/favh0go/): **2019-12-14 21:26:57 UTC**.
- Public [Imgur gallery ipjWYEz](https://imgur.com/gallery/ipjWYEz), title `INSIDE x Iam8bit x RealDoll reverse cover`.
- **6 original photographs** successfully recovered with `gallery-dl`, all inspected together as a contact sheet. They depict the INSIDE reversible PS4 cover art, including the clock and interior workstation imagery; no numbered CE seal appears.
- This link is already documented under **PS4 cover hidden mystery** in the original [twinysam INSIDE-ARG research](https://github.com/twinysam/INSIDE-ARG). It is a successful retrievability/dated-source positive control, **not a new CE sticker or owner lead**.

### Gallery 2: real numbered seal, existing #171

- Exact [Reddit photo-bearing comment](https://www.reddit.com/comments/e9bteo/_/ffptzb1/): **2020-01-27 06:13:51 UTC**. The comment says *“Inside collectors seal”*, links the gallery and notes that a cell-phone camera was the best available. That is contextual first-person photo provenance, not evidence of a new sticker.
- Public [Imgur gallery YLXcetH](https://imgur.com/gallery/YLXcetH), title `Inside collectors seal`; precisely **one image**.
- Exact original [Imgur media file](https://i.imgur.com/mOHC6nr.jpg) was downloaded, **857,634 bytes**, SHA-256 **`fc1bde45ecc8c7504c81729c3ec4fdebd60af83e3c649630fce63a21eaa068db`**; gallery-dl metadata records **2020-01-27 06:10:44 UTC**.
- The photo visually shows the complete sticker number **171** with a large **slash**, over one of the faint patterned backgrounds. The visual reference matcher found a **byte-identical match** against the physically accepted original `archive/stickers/originals/171/171.jpg` (manifest: **171 = slash, background I**).
- The older canonical [community sticker ledger](https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md) already attributes #171 to the Dec 14, 2019 owner/unboxing provenance. The recovered Jan 27, 2020 Reddit/Imgur trail is an **additional public posting of exactly the same physical photo**, not another edition or another independent observation.

### Verification and known failure

The first comment-media CI run [38462449708](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38462449708) correctly extracted the two gallery URLs but encountered a zero-direct-image downloader error. The subsequent Imgur photo run **38462782091 passed**, preserving seven original photographs, gallery-dl sidecar JSON, public comment links, 20 separate publisher-negative photo references, and visual SHA comparisons. It returned one canonical #171 match.

**Provenance-export defect discovered in the one-off runner:** its ad hoc `acquisition.json` writer emitted a trailing literal backslash-n, invalidating that JSON file. Consequently the visual matcher reported blank `candidate_source_url` even though the original archive and extracted comment records preserved the correct source URLs. The photographed bytes/hash and original Imgur metadata are unaffected. The new tested `index_public_imgur_gallery.py` uses valid JSON, reconstructs source-page and media-permalink metadata **per photograph**, and verifies original file bytes/dimensions/metadata before indexing. The reusable manual CE visual workflow can now acquire/index the two exact historical galleries with limits and fail/report unavailable sources.

## Interpretation

**Discoveries:** two explicit historical Reddit comment → Imgur source trails; seven verifiable original media downloads; a second known published source for **#171**, plus six genuine early PS4 reverse-cover reference photos. Historical media recovery and the exact-image recognizer work on actual independent archive services.

**Sticker outcome:** **0 new numbered stickers**. **0 new physical owner cases** proven. The new #171 gallery link is source provenance for a **known** sticker. Neither the same canonical photo at another URL nor multiple old comments should be counted as independent stickers.

**Next source class to prioritize:** other publicly accessible 2018–2021 owner unboxings and marketplace galleries whose original URLs differ from the known physical photo archive; run exact/near-duplicate checks before creating a lead for raezores. The current pilot demonstrates that archive retrieval yields real original evidence rather than merely search snippets, but quantitative *novel-owner recall* remains unmeasured.
