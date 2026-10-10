# CL-15: source-integrity pipeline for original cover scan comparison

_9 October 2026. Bounded implementation of [CL-14 COVER-A](2026-10-09-cl14-cover-acorn-historical-clue.md) A1/A2. **Status: hash-authenticated acquisition and preview pipeline committed, original full-resolution pixel comparison awaiting a successful run and inspection of artifacts.** No CE sticker foreground interpretation is derived._

## Why this test needs actual source bytes

The reversibly printed PS4 cover is explicitly advertised by iam8bit as containing a clue. The original April 2020 primary-Discord-archived scans reportedly have both pages at **6552×5040**; the 2022 cover-interpretation messages describe an incomplete acorn on a monitor and a running figure outside the monitor. A 2021 original Discord summary says the original acorn solution used an acorn-41 Game of Life mask over a separate running-man puzzle image. This is a credible **source/audience/timeline** connection but not a pixel-identical artwork identification.

The earlier connector supplied the **exact upstream Git blob IDs** for the original high-resolution cover files, but did not return their large binary bytes. Direct network fetching from the research container also failed due DNS. These are **acquisition limitations**, not evidence that the source images no longer exist.

Source-recovery program: [`scripts/probe_original_cover_a1.py`](../../scripts/probe_original_cover_a1.py); one-time runner: [original-cover integrity workflow](../../.github/workflows/one-shot-cover-source-a1.yml). This distinct lane does **not** modify the other agent's open [2016 in-game scene witness probe #179](https://github.com/gamesbyian/GRA-EDISNI/pull/179).

## Strict original evidence manifest

Source repository: `gamesbyian/playdead-unofficial-exports`, original public `assets/` paths.

| Witness | Git blob SHA1 from the source repository | Use |
| --- | --- | --- |
| `INSIDE_A-5d197786f158c567.JPG` | `875403acac93d83a8acae97e14240c35b88d33ab` | 6552×5040 archived **inside** cover |
| `INSIDE_B-80fbff1237c37913.JPG` | `d533d4161f0572b65d134d54f4fa6477029f2d64` | 6552×5040 archived **outside** cover |
| `image-7be117e2c68d1b1e.png` | `40039a204800383f69c1b0e4475edcc0989944ef` | Archived pixel-small cropped cover *acorn* monitor |
| `image-46edcfb62af0b550.png` | `24b6429bfab9557760313401f3cb2184664fada6` | Historic acorn reference/compare |
| `image-21b86ef8e34e269b.png` | `c07e87d72a92d4181b1014f3a8269e086a4ef471` | Archived cover *planet* monitor |
| `image-d6d0d0f76ab751ca.png` | `b6216e584a62e44ae0594cb881c9ad27ef5266fe` | Archived cover *graph* monitor |

All names, IDs, and monitor-family provenance are independently cross-checked against [Exp. 409](../experiment-409-cover-operation-family-audit.md) and [Exp. 410](../experiment-410-cover-monitor-source-inventory.md). The 2020 scans and individual 2025 crop sources do **not** by themselves prove a 2019 print-to-source registration.

The script reads only six **exact allowlisted upstream URLs** over HTTPS, enforces a 32 MB/file cap and three-allowlisted public GitHub redirect hosts, checks file magic and decoded image dimensions, and authenticates **Git blob SHA1 of the original byte stream**, calculated using the `blob <length>\0<bytes>` Git envelope. It additionally records independent SHA-256 and sizes in `report.json`. A *successful HTTP response or GitHub rendering* is not itself source authenticity.

## Produced inspection materials

The one-time GitHub Action produces a short-lived `authentic-original-inside-cover-coordinate-review` artifact (30-day retention) containing:

1. Exact hash-authenticated original image bytes under `verified_source/` (not recompressed).
2. A 2,800px-wide overview showing both cover scans.
3. **Two 4×3 coordinate-indexed contact sheets**, each with twelve labeled tiles covering the **entire native image** at fixed pixel bounds. This ensures researchers can actually inspect the running figure / monitor relation and avoids cutting to a hand-picked interpretation.
4. Five-times nearest-neighbor display enlargements of the four preexisting historic monitor crops, tagged as renditions, *not* as additional photographic detail.
5. `report.json` listing each source Git hash, SHA256, geometry, bytes and any retrieval problems. A failed exact source hash must fail the job rather than show a visually plausible reconstruction.

The workflow runs **once on its addition to main** (trigger paths deliberately restricted to this runner and its workflow), and can be invoked manually if archiving is needed. It has no watcher or repeated schedule. A separate `--self-test` path checks only the tiler/digest code on synthetic pixels, not the historical art.

## How to evaluate without inventing a decoder

