# Sticker prediction and holdout-validation lane

_Status: active, 2026-09-29. This document freezes the current unobserved-cell guesses and separates several different notions of "prediction" that must not be conflated._

## Motivation

The current public corpus contains 82 physical sticker records but only 65 distinct H108 residues. Forty-three H108 cells have never been physically observed in the canonical ledger.

Under the preferred closed-corpus machine:

- the A-I background class is deterministic from serial phase;
- 30 of the 43 unobserved foreground cells are invariant across all 14 canonical hidden states;
- 13 are state-register cells whose symbol depends on the unresolved hidden state;
- some of the 30 canonical invariants sit on known physical gauge supports and are therefore not invariant across broader gauge-equivalent representations;
- 22 unobserved cells remain fixed even after removing the known primary and Q4 physical-representation gauges discussed below.

The explicit current predictions are frozen in:

`data/unobserved-sticker-predictions.csv`

This is intended to make future physical discoveries scoreable before the model is changed.

## Current preferred guess family

The preferred representation is:

1. exact primary column POS3;
2. zero primary physical gauge;
3. globally homogeneous slash-exception Q4 stacks;
4. canonical two-pass recursive address operation;
5. modal hidden-state symbol where the 14 surviving physical states disagree.

This gives one preferred foreground guess for every currently unobserved H108 residue, but the support column must be read literally:

- `14/14` means invariant over hidden state in the preferred physical representation;
- `10/14` or `8/14` means a modal state-dependent guess;
- `7/14` is a true state tie.

The modal guess is not a probability estimate. The 14 states are surviving logical possibilities, not a calibrated stochastic distribution over what Playdead printed.

## Gauge-aware alternatives

Several physically different complete masters implement the same or nearly the same reconstructed transition.

### Exact primary physical gauge

Two transition-invisible swaps affect only unobserved cells:

- residues 6 and 8: F/H in primary frame q0,d0;
- residues 41 and 45: E/I in primary frame q1,d1.

Exact column POS3 chooses the zero-gauge representative. Independent transport/smoothness criteria also prefer it, but those criteria are authoring priors rather than new observations.

### Exact Q4 A/C polarity gauge

The entire A and C Q4 stacks are absent from the public physical corpus:

- A: residues 82, 91, 100;
- C: residues 84, 93, 102.

Flipping either stack's slash/dot exceptional-symbol polarity leaves selector depths and the exact canonical transition unchanged. The homogeneous all-slash-exception representative is preferred by physical simplicity and the global 54/36/18 symbol census, but again this is a representation prior.

### Broader F+I branch

A coupled F+I Q4 polarity branch can alter residues including 99 and 105 while retaining 14 states and terminal 100, but it changes first-pass words and fails the canonical three-route shell. Treat this as a broader recursive-family alternative rather than an exact canonical-transducer gauge.

## Tier 1: representation-conditional leave-one-residue-out

`scripts/audit_sticker_prediction_holdouts.py` removes every physical record for one known H108 residue, reconstructs the raw machine family under the current fixed representation/recursion grammar, and asks what symbol the reduced evidence permits at the withheld residue.

The unit of deletion is the H108 residue, not the physical sticker serial, so duplicate records cannot leak the answer.

Frozen output:

`data/sticker-holdout-residue-results.csv`

Current result over all 65 observed H108 residues:

- 44 are **forced correct** after withholding;
- 21 become **ambiguous but include the observed value**;
- 0 exclude the observed value.

This is a strong redundancy result but **not an independent validation accuracy of 44/65**.

Why not? With the grammar fixed, deleting an observation only relaxes constraints. Every one of the original 14 full-corpus machines must remain a survivor of the reduced problem, and those machines already reproduce the withheld observation. Therefore the true symbol cannot be excluded unless there is a software/model inconsistency.

The useful quantity is the 44 forced cells: for those residues, the *other* observations plus the frozen structural grammar uniquely recover the missing symbol. The 21 ambiguous cells identify where that local predictive redundancy runs out.

This test should therefore be called:

> conditional recovery / redundancy under the frozen machine grammar

not:

> blind predictive validation.

### Stronger grouped deletions

The same harness supports two grouped modes:

- `--mode primary-frame`: hide all known cells from one primary q,d frame;
- `--mode q4-stack`: hide all known cells from one observed Q4 A-I depth stack.

A preliminary exact run of the same reconstruction logic gives:

- primary-frame deletion: 10/54 withheld primary residues remain forced, 44 become ambiguous, none exclude the truth;
- Q4-stack deletion: 10/11 withheld Q4 residues remain forced, one becomes ambiguous, none exclude the truth.

