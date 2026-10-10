# CX-E3: literal source-receiver control for both native nine-class fields

_9 October 2026. Observation-only bounded negative comparison. Source: original physical [sticker ledger](../../data/observations.csv), original Xbox [printer rows](../../data/printer-reference/xbox-one-raw.txt) and already solved CE background URL digit sequence `534965398`. Executable: [CX-E3 native receiving audit](../../scripts/conjecture_lab_cx_e3_native_receivers.py). No sticker filling, decryptions or inferred physical observations._

## Hypotheses to try to break

The rail-field proposal [CX-E2](2026-10-09-cx-e2-four-nine-twelve-fields.md) splits each 27-symbol quarter at two physically observed `/` separators: `4 / 9 / (9+3)`. Consequently it yields **two** separately complete nine-image-class fields per quarter:

* **Middle field** positions 6–14 in each quarter: F G H I A B C D E, with **19/36** observed.
* **Second/suffix field** positions 16–24: G H I A B C D E F, with **24/36** observed.
* Both can be placed in independently solved IAB/CDE/FGH physical geometry, or flattened as four nine-symbol serial strips. No unlicensed class permutation is required by these chosen layouts.

Four nine-symbol fields give 36 symbols, exactly the original Xbox printer width. To test the *cheapest exact source match*, the script compares both channels in three **predeclared** orders with **all 35 unique historical full-width Xbox strips**, forward or reversed. Missing sticker symbols are wildcards, **not** filled from printer symbols. This is six fields-readouts × 35 original rows × 2 directions = 420 literal comparisons; the Xbox duplicate boundary row is not double-counted.

| Field | Fixed 36-symbol order | Observed sites | Minimum observed conflicts out of 35×2 comparisons |
| --- | --- | ---: | ---: |
| middle | quarter-major, native serial order | 19 | **6** |
| middle | quarter-major, physical IAB/CDE/FGH | 19 | **6** |
| middle | class-major, four quarters per class | 19 | **9** |
| second | quarter-major, native serial order | 24 | **10** |
| second | quarter-major, physical IAB/CDE/FGH | 24 | **11** |
| second | class-major, four quarters per class | 24 | **10** |

Every tested unchanged-row reuse fails on already observed physical marks. Relative to Experiment 476, this tests **different 36-symbol channels extracted from 4×27 rails**, rather than the three contiguous 36-residue H108 sections. It closes these literal readouts, **not** a multirow composite, selective mask, native overlay, or reader using transformations defined by a different source.

## A second literal receiver: nine URL digits as shared-value keys

Experiment 382 previously established the sticker background classes' row-major physical layout IAB/CDE/FGH as the native class registration. Treat the nine URL digits `534965398` as labels on that physical grid:

```text
class:   I A B     digits: 5 3 4
         C D E             9 6 5
         F G H             3 9 8
```

Three labels occur twice: **5** at I/E, **3** at A/F, and **9** at C/G. Suppose a simple lookup decoder means that *within one quarter*, an identical digit means **an identical slash/dash/dot state**, regardless of which tile carries it.

The **first** nine-symbol middle field already falsifies this strict rule twice, on complete observed pairs:

* Label 5: I observed `/`, E observed `-`.
* Label 9: C observed `-`, G observed `/`.

The label-3 pair still contains an unobserved cell in this quarter. No unknown physical cell can repair the two known equality contradictions. Other quarters do not supply an offsetting rescue: the rule asserted equality **within each** quarter.

This rejection has narrow scope. It does not refute digits as pointers, values to increment/toggle, repeated writes, checksums, geometric offsets or ternary-row coordinates. [SR-03's three rival repeated-address operators](../speculative-sr03-keypad-revisit-pilot-2026-10-09.md) remain separate; they cannot be relabelled as the falsified simple same-state decoder.

## Receiving artifact status

The authentic linked [`534brn` source page](../../archive/external/twinysam-inside-arg/terminal41.link/dat/534brn9653f9j8mmd/index.html) contains an embedded corrupted JPEG-like byte stream and a Terminal41 tail, not a preserved `4/9/12` input form or character-code legend. This page's exact original bytes and damaged-image alignment ambiguities are audited in CL-09/10. The [PS4 cover](../experiment-409-cover-operation-family-audit.md) has four monitor references and is genuinely clue-bearing, but source-matched research found no repeated native transformation across all four references (Exp. 412). The [foldout poster](../experiment-481-poster-cross-edition-gallery.md) has approximately nine authored sketches; no independent correspondence to the CE glyphs is established.

There is therefore **no authenticated consumer for these fields** in the source material reviewed for this particular test. This is not a claim that the entire historic Internet or complete original source corpus lacks one. The next valuable acquisition is a source-defined use of the nine-site class grid *or* a specific delimiter/adapter, rather than another fitted 36-character string.

## Reproduction and disposition

```sh
python scripts/conjecture_lab_cx_e3_native_receivers.py
```

**VALIDATE limited negatives:** 420 exact unchanged Xbox-row comparisons fail; equal-digit→equal-symbol rule fails on two physically observed pairs. **DEVELOP remains open:** field delimiters, operations on the two grids, and payload metadata can still be conjectured. Do not raise a positive evidence score on the basis of their 36-character capacity alone.
