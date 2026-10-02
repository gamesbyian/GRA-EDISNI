# Experiment 360 — cross-format row-order predictivity audit

_Status: exploratory utility calibration, 2 Oct 2026._

## Prompt

A community solver suggested that the next useful step may be to sort the row order under the competing 9×12 and 12×9 layouts, because a better row order could make the missing sticker values easier to guess.

Experiments 345 and 347 already asked whether same-symbol boundary continuity identifies an attractive row order. They found no independently licensed order. What they did **not** test is the practical claim behind the suggestion:

> even if the optimized row order is not evidence by itself, does it actually make held-out known stickers easier to infer?

Experiment 360 tests that directly.

## Inputs and guardrails

Use only `data/observations.csv`.

No prediction-matrix fills, background pixels, POS3, recursive machine, Pigpen codebook, semantic image target, or unknown sticker guesses enter the optimization.

The ordering score is not newly fitted here. It is the same frozen observation-only boundary score used in Experiments 345 and 347:

- +1 for aligned known-known symbols that match;
- -1 for aligned known-known symbols that differ;
- 0 if either cell is unknown.

Both obvious format/order families are tested:

1. **9×12:** nine A-I traces are the permutable rows;
2. **12×9:** twelve consecutive 9-residue H108 rows are the permutable rows.

This is an exploratory utility calibration, not prospective evidence for an ordering mechanism. The score and format families existed before this test, but the held-out-prediction statistic is new.

## Leave-one-observation-out test

For each of the 65 known H108 residues:

1. hide that residue;
2. rebuild the chosen matrix;
3. find **all** row orders maximizing the frozen boundary score on the remaining 64 known residues;
4. locate the hidden cell's row in every maximizing order;
5. inspect only currently known cells directly above/below it at the same column;
6. score each legal symbol by whether it agrees with those neighbors;
7. average over the complete maximizing-order ensemble;
8. predict only if one legal symbol has a strictly higher score; otherwise abstain.

The legal alphabet is fixed by the physical split:

- residues 1–81: `/` versus `-`;
- residues 82–108: `/` versus `.`.

The comparison baseline is deliberately cheap: predict the observed majority symbol in that same alphabet. On the current corpus that is `/` for the first 81 residues and `.` for the final 27.

## Results

| format | held-out predictions | correct | accuracy | majority baseline on same cells |
|---|---:|---:|---:|---:|
| 9×12 A-I row permutations | 47 / 65 | 29 | 61.70% | 33 / 47 = 70.21% |
| 12×9 sequence-row permutations | 49 / 65 | 16 | 32.65% | 29 / 49 = 59.18% |

Paired outcomes sharpen the comparison:

- **9×12:** row ordering alone rescues 5 cells the majority baseline misses, but the majority baseline rescues 9 cells the row-order predictor misses.
- **12×9:** row ordering alone rescues 3 cells, while the majority baseline rescues 16.

The body/tail split does not rescue either result:

| format | body correct / predicted | body baseline | tail correct / predicted | tail baseline |
|---|---:|---:|---:|---:|
| 9×12 | 25 / 39 | 27 / 39 | 4 / 8 | 6 / 8 |
| 12×9 | 15 / 39 | 22 / 39 | 1 / 10 | 7 / 10 |

The optimization is also not uniquely identifying one stable order. Across the leave-one-out runs, the 9×12 family has 2–16 maximizing directed orders; the 12×9 family has 4–246.

## Interpretation

The community proposal is useful because it suggests a falsifiable practical criterion: a correct or nearly correct row order ought to improve interpolation of missing cells.

Under the only row-order score already independently frozen in the project, that criterion fails.

The result is stronger than saying the optimized layouts do not obviously look meaningful. Their inferred adjacency structure does not improve blind recovery of known sticker symbols. In 9×12 it performs modestly worse than an extremely weak alphabet-majority baseline; in 12×9 it performs much worse.

Therefore:

- do **not** use continuity-optimized 9×12 or 12×9 row orders to fill unknown stickers;
- do **not** treat the maximizing orders from Experiments 345/347 as useful latent image geometry;
- keep the broader scrambled-row hypothesis open only if an **independent ordering cue** appears, or if a different image statistic is specified before inspecting its output;
- if a future ordering cue is found, rerun this exact holdout harness against that externally supplied order. A genuine ordering channel should earn its keep by improving prediction rather than merely producing a visually suggestive arrangement.

This turns row ordering into a reusable validation surface: any new proposed order can now be scored by how much it improves held-out inference over the same trivial baseline.

## Reproducibility

Run:

```bash
python scripts/audit_cross_format_row_order_predictivity.py
```

The script writes `data/experiment-360-row-order-predictivity.json` and contains frozen regression assertions for the current corpus.
