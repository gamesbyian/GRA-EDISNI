# Experiment 333 — direct background-coordinate registration audit

_Status: completed negative structural test, 30 Sep 2026._

## Question

The solved background images already provide an independent physical 3x3 coordinate system:

```
I A B
C D E
F G H
```

Experiment 332 shows that the frozen row-selector family also produces a 3x3 coordinate, plus a binary exceptional-symbol polarity.

The cheapest possible linkage is therefore:

> perhaps the foreground token's 3x3 coordinate is just the sticker background's 3x3 coordinate, possibly after one global rotation/reflection.

This is an attractive way the background image could "sort" the code, so it should be tested before inventing more elaborate uses of the artwork.

## Result: impossible as direct coordinate copy

Four row-family tokens are already fixed by physical observations:

```
B = (2,2, dash)
C = (2,1, slash)
E = (0,0, slash)
I = (2,1, dash)
```

C and I occupy **different physical background cells**:

```
C background = (1,0)
I background = (0,0)
```

but their frozen foreground token coordinate is identical:

```
C token coordinate = (2,1)
I token coordinate = (2,1)
```

They differ only in the binary exceptional-symbol polarity.

Therefore no injective map from the nine background coordinates to the nine foreground token coordinates can satisfy the already-fixed C and I observations. This rules out not merely D4 but **any one-to-one coordinate relabeling**.

For completeness, all eight D4 transforms of the physical `IAB/CDE/FGH` layout were tested against every class's observation-compatible token-coordinate set. **0/8 survive.**

## Interpretation

The solved background 3x3 cannot simply be copied, rotated, or reflected into the row-selector's 3x3 coordinate.

This is useful because it blocks an easy but seductive fusion of two independently present 3x3 structures.

It does **not** rule out the background layer as:

- an ordering cue;
- a mask;
- a transform key;
- an orientation signal more complex than coordinate copy;
- a source of a second family/mode;
- artwork whose collective image must be processed before being applied to the foreground.

Those possibilities still require independent evidence.

The C/I collision also explains why the binary layer matters: the complete 3x3x2 tokens remain distinct even though their 3x3 coordinates coincide.

## Consequence

Do not use the physical A-I coordinate itself as the missing Pigpen/grid mapping. Any connection between background artwork and the foreground token must carry more information than a global 3x3 coordinate transform.

This reinforces Experiment 319's warning that background geometry and within-class body positions inhabit different indexing domains.

## Reproducibility

```bash
python scripts/audit_background_token_coordinate.py
```
