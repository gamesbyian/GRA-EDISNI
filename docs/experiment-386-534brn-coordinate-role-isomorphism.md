# Experiment 386 — coordinate-role isomorphism between 534brn and the one-shot surface

_Status: completed bounded structural audit, 2 Oct 2026._

Experiment 385 showed that the old “90° CCW” description is not the most informative way to state the match.

There is a more principled parent family.

## Both objects are ternary coordinate relations

After the historically licensed DTMF-row reduction, every cell of the solved nine-piece background carries three ternary coordinates:

```
(r, c, k)
```

where:

- `r` = physical row of the CE background cell;
- `c` = physical column;
- `k` = DTMF keypad-row value of the corresponding `534brn` digit.

There are exactly nine such triples.

The one-shot G5 object can likewise be written as nine triples:

```
(Q, c, r)
```

where:

- `Q` = outer 27-cell layer;
- `c` = physical output column;
- `r` = decoded minority-row value.

So instead of trying arbitrary rotations and reflections, ask a bounded question:

> Which permutation, if any, of the three external coordinate roles `(r,c,k)` can serve as the target roles `(Q,c,r)`?

There are only `3! = 6` possibilities.

## Exact enumeration

Four of the six role permutations fail immediately.

They attempt to use keypad row `k` as one of the two target input axes. Because the observed `k` values do not give every input pair exactly once, those assignments do not even define a complete 3×3 function.

Only two role assignments survive as total grids.

### Direct

```
target Q     <- source r
target c     <- source c
target value <- source k
```

This is simply:

```
101 / 211 / 022
```

It has **zero** matches to the one-shot family under all six preregistered Experiment-266 q maps.

### Swapped physical axes

```
target Q     <- source c
target c     <- source r
target value <- source k
```

This is:

```
120 / 012 / 112
```

the strict matrix transpose.

Across all six one-shot states and all six preregistered q maps, there is exactly **one** hit:

```
external relation: 120 / 012 / 112
canonical state:    112 / 012 / 120
q map:              q' = 2q + 2
```

## Why this is stronger than a visual D4 match

The successful transform is no longer being selected from an arbitrary collection of ways to turn a square.

It is the unique match inside the smallest coordinate-role family connecting two independently ternary objects.

The alternatives are exhaustive and easy to state:

- choose which external coordinate becomes target Q;
- choose which becomes target column;
- the remaining coordinate becomes the target value.

Most alternatives are structurally invalid before the target family is consulted.

## What remains unresolved

This does **not** prove that Playdead intended the coordinate-role permutation:

```
(c, r, k) -> (Q, c, r)
```

The historical “transposed” discussion licenses re-registration broadly, not this exact formal role assignment.

Likewise `q'=2q+2` is selected from a preregistered six-way first-pass family by the external match rather than by a recovered authorial instruction.

So the result is best described as:

> a unique bounded ternary-coordinate isomorphism candidate.

That is substantially stronger than “one rotation happens to look right,” but it is still a candidate.

## Next falsification target

The best remaining evidence would explicitly connect:

- background **physical column** to foreground outer `Q`;
- background **physical row** to foreground output column;
- or reverse the `Q` ordering.

Any such cue would independently fix part of the unique role assignment.

Do not expand beyond the six coordinate-role permutations.
