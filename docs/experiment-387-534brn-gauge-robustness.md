# Experiment 387 — gauge robustness of the 534brn coordinate match

_Status: completed exact gauge audit, 2 Oct 2026._

Experiment 386 found a unique match inside the six coordinate-role permutations:

- external direct `(r,c)->k`: no hit;
- swapped `(c,r)->k`: one hit, canonical `112/012/120` under `q'=2q+2`.

But Experiment 352 established an important caveat: the numeric labels `0,1,2` attached to physical minority rows are coordinate gauge until another operation fixes them.

So the external match must be tested against that known gauge freedom rather than quietly assuming canonical labels.

## Shared physical-row gauge

First allow every global permutation of the three row labels.

There are `3! = 6`.

For each of the six one-shot states, each of the six preregistered q maps, and each global row-value permutation, test exact equality with both external coordinate-role grids.

Result:

- direct role assignment: **0 hits**;
- swapped/transposed role assignment: **1 hit**.

The unique hit remains:

```
state:      112 / 012 / 120
q map:      q' = 2q + 2
value map:  identity 0,1,2
```

So the match is not an artifact of choosing one convenient global renaming of top/middle/bottom.

In fact, the external artifact selects the canonical physical-row labels rather than merely some permutation of them.

## Maximum local gauge control

Experiment 352 also noted the much looser mathematical possibility that each physical column could have its own independent row-label gauge.

That gives:

```
(3!)^3 = 216
```

column-local value-label systems.

This is less natural once `r` is treated literally as one shared physical row coordinate across a 3×3 frame, but it is the correct adversarial control.

Result:

- direct role assignment: **0 hits**, even with all 216 local gauges;
- swapped/transposed role assignment: **4 hits**.

Every one of those four still requires:

```
q' = 2q + 2
```

and every one keeps the outer two columns' value labels at the identity map.

The four compatible canonical one-shot states are:

```
102 / 002 / 120
112 / 012 / 100
112 / 012 / 120
122 / 022 / 100
```

The only freedom is a relabeling of the **middle** output column.

That is exactly where Experiment 374 already found all one-shot-family variation.

## Interpretation

This separates two claims that had been bundled together.

### Robust

The external artifact strongly selects:

- the swapped coordinate-role assignment rather than the direct one;
- the q reversal `q'=2q+2`.

Those facts survive even an extremely generous per-column row-label gauge.

### Gauge-sensitive

The claim that the external artifact selects **specifically** canonical state `112/012/120` assumes that physical top/middle/bottom constitute one shared row coordinate across all three columns.

That is the natural literal geometry of a 3×3 frame, and under that shared coordinate the state is uniquely selected.

But if one permits each column to rename its rows independently, four canonical one-shot representatives become equivalent to the same external object.

## Consequence

The active candidate should now be stated at two levels:

**geometry-level robust claim**

> the `534brn` DTMF-row relation uniquely selects the swapped physical-axis registration and q reversal `q'=2q+2`.

**canonical shared-row representative**

> under one shared physical-row coordinate, that relation is exactly `112/012/120`.

This is stronger and cleaner than pretending every numeric label was independently fixed from the start.
