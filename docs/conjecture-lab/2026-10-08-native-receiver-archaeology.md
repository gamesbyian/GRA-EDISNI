# Conjecture Lab CL-04: actual image receivers, not an imaginary 512-entry library

_Date: 2026-10-08. Status: DISCOVER/DEVELOP. Supports the [first sprint](2026-10-08-first-sprint.md), [second sprint](2026-10-08-second-sprint.md), and [source-first consumer audit](../experiment-476-receiver-native-geometry-audit.md). A candidate location is not evidence of a sticker decoder._

## What changed

The first two CL-01/02 sprints showed that the sticker body *could* be treated as nine 9-bit addresses in `0..511`, while each one-hot Q4 stack *could* select one of three readout channels. Looking for a hypothetical “512-entry three-channel artifact” is too abstract. The original Playdead ARG **already contained image artifacts with explicitly demonstrated pixel selection and colour operations**:

1. A historically delivered Playdead printer output had a third image reported at **6656 × 6656 pixels (~25 MB)**. The first two printouts used **red/green/blue colour-coded lines**, with red as separator, green as bit 1 and blue as bit 0. This is an *actual established output mechanism*, not a conjectured static web index. The third image encoded a spectrogram leading to Terminal41. Source: [Game Detectives Printer Button](https://wiki.gamedetectives.net/w/Inside_ARG#Printer_Button), and the 2019 uploader's separate [first](https://wiki.gamedetectives.net/w/File:Inside_printout_1.png) and [second](https://wiki.gamedetectives.net/w/File:Inside_printout_2.png) **2222 × 2222 copies**. Those wiki sizes describe preserved/reduced copies; do not assume they are the original source sizes.
2. The historically linked `/comms/gate/98/` transmission image is reported at **2048 × 4096** pixels. Community solvers sampled pixels of exactly selected RGB values **every 16 pixels** from the top-left corner and combined **seven different exact colour selections** to reconstruct a hidden URI and planet scan. Source: [Game Detectives gate-98 sequence](https://wiki.gamedetectives.net/w/Inside_ARG#Printer_Button). This is unusually strong historical precedent for a **pixel-position and channel/layer extraction operation**.
3. The full preserved gate-98 PNG exists as a **19,360,240-byte Git blob** in [twinysam/INSIDE-ARG](https://github.com/twinysam/INSIDE-ARG), at `terminal41.link/comms/gate/98/transmission_id41786174541g1f561f4186454544fdrfd532430980980000000000000000k.png`, Git blob SHA-1 `127d8772912ffc499e5afaffe321d5bab7e920df`. This repository currently preserves the link and HTML but not the large PNG. The [CL-04 original-pixel probe](../../scripts/conjecture_lab_gate98_real_pixels.py) verifies its **exact bytes before analysis** and refuses a different source.

**Chronology:** these printer/terminal images existed during the **2018** original ARG, predating the CE shipments in December 2019. A sticker relation would be an intentionally delayed/retrospective second use, not evidence those older images were originally made for the CE.

## Receiver fit: what is genuinely native?

| Candidate original asset | Real pre-sticker operation | Can contain 512 numeric positions? | Three independent channels actually instructed? | CE sticker bridge |
|---|---|---|---|---|
| 74 archived Terminal41 URLs | Browse routes; CE *background* path source-indexed | **No** for four literal nine-bit conventions using observed sticker bits alone (CL-01 v2) | No | Negative for this direct reader |
| Third Playdead printout, reported 6656² | Spectrogram conversion; preceding first/second images use RGB colour→binary | Numerically yes: `6656 = 13 × 512`; very many possible banks/rows | **No demonstrated three independent selectable pixel planes for the third image** | Weak capacity coincidence, true design-family analogy |
| Gate-98 2048×4096 source PNG | **Exact-colour image selection at stride 16; 7 palette selections historically combined** | Grid after stride 16 is `128 × 256 = 32768` positions = `64 × 512` | Historical seven exact RGB colours are **not** a documented three-way RGB-channel selector | Strong operation precedent, **no source-fixed 512 block or channel mapping** |
| Physically linked damaged `534brn...` CE page | CE background identifies page; partially damaged image/footer `128 UNSOLVED` | Unknown decoded image size / no 512-record index defined | No | **Best direct same-sticker destination**, but lacks a reader |
| Surviving 22-underscore Viewgate / 22-char SAF island | Display and static source field | No shown numeric corpus | No | Not a verified input control |
| In-game original lever | Genuine ordered three-direction actions, 14 known moves | Not a numeric table | Yes, but input type is *actions*, not RGB channels | No nine-position consumer in preserved authentic game |

A direct 9-bit *address* is not automatically a pixel x-coordinate, nor a flattened index into arbitrarily partitioned image data. A modern PNG's red/green/blue storage does not prove Playdead intended `Q4=RGB`. The historical code used **seven exact RGB colours**, not three raw components; seven and three are materially different alphabets.

## Quantify the severe ambiguity before searching for an output

**Gate-98**. The historically described `16`-pixel sampling produces `128` positions horizontally and `256` vertically, or `32768` sampled sites. Choosing a contiguous 512-site **row-major block** divides that into **64 possible non-overlapping banks** of `128×4`. Nothing in the known archived clue supplies a bank `0..63`, or establishes that records should be grouped row-major, or says selector depth `0,1,2` means `R,G,B`. Allowing all possible 16×16 sampling origins, arbitrary permutations of the three RGB component labels, or x/y traversal would vastly inflate selection freedom. **CL-04 fixes origin (0,0), original row-major order, one 512-site bank, native Q4-to-RGB order solely as an *invented and logged* test**, and enumerates all 64 banks without choosing the best one.

**Third printout**. Taking its original `6656` pixel width literally, it divides into **13** non-overlapping strips of width 512. If a 9-bit value indexed the x coordinate in any one of 6656 rows, there would already be `13×6656 = 86,528` equally sized source positions for selecting which strip and which row, before channel choices or alternate origin. The existence of a 512-divisible dimension is a **capacity match**, not a source instruction. The preserved 2222-pixel wiki copies cannot be used as original 512-lattice controls because scaling alters coordinates.

**CL-02 three numeric rows**. The post-selected binary `189 / 252 / 315` cannot all be *direct sampled x indices* of the gate-98 lattice (max x=127), nor all direct *sampled y indices* (max y=255). A flattened address into any 512-site bank remains numerically allowed but requires the bank and traversal bridge. This is a concrete small negative for an especially tempting simple interpretation.

## Exact original-image replay

`scripts/conjecture_lab_gate98_real_pixels.py` provides an executable, reproducible experiment:

```bash
python -m pip install Pillow
python scripts/conjecture_lab_gate98_real_pixels.py --source /path/to/original.png --output gate98-cl04-results.json
# Or omit --source to fetch exact original bytes from upstream GitHub.
```

It performs:

1. **Source authentication first**: 19,360,240 bytes, Git SHA-1 `127d877...`, original PNG dimensions 2048×4096; refuse changed or substituted PNG bytes.
2. Compute the full 128×256 stride-16 sampled lattice at fixed top-left (0,0). Record original image mode, full RGB colour census and the most common exact pixel colours, including black/white counts. This helps distinguish actual encoded colour classes from normal RGB image detail.
3. Enumerate **all 64 bank readouts** for the two conditional balanced-Q4 complete masters (the already-known canonical hidden states `0100` and `1100`). Decode all nine class-word addresses forward slash=1, take the native depth selector as provisional R/G/B component, and preserve **every output in hex** with bank number.
4. Report ASCII-printable bytes for diagnostics only. An attractive bank is not chosen as a solution, and no statistical significance or target recovery is claimed from a dictionary/ASCII fit.

The source image is ~19.36 MB, so the experiment uses a **temporary narrowly scoped PR workflow** to obtain it via the public original repository without embedding a near-20-MB duplicate in our main history. The small results artifact and measured properties should be extracted into `data/` and cited here; remove the temporary network workflow before final merge.

The temporary file's original hash is a Git blob hash, not a PNG pixel checksum or a historical server certificate. Passing it shows that we analysed the **same bytes as the preserved original-community Git repository**, not that the original web server bytes and publication date are independently authenticated.

## Outcome interpretation and decisive next source requests

- **Success for source acquisition:** exact Git SHA verified; PNG decoded; native sampled lattice reproduced; all candidate readouts enumerated. This does *not* make the hypothetical sticker connection true.
- **Success for an evidentiary decoder:** requires an **independently authored** rule selecting a 512-site bank, the A–I class order and which RGB colour value/channel to read, **plus** a recognizable output or untouched holdout. No such rule is currently known.
- **Failure of this frozen simple implementation:** source bytes or 16px grid absent; addresses out of bounds; no native source support; or uninterpretable exhaustive 64-bank results. A failure only rejects this exact image reader, not every possible visual/overlay scheme.

**Highest-value original evidence:** authentic gate-98 sprite/PNG palette instructions, historical Discord image assembly notes fixing the precise seven hex RGB values, a pre-CE or CE-era instruction that says “which 512 sites” to read, and the original untouched third printout (not reduced wiki display). Keep the physically linked `534brn` page as a parallel top destination, even if Gate-98's previously solved image never accepts new CE input.

## Physical prediction boundary

The Q4 balance reader is *not* independent from the incumbent: exactly the two existing `p=0, G=0` 10-state live machine candidates survive. Its forecast at missing residue **84** is slash, in direct conflict with the [frozen 329 row-selector forecast](../../data/frozen-row-selector-predictions.json) of dot. Residue **102** is dot, also opposed to frozen 329's slash. These are genuinely mutually exclusive **prospective** physical tests of two *conditional* theories. But neither physical mark would by itself connect them to Gate-98; that still demands a source-native consumer.

_Conclusion: we have located an authentic image-reading operation family with enough pixel capacity for the speculative 512+RGB notion; we have not located an independently constrained foreground reader. The difference is now quantified, source-pinned, and testable rather than rhetorical._
