# Experiment 373 — native coordinate typing resolves the G5 axis

_Status: completed structural audit, 2 Oct 2026._

This is the strongest consequence of pushing the Xbox/positional line downstream.

The 108-residue foreground already has a native arithmetic address:

```
r - 1 = 27Q + 9d + j
```

with:

- `Q` = 27-cell quarter/layer;
- `d` = 9-cell depth inside that quarter;
- `j` = A-I class / physical cell.

For residues 1–81, `Q = 0,1,2`. For residues 82–108, `Q = 3`.

That means the so-called 9+3 word for any fixed A-I class is not merely an arbitrary twelve-character split. Its positions are exactly:

```
Q0d0 Q0d1 Q0d2
Q1d0 Q1d1 Q1d2
Q2d0 Q2d1 Q2d2
Q3d0 Q3d1 Q3d2
```

The final three tail positions therefore vary in **d**, not in Q.

Experiment 317 independently established that the tail is compatible with one slash marking exactly one of those three positions. So the tail selector `S(j)` is natively typed as a **d-coordinate**.

That changes the G5 question substantially.

If the independently motivated tail/index is applied to the preceding 3×3 `(Q,d)` body while preserving native coordinate type and A-I registration, there is only one direct operation:

```
(Q,d,j) -> (Q,S(j),j)
```

That is exactly G5.

No first-pass output, terminal `100`, route shell, hidden-state count, or recursive closure is needed to choose the axis.

## Reinterpretation of Experiment 318

Experiment 318 compared two observation-only readings of the nine body positions:

- row/chunk;
- column/rail.

Under the native `(Q,d)` coordinates:

- **row/chunk** means interpreting the tail's d-position as a Q selector;
- **column/rail** means using the tail's d-position as d.

So the previously symmetric-looking alternatives are not equally typed.

The column/rail interpretation is the type-preserving one. It is also the physical extraction implemented by G5: for each class `j`, choose depth `d=S(j)` while leaving all three Q layers present.

## Why this is stronger than Experiment 354

Experiment 354 showed that once literal G5 is admitted, only the identity tail→depth label registration survives first-pass POS3 closure.

Experiment 373 acts earlier. It says why **depth is the correct axis to consume in the first place**: the selector's three physical positions already are the three native depth positions.

This directly addresses Experiment 353's remaining bridge:

> which body coordinate is selected/replaced, and why?

Answer:

> the body depth coordinate, because the tail index is physically a depth coordinate.

The remaining nontrivial premise is now only that the tail is intended to index the preceding body at all. That premise already has independent support from the historical 9+3 body/index proposal, Experiment 317's one-slash tail architecture, and Experiment 372's Playdead positional-selector precedent.

## Consequence for G6

This same typing result cuts the other way for the second selector application.

After G5, the remaining three surfaces are indexed by **Q**. Reusing `S(j)` to choose Q treats a physical d-coordinate as though it were a Q-coordinate.

That is a cross-axis coercion, not a type-preserving continuation.

So Experiment 373 strengthens G5 while weakening the naturalness of G6. G6 can still be a valid model-level transform, and Experiments 291/322/269 show it is strongly constrained once admitted, but native address geometry does not motivate it.

## Guardrail

This result does not prove authorial intent. It establishes a uniquely natural typed interpretation of the already observed serial geometry.

Do not infer recursion, route semantics, or terminal meaning from it.
