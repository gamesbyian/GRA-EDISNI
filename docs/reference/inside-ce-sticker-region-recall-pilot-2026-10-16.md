# INSIDE CE image region matching: controlled feasibility pilot (16 October 2026)

**Purpose:** Test whether a small marked paper sticker in a larger public collector photograph is recoverable by bounded, multi-scale region matching. **Mode:** RESEARCH / falsifiable instrument, not a working sticker detector or a claim of recovered serials. No owner outreach, OCR, API calls, scraping, model downloads, or automatic physical claim promotion.

## The central challenge

The existing `visual_index.py` uses full-frame and 75%-crop dHash/aHash comparisons. That is useful for photographs reposted with compression/resizing or slight cropping, but cannot reliably find a sticker occupying perhaps 2–5% of a photograph. The referenced sticker photographs themselves commonly contain an entire dark wrapper, sticker paper, glare, serial and shadows. Full-reference hashing therefore represents a whole **photo**, not a unique visual signature of the sticker serial. The pilot explicitly crops five genuine source-pinned physical photographs first, then searches many candidate windows independently.

## First five physically grounded, visually inspected ROI annotations

[Original-photo crop manifest](../../data/reference/inside-ce-sticker-region-pilot-rois.csv) includes **003, 037, 038, 065 and 125**. Each has the exact approved `archive/stickers/originals/` file path, repository original-source SHA256 and normalized sticker-paper coordinates. Annotations derive from manual inspection of the corresponding source photographs. The crop's serial is already known; that label is attached to *reference provenance only*, never inferred as the serial of a new image. Reference source SHA drift is a hard error. In initial manifest construction, several duplicate derived resized rows appeared later than the original rows. This was caught and corrected before the code's reference loader; the loader now requires the `originals` subtree and exact pinned SHA.

## How the bounded ROI scan works

- Candidate inputs are **already acquired** images in the existing visual provenance index. Each candidate's recorded SHA256 must match the file actually scanned; no known-URL fetching is performed.
- Original photos are EXIF-oriented. Each reference crop is fingerprinted at four right-angle rotations using 64-bit dHash and aHash. No trained model and no claim of learned recognition.
- Candidate proxy images are downscaled only for comparison, up to 1100 px on the longest side. Proposed windows span eight relative sizes from 7.5% to 75% of the image's shorter side and three aspect ratios, with overlapping location grids. Default maximum **1600** scored windows per candidate, and **48** candidates per run. Original image coordinates are retained for follow-up review.
- When the budget excludes windows, record **total proposals, scored windows, omitted windows, available strata, sampled strata**, and `not_exhaustive_when_capped`. The cap is sampled across scale/aspect strata rather than silently using only the earliest-smallest region.
- Rank regional similarities by aggregate fingerprint distance, then spend at most **1200 additional** windows on a **separately accounted coarse-to-fine pass** around up to 16 spatially distinct promising regions. This is intended to recover the full paper boundaries when the first pass finds only the dark mark inside the sticker. Report refinement seeds, proposed/scored/skipped windows and combined fingerprint count; suppress overlapping near-duplicate suggestions; preserve up to eight different review locations. **No threshold is calibrated to distinguish real sticker from ordinary white paper, printing, game boxes or other dark marks.** Every row says `unvalidated-region-similarity-only`, `new_sticker_confirmed=false`. A best matching reference's known serial is NEVER a candidate's new serial.
- The existing source-first contact sheet and source-image hash/marketing negative controls still apply. No standalone-game photo is independently sufficient to establish CE ownership.

## Tests and what they do not prove

The synthetic-scene tests use the actual source SHA-pinned crops from the five manually inspected sticker photographs: resize and paste them into a cluttered mock collector-table photo, include one 90-degree-rotated example, and check if a reasonably overlapping region is included in top review results. Other tests ensure invalid paths and mismatching image digests are rejected, fixed budget accounting, repeatable proposal selection, rotation variants and that a lookalike white rectangle **does not imply a new sticker**.

**Critical scope limit:** pasting the very same original sticker image into a background is effectively a transformed near-duplicate test. It is *not* independent evidence that an untrained matcher will recognize different instances of the same sticker class, unreadable serial text, new symbols or genuine phone-camera perspective distortion. The uncalibrated score must not be called a probability. A live masked/negative evaluation set remains necessary.

## How to run

After explicitly acquiring permitted public candidate images through the existing manual `CE visual provenance` workflow, opt in to `run_region_pilot=true`, or run locally:

```bash
python scripts/external_evidence/visual_region_probe.py \
  --repo-root . \
  --roi-manifest data/reference/inside-ce-sticker-region-pilot-rois.csv \
  --candidate-index visual-evidence-work/candidate-index.json \
  --candidates evidence-work --max-files 48 --max-windows 1600 \
  --output visual-evidence-work/region-suggestions.json
```

The workflow uploads the JSON with the pre-existing review-gallery artifact. In ordinary PR checks only synthetic tests run; **no external image download or provider search is made**. A zero candidate count is a valid no-data report, not absence of stickers on the Internet.

## Next falsifiable experiments before larger deployment

1. Measure held-out **real** source-photo localization precision/recall on independently collected, permitted photo pairs where a known sticker is physically present at differing scale/angle/lighting. Compare against hard lookalikes (white paper, PS4 cases, official promotions) and the current full-image matcher. Include the *unranked/discarded proposal* set in false-negative auditing.
2. Compare three proposals at the same per-image CPU and 1600-window limit: this hashed ROI baseline, PDQ/perceptual feature localization, and an opt-in local patch-embedding model. Do not automatically import large model weights or introduce opaque scores as ownership evidence.
3. Add a review visualization of the candidate region boxes and their original-source image coordinates. Require a human to inspect serial/symbol and check current canonical [numbered/L/U] cases before forwarding anything.
4. Assess whether the region search actually finds useful new original-source details. If it cannot, retire it rather than continue paid image harvesting on optimistic assumptions.

**Outcome at implementation:** tiny-region search instrument plus tests; no new CE, sticker observation, decoded string or new-owner handoff.
