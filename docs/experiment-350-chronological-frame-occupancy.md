# Experiment 350 — chronological 3/6 frame-occupancy replay

_Status: preregistered retrospective replay; result not yet inspected._

## Motivation

Experiments 348–349 independently motivate the historically attested twelve-square frame representation and give the exact 3/6 frame census substantially better chronological predictive economy than the remaining 4/5 census rival.

G1 is stronger than 3/6. It additionally asserts that the three minority cells occupy one per physical column of the solved 3×3 background geometry. Experiment 350 isolates that spatial claim before any exceptional-position/ternary meaning, tail selector, or recursion is introduced.

## Frozen frame geometry

For every consecutive 9-residue frame in residues 1–81, map the serial A-I positions into the independently solved background layout:

```
I A B
C D E
F G H
```

Each complete 3/6 frame has exactly three cells bearing its minority symbol and six bearing the other symbol. Frame polarity is free and independent; slash may be the three-cell minority or dash may be the three-cell minority.

## Candidate occupancy family

Score four natural nested models:

1. **unrestricted** — any three minority cells among nine;
2. **one_per_row** — exactly one minority cell in each physical row;
3. **one_per_column** — exactly one minority cell in each physical column;
4. **permutation_matrix** — exactly one minority cell in every physical row and every physical column.

All models include both possible frame polarities. Complete assignments receive equal weight within each model.

This family is frozen before result inspection. No class-specific orientation, D4 optimization, or per-frame choice between row and column models is allowed.

## Chronology and scoring

Use the same ledger-received chronology protocol as Experiment 349:

- source: `archive/external/twinysam-inside-arg/stickers.md`;
- keep the earliest received physical observation for each H108 residue 1–81;
- group same-date discoveries into one batch;
- repeated observations of already-known residues do not score again.

For each model and date batch, calculate the exact number of compatible complete assignments before and after the batch for every affected frame. The batch conditional probability is the product of `after/before` ratios. Accumulate `-log2(probability)` surprise.

A model reaching zero compatible assignments is eliminated permanently.

## Primary questions

Report:

- whether each model survives the final physical corpus;
- cumulative predictive surprise for every surviving model;
- exact likelihood ratios among unrestricted, row, column, and permutation-matrix models;
- dates/residues causing the largest row-vs-column likelihood shifts;
- dates of any model eliminations.

## Interpretation guardrail

This is retrospective bounded model comparison. The candidate family is natural on the independently historical physical 3×3 representation, but it is formalized after the current corpus exists.

Evidence favoring `one_per_column` would support the **spatial occupancy part** of G1 only. It would not establish:

- that the occupied position is a ternary value;
- a fixed frame polarity rule;
- POS3 reuse in the tail;
- selector semantics;
- recursion;
- any downstream machine consequence.

Likewise, a row/column tie would mean the present corpus supports a straight-axis occupancy grammar without fixing orientation.

## Reproducibility

```bash
python scripts/audit_chronological_frame_occupancy.py
```
