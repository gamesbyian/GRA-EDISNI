# CL-13 / CX-C source correction: 2021 acorn + running-man overlay finally explained LIFEDETECTED

_9 October 2026. Historical source reconciliation and source-native positive control. This corrects incomplete **status metadata** and the newer speculative four-stage cover writeup. It does not discover an original sticker foreground decoder._

## What the original source actually reports

The original archived Playdead Unofficial #tldr Discord export held in `gamesbyian/playdead-unofficial-exports`, file `Playdead Unofficial - ARG - tldr [462637922944811028].txt`, immutable Git blob `20600a0756002ef7a7f2994b2a5e7b7e4852333d`, includes the following entries:

- **13 April 2019 (contemporary):** `LIFEDETECTED` was **guessed** and accepted by the Playdead print button; the link from PC/PS4 acorn printer art to that string had not been recovered.
- **10 June 2021 (reported discovery):** solver `4987372` reportedly offered the missing operation. The archived #tldr records the contemporary [original message ID 852612048482336788](https://discord.com/channels/460626942190813184/461275582970462209/852612048482336788).
- **25 June 2021 at 00:26–00:27, export wall clock, timezone unspecified:** the curator explicitly reports that evolving the Conway acorn **seed to generation 41** and **overlaying its output onto the separately known running-man puzzle** reveals `LIFE DETECTED`. [Archived demonstration video attachment](https://cdn.discordapp.com/attachments/461275582970462209/857907060334919700/acorn.mp4), not newly byte-authenticated in this study.
- The same curator reports generation **42** with the separate acorn-42 / Ford Cipher puzzle as a second application of the operation class. Do **not** conflate that with the original `LIFEDETECTED` step.

A contemporaneous [25–26 June 2021 Steam thread](https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=69) has PitchBright explicitly announcing that the previously guessed acorn password was finally deciphered and pointing people back to the Discord. This corroborates contemporary **community acceptance** but is not an independent pixel-level replay of the decoder.

[Game Detectives](https://wiki.gamedetectives.net/w/Inside_ARG) still says the acorn-to-`LIFEDETECTED` extraction remains unknown. That summary is chronologically incomplete relative to the dated 2021 record. The pre-existing project [historical technique inventory](../discord-historical-technique-inventory.md#conways-game-of-life-overlay) already had the correct later account; the 2026 printer metadata and the newer CX-C comparison continued to report the earlier 2019 state. This is a documentation inconsistency now reconciled, not wholly new evidence to the project.

## Precise typed historical operation (positive-control design)

| Step | Object / input type | Operation | Output / confirmation |
| --- | --- | --- | --- |
| 0 | PC/PS4 32 long printer rows plus nine shorter symbols | Use historic side-boundary/interlace cues to restore the 32×32 acorn + 41 art (canonical order saved) | Two **distinct authored instructions**: named Acorn seed and integer **41** |
| 1 | Standard seven-live-cell Game of Life acorn seed, B3/S23 | Evolve exactly 41 generations on the infinite integer grid | A **binary image mask** |
| 2 | Distinct original running-man art / image, original geometry | **Overlay** generated mask with native target at the solution's proper registration | The reported `LIFE DETECTED` graphic/readout |
| 3 | Human-recognized word/phrase | Enter `LIFEDETECTED` on the original historic Playdead site | Already known accepted password from 2019 |

**What is proved here:** original community *attested* all four steps by June 2021. The extracted 2018 long-row *canonical order* is already pinned in `data/printer-reference/pc-ps4-acorn-order.txt`. An independently reconstructed standard acorn can be evolved exactly (below).

**What remains unverified in this study:** unmodified 2021 video bytes, independent original running-man source pixels, the translation/crop/scale that aligns generation 41 with it, and a complete from-source readout of `LIFE DETECTED` under that registration. Thus write "reported community solve, not replayed", not "still only guessed" and not "original game engine confirmed decoder".

## Executable source-native component

The exact standard [Acorn RLE](https://conwaylife.com/wiki/Acorn) is `x=7, y=3, B3/S23, bo$3bo$2o2b3o!` (seven cells). [Our fresh standard-library-only verifier](../../scripts/verify_historical_acorn_41_life.py) advances B3/S23 and confirms:

| Generation | Live cells | Bounding rectangle (zero-indexed seed coordinates) | Size |
| ---: | ---: | --- | ---: |
| 0 | 7 | `x0..6, y0..2` | 7×3 |
| **41** | **102** | `x−14..15, y−8..6` | **30×15** |
| 42 | 92 | `x−14..15, y−8..6` | 30×15 |

Run `python scripts/verify_historical_acorn_41_life.py --render` to print the exact cropped live-cell mask. Generation 41 geometry is a **source-native positive-control mask**, independently reproducible without fitting any sticker output. A 30×15 box is not a verified cover/CE receiving surface merely because some physical width resembles 30 or 32.

The verification is a *necessary mathematical subroutine*, not a reconstruction of the original 2021 overlay. We deliberately do not position it onto a modern guessed 32×32 text or claim an overlap readout absent original registered pixels.

## What it changes for the sticker revivals

* **Strengthens operation-class prior:** Playdead *community-solvable* operations are demonstrably multi-source: first recover a structured visual object that *names and parameters* a known cellular automaton; then register the generated output onto a **different existing artifact**. This is stronger than a generic imagined "image overlay" precedent.
* **Focuses the missing bridge:** For [CX-E4 dual 3×3 planes](2026-10-09-cx-e4-dual-grid-transfer.md), it is plausible to **DEVELOP** an operation that transforms plane A and composes it with plane B. The original acorn solution supplies no reason to pick transpose, invert, XOR, nine-class tile layout or a 4/9/(9+3) segmentation. Those conjectures remain unsupported as authored CE methods.
* **A better falsification requirement:** A valid CE overlay story needs an independently supplied **transform identity**, **input/seed**, **parameter**, **output plane**, **registration**, and **human-recognizable result**. Merely making four quarters look plausible with chosen D4 rotations or XOR is far short of the positive control's chain.
* **Chronological clarity:** The password existed/was accepted in 2019; its missing extraction was retrospectively worked out in 2021. A later successful extraction is compatible with the already-completed Terminal41 status slots, and does not imply new CE server responses.

## Bounded next action

Recover the original 2021 `acorn.mp4` or an exact contemporaneous frame sequence together with the original running-man art as separate genuine source assets. Freeze its initial registration *without studying CE glyph outputs*; independently replay the overlay. If that can be done, reuse the *methodological types* (authorial operation and parameter, exact registration, checkable output) as a calibration against hypothetical CX-E4/E5 steps. If assets remain inaccessible, the 2021 first-person source/archived community report is still adequate to correct the project's historical metadata but not to establish a new sticker cipher operation.

**Disposition:** historical chronology and typing corrected; generation-41 code component verified; full 2021 running-man overlap not independently replayed; no CE foreground validation.


## Verified follow-up (10 October 2026 UTC): source MP4 and full 90-pixel replay recovered

The initial limitation in this CL-13 note, namely that the original `acorn.mp4` and full running-man/PC-grid registration could not be independently replayed, **has now been closed**. Read the [complete CL-16 source-pixel replay report](2026-10-09-cl16-full-2021-life-overlay-replay.md) and [source-anchored positive-control fixture](../../data/historical-2021-acorn-41-overlay-positive-control.json), not the now-superseded "unverified" status in the initial investigation above.

The old Discord CDN direct URL returned HTTP 404, but the original `gamesbyian/playdead-unofficial-exports` asset tree retained an authentic 408,693-byte `acorn-c53ef409753e9fa2.mp4` (original Git blob `0480da448164c0a1bbd115f1065ffd9d68f70bf2`), along with the original 32×32 PC printer coloured raster `Inside_pc_acorn_fixed-081372579ea1409c.png` (Git blob `c04ac01fc6f3f3af05d00f7e2b104396ade440e1`). [Source recovery passed in GHA run 38025192150](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38025192150).

**New completed result:** evolve standard B3/S23 Acorn to generation 41 (102 live cells, native footprint 30×15), place its normalized footprint at source pixel **(1,16)** in the 32×32 printer grid, and keep original orange-dot pixels *outside* the mask while recolouring original blue-dash pixels *under* the mask orange. Mask matches 2021 video **102/102**; output has exactly **90 orange cells**, matching the 2021 video's final `LIFE DETECTED` bitmap **90/90**, with **zero differences**. Exact output bitmap SHA256 `38ea14a45bffbd735cec104cad5ba0499bbb36163bc3c2bf0b9cf250b773bd6d`.

The received image is visibly the **original PC/PS4 printer's own 32×32 acorn/running-man art**. Thus the later historical overlay is **two interpretations/layers of this authenticated puzzle surface**, not a demonstrated CE-sticker overlay or a novel, unrelated third artifact. The printed cover's tiny three-dimensional running figure remains a different, **unmatched** visual and authorial-intent question.

