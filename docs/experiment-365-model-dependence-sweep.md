# Experiment 365 — model-dependence sweep of recorded conclusions

_Status: completed audit, 1 Oct 2026. Corrects how several results are cited; no machine change._

## Question

Which recorded conclusions are supported by raw physical sticker observations alone, and which depend on model-selected structure (the incumbent completions, or a rival family fitted to the full corpus)? In particular, are any model-conditioned conclusions cited as if they were raw-data facts?

## Scope and limitation

- **Audited in detail:** Experiments 298–364, which have dedicated write-ups in this repository (56 documents), plus the summary documents that cite them (`current-state.md`, `research-queue.md`, `sticker-prediction-validation.md`).
- **Not auditable here:** Experiments 1–297 appear in this repository only as ledger titles (86 have any prose reference elsewhere in the repo). Their methods live in the long-form Google Docs, which were not accessible to this audit. The closed-branch list (XML, MIX, MISS, Braille, generic alphabets, bitmap fitting, Experiment-240 decoder families) rests mainly on that unaudited range.

## Foundation check

The H108 period was rechecked against raw data across every period from 2 to 399. At period 108, all **19** same-residue sticker pairs agree, with **0** disagreements. The best other contradiction-free period has 7 agreeing pairs; the multiples 216 and 324 follow. The period is not a model artifact.

Raw coverage remains thin: 65 of 108 residues are observed, and **50 of those 65 rest on a single sticker record**, so they cannot be internally cross-checked. `observations.csv` carries no read-confidence field.

## Classification of Experiments 298–364

| class | experiments | status |
|---|---|---|
| Raw-only exclusions, sound | 317, 319, 326, 327, 328, 345, 346, 347, 362 | Conclusions follow from physical observations with unknowns as wildcards. |
| Historical / provenance / triage | 298–302, 315, 316, 324, 325, 337, 338, 342, 344, 351, 357, 361, 363, 364 | No model dependence in their conclusions. |
| Retrospective model comparison, caveats stated | 349, 350 | Correctly labelled as retrospective; not prospective Bayes factors. |
| Explicitly conditional on the incumbent family | 313, 314, 318, 320–322, 352–356, 358, 359 | Internal uniqueness/gauge audits, framed as conditional. |
| Conditional on the Exp-329 row-selector rival | 329–336, 339, 340 | Mostly framed correctly; 340 already corrects 330. |
| **Needs correction** | **323, 333, 335, 343, 360** | See below. |

## Corrections

### 1. Experiment 323: the incumbent's Q4 holdout advantage is not independent evidence (substantive)

Experiment 323 compares 10/11 forced Q4 holdouts for the incumbent against 3/11 for the tail-only family and concludes that "predictive sharpness is evidence" for the incumbent's extra grammar. `current-state.md` summarises this as "the incumbent is more predictive", and `research-queue.md` R5 repeats it.

The incumbent holdout table is produced by `scripts/audit_sticker_prediction_holdouts.py`, whose own docstring states that "premises historically derived using the full corpus remain fixed." Experiment 340 proved for the row-selector rival that, after full-corpus model selection, **a forced leave-one-out prediction cannot be wrong**. The same proof applies here unchanged:

- "0/11 exclusions" is guaranteed for both families, so it is not a result;
- "10/11 forced" measures how tightly a grammar fitted to all 11 Q4 cells constrains each of them. Richer post-hoc grammars force more cells by construction, so the count cannot by itself distinguish real structure from fit.

**Corrected status:** Experiment 323 shows the two families are both compatible with the Q4 data and differ in sharpness. It provides **no evidence of predictive superiority** for the incumbent. A fair comparison needs either a selection-aware null (as Experiment 340 built for the row rival) or genuinely new observations scored against the frozen prediction matrix. `sticker-prediction-validation.md` already frames the 44/65 table correctly; only the cross-family use was overstated.

**Knock-on:** Experiment 359's criterion 5 ("cross-family comparison — adequate") lists this comparison first. With it downgraded, criterion 5 rests on the frozen prediction matrix and prospective discriminators (residues 84, 102), which remain valid but are not yet tested. The stopping boundary still holds for blind widening, but the incumbent has **no current independent comparative evidence** over the simpler tail-index family.

### 2. Experiment 343: "independent of every unobserved foreground cell" is overstated

The lever-password exclusion is independent of unobserved cells' identities **only if the 81/27 alphabet split extends to the 43 unseen residues**. The split is strongly supported (54 body sightings, 0 dots; 11 tail sightings, 0 dashes), but it is an inference about unseen cells. On raw observations alone (Experiment 342), one weak rotated placement survives. Restated: *excluded, given that the observed alphabet split holds for unobserved cells.*

### 3. Experiment 333: "impossible" applies to the row-selector coordinates only

The four "observation-fixed" tokens (B, C, E, I) are fixed **within the Experiment-329 row-selector family**. The result rules out copying the background layout into that family's token coordinates, not background registration in general. Experiment 359 lists "direct background-coordinate registration" as a falsified rival; it should read as falsified *for the row-selector carrier*.

### 4. Experiment 335: "observation-compatible tokens" are row-family tokens

The 900-per-codebook / 14,400 string counts are conditional on the Experiment-329/332 carrier. The multiple-comparisons warning stands, but the counts are not raw-data quantities.

### 5. Experiment 360: already corrected

Only 6 of 36 readout trits are raw-determined; the doc now carries a conditional caveat.

## Recommended follow-up

1. Build a selection-aware null for the incumbent's Q4 holdout, the analogue of Experiment 340, so the 10/11 figure can be calibrated.
2. Add a read-confidence column to `observations.csv` (photo quality / independent confirmation), then rerun the reconstruction with the weakest single-record readings withheld.
3. If the Google Docs become reachable, extend this sweep to Experiments 1–297, prioritising the closed-branch experiments (13, 87, 94, 112, 211, 240) and any exclusion run on completed masters.
