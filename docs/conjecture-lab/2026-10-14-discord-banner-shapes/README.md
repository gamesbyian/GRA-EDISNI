# Discord 108-cell banner layout / row-order follow-up

14 October 2026. **DISCOVER, exploratory only.** The new Discord screenshot places the 108 entries into **6 columns × 18 rows** (left) and **4 columns × 27 rows** (right). The proposal is to permute entire rows without filling missing stickers, and possibly discover an inscription when rotated sideways.

## Evidence and provenance

- The canonical source is the 108-character community master plus **physical** observations in data/observations.csv: **66 physically supported symbols, 42 unknown**.
- Sticker **427** physically confirms **residue 103 as a dot** (its background tile remains unknown). The Discord spreadsheet author also reports a **YouTube-comment** dot claim for 103; that is weaker provenance, not a reason to discard the 427 report.
- The screenshot's residue **045 dot** is a **YouTube comment, unconfirmed physically**. We explicitly test 045 as unknown *and*, separately, as a dot. No observation ledger was altered.
- All seven confirmed dots are in the **last 27** positions, which **mechanically concentrates yellow into the bottom part of narrow row-major grids**. That is an expected artifact of the source data, not standalone evidence of a glyph.

## Browse the candidate galleries

Each file shows the original and row-permuted arrangements, both upright and **rotated 90°**; unknown cells remain white. The row-source numbers are preserved.

| Corpus variant | 4×27 | 6×18 |
| --- | --- | --- |
| **66 confirmed symbols only** | [4×27 gallery](verified-4x27-gallery.svg) | [6×18 gallery](verified-6x18-gallery.svg) |
| **66 confirmed + provisional 045** | [4×27 gallery](unconfirmed-4x27-gallery.svg) | [6×18 gallery](unconfirmed-6x18-gallery.svg) |

The earlier [12×9 and 9×12 galleries](../2026-10-14-discord-row-order/README.md) remain separately archived.

## Algorithm and null controls

Score each adjacent row pair by comparing only columns where **both cells are known**: **+1 for matching symbols, −1 for different symbols, 0 if either unknown**. Optimize the order of whole rows. This objective does **not** perform OCR or discover words.

- For **12 rows or fewer**, exact Held–Karp dynamic programming maximizes this additive score without literally rendering every permutation.
- For **18, 27 and 36 rows**, deterministic greedy seeds, random seeded restarts and 2-opt yield a **heuristic lower bound**. We do **not** claim that all 27! arrangements were examined.
- In each negative control, shuffle **known marks within their original row**, retaining that row's original blank mask and counts of each mark; then apply the same optimizer. The null thus matches the physical missingness and preserves within-row symbol counts.
- Different widths, alternative scoring ideas, post-hoc orientation choice and visual reading can create false positives. Unadjusted tail fractions below are **exploratory**, not an independent multiple-testing-adjusted probability of a decoded word.

### Primary comparison: 1,000 controls per configuration

| Layout | Input | Raw original | Optimized | Mean null optimized | Nulls at least as high |
| --- | --- | ---: | ---: | ---: | ---: |
| **4×27** | Physical | 3 | 45 | 42.497 | **71/1000 (7.1%)** |
| **6×18** | Physical | −6 | 30 | 31.577 | **790/1000 (79.0%)** |
| **27×4** | Physical | 2 | 6 | −0.092 | **101/1000 (10.1%)** |
| 4×27 | +unconfirmed 045 | 3 | 45 | 42.232 | 67/1000 (6.7%) |
| 6×18 | +unconfirmed 045 | −8 | 28 | 31.069 | 914/1000 (91.4%) |
| 27×4 | +unconfirmed 045 | 0 | 4 | −1.106 | 175/1000 (17.5%) |

The 4×27 orientation is mildly more structured under this chosen score than its row-shuffled controls, but **not even below the conventional 5% nominal cutoff**, much less corrected for trying multiple widths. The **6×18** candidate is no better than random arrangements. Neither produced an unambiguous image or text. Inclusion of 045 doesn't change the conclusion.

### Exploratory eight-width sweep (240 controls per width)

| Width × height | Optimizer | Nulls ≥ optimized original |
| --- | --- | ---: |
| 3×36 | heuristic | 221/240 |
| 4×27 | heuristic | 12/240 |
| 6×18 | heuristic | 197/240 |
| 9×12 | exact | 171/240 |
| 12×9 | exact | 200/240 |
| 18×6 | exact | 137/240 |
| 27×4 | exact | 29/240 |
| 36×3 | exact | 144/240 |

The 240-trial and 1,000-trial results are **separate** matched experiments, not independent corroborating probabilities. Raw candidate scores, row orders, the null protocol and provenance are in the [machine-readable results](../../../data/conjecture-lab-banner-row-sweep-2026-10-14.json).

## Run it from the repository root

Python standard library only:

    python scripts/conjecture_lab_banner_row_sweep.py --controls 240 --out out/banner-all
    python scripts/conjecture_lab_banner_row_sweep.py --widths 4 6 27 --controls 1000 --out out/banner-focus
    python scripts/conjecture_lab_banner_row_sweep.py --widths 4 6 27 --controls 1000 --include-045 --out out/banner-045

For each width, write the original and optimized SVG and a machine-readable result.

## Interpretation and next discrimination

This is a **negative/weak result for these particular row-seam objectives**, not a proof the code cannot yield an image, word, address, instruction, or output requiring a separate operation. With **42 unknown** cells, the correct order could even fail to look legible. Three symbols might represent ternary digits, spatial layers, action codes, selectors or a receiving mechanism rather than three pixel colours.

If the intended 4×27 view is rotated into a **27 pixels wide × 4 high** text banner, it demands an unusually low-height font; the 6×18 view becomes **18 × 6** and could accommodate a small number of conventional 5-high letters. A fair word test needs an independently fixed alphabet, reading direction, glyph height and spacing, and held-out or negative controls **before** picking a pleasing inscription.

More stickers would be welcome but are **not mathematically required** by this result. Prior Experiments **345, 347, 360, 362 and 363** already found that maximized row continuity can select wrong orders even with a solved positive-control acorn image.

## Questions for Discord

1. Could the author share the **exact YouTube comment links and timestamps** for residues **045 and 103**? Is there any photograph or owner evidence behind 045? For 103, our ledger already records physical sticker 427 as a dot.
2. Does "banner" have any independent **orientation, border, line break, font, size, margin or registration clue**, or is it deliberately free exploration?
3. Is the proposed output specifically **horizontal lettering when rotated 90°**, or a vertical inscription in the upright portrait? A fixed reading geometry would let us test actual glyph templates and calibrate against matched blanks.

No new symbols were promoted to physical observations; no decoded inscription claimed.
