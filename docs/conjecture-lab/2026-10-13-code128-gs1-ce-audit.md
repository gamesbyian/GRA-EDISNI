# CL-BAR-01: Code 128, GTIN, and physical CE barcode audit

**Date:** 13 October 2026. **Research mode:** DISCOVER with exact bounded negative tests, source-first subsequent acquisition. **Status:** direct sticker-width model rejected; no independently decoded INSIDE/CE barcode supplied. **No new physical sticker, recovered solution, consumer, or changed machine state.**

## Trigger and independent distinctions

A Discord participant reported using [CrypTool 2](https://www.cryptool.org/en/ct2/) on a barcode in the INSIDE ARG. They shared a screenshot of the **Code 128 specification text**, including the phrase "108 symbols," and another participant suggested GTIN/GS1 application identifiers. The pictured text is a *barcode alphabet specification*, **not a decoded barcode payload**. The source barcode image, its location, the exact symbology identification and its actual scanner output are **not available in this report**.

- **Code 128** is a variable-length 1D barcoding symbology, with code sets A/B/C, a mandatory weighted **modulo-103** checksum and start/stop patterns. The commonly quoted **108** counts distinct symbol patterns (including reverse-stop representation), **not** 108 characters of user payload or 108 modules in a scanned barcode. Each ordinary character uses six alternating bar/space widths, total **11 modules**. Its stop is **seven elements / 13 modules**. GS1 standard: [GS1 General Specifications, 5.4](https://ref.gs1.org/standards/genspecs/21.0.1/).
- **GS1-128** is a *constrained usage of Code 128*, recognized by a **FNC1 immediately after its start**. The Application Identifiers (AIs) are part of its decoded data. A plain Code 128 string beginning with `01` is **not automatically** a GS1 GTIN field. See [GS1 FAQ](https://support.gs1.org/support/solutions/articles/43000734455-what-is-the-format-of-gs1-128-) and [GS1 US](https://www.gs1us.org/upcs-barcodes-prefixes/gs1-128).
- **GTIN** is an item identifier, commonly represented by EAN/UPC/ITF or as a GS1 AI field `(01)` with **14 following digits**. `(10)` means lot/batch, `(21)` means serial; some values are variable length and require GS/FNC1 separation if followed by another field. A checksum-valid GTIN does **not** prove issuer assignment, a particular sticker number, or puzzle content. [GS1 US technical AI summary](https://gs1us.org/content/dam/gs1us/documents/industries-insights/by-industry/food/North-American-Guidance-for-Case-Code-Labeling.pdf).
- The formerly observed **128 UNSOLVED** footer of the damaged `534brn` JPEG belongs to prior [Experiment 413](../experiment-413-534brn-footer-128-unsolved.md); **128** there has no demonstrated Code 128 or GS1 relationship. [Experiment 423](../experiment-423-534brn-mcu-constraint.md) already documents why damaged entropy cannot uniquely fix 128×128.

## CL-BAR-01 bounded raw-foreground width test

**Inputs:** exact repository `data/observations.csv` current as of this test: **84 physical rows, 66 distinct H108 residues, 42 unknown**; do *not* replace unknowns with incumbent-machine predictions or the Discord rendering. Serial ascending positions 1..108; residue 108 is the cycle's zero position.

**Conditional model:** one sticker mark (`-`, `/`, `.`) encodes **one bar or space element width** in a Code 128 character. Test *injective* width assignments of three different marks to three of the possible four element widths (24 maps), both directions, and all 6 phase offsets. In each resulting complete six-element chunk, require at least one match with the **106 actual six-element Code 128 patterns** (0..105), respecting known sticker marks and treating the rest as genuinely missing. Ignore unmatched boundaries to make the proposal more permissive. This is a test of a **specific** three-width embedding, not every possible barcode embedding or a generated codeword model.

**Measured result** (`python scripts/conjecture_lab_code128_widths.py --controls 500`):

| Observable | Result |
|---|---:|
| Candidate fitted map/direction/phase combinations | 288 |
| Candidates with all tested chunks compatible | **0 / 288** |
| Minimum incompatible six-element chunks across all fits | **3** |
| Fitted candidates attaining minimum 3 | 4 |
| Frame-preserving shuffled controls with *at most* 3 failures | **500 / 500** |
| Region-preserving shuffled controls with *at most* 3 failures | **497 / 500** |
| Region-preserving controls with **0** failures | 5 / 500 |

Controls are reproducible pseudo-random shuffles with seed `128108`. The frame-preserving null retains the nine-position frame, original observation-mask positions, each frame's glyph counts, and the first-81/last-27 mark-type distinction; the region-preserving null retains observation masks and symbol counts separately within 81/27. In **both**, model selection is repeated across all 288 parameter fits for each shuffled corpus (not merely compared to the real-data winning map). These tests are conditional, exploratory and matched-null descriptive, **not** estimated probability that *any barcode hypothesis* is true.

**Conclusion:** The straightforward three-mark → three-distinct-Code128-element-width scheme is contradicted at at least three chunks under every tested direction/phase/mapping. Real sticker data are no more barcode-pattern-compatible than either matched-null family. This cannot exclude a different width mapping (e.g. two glyphs sharing a width), an unspecified stripe run transform, a rearranged order, a separate codeword dictionary, an explicit key to a scanned barcode, or a more complex inter-artifact reader. Such extensions need an actual external cue before being treated as validation.

**Separate exact length rejection:** 108 marks viewed as individual *modules* cannot form an entire Code 128 symbol without quiet zones because the total is `11 * N + 35` (one start, N intermediate characters, one check, 13-module stop), and 108−35=73 is not divisible by 11. Adding GS1 FNC1 gives `11 * N + 46`, and 108−46=62 is likewise not divisible by 11. Requiring the two minimum 10-module quiet zones cannot fix either congruence. If 108 stickers represent *individual bar/space elements*, a complete standard symbol requires `6*(N+2)+7` elements, also inconsistent with 108. An *incomplete* region or an element-multiplier can still be imagined, but it is a different hypothesis. Code 128's "108 distinct symbols" alone gives no indexing relationship to a 108-position sticker *sequence*.

## A separate prospective source-first test: actual packaged barcode

The official [iam8bit full Collector's Edition listing](https://www.iam8bit.com/products/inside-collector-s-edition) establishes a boxed edition with a physical PS4 disc, art cards and poster. The [standalone limited PS4 game](https://www.iam8bit.com/products/inside-ps4-physical-game) is a **different product**, even though it was also sold by iam8bit and has related marketing art. A product listing's identifier is not necessarily a printed symbology or the edition-specific copy serial. See [the repo's exact product differentiation](../reference/inside-ce-edition-product-differentiation-and-triage.md).

**Acquire without bothering owners:** original high-resolution exterior packaging/back-of-case photos already in the public CE/PS4 scans, auction/unboxing media, original ARG image files, and first-party dated source mirrors. Do not use synthetic upscales as barcode witnesses. For each original image, preserve its source URL/asset identity, date, exact physical object classification (CE premium outer box, numbered wrapper, enclosed PS4 case, standalone PS4 case, printer/ARG page, in-game texture), and whether the barcode pixels are actually legible. Reused publicity images and copies transferred between sellers are not independent specimens.

**Decode workflow:**

1. Record unmodified source image and apparent human-readable digits before analysis. For machine scan, install optional `zxing-cpp` and Pillow and run `python scripts/inspect_arg_barcodes.py --image /path/to/file.png`; capture the declared symbology, scanner identifier, escaped payload and raw bytes. Recheck important finds independently with a second decoder, e.g. ZBar or a separate ZXing implementation; never silently OCR digits or autocorrect a checksum failure.
2. If only a human-decoded numeric value exists, run `--payload '...' --format EAN-13` *only if the physical barcode family is externally identified*. The standard-library tool validates the check digit without turning any 13-digit substring into a manufactured product match. For scanner-verified GS1-128, preserve the leading `]C1` if provided and explicit ASCII GS (`\x1d`) separators. Printed parentheses are **human-readable annotation**, not data encoded as parentheses.
3. Compare independently confirmed product identifiers against official registries or first-party item records; note if CE and standalone case barcodes coincide. Check checksum and segment AI structure **before** testing any overlap with sticker numbers, the `534brn` URL's nine digits, ARG string snippets, or conditional model outputs. All such cross-puzzle matches are post-hoc until an original physical cue specifies an operation.
4. Never claim that a randomly scanned Code 128 text is "cryptic" because its content looks odd; or that a legitimate retail UPC necessarily contains ARG information. Actual scanner output, physical provenance, and explanation of why that field might be used are the discriminators.

## Status / evidence needed for next step

- **Completed:** no mapping of three marks to three distinct widths yields a physically compatible standard six-element sequence across all 108 positions; control distributions included. Reproducer and JSON artifact linked above, and deterministic unit tests under `tests/test_inspect_arg_barcodes.py`.
- **Not yet available:** the photographed code the Discord user entered, its exact scanner output, and an authoritative CE or enclosed PS4 case barcode value. Thus **no CE barcode has been independently scanned or connected to the ARG in this lane**.
- **Highest-value new fact:** specific barcode *image + original location + exact decoder output*. This supplies a naturally limited source-driven comparison without inventing a second cipher from the number 108.

**Re-run:**

```bash
python -m unittest discover -s tests -p test_inspect_arg_barcodes.py -v
python scripts/conjecture_lab_code128_widths.py --selftest
python scripts/conjecture_lab_code128_widths.py --controls 500 --output data/conjecture-lab-code128-widths-2026-10-13.json
python scripts/inspect_arg_barcodes.py --payload ']C1010400638133393121A37' --format CODE-128
```