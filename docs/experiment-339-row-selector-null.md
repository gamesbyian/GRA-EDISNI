# Experiment 339 — null calibration of the row-vs-column asymmetry

_Status: completed retrospective calibration, 30 Sep 2026._

## Why this matters

Experiment 329 found 12 observation-compatible row/chunk assignments and zero column/rail assignments after introducing the one-exception criterion.

That criterion was introduced **after** the row/column outputs had already been inspected. The 12-vs-0 contrast therefore needs hostile calibration before it can be treated as evidence of intended design.

## Null 1 — global fixed-mask/census permutation

Preserve the exact 54 observed body locations, all unknown locations, the global 32-slash/22-dash census, and the tail-derived selector domains from Experiment 317. Randomly permute slash/dash labels over the known-cell mask.

With 200,000 deterministic permutations (seed 339), the qualitative event:

```
row survivors > 0 AND column survivors = 0
```

occurs:

```
55,766 / 200,000 = 27.883%
```

The exact post-hoc outcome `row=12, column=0` occurs 8,631 times = 4.316%. That exact count was not specified beforehand and is not a confirmatory p-value.

## Null 2 — within-class matched permutation

Preserve, separately for each A-I class, the observed-cell mask and that class's slash/dash census. Shuffle only within class.

The qualitative `row>0, column=0` event occurs:

```
44,807 / 200,000 = 22.404%
```

The exact `12,0` outcome occurs:

```
6,459 / 200,000 = 3.230%
```

## Interpretation

The qualitative Experiment-329 asymmetry is not rare. Roughly one quarter of matched null datasets tell the same story: some row solution survives while every column solution dies.

This materially downgrades the retrospective case for the row-selector interpretation.

The correct status is now:

- Experiment 329 is a **weak/post-hoc hypothesis generator**;
- Experiment 330's leave-one-out results remain legitimate tests performed after freezing;
- Experiment 336's residue-84/residue-102 predictions remain frozen prospective falsification targets;
- the 7/9 selector-domain agreement with the incumbent in Experiment 331 remains descriptively interesting, but should not inherit evidentiary strength from the original 12-vs-0 contrast.

## Consequence

Do not add more constraints to improve the row family on the current corpus.

Future positive weight must come from genuinely new evidence: a physical residue 84/102, a historical message independently specifying the same operation, another ARG artifact that supplies it, or another clean holdout.

## Reproducibility

```bash
python scripts/audit_row_selector_null.py
```
