# Experiment 340 — selection-aware calibration of the row-selector leave-one-out

_Status: completed epistemic correction, 30 Sep 2026._

## Question

Experiment 330 reported that, after the Experiment-329 row-selector family was frozen, hiding each of the 54 observed body cells one at a time produced four forced predictions and all four were correct.

That sounded like a post-freeze validation result. But the family itself had been chosen using the **complete 54-cell corpus**. Freezing the rule before running leave-one-out does not erase that model-selection leakage.

Experiment 340 asks two things:

1. Is "all forced leave-one-out predictions are correct" actually independent evidence?
2. Is getting four forced cells unusual among null datasets that would have produced the same qualitative row-survives / column-dies discovery?

## Logical result: correctness is guaranteed

For any observed dataset that satisfies the frozen row family, hide one observed cell.

The original full-data assignment remains a valid witness for the hidden problem. Therefore the true held-out symbol is necessarily among the possible values.

If the hidden problem has only one possible symbol, that singleton **must** be the original true symbol.

So:

> once the family has been selected to fit the complete corpus, a forced leave-one-out prediction cannot be wrong.

Experiment 330's `4/4 correct, 0 wrong` result is therefore not an independent validation statistic. It is a consequence of conditioning on full-corpus compatibility.

This is stronger than merely saying the result is "same-corpus evidence."

## Selection-aware permutation calibration

Use the same two nulls as Experiment 339, but retain only randomized datasets that recreate the qualitative discovery event:

```
row survivors > 0
column survivors = 0
```

Then run the Experiment-330 leave-one-out procedure.

### Global fixed-mask/census null

200,000 permutations, seed 340.

Datasets passing the discovery condition:

```
55,410
```

Forced-cell counts among those datasets:

```
3 forced: 46,940
4 forced:  8,470
```

Thus a null dataset selected for the same row-vs-column story produces at least the observed four forced cells:

```
8,470 / 55,410 = 15.286%
```

Wrong forced predictions across all 55,410 selected datasets:

```
0
```

### Within-class matched null

Selected datasets:

```
44,438
```

Forced-cell counts:

```
3 forced: 38,148
4 forced:  6,290
```

At least four forced cells:

```
6,290 / 44,438 = 14.155%
```

Wrong forced predictions:

```
0
```

## Interpretation

Experiment 330 should be downgraded.

Its four forced cells are mildly uncommon under the selection-aware nulls, but not rare: about **14–15%** of null datasets that would have suggested the same row-over-column hypothesis also produce four forced leave-one-out cells.

More importantly, their perfect correctness is mathematically guaranteed by the procedure after full-data model selection.

Therefore the current evidence hierarchy for the frozen row family is:

- Experiment 329 discovery contrast: weak/post-hoc, per Experiment 339;
- Experiment 330 leave-one-out correctness: **not independent validation**;
- Experiment 331 agreement with the incumbent: descriptive cross-family overlap, not independent physical evidence;
- Experiment 336 residues 84 and 102: genuinely frozen **prospective** predictions and the cleanest future test.

## Consequence

Do not cite Experiment 330 as validation of the row-selector family.

Keep the family frozen only as a hypothesis with explicit prospective falsifiers:

```
84  = .
102 = /
```

A new physical observation at either residue is qualitatively different from reusing the corpus that generated the hypothesis.

No further same-corpus fit refinements should be added.

## Reproducibility

```bash
python scripts/audit_row_selector_holdout_selection.py
```
