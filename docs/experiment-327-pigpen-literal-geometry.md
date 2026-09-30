# Experiment 327 — literal-stroke Pigpen compatibility audit

_Status: completed bounded negative test, 30 Sep 2026._

## Question

If the foreground marks are taken **literally as drawn strokes**, can a nine-cell slash/dash body become one ordinary Pigpen-style glyph using only the preregistered D4 symmetries (90-degree rotations and reflections)?

This is deliberately narrower than "is there some Pigpen-related encoding?" It tests the cheapest literal-symbol reading before introducing a categorical codebook.

## Geometry

Under D4 symmetries:

- a dash can become horizontal or vertical, but stays in the orthogonal orientation family;
- a slash can become either diagonal, but stays in the diagonal orientation family.

A standard Pigpen-style alphabet has two geometric glyph families:

- tic-tac-toe/grid cells made from orthogonal strokes;
- X-grid cells made from diagonal strokes.

Dots distinguish paired alphabets in the familiar construction, but do not make one glyph mix the two stroke-orientation families.

Therefore a body containing both literal slash and dash strokes cannot, by D4 transformation alone, become one standard Pigpen glyph.

## Observation-only result

Every one of the nine A-I body traces already has at least one physically observed slash **and** at least one physically observed dash:

| class | body observation trace | observed / | observed - |
|---|---|---:|---:|
| A | `?--?-/???` | 1 | 3 |
| B | `/?//////-` | 7 | 1 |
| C | `---///-/-` | 4 | 5 |
| D | `-/?-/???/` | 3 | 2 |
| E | `/--/??/??` | 3 | 2 |
| F | `?/-?/-///` | 5 | 2 |
| G | `/???/??-/` | 3 | 1 |
| H | `?/-?--?-/` | 2 | 4 |
| I | `/-?/??/-/` | 4 | 2 |

So the direct "both printed marks are the strokes of one Pigpen glyph" interpretation is incompatible with the observed corpus for **9/9 classes**. Unknown cells cannot repair that, because the mixed orientation is already observed.

## What survives

This does **not** kill the broader geometric-alphabet idea. Several materially different interpretations remain possible:

1. one body symbol is ink/edge and the other means empty/background;
2. slash and dash are categorical states that first pass through a fixed transform into edges;
3. the nine body cells define a grid, mask, or address rather than directly drawing the final glyph;
4. the three-cell tail selects a row/column/cell or geometric subfamily;
5. the collective 9x9 body, rather than each individual class body, is the geometric object.

Those alternatives require an extra rule. The rule must come from sticker structure, historical solver provenance, another ARG artifact, or a preregistered minimal family. It cannot be chosen because a resulting letter looks attractive.

## Tail mismatch worth preserving

The one-slash tail supported by Experiment 317 is naturally a **three-way** positional value. Classic dotted/undotted Pigpen distinction is binary. Therefore mapping the entire three-cell tail merely to "dot/no dot" would discard one native state unless an independent rule explains the collapse.

That makes "tail chooses one of three cells/rows/rails" a cleaner structural fit than "tail is just Pigpen's dot bit", though neither interpretation is established.

## Consequence

Close the most literal Pigpen reading. Keep the wider **9 body = geometry / 3 tail = selector** family active.

Next useful tests are:

- observation-only renderer with explicit unknowns and actual slash/dash strokes;
- one-symbol-as-edge alternatives, but only under a fixed global rule;
- selector-conditioned row/column extraction;
- independently measured background-art geometry as a possible source of the missing transform.

## Reproducibility

```bash
python scripts/audit_pigpen_literal_geometry.py
```