Again, these measure redundancy under fixed premises rather than independent validation.

## Tier 2: training/holdout model selection

A materially stronger test must prevent the held-out data from choosing the model parameters or representation among a preregistered candidate family.

The repository already contains an important example: Experiment 265 uses a 34-residue discovery / 20-residue holdout split to nominate rail partitions from discovery data and then tests them on the withheld primary observations. Only physical columns generalize to all holdout data.

The next tests should extend that discipline to the complete prediction problem.

### Proposed nested holdout protocol

For each split:

1. choose the training residues before reconstruction;
2. enumerate a preregistered family of candidate representations/operations;
3. use training data only to eliminate or rank candidates;
4. freeze every remaining prediction for the holdout set;
5. score exact symbol sets and modal guesses on the holdout;
6. only after scoring may the holdout be reincorporated.

Candidate-family complexity must be fixed before seeing holdout performance. Otherwise this becomes model fitting with the answer key visible.

Useful scores:

- forced prediction coverage;
- forced prediction accuracy;
- set-valued coverage: whether the actual symbol lies in the predicted set;
- mean predicted-set size;
- modal accuracy for state-dependent cells;
- log score only if an explicit probability model is independently justified.

## Tier 3: historical/prospective holdout

This is stronger than synthetic deletion.

Where acquisition chronology is reliable, freeze the evidence set at a historical date and use only observations known by that date. Later physical sticker discoveries become genuine holdouts.

Important caveat: a model invented in 2026 still carries hindsight unless its candidate grammar is itself frozen independently of the later sticker values. Historical holdout is strongest when paired with a preregistered model family or a genuinely frozen historical prediction.

The Discord archaeology already preserves one relevant lane: May-2026 community predictor outputs for residues 103 and 45 predate later text-only claims. Those later claims remain unverified and must not enter the observation ledger until provenance-backed physical evidence appears.

## Tier 4: prospective proof stickers

The cleanest test is future evidence that was not available during model construction.

When a new provenance-backed sticker image arrives:

1. record its serial before inspecting foreground details if practical;
2. compute residue and background class mechanically;
3. freeze the current prediction from `data/unobserved-sticker-predictions.csv`;
4. classify whether the residue is:
   - broad-family invariant;
   - canonical invariant but gauge-sensitive;
   - hidden-state dependent;
5. inspect/classify the physical foreground;
6. score before any model update.

The highest-value unseen proof stickers are the 22 cells currently fixed outside the known physical gauge supports:

`1, 11, 16, 27, 28, 33, 34, 35, 49, 50, 52, 54, 62, 64, 67, 68, 73, 77, 83, 87, 104, 107`.

A contradiction at one of these is substantially more damaging than a contradiction to a modal state-dependent guess.

Gauge-sensitive cells are also valuable, but they answer a different question: which physical representative Playdead printed, rather than whether the reconstructed functional machine is correct.

## The "how many stickers were actually needed?" question

The motivating hypothesis is that the creators did not expect solvers to obtain dozens of Collector's Editions. If so, the 82 currently catalogued physical stickers should contain substantial redundancy.

The right experiment is a repeated subset learning curve:

- choose training sets of N distinct residues, with N decreasing from 65;
- reconstruct only within a preregistered bounded family;
- score the remaining known residues as holdout;
- repeat many stratified splits;
- report forced coverage and accuracy versus N.

Stratification matters. A random 30-cell sample concentrated in the first 81 positions is not equivalent to one that exposes the late Q4 selector. Report at least:

- total N;
- primary/Q4 counts;
- number of represented 9-cell frames;
- number of represented background classes;
- whether repeated serial evidence was available for discovering H108.

This can locate a practical transition from "insufficient to identify the mechanism" to "enough to predict much of the rest."

It should not be described as the historical intended minimum unless the discovery steps themselves are reproducible from that reduced raw evidence.

## Interpretation discipline

Keep four claims separate:

1. **fit:** the full-corpus model reproduces known stickers;
2. **redundancy:** after deleting a sticker, fixed-premise reconstruction recovers it;
3. **holdout generalization:** a model/candidate selected without the held-out sticker predicts it;
4. **prospective prediction:** a frozen model predicts a genuinely new physical observation.

Tier 1 establishes (2). Experiment 265 supplies a bounded example of (3). Future newly acquired stickers can establish (4).

The current 43-cell guess list is deliberately frozen now so that future evidence cannot silently rewrite what was predicted.
