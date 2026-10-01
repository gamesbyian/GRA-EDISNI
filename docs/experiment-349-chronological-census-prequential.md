# Experiment 349 — chronological census prequential replay

_Status: preregistered retrospective replay; result not yet inspected._

## Motivation

Experiment 348 finds that the historically attested twelve-square representation leaves two current full-corpus census families alive for the first nine slash/dash squares: 3/6 and 4/5.

A naive chronological holdout would still be circular: because both families fit the final corpus, any cell that becomes logically forced by an earlier subset is guaranteed not to contradict the later full-corpus observations.

Instead, score **predictive probability**, not forced correctness.

## Historical chronology

Use the archived community ledger:

`archive/external/twinysam-inside-arg/stickers.md`

Its stated dates are dates when sticker image/information was received by the community ledger. They are used only to reconstruct the order in which structural information became available, not the manufacture date or original publication date of a photograph.

For every physical sticker in `data/observations.csv`:

1. recover its first ledger-received date from the corresponding sticker entry;
2. map serial to H108 residue;
3. for residues 1–81, keep only the earliest received physical observation for each residue;
4. group observations received on the same calendar date into one batch so no arbitrary within-day ordering can affect the result.

Repeated physical stickers at an already-known H108 residue are controls and do not score again.

If any observation cannot be assigned a ledger date, stop rather than silently dropping it.

## Candidate family

Score all five unordered binary 3×3 census families symmetrically:

`0/9, 1/8, 2/7, 3/6, 4/5`.

For a minority count `w`, a complete square is any slash/dash assignment containing either `w` slashes or `9-w` slashes. All such complete assignments are given equal weight.

No machine frame polarity, POS3, tail selector, recursion, spatial shape score, or semantic target is used.

## Prequential score

For each date batch and each candidate `w`:

1. count the complete assignments compatible with all observations available **before** the batch, independently for each affected 3×3 square;
2. add the entire same-date batch;
3. recount compatible assignments;
4. the exact conditional probability of that batch is the product, over affected squares, of `after_count / before_count`;
5. accumulate `-log2(probability)` as predictive surprise in bits.

If a family reaches zero compatible assignments, it is eliminated on that date and remains eliminated.

The primary comparison is total cumulative surprise through the final unique first-81 observation. Lower surprise means the family assigned greater probability to the historical sequence of newly discovered symbols.

## Guardrails

This is a retrospective prequential comparison, not a prospective experiment. The candidate family was motivated after the current corpus existed, so score differences are evidence about relative descriptive/predictive economy inside this bounded family, not independent proof of intended authoring.

Do not tune chronology cutoffs, priors, square orientation, symbol polarity, or weighting after seeing the result.

Report:

- the elimination date for each eliminated family;
- cumulative surprise for every family up to elimination/final date;
- the 3/6 versus 4/5 surprise difference;
- dates/batches contributing the largest likelihood-ratio shifts between 3/6 and 4/5;
- the exact number of unique first-81 residues scored.

## Reproducibility

Run:

```bash
python scripts/audit_chronological_census_prequential.py
```
