# Experiment 383 — the remaining quarter-turn is real, not coordinate gauge

_Status: completed coordinate-typing audit, 2 Oct 2026._

Experiment 382 removes most of the arbitrary 3×3-registration concern. The nine URL digits can be associated naturally with native serial classes `0..8`, and those classes already occupy the solved physical grid in row-major order.

That leaves the 90° counter-clockwise turn.

It is tempting to dismiss that as harmless orientation freedom between two square grids. That would be too generous.

## The two grids share one physical axis

The `534brn` source grid lives on the solved background coordinates:

```
physical row r × physical column c
```

The one-shot G5 object is different:

```
outer layer Q × physical column c
```

and each cell contains the decoded minority-row coordinate `r`.

So both surfaces contain the same physical-column coordinate `c`.

A truly type-preserving registration would therefore keep the column axis as the column axis.

The successful transform does not.

Starting from:

```
101
211
022
```

the unique one-shot hit is:

```
112
012
120
```

obtained by a 90° counter-clockwise turn.

That swaps the source axes. In coordinate language, the hit identifies one source physical axis with the machine's outer `Q` axis.

Therefore this is a substantive operation, not merely choosing which way to hold a square.

## Exact D4 audit

All eight rigid square symmetries were classified by whether they preserve the two grid axes or swap them.

Result:

- axis-preserving transforms: **0 hits**;
- axis-swapping transforms: **1 hit**;
- unique hit: **90° counter-clockwise → `112/012/120`**.

This sharpens the candidate considerably.

## Historical control cuts both ways

There is genuine provenance for the operation family.

The solved Xbox printer requires a 90° rotation before its Braille layer becomes readable. That proves Playdead used a quarter-turn between registered carrier and secondary readout elsewhere in the same ARG.

The Nov-2025 sticker discussion also explicitly proposed “transposing” / reorganizing 3×3 sticker cells in relation to the `534brn` puzzle.

But the exact Xbox solution uses **90° clockwise**.

The current candidate requires **90° counter-clockwise**.

Testing exact historical reuse therefore gives a negative control:

> clockwise does **not** hit the one-shot family.

So “Xbox rotated” cannot be used to smuggle in the successful direction.

## Revised burden

The `534brn` candidate is now in an unusually clean state.

Independently supported or natively typed:

- nine-piece 3×3 source carrier;
- nine URL digits as a historically noticed sticker-adjacent layer;
- native serial modulo-9 registration of the nine positions;
- DTMF keypad row coordinate as the ternary reduction.

Still unresolved:

> why perform the specific axis-swapping 90° CCW registration that maps the background `(r,c)` carrier into the one-shot `(Q,c)` surface?

That is now essentially the whole remaining burden.

## Next move

Search only for evidence that can fix an **axis swap or direction**, for example:

- an arrow, rotation cue, handedness, or reading-direction cue in the solved nine-piece image;
- a historical message explicitly rotating/transposing the background or foreground in a stated direction;
- a downstream artifact whose coordinate labels force the `r,c → Q,c` registration.

Do not add more transforms.
