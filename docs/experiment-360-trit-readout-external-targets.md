# Experiment 360 — three-position readout vs. lever password and LIFEDETECTED

_Status: completed bounded negative, 1 Oct 2026._

## Question

Experiments 342/343 closed the bunker password as a contiguous window of **raw marks**. They did not test the password against the **three-position readout** (the 36-trit "groups of three" reading that the community proposed independently; see Experiment 351). Separately, the 12 trigrams of that readout match the length of `LIFEDETECTED`, the only accepted Playdead-site phrase whose derivation from its source puzzle has never been found, and the phrase was entered from the PS4 line that the CE belongs to.

This tests those two externally supplied targets. It does not add free parameters.

## Parent family (stated before inspecting outputs)

- **Readout R.** For each of the nine slash/dash rows of the 12×9 master, laid out on the physical `I A B / C D E / F G H` background, take the row of the single odd mark in each physical column (3 trits per row, 27 total). For the three slash/dot rows, take which tail row carries the slash for each A–I letter (9 trits). That gives 36 trits, or 12 trigrams.
- **Variants.** Per-row column order mirrored or not; body only, tail only, body+tail, tail+body; forward, reversed, cyclic; trigram digit order reversed; all 12 cyclic starts for the phrase test.
- **Completions.** All 14 legal completions from `generate_master.py`. The script asserts the one-odd-mark-per-column/stack premise on every completion.

## Results

| target | test | outcome |
|---|---|---|
| `UURLRRRUUURLLL` (secret-ending lever) | any bijection of trit values to U/R/L; forward and reversed password; 6,272 windows | **0 hits** |
| `LIFEDETECTED` | monoalphabetic reading of the 12 trigrams; needs one trigram ×4 (E), two pairs (D, T) | **0 hits**; max trigram multiplicity over every readout variant is **2** |

The multiplicity bound is broader than the phrase test. Under readout R no trigram value occurs three or more times in any completion, so no 12-letter substitution reading with a tripled letter is possible at all.

## Consequence

- The lever-consumer idea is now closed for the normal password at both the raw-mark level (Exp 343) and the three-position-readout level. It is still live only for an unknown **different** lever sequence with an independently cued ordering.
- `LIFEDETECTED` is not the sticker foreground's plaintext under the community's natural groups-of-three reading. Its missing derivation stays with the PC/PS4 acorn data.

## Reproducibility

```bash
python scripts/audit_trit_readout_external_targets.py
```

The script fails loudly if either negative result changes.
