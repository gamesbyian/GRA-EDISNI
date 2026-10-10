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
