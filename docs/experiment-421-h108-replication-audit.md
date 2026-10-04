# Experiment 421 — empirical H108 replication audit

_Status: completed physical-corpus audit, 4 Oct 2026._

Sticker 043 does not add a new H108 residue, but it creates another physically independent same-residue replication. That makes it useful for a different question:

> How strongly does the observed sticker corpus itself support period 108, without using any completion-model assumptions?

## Current replication corpus

The checked-in physical corpus now contains:

- **84 physical stickers**;
- **66 unique H108 residues**;
- **16 residues represented by two or more physical stickers**;
- **20 same-residue sticker pairs** in total.

Across all 20 pair comparisons:

```
foreground agreements: 20
foreground disagreements: 0
```

Two residues have three observed physical copies:

- residue 15: 123 / 231 / 339, all slash;
- residue 38: 38 / 362 / 470, all slash.

Sticker 043 adds the new long-baseline replication:

```
43 / 475
delta = 432 = 4 × 108
slash / slash
```

The other four-period foreground replication is residue 37:

```
37 / 469
dash / dash
```

So the repeat is not supported only by adjacent-cycle pairs.

## Conditional symbol-permutation null

The 16 repeated H108 residues all lie in the slash/dash primary zone. Across the **72 observed primary-zone physical stickers**, the corpus contains:

```
44 slash
28 dash
```

Condition on those totals exactly, randomly permute the 44 slashes and 28 dashes among the 72 observed primary serial positions, and ask for every H108 collision group to be internally homogeneous.

The repeated-group structure is:

```
14 groups of size 2
 2 groups of size 3
38 singleton positions
```

The exact combinatorial probability is:

```
P(all 16 repeat groups homogeneous | 44/28 totals)
  = 440,079,448,381,568 / 75,553,695,443,676,829,680
  ≈ 5.8247 × 10^-6
  ≈ 1 in 171,682
```

This is deliberately **not** presented as a blind period-search p-value. Period 108 was already independently hypothesized from the corpus structure; the scan below is a separate descriptive comparison. The null is useful as a scale for how unlikely perfect repeat consistency would be if the observed primary symbols were exchangeable across the observed serial positions.

## Bounded period scan

To test whether 108 is merely a convenient grouping, every integer period from **2 through 216** was scored on the same 84 serial/symbol observations.

For each candidate period:

1. reduce every serial modulo that period;
2. collect collisions;
3. count all colliding sticker pairs;
4. count whether each pair agrees in foreground symbol;
5. count residue groups containing any foreground conflict.

Only three candidate periods in the scan have **zero conflicting repeated groups**:

| period | agreeing pairs | conflict groups |
|---:|---:|---:|
| **108** | **20** | **0** |
| 216 | 8 | 0 |
| 197 | 6 | 0 |

Period **108** therefore has by far the deepest zero-conflict replication support in the entire bounded scan.

The 216 result is unsurprising as a coarser multiple: it merges only observations separated by even numbers of H108 cycles, so it throws away many valid 108 repetitions rather than explaining more data.

Period 197 happens to create six symbol-compatible collisions in this sparse corpus, but with much less support and no known structural relationship to the CE carrier.

## Epistemic consequence

The H108 cycle should now be treated as a directly replicated physical property of the sticker corpus, not merely as a reconstruction convenience.

This result is independent of:

- POS3;
- the one-slash-per-depth-stack model;
- G5/G6 recursion;
- the 534brn hypothesis;
- XOR overlays;
- background-tile ordering.

Those downstream models may still be wrong while the period-108 foreground recurrence remains strongly supported.

## Acquisition consequence

A newly found sticker can now have three different evidentiary values:

1. **new H108 residue**: strongest for pruning the missing foreground;
2. **repeat of a model-variable residue**: strongest for prospective model checking;
3. **repeat of an already fixed residue**: weaker for completion pruning but useful as independent recurrence replication and source-quality confirmation.

Sticker 043 is category 3.

Future acquisition reporting should therefore distinguish **new physical sticker count** from **new unique H108 residue count** rather than treating every new sticker as equivalent.
