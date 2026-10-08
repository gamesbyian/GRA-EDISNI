# Experiment 462: can registered completions predict genuinely withheld stickers?

## Motivation and frozen operation

Literal same-coordinate **copying** between primary cubes previously
lost to majority guessing (Experiment 454). That does not test whether
a *complete candidate string* selected for registration coherence can
predict withheld physical marks.

This experiment starts with the 3-of-9 primary **physical-column**
grammar and the independently considered Q4 one-slash-depth-stack
grammar. A candidate's score is the difference between:

1. its fraction of same-symbol matches across all unordered
   different-cube pairs occupying the **same coordinate**;
2. its fraction of same-symbol matches across different-cube pairs
   displaced horizontally by **±1 in the alphabetical ABC/DEF/GHI
   3×3 layout**, with no wrap.

This is the exact Discord Lab geometry, not a newly optimized
correlation. For a family of complete candidate masters, assign
a nonnegative weighting `w(master) = exp(beta × score(master))`,
then predict the slash probability at each withheld position as the
weighted fraction of candidates with a slash.

Test the fixed sensitivity grid
`beta∈{0,10,25,50}`; `beta=0` is uniform weighting.
The choice of **alphabetical X** and the strength grid is
retrospective and **must not** be advertised as a blind prospective
registration clue.

A direct ablation replaces the all-four-cube pair score with the
same score using only Q1–Q3, leaving the grammar and physical Q4
observations unchanged.

## Nine whole-nine-sticker-frame erasures: exact enumeration

For each of the nine primary 9-cell frames, remove **every
physically observed symbol in that frame** from the constraints.
Enumerate all compatible primary-column bodies and Q4 slash-depth
selectors from the remaining data, and predict only the
previously hidden physical symbols. No score uses a withheld physical
mark. There are 54 physical known primary symbols overall.

| Method | Correct / 54 | Brier score |
| --- | ---: | ---: |
| Simple training-only slash-majority classification | **32** | 0.25125 |
| Uniform, unweighted column grammar (beta 0) | **32** | 0.25000 |
| Alphabetical-X weighting, beta 25, all four cubes | **40** | **0.21961** |
| Alphabetical-X weighting, beta 50, all four cubes | **41** | **0.21281** |
| Alphabetical-X weighting, beta 25, Q1–Q3 only | **38** | **0.21803** |
| Physical-X weighting, beta 25, all cubes | **33** | 0.24294 |
| Physical X/Y/Z-averaged contrast, beta 25, all cubes | **30** | 0.23409 |

The training-majority baseline always chooses slash because the
known primary corpus has 32 slash and 22 dash symbols. The Brier
score measures squared error of predicted slash probability; lower
is better. The baseline's probability is recomputed from all other
known primary symbols on each frame fold, not from the withheld frame.

The result is **stronger than single-residue copy tests**, but the
choice of alphabetical X and beta was made after existing
full-corpus exploration. There are only nine correlated frame folds,
and the improvements are uneven across frames. At beta 25 the
accuracy difference is +8 total correct against majority, coming
from per-frame gains `[+2,+3,+4,0,-1,-1,0,+2,-1]`. A nine-frame
cluster bootstrap has a **90% interval roughly −1 to +17** for
the total accuracy gain. This is a sensitivity estimate rather than
a formally discovery-adjusted confidence interval.

## Three entire 27-sticker cube erasures: sampling all unseen arrangements

As a harder test, for each of Q1,Q2,Q3 remove **all its physically
observed marks**, retain the other primary cubes and Q4, and
sample **250,000 uniformly weighted compatible complete strings**
for that cube fold. Reweight the strings by their full registration
score and measure the prediction at each of the 54 withheld primary
positions. Repeat with two independently seeded Monte Carlo streams.
The physical-column grammar in each of the three hidden frames
still applies; no target-cube sticker symbol is allowed in
candidate generation.

| Whole-cube predictor | Correct / 54 (seed 20261008) | Correct / 54 (seed 951733) |
| --- | ---: | ---: |
| Majority trained on other primary cubes | **32** | **32** |
| Uniform column model (beta 0) | 27 | 27 |
| Full four-cube registration, beta 25 | **41** | **40** |
| Registration using Q1–Q3 only, beta 25 | **37** | **37** |

Full-registration beta 25 Brier is approximately **0.2196**
across seeds versus the whole-cube majority-frequency Brier
**0.2626**. The two sampled runs differ by one classification
at a near-threshold position; they are not independent data
sets, only stability checks.

This improvement is **not evenly spread**:
with beta 25, the first seeded run yields Q1 **17/19 correct**
vs training-majority **8/19**; Q2 **11/17** vs **12/17**; and Q3
**13/18** vs **12/18**. In particular, the model's recovery
of Q1's dash-heavy observed distribution drives most of the gain.

## What these tests can and cannot establish

- The broad negative claim that *no* cross-cube method predicts
  withheld marks is **too strong**. A registration-weighted
  completion ensemble appears predictively useful on this dataset.
- This does not establish a puzzle solution. The **alphabetical**
  ordering gives a stronger result than the historically solved
  **physical IAB/CDE/FGH** ordering, and the relative-pair rule
  is statistical, not an independently clued consumer/readout.
- **Cube 4 is not necessary** for much of the gain. The primary-only
  scoring ablation gets 38/54 on nine-frame erasures and 37/54 on
  full-cube erasures with beta 25. Evidence specifically assigning
  an instruction role to Q4 remains weak.
- The entire-score family was explored retrospectively. Comparing
  beta 0/10/25/50 and several coordinate rules imposes a genuine
  model-selection burden not removed by after-the-fact frame/cube
  holdout checks.
- These validation folds use all existing physical observations
  to inform which operations were worth testing. New physical
  observations or an independent Playdead-authored consumer clue
  are still needed for truly prospective validation.

## Reproduction

```bash
node scripts/audit_cube_registration_predictive_holdout.js
node scripts/audit_cube_registration_predictive_holdout.js --fast
```

The first command exhaustively enumerates all nine frame-erasure
candidate families, then samples 250,000 masters per primary cube,
twice with independent seeds. The second uses 10,000 candidates
per cube for a quick smoke check. A separate NumPy
implementation independently obtained the same nine-frame
rates and near-identical two-seed whole-cube estimates.

Do not overwrite existing physical-observation or frozen-machine
prediction matrices with this exploratory statistical predictor.
