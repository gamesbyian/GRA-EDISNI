# INSIDE CE: geometric image-region proposals, external-system review and development comparison

**16 October 2026. Status: EXPERIMENT. Not sticker detection or confirmed identification. No new public sources acquired in PR CI.**

## What changed in our thinking

The prior [fixed tiny-sticker stress test](inside-ce-region-specificity-small-scene-2026-10-16.md) measured **1/4** composite hits at **1%** paper area; **3/4** at **3%**, **4/4** at **8%**, all using an 8-box review queue and IoU ≥0.40. The earlier five-reference rotated dHash/aHash model then produced review prompts on **all four sticker-free synthetic scenes** at hash distance 32. This is a **localization + specificity** problem, not one that more search queries can solve.

### External systems and the adoption decision

| Source, first-party when possible | Relevant working idea | Decision for GRA-EDISNI |
|---|---|---|
| [OpenCV contours and bounding rectangles](https://docs.opencv.org/4.x/da/d0c/tutorial_bounding_rects_circles.html) | Binarize a page, extract external contours, bound and score candidates. | **Implement independent light-paper proposal stage** with multiple global luminance thresholds, small morphology closing, aspect/extent/local contrast filters, capped ranking. The resulting box is **not proof of a sticker**. |
| [OpenCV template matching](https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html) and [multiscale tutorial](https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/) | Pixel/edge correspondence works at known scale, less reliably under rotation or perspective; correlation has no guaranteed reject threshold. | **Not direct adoption** for serials: CE stickers share common paper, dash/slash/dot and generic background; source photo illumination and rotation vary. May be useful for *close-copy* detection with a calibrated multi-scale matcher. |
| [OpenCV ORB/AKAZE planar-object tracking](https://github.com/opencv/opencv/blob/5.x/doc/tutorials/features/akaze_tracking/akaze_tracking.markdown) and [RANSAC homography](https://docs.opencv.org/4.x/d1/de0/tutorial_py_feature_homography.html) | Feature correspondences and geometric consistency can reduce background coincidences and handle perspective. | **Next bounded second method**, but these plain paper stickers may have too few distinctive keypoints to produce four reliable matches. Measure no-match rate rather than assuming success. |
| [SAHI / obss/sahi](https://github.com/obss/sahi), [documentation](https://obss.github.io/sahi/) | Overlapping image tiling preserves small objects that would vanish in full-scene resize; fold tile coordinates back and deduplicate overlaps. | **Next promising small-object architecture** for local, explicitly approved images. Reuse the tiling/proposal principle without downloading deep-learning detectors by default. Compare extra CPU, source coverage, box recall and duplicate explosion to ROI baseline. |
| [FiftyOne similarity and review](https://docs.voxel51.com/user_guide/similarity.html) | Evaluate proposals, nearest neighbors and false negatives interactively with visual provenance. | Existing local self-contained gallery is sufficient for current 16-image development case; add only if real public corpus grows and blind reviews demonstrably improve. |

## Implemented independent proposal stage

[visual_geometry_proposals.py](../../scripts/external_evidence/visual_geometry_proposals.py) uses opt-in `opencv-python-headless` + NumPy and accepts only already-acquired, SHA-confirmed local source images. On an EXIF-oriented proxy at most **1100 px** long side, it generates six or fewer fixed grayscale threshold masks from global Otsu and brightness limits (not fitted to a test label), performs 3×3 closing, and checks external contours for near-square shape, area, rectangular extent, median brightness and local contrast.

It ranks **up to 48 distinct review candidates** per source, preserving total contours, shape rejections, component and result caps, thresholds attempted and the exact original oriented source-coordinate bounding box. As with the earlier five-photo reference matcher, all result rows have `new_sticker_confirmed=false`. Source-level image caps are still distributed fairly; no unapproved URL is acquired.

**Expected problem:** the exact same geometric filters can propose blank tickets, packing slips, PS4 boxes, labels, white cards and posters. Consequently a perfect paper-boundary localization does not prove a *sticker* or *Collector's Edition owner*. There is no calibrated posterior probability.

## Honest comparison design

[benchmark_sticker_geometry_development.py](../../scripts/external_evidence/benchmark_sticker_geometry_development.py) runs the alternative on:
- the **12 previously seen** frozen 1%/3%/8% synthetic compositions made from the four genuinely different known sticker originals;
- the same **four previously seen** synthetic no-sticker decoy scenes;
- the **four previously seen** large frontal source-original sticker photos.

All are **development/diagnostic data already viewed by the research programme**. Do not report this as independent, held-out accuracy, even if the OpenCV method appears to outperform the original hash baseline. Use the same *top-eight human review budget*, count boxes with IoU ≥0.40 against fixed ground-truth paper extents, and separately report no-sticker images with any misleading proposed region. Preserve all proposals and component/cap waterfall in a 30-day CI artifact.

**No predeclared production decision threshold** is selected on these examples. Performance on real photographs without numbered stickers still requires the separately opted-in [SHA-pinned photographic negatives](inside-ce-region-specificity-small-scene-2026-10-16.md). Those images are not automatically fetched by PR CI; missing images must never be called clean negatives.

## Deployment and future independent evaluation gates

Only merge after the no-network `CE visual provenance` and external-evidence suites pass on the exact PR head. A successful development contrast can justify an **opt-in research lane**, not replacement of current source-first image collection or any automatic assignment of sticker number.

1. Create a **new** disjoint set of owner-source original photographs with *truly* tiny sticker regions, plus source-verified non-sticker paper/box photos. Freeze annotations and SHA before comparing alternatives.
2. Compare four independent steps: baseline multiscale hashes, independent geometry, SAHI-style overlapping tiles plus geometry, and optionally local ORB/A-KAZE where distinct features permit. Report recall at IoU .25/.40/.60, original-byte recovery, false visual prompts per image, top-eight precision and median CPU seconds per image.
3. Use a fixed 48-image **source-diverse** opt-in deployment budget; inspect a representative sample of matches *and unmatched originals*. No sticker number or owner case may be promoted without independent full original and current community ledger reconciliation.
4. Preserve the failure case if geometric detection spuriously treats game cases or printed paper as stickers. That is a structural limitation, not a reason to silently exclude awkward negative examples.

**Outcome as of implementation:** research into comparable live systems and code/CI integration; actual geometry comparison numbers must come from the exact-head test logs, not from this document's assumptions.
