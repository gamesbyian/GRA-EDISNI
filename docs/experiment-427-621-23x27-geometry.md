# Experiment 427 — 621 as a 23×27 serial rectangle

## Question

If 621 is meaningful because `621 = 23×27`, does either natural rectangular orientation preserve the sticker system's independently established geometry?

Only two layouts are tested:

- 23 rows × 27 consecutive serials;
- 27 rows × 23 consecutive serials.

No symbol decoding, row permutation, visual scoring, or new arithmetic is introduced.

## 23 rows × 27 columns

This orientation fits the existing carrier exactly.

A row width of 27 means every row is one complete native 27-cell quarter of H108. The row-start residues are:

```
1, 28, 55, 82,
1, 28, 55, 82,
...
1, 28, 55
```

So the 23 rows are:

```
Q1 Q2 Q3 Tail   × 5
Q1 Q2 Q3
```

Equivalently, they are five complete H108 masters followed by exactly the 81-cell primary body of a sixth.

Because 27 is also `3×9`, every row contains exactly three complete background-image cycles and every row begins at the same period-9 phase.

Thus **all 23 row boundaries simultaneously respect the native 27-cell and 9-cell carriers**.

## 27 rows × 23 columns

The transpose does not inherit those properties.

A width of 23 gives:

```
23 mod 27 = 23
23 mod 9  = 5
gcd(23,108) = 1
```

Row starts therefore walk through the H108 carrier rather than staying on quarter boundaries, and the background phase rotates instead of resetting each row.

Only the first row begins on a 27-cell boundary.

So if a `23×27` object was intended, the carrier itself strongly privileges **23 rows of 27**, not 27 rows of 23.

## Sticker 597

The highest currently observed serial has a mildly interesting position in this hypothetical layout:

```
597 = 22×27 + 3
```

so sticker 597 lies at:

- row **23** of 23;
- column **3** of 27;
- H108 residue **57**.

In other words, the iam8bit 597 sticker would fall in the final 27-cell row of a 621-label rectangle.

This is not endpoint evidence. A high observed serial is naturally likely to lie near the end of any nearby hypothesized range, and 597 remains only a proof that a high serial existed.

## Interpretation

This strengthens a narrow conditional statement:

> **If** 621 was the authored serial-space endpoint, then `23×27` is not merely a numerical factorization. It has a uniquely natural orientation in which the entire rectangle is tiled by native 27-cell quarters while preserving the period-9 background phase.

That is a cleaner structural convergence than `598 = 23×26`.

It still does not establish that 621 labels were printed or that 621 Collector's Editions existed.

## Disposition

Preserve **23 rows × 27 serials** as the canonical 621 geometry.

Do not use the geometry to infer 621. Use it only as a prediction: if future manufacturing evidence gives 621, 23 rows, 27 columns, 27-label strips, or a sheet/imposition compatible with those dimensions, the independent pieces would converge sharply.
