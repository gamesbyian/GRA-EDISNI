# Experiment 330 — leave-one-out validation of the frozen row-selector rival

_Status: completed, 30 Sep 2026._

> **Evidentiary correction (Experiment 340):** the family was selected using the complete observed corpus before this leave-one-out analysis. Any forced singleton prediction is therefore guaranteed to match the hidden original symbol whenever the full corpus fits the family. The numerical result below is preserved, but `4/4 correct` is **not independent validation**. See `docs/experiment-340-row-selector-holdout-selection.md`.

## Question

Experiment 329 froze an exploratory rival family:

> one-slash tail selects one consecutive 3-cell body row, and the selected row contains exactly one exceptional mark.

Because the one-exception criterion was discovered after inspecting the row/column outputs, the right next move is not to decorate it with more rules. Test whether it predicts anything already observed when individual body cells are withheld.

## Protocol

For each of the 54 physically observed slash/dash residues in 1–81:

1. hide that one symbol;
2. rebuild the observation-compatible one-slash tail family from the unchanged physical tail observations;
3. enforce only the frozen row-selector + one-exception rule;
4. enumerate every surviving selector assignment and every compatible selected-row completion;
5. record whether the hidden cell is forced, ambiguous, or excluded.

No incumbent-machine information, predicted cells, recursion, route criteria, terminal, or semantic output is used.

If a hidden cell can lie outside the selected row in any surviving assignment, it remains unconstrained by this family.

## Result

Out of 54 leave-one-out body observations:

- **4 are forced** by the frozen family;
- **50 remain ambiguous**;
- **0 true observations are excluded**.

The four forced predictions are all correct:

| residue | class | true / forced symbol |
|---:|---|---|
| 5 | E | `/` |
| 66 | C | `/` |
| 72 | I | `-` |
| 74 | B | `-` |

So the frozen family has a modest but real predictive footprint: 4/54 exact body predictions under leave-one-out, with no contradictions.

## Interpretation

This is stronger than pure visual resemblance, because the rule was frozen before these leave-one-out tests were scored. It is still weak evidence overall:

- prediction rate is only 7.4%;
- 92.6% of holdouts remain unconstrained;
- the family was originally nominated after inspecting row/column output structure.

Therefore this result keeps the row-selector rival alive, but does not elevate it to the evidentiary status of a preregistered independent discovery.

Its most useful role is now prospective comparison. The family should remain frozen at exactly:

- one slash in each tail triple;
- tail position selects one consecutive body row;
- selected row has one exceptional slash/dash mark.

Do not add new constraints to improve fit.

## Prospective discriminator

Experiment 329's strongest unobserved consequence remains:

```
C tail residues 84, 93, 102 = . . /
```

The incumbent prediction matrix leaves 84 and 102 state/gauge-dependent, while 93 is invariant dot. Therefore 84 and 102 are high-value discriminators between the frozen row-selector family and broader incumbent completions.

## Reproducibility

```bash
python scripts/audit_row_selector_holdouts.py
```
