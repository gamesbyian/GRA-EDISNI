# CL-14 / CX-C: the reversible PS4 cover may have foreshadowed the acorn-running-man solution

_9 October 2026. Source-first retrospective interpretation, not a solved cover picture or sticker decoder. Companion: [CL-13 verified 2021 provenance](2026-10-09-cl13-2021-acorn-overlay-provenance.md), [Experiment 409 cover clue audit](../experiment-409-cover-operation-family-audit.md), [Experiment 410 monitor/source inventory](../experiment-410-cover-monitor-source-inventory.md), and [cross-edition audience test](../cover-cross-edition-dependency-audit-2026-10-08.md)._

## A specific historical conjunction

Four separable source facts had remained scattered across the project:

1. **December 2019:** iam8bit explicitly advertised the INSIDE PS4 reversible cover as containing a clue. The physical PS4 version was also available outside the Collector's Edition, to owners without serialized CE sticker wrap.
2. **December 2019 onward:** original community cover observations identified a **partial/top-only acorn-style monitor** and a **running-man-like figure in the scene outside the monitor**. The latter identification is observational/semantic, and must not be conflated with a pixel-identical overlay target. The exact original cover scans are named `INSIDE_A-5d197786f158c567.JPG` and `INSIDE_B-80fbff1237c37913.JPG`.
3. **June 2021:** user `4987372` reportedly demonstrated that standard Conway acorn generation **41** overlaid onto the separate running-man puzzle yields `LIFE DETECTED`, a password the community had originally guessed in April 2019 (primary archive #tldr, Git blob `20600a0756002ef7a7f2994b2a5e7b7e4852333d`; primary Discord ID `852612048482336788`).
4. **August–December 2022:** *before this 2026 project*, original solvers explicitly connected the **cover's acorn/running figure** with the **2021 successful overlay**, and proposed the cover may have once been an acorn clue, already rendered moot by the later independent solve.

The last item is especially strong as **anti-hindsight provenance**, not as proof of authorial intent. The original `gamesbyian/playdead-unofficial-exports` file `Playdead Unofficial - ARG - solving-breakout [463106924708233216].txt`, Git blob `064f6aba55e11b4aaf3759f1da672c2ee19e7f17`, records:

- **19 August 2022 20:33, saketho:** asks why the label *running man* was chosen and explicitly observes that the CE cover's most noticeable feature is a screen with the *top half of the acorn*, and that the boy looks out toward a *running man*.
- **13 September 2022 06:01, pitch_bright:** says the puzzle was named running man because it looked like one; this supplies a mundane name provenance rather than secret evidence.
- **24 December 2022 22:29–22:34, gs_base/aperson1:** proposes the cover clue may have been *accidentally solved* because the acorn was still unresolved when the 2019 CE was distributed but only solved later. A companion participant explicitly notes the alternative that the cover could have linked to CE stickers instead.
- **24 December 2022 22:57 onward:** community considers aligning foreground dots to the running man, but that was **speculation**, not a reported successful CE reading; the tiny then-known dot sample was acknowledged.

The original sources don't establish pixel-equality between the background figure and the historical running-man overlay, a deliberate cropping position, or an authorial statement that the cover has only one clue. They do establish the historical coexistence of both imagery classes, and that contemporary solvers recognized the potential connection.

## Two rival purpose models

### COVER-A: previously unsolved acorn overlay hint (currently economical)

*The 2019 cover was intended to hint at an operation already latent in the PC/PS4 printer system: join the acorn and running-man puzzles by evolving generation 41 and overlaying. Its clue was effectively consumed by the 2021 independent solve.*

This has a straightforward chronology and audience. A standalone PS4 buyer could in principle use the cover without owning even one CE sticker. It uses a real source-reported operation, and does **not** require a novel nine-class CE image address, four-stage machine, newly active website, or an unmotivated `27`-symbol key.

**Residual assumptions**: that the cover running figure directly references the *running-man puzzle* and not simply normal world artwork; that the partial acorn is intentionally omitted/masked as an **instruction** instead of a decorative quotation; and that the designer intended the 2019 clue to reveal the exact 2021 overlay rather than something else.

**Independent predictions**:
1. The precise original screen crop should align *qualitatively and maybe geometrically* with the acorn/running-man artwork as known before 2021.
2. The clue should be meaningfully interpretable from pre-2020 printer/cover data without any CE foreground values.
3. A direct cover-to-GHI, 4/9/(9+3), or 108-sticker address registration should **not** be necessary to explain its conspicuous acorn/running-man pairing.

### COVER-B: cover additionally keys CE foreground (still possible)

*The cover's known acorn reference is both a historical reminder and part of a fresh CE-specific registration, perhaps operating on sticker-payload slices or damaged `534brn` art.*

Requires at least one more independently source-fixed link:
- exact repeated A-I/sticker glyph coordinates,
- a typed 108/27/body-tail reader,
- a transform and fixed geometry exported by the cover to the foreground,
- or a new receipt/result that cannot be derived from old printer material.

Sharing PS4 cover artwork with non-CE buyers does not disprove collaborative B. It does make this an extra premise. Neither **four monitors** nor the **12:12 clock** currently supplies a source-native CE mapping.

## Three bounded experiments before another sticker overlay

**A1: original-art identity test.** On the existing preserved 6552×5040 cover scans, compare the foreground figure's source-asset identity with the historically reconstructed running-man mask and the relevant game scene. If the figure is a generic in-game running character, record this as such. If it is an exact or deliberate graphic quotation, record the matching feature and source bytes. Don't invent or fit an affine transform to force a match.

**A2: the 2019→2021 chronology test.** Determine if the partial acorn monitor + running figure pairing was part of the **original 2019 print artwork** (high-resolution scans and dated contemporary cover reactions) rather than a later mod, retouch or screenshot selection. The existing retail and December 2019 sources strongly favor the original, but original print source would close the condition.

**B1: CE-exclusive side test.** Compare exact as-shipped reversible cover artwork from standalone PS4 copies versus CE copies, front/back. If absolutely identical, it raises the prior for a standalone-completable explanation without excluding a communal CE dependency. Any **CE-only** structural mark or extra printed element would materially reopen COVER-B.

Run the authentic standard **acorn generation-41 mathematics** by `python scripts/verify_historical_acorn_41_life.py --render`. That 30×15 mask is only a component of the 2021 original operation; it is NOT yet an independently registered cover or CE overlay.

## Disposition and revised rank

**COVER-A is now the source-economical leading *interpretation* of the independently advertised cover clue.** It is a conditional, source-linked inference that explicitly pre-dates our project and is not a new claim to have solved the remaining CE foreground.

**COVER-B remains a research alternative**, and the [CX-C](2026-10-09-cx-c-typed-cover-stage-pilot.md) four-monitor scheme should no longer be the default destination hypothesis without original evidence identifying a true four-stage chain. Better to use cover as an *historical operation precedent* unless fresh source physics demands it as a CE receiver.

A negative result on A1 (figure wholly unrelated to old running-man graphic) would seriously weaken COVER-A as a specific cover decoder, but not erase the original 2021 cross-artifact operation. A result on any new actual CE sticker cannot by itself prove this particular cover purpose.

**No outreach undertaken. No symbol ledger changes. No new encoded message.**

## New actual A1 source-pixel evidence: the juxtaposition is in the archival 2020 print scan

[CL-15 original scan acquisition and source-registered crop audit](2026-10-09-cl15-cover-source-authentic-a1.md) has now **run successfully**, with all six original source Git hashes matched ([run 38024716054](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38024716054), [pixel-control run 38024971110](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38024971110)). The internal cover has two truly separate visible items:

* A **small orange acorn-family raster on a lit front monitor**, with native-source monitor crop at `x3780..3948, y3294..3418`. Historic 84×62 crop correlation **0.900300** to the source scan at fixed half resolution, vs **0.040212** at same spot on exterior control.
* A **running human silhouette on a brightly lit separate platform beyond the tall window**, visually visible in full-resolution native source A around `x5550..6500, y2850..3600`. This person is in a running pose; the image itself proves only a *scene figure*, not that it is the exact independent 2021 "running man" *cipher bitmap*.

For provenance, the planet and graph monitors also independently match at their source coordinates with grayscale correlations **0.912542** and **0.859104** (exterior controls negative). Exact coordinates, byte hashes, and script are fixed in [the machine-readable A1 source-provenance fixture](../../data/cover-original-monitor-registration-2026-10-09.json).

This **closes the physical coexistence question** with stronger evidence than the 2022 Discord interpretation, and eliminates the possibility that the source association was merely a misremembered composite screenshot. The remaining A1 question is **intentional reference/registration**, which remains open until an independently authenticated original running-man *puzzle graphic* or 2021 demonstration is available. Do not count a visual person as automatically the same piece of cipher data.

**Next retrieval:** [exact known 2021 acorn demonstration attachment](../../scripts/probe_historical_acorn_2021_video.py) has a separate one-time, read-only archival CDN probe ([workflow](../../.github/workflows/one-shot-acorn-video-2021.yml)). Any HTTP error must be reported as an access outcome, not treated as failure of the 2021 first-person witness testimony. Any retrieved MP4 still needs source/pixel verification before claiming independent reproduction of the historical overlay.

