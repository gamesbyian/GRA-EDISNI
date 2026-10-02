# Experiment 362 — known-solution calibration of row continuity on the PC acorn

_Status: completed historical positive control, 2 Oct 2026._

## Question

Experiments 345, 347, and 360 used a deliberately simple aligned-symbol continuity score to ask whether H108 rows could be self-ordered:

- +1 for aligned equal symbols;
- -1 for aligned unequal symbols.

The sticker results were negative, including failure to improve leave-one-out symbol prediction. But a negative result is much more informative if the score can actually detect a genuine Playdead row-ordering puzzle.

The newly recovered canonical PC/PS4 acorn row order provides exactly that positive control.

## Inputs

- raw PC/PS4 long rows: `data/printer-reference/pc-ps4-raw.txt`;
- primary archived solved order: `data/printer-reference/pc-ps4-acorn-order.txt`.

The solved fixture is independent of this test: it was posted by the community on 9 Jul 2018 as **“acorn order version.”**

Only the 32 full-length rows participate.

## Frozen score

For every pair of adjacent 32-character rows, compare aligned columns:

- +1 if the symbols match;
- -1 if they differ.

Sum across all 31 row boundaries.

This is the complete-data form of the same continuity statistic used on H108.

No image recognition, acorn template, `41` template, row-edge labels, or semantic fitting enters the score.

## Null

Generate 100,000 deterministic uniform random permutations of the same 32 rows with seed `362`.

The canonical order itself is not included specially in the null.

## Result

| measure | value |
|---|---:|
| canonical acorn score | **176** |
| random-permutation mean | about **−15.1** |
| random-permutation SD | about **32.3** |
| highest of 100,000 shuffled controls | **132** |
| shuffled controls scoring >= canonical | **0 / 100,000** |
| add-one Monte Carlo tail estimate | **< 0.00001** |

The source/publication row order scores 124. That is also unusually coherent, but it is not a valid random control because the published listing itself was already sorted/organized. The randomized null is the relevant comparison.

A simple z-style separation using the permutation mean and SD is roughly **5.9 standard deviations**.

## Where the signal lives

The same audit is repeated on preregistered descriptive slices, not as separate hypothesis tests:

- left 8 columns;
- right 8 columns;
- inner 24 columns.

The canonical order is especially strong in the left and inner regions, consistent with the 2018 discussion emphasizing first-appearance structure, margin slashes, and an interlaced body. This is descriptive support for the historical reconstruction, not a new decoding rule.

## Interpretation

This is an important calibration for the sticker row-order question.

The continuity statistic is **not intrinsically too weak** to register that a real Playdead image order has nonrandom adjacency. On the known PC acorn puzzle the canonical order produces an enormous positive signal without using an acorn template. Experiment 363 adds the crucial limitation: maximizing this score does not recover the canonical image and instead finds higher-scoring wrong arrangements.

That sharpens the negative H108 evidence:

- Experiment 345: neither known 9×12 order is unusually continuous;
- Experiment 347: the historical 12×9 serial order is ordinary-to-poor;
- Experiment 360: continuity-optimized H108 orders do not improve blind held-out symbol recovery;
- Experiment 361: the literal Xbox envelope grammar is physically contradicted;
- Experiment 362: the same generic continuity family gives the independently solved PC acorn ordering a strong positive-control signal;
- Experiment 363: blind maximization nevertheless overfits the PC corpus and does not reconstruct the acorn.

Therefore the present sticker corpus does **not** behave like the PC acorn under the most transferable image-adjacency statistic.

This does not prove that no row permutation exists. It means a productive future row-order hypothesis needs a different independently supplied registration channel, not merely more aggressive optimization of foreground adjacency.

## Reproducibility

Run:

```bash
python scripts/calibrate_pc_acorn_row_continuity.py
```

The script writes `data/experiment-362-pc-acorn-row-continuity.json`.
