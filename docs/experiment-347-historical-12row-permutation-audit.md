# Experiment 347 — historical 12-row permutation audit

_Status: preregistered; analysis not yet run._

## Historical cue

The archived sticker discussion supplies a more specific row-permutation proposal than Experiment 345 tested.

On 22–23 Dec 2022 the community:

- displayed the H108 object as a 12×9 matrix;
- noted that each of the nine columns corresponds to one repeating A-I background pattern;
- explicitly proposed rearranging the **12 rows** "like acorn 41", including the suggestion that the yellow/dot-bearing rows might become top/bottom structure.

Experiment 345 instead tested permutations of the nine A-I traces in the transposed 9×12 view. Experiment 347 tests the historically attested 12-row axis.

## Frozen input

Use only `data/observations.csv`.

Represent H108 as twelve consecutive 9-cell rows:

- row 1 = residues 1–9;
- ...
- row 12 = residues 100–108.

Unknown cells remain unknown. No model fills, Pigpen mapping, POS3, selector semantics, background pixels, or semantic target may enter the score.

## Frozen adjacency score

For two candidate rows placed next to one another, compare aligned columns:

- +1 for a known-known symbol match;
- -1 for a known-known symbol mismatch;
- 0 if either cell is unknown.

An ordering's score is the sum across its eleven row boundaries.

This deliberately mirrors Experiment 345's cheapest continuity test so only the historically different permutation axis changes.

## Exact search and null

Do not sample 12! orders.

Use subset dynamic programming over the complete 12-node weighted adjacency graph to compute:

1. the exact maximum achievable score;
2. every maximizing row order, up to a hard reporting cap only after the exact count is known;
3. the exact score distribution across all `12! = 479,001,600` directed permutations;
4. the percentile/tail fraction of the canonical serial row order `1,2,...,12`.

Because reversal leaves an undirected adjacency path's score unchanged, reverse pairs are expected and are not counted as independent structural confirmation.

The historical "one yellow at the top, the other at the bottom" suggestion is operationalized before analysis as follows: identify rows containing physically observed dots directly from `data/observations.csv`. If exactly two rows contain dots, test whether those two rows are the two endpoints of each maximizing order. Do not infer or fill missing dots.

## Interpretation rule

A high-scoring optimized order is not evidence by itself. The historical family becomes interesting only if one of these occurs without retuning:

- the canonical order is already unusually high under the exact permutation null; or
- the exact optimum is highly constrained and independently agrees with the specific historical yellow/dot boundary proposal.

Otherwise the result is another demonstration that free row permutation can manufacture structure from incomplete data.

No visual or semantic inspection of optimized arrangements is permitted until the exact structural result is frozen.
