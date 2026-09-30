# Experiment 337 — null calibration of the row-vs-column asymmetry

_Status: completed retrospective calibration, 30 Sep 2026._

## Why this matters

Experiment 329 found:

```
row/chunk one-exception survivors = 12
column/rail one-exception survivors = 0
```

That looked intriguing, but the one-exception criterion was introduced **after** the row/column outputs had already been inspected. It therefore needs a hostile null calibration before anyone treats 12-vs-0 as evidence of intended design.

This experiment does not convert the result into a pristine p-value. It asks a narrower question:

> how often does a qualitative "rows survive, columns die" asymmetry arise by chance under simple fixed-mask symbol permutations?

## Null 1 — global fixed-mask/census permutation

Preserve:

- the exact 54 observed body locations;
- 32 observed slashes and 22 observed dashes;
- all unknown locations;
- the tail-derived allowed selector positions from Experiment 317.

Randomly permute the 54 slash/dash labels over the fixed known-cell mask.

200,000 deterministic permutations, seed 337.

Observed qualitative event:

```
row survivors > 0 AND column survivors = 0
```

occurs:

```
55,905 / 200,000 = 27.95%
```

The exact post-hoc outcome `(row=12, column=0)` occurs 8,503 times = 4.25%, but that exact count was not specified beforehand and should not be interpreted as a confirmatory p-value.

## Null 2 — within-class matched permutation

A stricter null preserves, separately for each A-I class:

- which body cells are observed;
- that class's observed slash/dash census.

Only positions within the same class are shuffled.

Again 200,000 deterministic permutations.

The qualitative event `row>0, column=0` occurs:

```
44,721 / 200,000 = 22.36%
```

The exact `12,0` outcome occurs:

```
6,483 / 200,000 = 3.24%
```

## Interpretation

The direction of Experiment 329's result is **not rare** under either reasonable null.

Roughly one quarter of null datasets produce the same qualitative story: at least one global row-selector completion survives while every column-selector completion fails.

That substantially downgrades the retrospective evidentiary weight of Experiment 329.

The right status is:

- the row-selector family remains a coherent frozen rival;
- its 4/54 leave-one-out predictions from Experiment 330 remain genuine post-freeze tests;
- residues 84 and 102 remain valid prospective falsification targets;
- the original 12-vs-0 discovery itself should **not** be cited as strong evidence that row selection was intended.

## Consequence

Keep `data/frozen-row-selector-predictions.json` frozen for prospective testing, but label its discovery basis as weak/post-hoc.

Do not add further rules to rescue or strengthen the family from the current corpus.

Future evidentiary weight should come from:

1. a newly recovered physical residue 84 or 102;
2. an independent historical message explicitly proposing the same row+exception operation;
3. another ARG artifact supplying this operation;
4. or a genuinely preregistered holdout not used in forming the family.

## Reproducibility

```bash
python scripts/audit_row_selector_null.py
```
