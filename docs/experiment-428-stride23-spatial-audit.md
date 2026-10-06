# Experiment 428 — stride-23 spatial audit

## Question

If 23 is an intended sticker quantity, does traversing the H108 foreground by modular step 23 expose unusually coherent spatial structure?

The test is deliberately bounded:

- start at residue 1;
- use every stride coprime to 108, so each stride visits all residues exactly once;
- compare stride 23 and its reverse 85 against the full 36-stride family;
- reshape only into already-used natural H108 rectangles: 12×9, 9×12, 4×27, 27×4;
- score only generic local structure: equal-symbol edge fraction and homogeneous 2×2 blocks;
- average each score over the 10 currently live canonical completions.

No phase optimization, row permutation, symbol reassignment, image recognition, or hand-picked visual target is allowed.

## Result

Stride 23 is not exceptional.

| shape | stride 23 equal-edge rank | stride 23 2×2 rank | reverse 85 equal-edge rank |
|---|---:|---:|---:|
| 12×9 | 9 / 36 | 15 / 36 | 7 / 36 |
| 9×12 | 25 / 36 | 19 / 36 | 20 / 36 |
| 4×27 | 23 / 36 | 36 / 36 | 15 / 36 |
| 27×4 | 23 / 36 | 20 / 36 | 13 / 36 |

The ordinary serial stride 1 is the strongest equal-edge traversal in every tested layout, as expected from the native carrier's local structure.

Stride 23 therefore does not reveal a new image-like ordering under these preregistered generic metrics.

## Disposition

Negative.

Do not use 23 as a modular traversal key unless an independent clue specifically licenses stepping or modular indexing. The present evidence for 23 remains stronger in production-total/grouping geometry than as an H108 permutation operator.
