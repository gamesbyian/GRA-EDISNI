# Experiment 347 — historical 12-row permutation audit

_Status: completed; preregistration frozen before analysis, 30 Sep 2026._

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


## Result

The exact dynamic program enumerates the score distribution of all **479,001,600** directed row permutations.

| measure | result |
|---|---:|
| canonical serial order score | -9 |
| fraction of all orders scoring at least canonical | 84.5364% |
| exact score range | -28 to +20 |
| maximizing directed orders | 60 |
| maximizing orders with observed dot rows 10 and 11 as opposite endpoints | 0 / 60 |

The canonical 1→12 row order is therefore not unusually continuous. It sits in the weak part of the exact null distribution.

The optimized score of +20 is also not a unique reconstruction: 60 directed orders attain it. More importantly, **none** satisfies the independently frozen historical proposal that the two physically observed dot-bearing rows occupy the two opposite ends of the rearranged object.

This rejects the specific Dec-2022 "rearrange the 12 rows like acorn 41, maybe one yellow is at the top and the other at the bottom" formulation under the cheapest observation-only continuity interpretation.

## Interpretation

Do not inspect the 60 maximizing arrangements for a pretty picture or choose among them semantically. Their existence is expected after optimizing 12! candidate paths over incomplete data.

Together with Experiment 345, both obvious permutation axes are now calibrated:

- permuting nine A-I traces in the 9×12 transpose does not select the known serial or physical order;
- permuting twelve sequence rows in the historical 12×9 view does not make the canonical order special, and its preregistered yellow-row endpoint prediction fails exactly.

Experiment 346 additionally closes the most obvious independent physical-perimeter check-bit channel.

The remaining ordering/image lane therefore needs a **more specific independent operation**, not more permutation search. The Dec-2022 statement about "rearranging the top 9×9 grid to account for the repeating pattern" is a distinct historical lead and should be reconstructed literally before any new geometric search.

Exact score counts are preserved in `data/experiment-347-historical-12row-permutation-audit.json`. Workflow run `36809833465`, artifact `11139451730`, digest `sha256:b748182a6e822f02fd37b7c5b3d4d3da0f075dec9ffd083345fcfceb3f546fd5`.
