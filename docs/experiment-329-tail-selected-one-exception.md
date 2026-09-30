# Experiment 329 — exploratory one-exception selected-line audit

_Status: completed exploratory discriminator, 30 Sep 2026._

## Why this test

Experiments 317–318 leave 36 observation-compatible one-slash tail assignments and do not distinguish two direct meanings of the three-way selector:

- choose one consecutive 3-cell row/chunk from the 3x3 body;
- choose one 3-cell column/rail.

The geometric-alphabet discussion suggests a cheap additional structural question: does the selected line itself look like a simple ternary positional code, meaning exactly one mark differs from the other two?

Important epistemic warning: **this criterion was introduced after the row/column outputs had already been inspected.** It is exploratory, not preregistered confirmatory evidence for POS3 or the incumbent machine.

## Inputs

Only:

- `data/observations.csv`;
- the 36 one-slash tail completions from Experiment 317;
- unknown body cells remain wildcards.

No machine completion, recursion, route rule, terminal, plaintext, or prediction-matrix cell is used.

A selected line is compatible with "one exception" if some completion of its unknown cells gives either:

- one slash + two dashes; or
- two slashes + one dash.

## Result

Across all 36 tail assignments:

| interpretation | assignments compatible with one-exception selected lines in all A-I classes |
|---|---:|
| row/chunk | **12 / 36** |
| column/rail | **0 / 36** |

The column interpretation fails immediately because the already-forced E and F selectors expose observed `///` columns.

The row interpretation survives and sharpens the tail positions to:

| class | surviving selector positions |
|---|---|
| A | 0 / 1 / 2 |
| B | 2 |
| C | **2 only** |
| D | 1 / 2 |
| E | 0 |
| F | 1 |
| G | 0 / 2 |
| H | 2 |
| I | 2 |

So the exploratory rule cuts the tail family from 36 completions to 12 and, importantly, forces the entirely unobserved C tail to:

```
C tail residues 84, 93, 102 = . . /
```

## Why the row result is interesting

The five classes whose tail selector was already physically forced before this test all expose row patterns compatible with exactly one exception:

- B -> `//-`
- E -> `/--`
- F -> `?/-`
- H -> `?-/`
- I -> `/-/`

For F and H, either completion of the one unknown selected cell still yields one exception.

By contrast, the forced E and F columns are both `///`, so no unseen cell can rescue the column version.

## Relation to the incumbent

This is not independent confirmation of the incumbent POS3 grammar because the one-exception criterion was chosen after looking at the selected-line outputs.

It is nevertheless a useful **new rival-family specification** that can now be frozen prospectively:

> one-slash tail selects a consecutive body row, and the selected row has one exceptional mark.

Its strongest current prediction is C = `../`.

The frozen incumbent prediction matrix gives C residue 93 as dot invariant, while residues 84 and 102 remain state/gauge-dependent. Therefore a future physical C-tail observation at 84 or 102 is genuinely discriminating against this frozen row-selector family; residue 93 is not.

## Consequence

Promote this exact row-selector + one-exception family to R5 as an exploratory frozen rival. Do not add more visual criteria to it.

The next useful work is to compare its prospective/holdout predictions against the incumbent and against any independently specified geometric codebook, without tuning the row family further.

## Reproducibility

```bash
python scripts/audit_tail_selected_one_exception.py
```
