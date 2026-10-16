# INSIDE CE: overlapping tiled paper proposals and novel original-crop challenge (16 October 2026)

**Mode: research / bounded optional tool, not autonomous sticker identification. No web/media acquisition by CI, no owner outreach and no confirmed new serial.**

## External precedent and why this is a different experiment

The [SAHI sliced-inference project](https://github.com/obss/sahi/blob/main/docs/guides/sliced-inference.md) describes a three-part strategy for finding small objects in large photographs: **overlapping source-resolution tiles, local candidate generation and merging mapped full-image boxes**. The official [SAHI guide](https://obss.github.io/sahi/quick-start/) notes that *sahi itself does not provide an object detector*. Therefore downloading a neural detector or blindly importing SAHI would not supply an INSIDE-specific paper/sticker classifier. We reuse the *tile algorithm*, feeding each slice through our existing low-cost, CPU OpenCV bright-paper contour proposal engine.

The previous original-source [OpenCV geometry PR #305](inside-ce-geometric-proposals-external-research-2026-10-16.md) found **12/12** small paper composites at 1%/3%/8% area in previously inspected development material but proposed regions in **4/4** synthetic negatives. So tiling is **not expected** to solve the false-sticker problem. It is only worth keeping if it helps recover very small candidates or off-center small objects without unacceptable extra cost/visual-review overload.

## Source, slice, detect, merge

[Implementation](../../scripts/external_evidence/visual_sliced_geometry.py) uses PIL and the previously integrated optional OpenCV detector:

1. Read a previously acquired local public-source photograph. Before processing, verify its recorded SHA256 and require its path to remain within the approved media root. Apply EXIF orientation once, then work in **original oriented pixels**.
2. Generate overlapping, square-ish local tiles of side `min(max(round(0.55*shorter_side),240),768)`, capped to the image extents, with fixed **25% overlap**. This may recover paper detail that a 1100-pixel global proxy loses.
3. Process at most **24 tiles per photo** in ordinary pilot mode, up to 16 generic OpenCV paper proposals per tile. If there are too many tiles, choose a deterministic, spatially dispersed subset with corners represented. Record *proposed / scanned / censored* tiles, location coordinates and per-tile stats. **Unvisited tiles remain censored; absence is never claimed.**
4. Map each candidate's coordinates to the source frame. Retain a **global full-image pass** for large objects, as recommended by SAHI. Rank these *paper candidates*, then suppress duplicates using **intersection-over-smaller > 0.72**. This is not a trained score or probability. Keep **eight** candidate regions in the comparison, a fixed human-review budget.
5. Return source identity, full-image bounding box, tile origin and raw counts. The opt-in CE visual job stores `sliced-paper-proposals.json` and displays its proposals in the **existing offline gallery**. If geometry and tiled candidates both exist, the gallery displays the tiled alternative; the full original files and raw geometry JSON remain preserved separately. There is **no automatic serial decoding** or owner matching, and every row sets `new_sticker_confirmed=false`.

This intentionally does not import SAHI, Ultralytics, a downloaded model, an OCR engine or a video/image network harvester.

## Newly disjoint physical-source stress cases

The original paper photographs **/021** and **/171** were not among the five source photos used as templates for the prior hash recognizer (**/003, /037, /038, /065, /125**), nor the four development/comparison positives (**/039, /047, /063, /118**). Both are now frozen in a [source-sha-pinned crop manifest](../../data/reference/inside-ce-novel-tiny-paper-crop-holdouts-20261016.csv) with visually inspected approximate paper boundaries.

The [new comparison](../../scripts/external_evidence/benchmark_sliced_geometry_new_sources.py) uses the source bytes of those two previously unused originals, then independently resizes and places each paper into three wide **1440×1080** generated collector-like scenes at **0.1%, 0.3% and 1%** paper area. The six synthetic positive scenes have frozen rotation/location/background choices. Four fresh code-generated *negative* scenes include plain clutter, a game case, shipping ticket and bright collector packaging. The test reports **global contour method vs sliced contour method** under exactly the same eight-review-box budget and IoU ≥ 0.40. Both methods can suggest ordinary paper; negative outputs remain visual prompts, not physical sticker evidence.

**Scope warning:** these are distinct original *cropped source photographs*, but the wide scenes are **synthetic compositing**, not genuine independent wide-scene public owner photographs. When the numerical results are observed, they become **development data**. Do not optimize parameters on these same six examples and then claim fresh validation. The four negative backgrounds are not a real-world false positive dataset. Our independently collected public negative images still require the separate manual opt-in source verification run.

## Workflow correctness improvement

The previous manual image provenance workflow installed Pillow, gallery-dl and yt-dlp but **not opencv-python-headless**, even though its opt-in region pilot was calling `visual_geometry_proposals.py`. That would have caused an import failure on a future opted-in run even when CI was green. This PR adds bounded OpenCV installation to that manual job, separately from ordinary no-network PR test dependencies.

The optional `run_sliced_pilot=true` flag runs only **after** the existing public-source image harvesting and canonical image-index creation. No new URL acquisition is triggered by the flag itself. Ordinary PR CI runs new synthetic/archived-original tests and the fixed comparison, not the manual live-fetch route.

## Decision gates

- **Acceptable:** algorithm succeeds on source-derived small crops, records all censored tiles, safe source digests and box coordinates, and is useful as a human reviewer **alternative** to hash and un-tiled geometry.
- **Not acceptable as a release gate:** claiming probability of a true INSIDE sticker, interpreting a bright ticket as a numbered CE symbol, assuming every missed source photo was searched, or tuning weights on already-used photo crops and calling it heldout evaluation.
- **Next:** original public-image negative controls via explicit opt-in workflow; independent public original **wide scene with paper <1%**, with SHA-pinned ground-truth bounding boxes and no reference leakage. Compare global geometry, sliced geometry, hash, and possibly ORB feature homography *only if enough points are present*. The user's primary outcome remains **novel canonical-reconciled CE sticker sources**, not synthetic leaderboard improvements.

**At initial authoring:** numerical performance unmeasured until the exact CI run; preserve both positive misses and negative prompts in the run artifact.
