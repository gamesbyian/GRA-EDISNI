# Experiment 349 — chronological census prequential replay

_Status: completed retrospective replay; scoring frozen before result inspection, 30 Sep 2026._

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


## Result

The ledger provides dates for every observation used by the replay. After collapsing repeated physical serials onto their earliest H108 residue observation, the first-81 corpus contains **54 unique residues** arriving in **43 date batches**.

The five common-census families eliminate as follows:

| census | status | elimination / cumulative surprise |
|---|---|---:|
| 0/9 | eliminated | 15 Jan 2020 |
| 1/8 | eliminated | 13 Apr 2020 |
| 2/7 | eliminated | 23 Dec 2025 |
| 3/6 | survives | 52.869079 bits |
| 4/5 | survives | 57.659810 bits |

The surviving-family difference is:

```
4/5 surprise - 3/6 surprise = 4.790731 bits
likelihood ratio P(history | 3/6) / P(history | 4/5)
                              = 27.6792
```

Under the frozen uniform-completion model, the historical sequence of newly learned symbols is therefore about **27.7 times more likely under 3/6 than under 4/5**.

The largest individual shift toward 3/6 occurs on 23 Jul 2021 at residue 78: conditional probability 2/3 under 3/6 versus 1/4 under 4/5, a 1.415-bit likelihood-ratio shift. Residues 21 (6 Apr 2020) and 43 (30 Jan 2021) each contribute 1.322 bits toward 3/6. Some later batches move the other way: residues 44+72 on 23 Dec 2025 and residue 13 on 9 Mar 2026 each favor 4/5 by 1.170 bits.

## Interpretation

This is meaningful evidence **inside the bounded common-census family**, but its status must remain precise.

It is stronger than a same-corpus compatibility count because each date batch is scored against the completion distribution left by earlier community knowledge. The score rewards a family for assigning higher probability to symbols before those symbols are admitted to the cumulative state.

It is still retrospective model comparison. The five-member census family was formalized after the present corpus existed, and the uniform-completion prior is a modeling choice. Therefore the 27.7:1 ratio is not a prospective Bayes factor for author intent and does not promote 3/6 to Layer 0.

The justified upgrade is narrower:

> Among the complete symmetric common-census family motivated by the historically attested twelve-square representation, 3/6 has substantially better chronological predictive economy than the only surviving rival 4/5.

That gives exact 3/6 an independent reset-era support line that does **not** use POS3, frame polarity, the tail selector, recursion, route criteria, terminal 100, or machine-filled cells.

## Consequence

Update the premise classification accordingly:

- twelve consecutive A-I blocks as 3×3 foreground squares: historically attested representation;
- common per-square census: independently motivated structural family;
- exact 3/6: not direct observation, but now supported over 4/5 by bounded chronological prequential evidence;
- per-frame minority polarity and one-per-column POS3: still separate higher-level claims.

Do not multiply the 27.7 likelihood ratio with machine-selection ratios as if the evidence streams were independent without an explicit dependence audit.

Compact exact results are preserved in `data/experiment-349-chronological-census-prequential-summary.json`. Full batch histories are reproducible from the script and preserved in workflow run `36810578829`, artifact `11139278540`, digest `sha256:dc1b0c45cc9dca0a3d2c081d7b39cf5de52a5a3930428d3f050f3c41c2387987`.
