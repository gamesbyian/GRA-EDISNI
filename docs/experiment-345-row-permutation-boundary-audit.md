# Experiment 345 — observation-only row-permutation boundary audit

_Status: completed, 30 Sep 2026._

## Question

A new community formulation proposes that the 108-period sticker stream may be arranged as either 9×12 or 12×9, with rows then permuted until they form a coherent image, by analogy with the earlier PC/PS4 printer puzzle.

The historical analogy is legitimate at the level of **operation class**: the PC printer/acorn solve used ordering constraints external to the row payload before a coherent image emerged. It does not establish that the CE foreground itself contains enough information to recover a row permutation.

This experiment asks the cheapest pre-image-recognition question:

> If the 9×12 transpose is treated as nine 12-cell A-I class rows, do the observed foreground symbols themselves constrain a row ordering through simple boundary continuity?

## Inputs and guardrails

Use only `data/observations.csv`.

- unknown cells remain unknown;
- no prediction-matrix fills;
- no POS3;
- no recursive machine;
- no Pigpen codebook;
- no semantic or image target;
- all `9! = 362,880` A-I row permutations are enumerated exactly.

For every adjacent pair of candidate rows, compare aligned known-known cells. The frozen continuity score is:

```
+1  same observed symbol
-1  different observed symbol
 0  either cell unknown
```

The score is summed over the eight row boundaries. It is reported separately for:

- body columns 1–9;
- tail columns 10–12;
- all 12 columns.

This is intentionally crude. A failure means only that **plain same-symbol continuity is not an ordering channel**. It does not reject a separately cued permutation, an edge feature outside the foreground, or a more specific historically attested registration mark.

## Results

### All 12 columns

| order | net | matches | mismatches | known-known comparisons | fraction of all permutations scoring at least as high |
|---|---:|---:|---:|---:|---:|
| serial `ABCDEFGHI` | 0 | 18 | 18 | 36 | 0.623787 |
| physical flattening `IABCDEFGH` | -1 | 16 | 17 | 33 | 0.692014 |

The exact score range over all 362,880 permutations is **-19 to 20**.

Only two permutations attain the maximum score 20, and they are reversals of the same path:

```
ACBEIGHDF
FDHGIEBCA
```

That optimum is not evidence for this order. It is the inevitable winner of an exhaustive optimization over the same incomplete data and has no independent ordering cue.

### Body only

Both preregistered orders score net **+1**. Exactly **50.242%** of all permutations score at least that high. The full body range is -19 to 19.

### Tail only

The serial order scores **-1** and the physical flattening scores **-2**. Respectively **92.917%** and **98.631%** of all permutations score at least that high. The tail range is -4 to 5.

## Interpretation

The observed 9×12 foreground does **not** reproduce the crucial useful property of the historical printer/acorn ordering stage: it does not provide an obvious boundary-continuity signal that selects either serial order, physical order, or a narrow permutation family.

Therefore the community's "scrambled rows forming an image" hypothesis remains live only in a stronger, historically faithful form:

1. an independent sticker-native or cross-puzzle cue must specify or constrain the row permutation; or
2. a measurable physical side/perimeter/background feature must play the role that side/check marks played in the printer puzzle.

Blindly optimizing row order for a visually coherent result is not licensed. The maximum-continuity order above is retained only as a negative-control demonstration of how easily an attractive order can be manufactured by exhaustive search.

This result increases the value of the already-open physical-perimeter lane after Experiment 344, because that lane can test for a genuinely separate ordering/check-bit channel without using the foreground payload to select itself.

## Terminal41 note

Public ARG histories place `terminal41` before the Collector's Edition sticker phase: it was discovered through the hidden YouTube/website trail and later became an ARG hub. A second occurrence of the literal string on sticker material would therefore be evidence of a deliberate cross-stage link or label, not automatically another foreground payload token.

Search/acquisition should treat exact and near-variant `terminal41` occurrences as a separate provenance question.

## Reproducibility

Run:

```bash
python scripts/audit_row_permutation_boundaries.py
```

The script writes `data/experiment-345-row-permutation-boundary-audit.json` and contains regression assertions for the current corpus.
