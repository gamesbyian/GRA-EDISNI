# Experiment 385 — the “CCW rotation” decomposes into historical transpose + preregistered q gauge

_Status: completed bounded reconciliation, 2 Oct 2026._

Experiment 383 left one concentrated problem:

> why does the registered `534brn` keypad-row grid require a 90° counter-clockwise turn to hit the one-shot family?

A better decomposition was already sitting in the repository.

## The external grid

After the independently supported steps:

- nine-piece native serial registration;
- `534965398`;
- DTMF keypad **row** coordinate;

the external grid is:

```
101
211
022
```

Experiment 383 described the successful operation as:

```
90° CCW -> 112 / 012 / 120
```

## But 90° CCW is transpose + row reversal

Transpose the external grid first:

```
101      120
211  ->  012
022      112
```

That exact **transpose** operation has historical sticker-specific provenance.

On 2 Nov 2025, before the current machine work, lime8159 explicitly proposed that the sticker puzzle might need to be **transposed** in relation to the already-solved `534brn` puzzle.

So transpose itself no longer needs to be invented from the fit.

The remaining difference between:

```
120 / 012 / 112
```

and the canonical one-shot state:

```
112 / 012 / 120
```

is simply reversal of the three external `q` rows.

## That row reversal was preregistered before this hit

Experiment 266 exhaustively tested all 432 invertible affine maps on the two ternary coordinates `(q,S)`.

Its six maximum-retention maps all had:

```
d' = S
q' = a*q + u
a ∈ {1,2}
u ∈ {0,1,2}
```

In other words, all six affine permutations of the external q labels survived equally at the maximum 20-state first-pass retention.

Experiment 355 later reconciled that result during the epistemic reset.

One of those six frozen maps is:

```
q' = 2q + 2  (mod 3)
```

which orders the canonical internal rows as:

```
2, 1, 0
```

Applying that already-known q relabeling to canonical one-shot state:

```
112
012
120
```

gives:

```
120
012
112
```

which is **exactly the transposed external grid**.

## Exact audit

Test all six Experiment-266 q relabelings against all six Experiment-374 one-shot states.

Results:

- untransposed external grid `101/211/022`: **0 hits**;
- transposed external grid `120/012/112`: **1 hit**;
- unique pair:
  - canonical one-shot state `112/012/120`;
  - q map `q'=2q+2`.

Thus the previously successful CCW turn has the exact decomposition:

```
historically proposed transpose
+
one member of a preregistered six-way q-relabeling family
```

rather than:

```
invent a free D4 orientation and pick the one that works
```

## Why this matters

The candidate's geometry is now much less post-hoc.

The transpose operation was independently proposed in the historical sticker discussion.

The six q relabelings were independently enumerated as equal first-pass maxima before the `534brn` external hit was discovered.

The external match therefore selects one member of an already-existing unresolved gauge/operation family instead of requiring a new transform family.

That is exactly what an external consumer is allowed to do.

## Important caveat

Experiment 266 also noted:

> fixing physical q labels leaves the canonical identity map.

So `q'=2q+2` should not be waved away as pure physical gauge. Native serial q order still exists.

The correct statement is narrower:

> the machine already had a six-way first-pass q-registration ambiguity; the external transposed grid selects the reversal member.

That is a genuine reduction in arbitrariness, not proof of authorial intent.

## Revised remaining burden

The old “why CCW?” question is superseded.

The remaining question is now:

> why should the external `534brn` consumer fix the otherwise underdetermined q registration specifically to `q'=2q+2`?

That is a much smaller and better-typed question.

Do not reopen arbitrary D4 transforms.
