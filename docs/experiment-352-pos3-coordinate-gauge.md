# Experiment 352 — POS3 coordinate/gauge audit

_Status: completed exact structural audit, 1 Oct 2026._

## Motivation

Experiment 350 independently supports this physical skeleton for each first-81 3×3 frame:

> exactly one minority mark occurs in each physical column.

Experiment 351 shows that three-position coordinate/index readings were historically explored before the present machine, but it does not recover the exact modern POS3 rule.

The apparent remaining question has therefore been phrased as:

> Why should the minority mark's row position be read as a ternary value?

Experiment 352 asks whether that is actually an additional structural hypothesis, or merely the canonical coordinate system of the already-supported occupancy pattern.

## Exact state space

Take one 3×3 frame with exactly one minority cell in each of its three physical columns.

For column `c`, let `r_c` be the row containing its minority cell.

Then every occupancy is represented by:

```
(r0, r1, r2),   each r ∈ {0,1,2}
```

There are exactly:

```
3 × 3 × 3 = 27
```

such occupancy patterns.

The map is bijective:

- occupancy → row triple: read the unique minority row in each column;
- row triple → occupancy: place the minority cell at that row in each column.

No information is discarded and no extra combinatorial restriction is introduced.

If the frame's minority symbol itself remains free, slash-minority versus dash-minority adds one independent binary polarity bit:

```
2 × 27 = 54
```

which is exactly the Experiment-350 one-per-column assignment count.

## What "ternary value" adds

Assigning the three physical rows labels `0,1,2` does **not** select a new subset of physical states. It merely names the three alternatives.

There are:

- `3! = 6` global ways to relabel the physical rows with three ternary symbols if all columns share one orientation;
- `(3!)^3 = 216` ways if each column is allowed its own independent row-label gauge.

Every one of these labelings is a bijection over the same 27 occupancy states.

Therefore the statement:

> "the minority mark's row position is a ternary coordinate"

is structurally equivalent to:

> "record which of the three rows contains the unique minority mark."

Given Experiment 350's skeleton, that coordinate extraction is lossless and essentially forced if the goal is to preserve the occupancy information column-by-column.

## Relation to POS3

The project's `POS3(v; exceptional, background)` primitive contains two conceptually different claims that should now be separated:

1. **physical positional code:** one exceptional cell among three positions;
2. **semantic/operational use:** the position label `v` participates as a value in another operation.

Experiment 350 independently supports the first part for the primary frames.

Experiment 352 shows that representing that physical state by a three-valued coordinate is not an additional empirical burden. It is a canonical coordinatization, modulo row-label gauge.

What remains unsupported by this result is the second part: that these coordinates are consumed as addresses/values in the specific downstream operations of the incumbent machine.

## Epistemic consequence

G1 should be split more sharply.

### Independently supported / structurally forced

- 3/6 frame census, with reset-era chronological support;
- one minority cell per physical column, with reset-era chronological support;
- a lossless three-valued coordinate per column obtained by recording the minority row.

### Gauge / convention

- whether physical top/middle/bottom are named `0/1/2`, `1/2/0`, or another permutation;
- absent an external orientation cue, the numeric labels themselves.

### Still substantive hypotheses

- one shared row-label orientation across all columns if an operation cares about label identity;
- interpreting coordinates arithmetically rather than categorically;
- reusing the same positional primitive in the tail;
- selector semantics;
- recursive address substitution;
- route/terminal consequences.

The research frontier therefore moves downstream:

> not "why ternary?", but "what independently motivates consuming these three positional coordinates in the way the incumbent machine does?"

## Reproducibility

Run:

```bash
python scripts/audit_pos3_coordinate_gauge.py
```

The script exactly enumerates all 27 occupancy states, verifies the coordinate bijection, verifies the 54-state polarity factorization, and verifies all 216 independent per-column row-label gauges.
