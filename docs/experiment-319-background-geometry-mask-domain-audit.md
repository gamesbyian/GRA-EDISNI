# Experiment 319 — Background-geometry mask domain audit

_Status: completed reset R3 discriminator, 30 Sep 2026._

## Question

Experiment 318 left one deliberately preregistered third selector family to test:

> three fixed masks tied to the independently solved A-I background geometry.

The reset rule says those masks must be declared from the solved geometry **before** inspecting foreground outputs. If the geometry does not uniquely motivate a small mask family, record that failure rather than sweeping masks.

## Inputs

- `data/observations.csv`
- the historically attested background arrangement:

```
I A B
C D E
F G H
```

No predicted cells, machine state, POS3, recursive survival, route criteria, terminal object, plaintext target, or foreground-output scoring is used.

## Domain audit

The proposed operation contains a hidden type mismatch.

The solved 3x3 background geometry indexes the **nine image classes A-I**.

By contrast, a single class's 9+3 foreground word is formed from H108 residues

```
c, c+9, c+18, ... c+99
```

for one fixed image class `c`. Its first nine positions are therefore **nine successive occurrences within the same image class**, not the nine A-I image classes.

For example, every body position in B's nine-cell body is a B-background sticker position. The same is true independently for A, C, ..., I.

So a background-row or background-column mask cannot be projected onto those nine body positions until an additional mapping

```
body position 0..8  ->  background class A..I
```

is supplied.

No such mapping is present in the raw sticker ledger, the serial modulo-9 relation, or the solved `IAB/CDE/FGH` geometry.

## Convention count

A full identification of the nine body positions with the nine background classes has

```
9! = 362,880
```

possible bijections.

Even if only the three labelled rows of the solved background are retained and within-row order is ignored, there are

```
9! / (3!^3) = 1,680
```

possible ordered 3+3+3 mask partitions of the body.

Choosing one of those after viewing foreground outputs would be exactly the kind of free parameter search prohibited by the reset.

## Result

**No background-derived body-mask family is independently identified.**

This is a useful negative result. It prevents a superficially attractive cross-layer operation from acquiring evidentiary weight merely because both objects happen to contain nine positions.

Experiment 318's row/chunk and column/rail selector readings remain legitimate because they act directly on the body's own 3x3 indexing. The solved A-I artwork geometry does not currently supply a third equally direct mask family.

## What could reopen this family

A geometry-derived body mask becomes testable if independent evidence supplies the missing domain bridge, for example:

- a historical pre-machine statement explicitly identifying the nine body positions with A-I;
- a physical/layout feature that labels body occurrence positions by background class;
- another ARG artifact specifying that identification or permutation;
- a manufacturing/source artifact showing that the nine within-class occurrences were authored in A-I spatial order.

Until then, do not enumerate the 1,680 row-mask partitions or 362,880 full bijections.

## Reproducibility

Run:

```bash
python scripts/audit_background_geometry_masks.py
```

The script verifies the residue-to-image-class relation for every observation and asserts the convention counts above.
