# Cube Registration Lab research package (8 October 2026)

This package is an observation-anchored, source-faithful continuation
of the Discord Cube Registration Lab. It deliberately makes **no**
claim to have decoded the sticker endgame or identified an intended
three-dimensional consumer. The user-supplied HTML, whose bundled fonts
and source belong to its original author, is **not** redistributed.

## Experimental index

| ID | Question and bounded finding |
| --- | --- |
| [459](experiment-459-cube-registration-lab-replication.md) | Reproduce the supplied 65-sticker Lab precisely, account for the 66th residue (427 dot), and compare the same registration statistic across 324 completed structural strings. |
| [470](experiment-470-completion-registration-coverage.md) | Under 233,280 weaker compatible 3-of-9 full masters, same-spot rates exceed alphabetical X in 233,136 (99.94%). The *sign* of registration is not very discriminating. |
| [471](experiment-471-cube-registration-structural-null.md) | Preserve the observation mask and per-frame observed slash census while shuffling grammar-compatible labels. The *observed size* of the alphabetical-X contrast remains unusual in two non-equivalent structural null families, but the test is retrospective. |
| [472](experiment-472-registered-holdout-prediction.md) | Use alphabetical-X registration as a score over complete candidate codes, not literal symbol copying. Nine whole-frame erasures recover 40–41/54 vs 32/54 majority; three full-primary-cube erasures recover about 40–41/54, driven heavily by Q1. Much of the gain remains with Q4 omitted from the score. |
| [473](experiment-473-registration-q4-reader-conflict.md) | Weighting by alphabetical-X coherence favours the relabelled-quarter axis family more than the native-depth axis family, but it doesn't establish either instruction operation and gives conflicting expectations at 50/54/93. |
| [474](experiment-474-q4-erasure-scope.md) | Native-depth Q4 reader recovers 11/12 observed symbols under one-depth-stack-at-a-time erasure but only 8/12 after erasing all known Q4 symbols simultaneously. Internal coupling is not primary-to-Q4 reconstruction. |
| [475](experiment-475-primary-only-registration.md) | Remove Q4 from pair statistics and nulls entirely. Q1–Q3 alone have 24/40 exact matches vs 16/47 alphabetical-X, and census-constrained structural-null tail ~0.014, six-comparison max ~0.043. Q4 is not necessary for the observed X contrast. |

## Reproduce

```bash
node scripts/audit_cube_lab_replication.js
python scripts/audit_cube_lab_completion_ensemble.py
node scripts/audit_cube_registration_extended.js
node scripts/audit_cube_registration_predictive_holdout.js
python scripts/audit_registration_q4_reader_conflict.py
python scripts/audit_q4_erasure_scope.py
python scripts/audit_cube_primary_registration_null.py --samples 250000
```

All scripts read the canonical `data/observations.csv` and contain
count assertions. The Node scripts use Node built-ins, and the
Python scripts use the standard library. A path-scoped
`.github/workflows/cube-registration-research.yml` smoke workflow
also exercises the updated research scripts.

The new operations are statistically appealing but are not
independently supplied by the ARG or Collector's Edition. Layouts,
weights and significance thresholds were examined after observing
some physical symbols, and randomized completion models supply
assumption-dependent nulls rather than fully calibrated
manufacturing probabilities.

## Closed-corpus continuation

Do not depend on new stickers arriving. Preserve all previously
frozen model-specific predictions without altering physical
observations. Prioritize historical/game-artifact evidence that
specifies an actual **consumer** of the symbol stream: coordinate
frame, input alphabet, transformation and output type. A serious
candidate should explain Q4's independent slash/dot instruction
content and make falsifiable consequences *without* maximizing
visual plausibility or matching a chosen plaintext.

Other agents are modifying `docs/experiment-ledger.md` and the
concept-map research infrastructure at the same time; the
experiment index here is deliberately self-contained to avoid
overwriting their concurrent edits. Integrate stable rows into the
canonical ledger after those branches have been reconciled.
