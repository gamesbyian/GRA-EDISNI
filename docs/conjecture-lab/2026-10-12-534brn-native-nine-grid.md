# CL-534-N9: source-native nine-slot and RGB-plane registration preflight

**12 October 2026 | DISCOVER/DEVELOP | Evidence-preserving source-first audit | No CE foreground consumer found**

## Question

Could the damaged original image at the CE-background-derived route /dat/534brn9653f9j8mmd/ provide a native 3×3 receiving grid or RGB-channel source for the sticker foreground? This preflight asks what the original source **forces**, rather than layering a chosen 3×3 over any visually appealing image.

No entropy repair, missing-sticker inference, candidate plaintext or image-output fitting is performed.

## Authenticated evidence

Offline script reads the original preserved Git blobs:

- B original page capture: SHA-1 f12c02c49f4c3f7589419fe8e20d655f7b95a9f4.
- Independent XMP fragment: SHA-1 b6f5ffed946d9d19dfd0a5d90a8b18759a90c496.
- Experiment 423 independently audited JSON for the source JPEG's SOF dimension range, sampling, possible MCU count and entropy ambiguity.

Both original binary sources are Git-blob-hash-checked before parsing. Only the **intact page preamble** is inspected for HTML affordances, not the corrupted image bytes. The preamble displays the Terminal41 title and an empty preformatted [] indicator, with no HTML input, form, image, canvas, SVG or script element preceding the JPEG-like body. **This is not proof of no consumer elsewhere or in lost bytes.**

The footer retains pe^!02un and dot runs 8, 2, 1, historically read upside down as **128 UNSOLVED**, followed by sys/terminate terminal/41/[conf.]. The independent XMP metadata gives creator AnSet and creation timestamp 2016-12-16T14:12:24.351. None of these preserved fields directly labels nine image-reading coordinates or three RGB channel keys.

## JPEG geometry: exact census

Established by prior source forensics, and asserted against the frozen Experiment 423 fixture:

- Both JPEG dimensions independently range from **128 to 255** inclusive.
- Component sampling is **Y 2×2, Cb 1×1, Cr 1×1**, i.e. **six 8×8 DCT blocks per 16×16 MCU**, not nine source-native tiles.
- All **43** geometrically possible MCU products remain consistent with the damaged entropy. Actual JPEG dimensions and pixels have not been recovered.

The new exact audit enumerates **16,384** possible width/height combinations and computes three distinct requirements for nine *equal-sized* native tiles:

| Conditional 3×3 requirement | Valid axis values | Valid dimension pairs |
|---|---:|---:|
| Equal whole-pixel thirds per axis (dimension divisible by 3) | 43 | **1,849** |
| Equal-number-of-MCUs thirds per axis (ceil(d/16) divisible by 3) | 48 | **2,304** |
| Both equal pixel thirds and borders aligned to complete MCUs (dimension divisible by 48) | 3 | **9** |

In the strict combined case each axis must be exactly **144, 192, or 240** pixels. These tests are alternative *design constraints*, not source instructions to pick one and not significance probabilities. Each variant leaves multiple geometries.

The conspicuous **128×128** hypothesis has an **8×8 MCU grid**. Neither 128 pixels nor eight MCUs divides into three equal strips. Therefore *three equal-sized 16px-MCU-aligned tiles per axis* cannot coexist with exact 128×128. Crucially, this does not prevent nine **unequally-sized tiles, point samples, scaled overlays, or logical positions**.

Even **granting 128×128**, two direct and reasonable candidates for centres of three sample sites disagree:

- Pixel-third centres using floor: **21, 64, 106**.
- MCU-third-band centres using floor and 16px MCU centres: **24, 72, 104**.

Take Cartesian products of each coordinate triple for all nine image-class locations; either interpretation fits the same source dimensions, and neither is independently selected. A putative square image would **not** uniquely specify where to read colour channels.

## What the three JPEG components mean

The captured JPEG stores a luma/chroma sampling structure consistent with common YCbCr 4:2:0, **not three independently available equal-resolution red/green/blue rasters**. A normal RGB value at any point requires JPEG entropy decoding and subsequent colour conversion. The source lacks authenticated fully decoded pixels. Its three component identifiers alone therefore do **not** deliver 3×3 RGB plane pixels for the sticker code.

This does not preclude Playdead deliberately putting a message in the decoded image, or the foreground providing instructions to decode it. It means that no such channel consumer has been demonstrated from the extant captures.

## Domain bridge: nine CE backgrounds versus nine repeated foreground positions

This geometric negative needs to be read together with [Experiment 319](../experiment-319-background-geometry-mask-domain-audit.md). The solved IAB/CDE/FGH grid indexes **nine different background classes**, each fixed by sticker serial modulo nine. But the nine consecutive occurrences in the *body of a single class's 9+3 foreground word* all carry the **same** background class. An A–I spatial mask cannot be moved to those within-class occurrences without an extra correspondence.

Experiment 319 quantifies that missing class-to-occurrence identification as up to **9! = 362,880** bijections (or 1,680 ordered three-row partitions). The candidate nine-site **JPEG image** map studied here is a separate missing correspondence: JPEG pixel/MCU addresses to the nine A–I classes. Neither ambiguity is repaired simply by observing the cardinality nine. Do not conflate them or silently compose one invented map with the other.

## Interpretation and next evidence gates

**Bounded negative:** neither the intact HTML/XMP wrapper nor verified JPEG header/entropy constraints supply a unique nine-slot RGB sampling rule. A 128-like footer and nine CE backgrounds together do not fix a pixel-address map.

**Still live:** a new lossless 534brn image capture; an original source-authored crop/colour registration from a different Terminal41 file; a nine-location receiving surface on the authentic assembled CE background; an explicit external input form; a JPEG repair key given by another stage.

**Best next acquisition:** original less-lossy 534brn bytes or a dated independent full image witness that settles dimensions and pixels. If that cannot be obtained, inspect original nine-tile CE background art for specifically authored marks or registration cues independent of any desired decoded output. Do not infer geometry from a 42×42 or 423×423 community derivative without proving original-byte lineage.

Once actual pixels exist, an unbiased consumer test needs the source raster hash, a source-provided pixel/MCU position rule, frozen IAB/CDE/FGH registration, fixed channel selection, explicit output condition, all compatible sticker completions and matched controls.

## Reproduce

Run from repository root:

    python scripts/audit_534brn_native_nine_grid.py --check-frozen
    python scripts/audit_534brn_native_nine_grid.py --check-frozen --output /tmp/534brn-nine-grid.json

Standard library only. The script refuses source-blob drift, changed HTML/footer/XMP fields, changed source-JPEG dimension premise, and unexpected geometry counts. No new workflow, synthetic original pixels, remote site requests, physical ledger edits, or incumbent-machine changes are involved.

This is a **new source geometry and information-path audit**, not a reopening of Experiment 423's exhausted entropy-recovery branch, and it does not undo the CL-RGB-01 literal six-key negative.
