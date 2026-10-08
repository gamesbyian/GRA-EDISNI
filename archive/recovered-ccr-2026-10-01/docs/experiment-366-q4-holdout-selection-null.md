# Experiment 366 — selection-aware null for the Experiment-323 Q4 holdout

_Status: completed, 1 Oct 2026. Replaces the evidential reading of Experiment 323._

## Question

Experiment 323 reported 10/11 forced Q4 holdouts for the incumbent against 3/11 for the tail-index-only family. Experiment 365 argued that, because the incumbent's grammar was fitted to the full corpus, its forced predictions cannot be wrong, so the count needs calibration. How informative is 10/11?

## Preregistered design

Fixed before inspecting outputs (see the script docstring):

- **Null datasets:** keep all 54 real body observations; permute the 11 observed Q4 symbols (4 slash, 7 dot) over the same 11 residues. All C(11,4) = **330** assignments are enumerated exactly.
- **Selection:** retain a dataset only if the incumbent's fixed grammar (the exact `reconstruct` used by `audit_sticker_prediction_holdouts.py`) admits at least one machine.
- **Statistic:** leave-one-residue-out forced counts for the incumbent and the tail-only family.

## Results

| quantity | value |
|---|---:|
| recursion-valid (payload, selector) pairs for the real body | 208 of 6 × 3^9 = 118,098 |
| shuffled tail datasets the **incumbent** fits | **7 / 330** (2.1%) |
| shuffled tail datasets the **tail-only family** fits | **192 / 330** (58.2%) |
| incumbent forced count among its 7 fitting datasets | **10 in all 7** |
| incumbent − tail difference ≥ 7 among fitting datasets | 6 / 7 |
| wrong forced predictions in any retained dataset | 0 (as Experiment 340 guarantees) |

## Interpretation

1. **The 10/11 holdout statistic carries no evidence.** Every dataset the incumbent can fit produces exactly 10/11 forced. Conditional on fitting, the number is certain, so the Experiment-323 comparison measures nothing beyond "the incumbent fits".

2. **The real evidence is the compatibility test.** The incumbent's grammar accepts only 7 of the 330 equally sized tail arrangements; the real arrangement is one of them. The tail-only family accepts 192. If both families had been fixed before the data were seen, and each treated its compatible arrangements as equally likely, that would be a likelihood ratio of about 192 / 7 ≈ **27:1** for the incumbent.

3. **That 27:1 is an upper bound, not a measurement.** The incumbent's Q4 representation and recursion closure were developed using the full corpus, including these 11 cells (see `audit_sticker_prediction_holdouts.py`: "premises historically derived using the full corpus remain fixed"). How much of the 2.1% restrictiveness was shaped to fit them cannot be recovered from this repository. The honest statement is: *the incumbent makes a sharp tail commitment that the real data satisfy, but how much of that commitment was tuned to the same data is unknown.*

4. **What would settle it:** a new physical Q4 sticker, scored against the frozen prediction matrix, or reconstruction of the order in which the Q4 grammar was fixed relative to the Q4 observations (the Results document's chronology may allow this).

## Reproducibility

```bash
python scripts/audit_q4_holdout_selection_null.py
```

Runs in a few seconds; asserts the real-data 10/11 and 3/11 counts and zero wrong forced predictions.
