# Experiment 300 — historical Sticker Studio prediction audit

_Date: 2026-09-29_

## Question

Did the prediction heuristics embedded in the recovered Discord `sticker_random_gen_New.py` contain useful out-of-sample signal on the 65 known H108 cells, or are they best preserved as historical negative controls?

The original application already includes leave-one-out checks. This experiment extracts that prediction logic into a dependency-free executable audit and compares every named rule with the application's own simple **zone-majority** baseline.

No model-filled cell is ever treated as an observation.

## Historical rules reproduced

The recovered tool contains:

- a simple mod-54 nearest-class vote;
- a multi-period vote over periods 54, 36, 27, 18, 12, 9, 6 and 4;
- a weighted model over periods 54, 36, 27, 18, 12, 9, 6, 4, 3 and 2 plus period-9 and same-nine-cell-row terms;
- a zoned version of that weighted model, which refuses cross-talk between the primary 1–81 slash/dash region and the 82–108 slash/dot tail;
- a cross-zone version;
- a zone-majority baseline.

The archived GUI labels its model-filled cells as guesses and exposes leave-one-out accuracy directly. Experiment 300 preserves that distinction.

## Leave-one-out result

All 65 currently known H108 cells are hidden one at a time and predicted from the remaining 64.

| Rule | Coverage | Correct | Accuracy |
|---|---:|---:|---:|
| zone-majority baseline | 65/65 | 39 | 60.0% |
| mod-54 | 65/65 | 37 | 56.9% |
| weighted model, zoned | 65/65 | 34 | 52.3% |
| weighted model, cross-zone | 65/65 | 36 | 55.4% |
| multi-period, min agreement 2 (historical default) | 65/65 | 31 | 47.7% |
| multi-period, min agreement 3 | 56/65 | 29 | 51.8% |
| multi-period, min agreement 3.5 | 46/65 | 23 | 50.0% |
| multi-period, min agreement 4 | 33/65 | 15 | 45.5% |

None beats the 60.0% zone baseline.

The weighted zoned model is worse than the baseline by five predictions; the cross-zone model is worse by three; mod-54 is worse by two. The historical default multi-period model is worse by eight.

Exact paired McNemar tests likewise provide no evidence of improvement over the zone baseline:

- mod-54: rule-only correct 10, baseline-only correct 12, p ≈ 0.832;
- weighted zoned: 8 vs 13, p ≈ 0.383;
- weighted cross-zone: 10 vs 13, p ≈ 0.678;
- multi-period min-2: 8 vs 16, p ≈ 0.152.

The abstaining higher-threshold multi-period variants also never outperform the baseline on their own covered subsets.

## Interpretation

This closes a useful historical loop.

The Sticker Studio was a competent exploration and visualization tool, but its guessed unknown cells should not be promoted into evidence. Its prediction machinery does not beat the extremely cheap fact that the first 81 cells are slash-heavy while the final 27 cells are slash/dot and also slash-heavy.

That makes the recovered source valuable for three reasons:

1. it documents what the community actually tried;
2. it preserves a negative predictive result that predates the current mechanical model;
3. it demonstrates explicit historical awareness that model fills were guesses rather than recovered sticker values.

The negative result also strengthens the anti-hindsight archive: the present POS3/selector mechanism did not merely inherit a successful old period-voting predictor.

## Consequence

Keep every Sticker Studio guessed cell quarantined from `data/observations.csv`.

Treat mod-54, multi-period voting, and weighted period/row prediction as **closed historical prediction families**. Reopen only if an independently motivated new target or historical frozen prediction can be evaluated against genuinely later observations.
