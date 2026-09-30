# Experiment 324 — observation-only 9x12 spatial-field audit

_Status: completed first pass, 30 Sep 2026._

## Motivation

The usual community display is 12x9 because every column then shares one A-I
background image class. That is a useful registration view, not evidence that
12x9 is the intended reading direction.

Transposing gives nine 12-symbol class traces. Each trace has the independently
attested 9+3 split:

- nine slash/dash body cells;
- three slash/dot tail cells.

This motivates a bounded alternative family in which the nine body cells are
spatial material and the three tail cells select, orient, or address something
about that material. Pigpen/Rosicrucian-style geometric alphabets are one
candidate member of that family, not a target to optimize toward.

The transpose also exposes a collective decomposition:

- 81 body cells = 9x9;
- 27 tail cells = 9x3, also 3x3x3 in cardinality.

That bookkeeping is worth testing because it is native to the observed 81/27
alphabet boundary and the historical 9+3 proposal.

## First test

Before trying to recognize letters, ask whether the *observed* 9x9 body already
has unusual contiguous binary geometry.

Inputs:

- only `data/observations.csv`;
- unknown body cells stay `?`;
- no prediction-matrix fills;
- no POS3;
- no recursive machine;
- no semantic target.

Two preregistered column orders are checked:

1. serial/background-class order `ABCDEFGHI`;
2. the independently solved physical flattening `IAB/CDE/FGH`, written
   `IABCDEFGH`.

For each layout, count orthogonally adjacent known-known body pairs whose
symbols match. Compare that count against a fixed-mask permutation null that
preserves:

- the exact 54 known body locations;
- the observed census of 32 slashes and 22 dashes.

The Monte Carlo null uses 200,000 deterministic permutations (seed 324).

## Result

| layout | known-known edges | matching edges | null mean | z | one-sided p for >= observed |
|---|---:|---:|---:|---:|---:|
| A-I | 64 | 30 | 32.516 | -0.650 | 0.784 |
| IAB/CDE/FGH flattening | 62 | 29 | 31.506 | -0.657 | 0.787 |

There is no evidence in this cheap statistic that the physically observed
slash/dash cells form unusually large same-symbol orthogonal regions. If
anything, the observed counts sit mildly below the null mean, but nowhere near
an interesting tail.

## Interpretation

This is a useful guardrail, not a rejection of geometric decoding.

A contrast-heavy collective image can look compelling even when:

- 27 of the 81 body cells are still physically unknown;
- unknowns are rendered as a visually strong color;
- a completion model has silently supplied cells;
- geometry depends on a transform or on literal slash/dash line orientation
  rather than same-symbol regions.

Therefore a Pigpen/Rosicrucian hypothesis should not be justified by apparent
large blobs alone.

The 9x12 / 9+3 architecture remains live. The present negative result only
closes the cheapest "the raw known body already clusters into obvious solid
regions" version.

## Registered next family

Proceed without semantic fitting:

1. render canonical 12x9, 9x12, 9x9+9x3, and nine paired 3x3+selector views,
   always showing unknowns explicitly;
2. test literal line geometry of slash and dash rather than only binary color;
3. enumerate only D4 rotations/reflections plus the two independently motivated
   class orders, not arbitrary cell permutations;
4. define Pigpen/Rosicrucian template compatibility before inspecting decoded
   letters;
5. freeze any global transform/codebook on a training subset and score held-out
   classes/frames;
6. separately inspect the contrast-enhanced assembled background artwork as a
   possible independently supplied mask/sorting key, using only supported
   master pixels and support masks.

The last item is deliberately separate from foreground fitting. If background
art supplies a mask, partition, edge, or orientation, that rule must be
measured from the image first and only then applied to foreground data.

## Reproducibility

Run:

```bash
python scripts/audit_9x12_spatial_field.py
```

The script emits both 9x9 body views, both 9x3 tail views, observed adjacency
counts, and the deterministic permutation-null summary.
