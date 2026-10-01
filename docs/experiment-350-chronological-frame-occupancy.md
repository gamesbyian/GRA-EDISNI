# Experiment 350 — chronological 3/6 frame-occupancy replay

_Status: completed retrospective replay; model family frozen before result inspection, 30 Sep 2026._

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


## Result

The replay scores 54 unique first-81 residues in 43 same-date batches.

| model | complete assignments / frame | result |
|---|---:|---:|
| unrestricted 3/6 | 168 | survives; 52.869079 bits |
| one minority per physical row | 54 | eliminated 13 Apr 2020 |
| one minority per physical column | 54 | survives; 47.624063 bits |
| one per row **and** column | 12 | eliminated 16 Jan 2020 |

Among the two surviving models:

```
unrestricted surprise - one-per-column surprise = 5.245016 bits

P(history | one-per-column)
---------------------------  = 37.9234
P(history | unrestricted)
```

So under the frozen uniform-assignment model, the historical sequence of sticker discoveries is about **37.9 times more likely** under exact one-per-column occupancy than under unrestricted three-of-nine placement.

The row/column symmetry is broken by the physical data. The one-per-row model is eventually impossible, while one-per-column remains compatible. The largest single row-versus-column shift occurs on 19 Mar 2020, when residues 20, 47 and 53 arrive together: that batch has probability 1/18 under one-per-row and 1/3 under one-per-column, a 2.585-bit shift toward columns.

## Interpretation

This is the cleanest reset-era evidence so far for the **spatial skeleton** that later became G1/POS3.

The evidence chain is now separable:

1. the twelve 3×3 foreground-square domain is historically attested independently of the machine;
2. Experiment 349 gives 3/6 better chronological predictive economy than 4/5;
3. conditional on 3/6, Experiment 350 gives one-per-column occupancy better chronological predictive economy than unrestricted placement, while the equally simple row-axis rival is physically falsified.

That supports:

> each first-81 3×3 frame contains three minority cells, one in each physical column.

It still does **not** establish that the row position of the minority cell should be interpreted as a ternary number. "Exceptional-position ternary POS3" therefore needs to be split epistemically into an independently supported physical occupancy pattern and a remaining code/readout interpretation.

This is retrospective bounded evidence. The candidate family was formalized after the present corpus existed. Do not multiply its 37.9 ratio by Experiment 349's 27.7 ratio as though independent: Experiment 350 is explicitly conditioned on the 3/6 family selected in Experiment 349.

## Consequence

G1 should no longer be described monolithically as only a generic simplicity prior. Its **one-per-column occupancy component** now has independent historical and chronological support; its **ternary exceptional-position semantics** remains a generic code-choice prior.

The next discriminating question should target that remaining semantic step: does any independently attested operation require reading the minority cell's row position as a three-valued symbol, rather than using the three physical positions in some other way?

Compact results are in `data/experiment-350-chronological-frame-occupancy-summary.json`. Full batch histories are reproducible from the script and preserved in workflow run `36810906296`, artifact `11138738782`, digest `sha256:b475eb67302fe52430108e2367777b9abdfb26f13c15f03e815202625a304ead`.