**A1, source-identity check:** use the real cover scan plus the original 2016–2021 *running-man target image*, once authenticated, to decide whether the printed figure is (a) an actual exact/recognizable reference to the textual cipher object, (b) just an ordinary running person in the game/cover scene, or (c) indeterminate. Never present a pixel comparison unless both original sources and their coordinate systems are in hand. A printed running figure does not automatically equal a *mask named running man*.

**A2, historical cover-originality check:** use the original Dec 2019 iam8bit clue advertisement and Dec 2019 discovery posts as witnesses for the artwork's existence by initial release. The first high-resolution scans are dated Apr 2020, so scans alone cannot determine original editorial date. If matching original 2019 product photo exists, compare it separately.

**B1, audience check:** compare this printed reversible art from the *standalone* PS4 copy against the CE copy without relying on *similar product names*. The public standalone product page advertises a physical edition, but exact as-shipped cover sides remain a comparison obligation. A shared cover suggests a standalone-readable instruction; it does not **exclude** an intended collaborative ARG metapuzzle.

### Completion gate

An actual **positive** COVER-A identification requires: a source-authentic running-man cipher image, a source-authentic cover detail, an independently specified source registration/crop that explains the omitted acorn portion, and a composition/interpretation deriving the 2021 operation. Matching the word “running” in Discord is *not* sufficient.

**Current state:** script/workflow shipped, SHA expectations registered, original image identity comparison still **not completed**; no plaintext, valid CE operator, or physical sticker predictions. Prefer leaving the cover clue *unresolved* over crediting it as solved by an attractive story.


## Actual execution: original binaries and three historical crops confirmed (10 October 2026 UTC)

This pipeline has now **completed successfully**, not merely been proposed. [Acquisition run 38024716054](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38024716054) fetched the two **byte-authenticated, original** 6552×5040 scans and all four pinned historic monitor/reference crops. [Follow-on source-registration run 38024971110](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38024971110) passed the extra independent crop-provenance audit. The large original binary scans were retained intact in a 30-day downloadable Action artifact. This experiment does **not** change the sticker data.

The genuine original A image visibly shows a glowing acorn-family **foreground monitor**, with a **small running person on a separately illuminated white platform outside the right-hand window**. This is a directly inspected spatial conjunction, not merely a textual report by a contemporary user. Two distinct uncertainties remain: whether the runner is an *exact graphic quotation of the old running-man cipher* rather than an ordinary game silhouette, and whether the designer intentionally used the juxtaposition to cue the generation-41 solution. In particular, the dated 2021 demonstration video and original independently registered running-man cipher pixels have not been recovered here.

### Source-to-source provenance control: historical monitor crops originate in this scan

An initial source-to-source template comparison localized three old, independently archived **small monitor crops** at fixed positions in the half-resolution version of original A. The [fully reproducible provenance checker](../../scripts/audit_original_cover_monitor_provenance.py) then froze the coordinates, checked the original images' Git blob hashes anew, and measured grayscale **Pearson correlation** between each crop and its native-scan rectangle. A matching rectangle on the original **exterior** scan B serves as a negative control. [Machine-readable exact-coordinate fixture](../../data/cover-original-monitor-registration-2026-10-09.json).

| Historic image family | Native pixel bounds in original A: x0,y0,x1,y1 | Original A correlation | Exterior B same-position control |
| --- | --- | ---: | ---: |
| Acorn monitor | `3780,3294,3948,3418` | **0.900300** | 0.040212 |
| Planet monitor | `1126,2938,1232,3036` | **0.912542** | −0.038328 |
| Graph monitor | `2232,2882,2378,2994` | **0.859104** | −0.176659 |

The comparison uses the intact original scan downscaled **exactly 50% with LANCZOS**, and the old source crops at their archived 84×62, 53×49 and 73×56 sizes. It checks this **fixed** registration; it does not represent a blind test of whether the *cover itself* matches a separately reconstructed game image. In particular, the correlations show that **older crop artifacts came from this same print/scan**, not that a new 4-stage CE code transform has been found. Source roles and naming were originally independently recorded in Experiment 410.

Native-resolution visual inspection context crops (not puzzle-fitted):
- acorn monitor x3630..4090, y3180..3520;
- runner/window x5550..6500, y2850..3600.

These crops can be re-created verbatim from the authenticated original A bytes. Inspection-brightened copies are **renditions**, not new recovered visual data. The original native artwork itself is in the acquisition artifact.

### Status after actual A1/A2 work

**Closed:** original A/B source byte integrity; true existence of acorn display and small running figure; archival monitor-crop provenance for acorn, planet and graph families. **Still open:** source-authentic 2021 running-man *cipher* image, a pixel-registered cover-to-cipher identity or overlay, and an explicit original author's intent. That is enough to **raise the historical COVER-A story above a purely imagined acorn juxtaposition**, but not enough to promote COVER-A to "solved".

