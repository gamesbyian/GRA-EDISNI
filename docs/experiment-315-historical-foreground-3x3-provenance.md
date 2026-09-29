# Experiment 315 — historical foreground 3×3 framing provenance

_Date: 2026-09-29_

## Question

Was the present project's decomposition of the 108-symbol foreground into twelve physical 3×3 frames a hindsight-only modeling move, or did the public community independently consider that geometry before the current machine reconstruction?

This experiment is historical/provenance work only. It does not use old community speculation as evidence that POS3, Q4 selector semantics, recursion, or terminal `100` are correct.

## Source

Public Discord export:

- repository: `gamesbyian/playdead-unofficial-exports`
- inspected commit: `5e5897e2ce70dad5a2bd85e459770637cb36610f`
- channel: `ARG / solving`
- channel ID: `461275582970462209`

The export preserves exact message IDs and attached images.

## 2022: the twelve-frame decomposition is already present

On **22 Dec 2022**, the discussion is explicitly using a 12×9 foreground rendering. In the message group anchored at:

`1055674055233118248`

a solver says:

> “I tried doing a 3x3 grid for each row but got nothing”

A 12×9 rendering has twelve nine-cell rows, so applying one 3×3 grid to each row is exactly the present project's **twelve 3×3 frame** decomposition. The attempt produced no semantic result, which is useful anti-hindsight evidence: the geometry was available long before the present mechanism, but the later local positional grammar had not been recognized.

On **23 Dec 2022**, message:

`1055973624135295086`

adds that in the 12×9 representation “each column corresponds to symbols with one of the 9 patterns.” In context, the community was already using the period-9 physical/background cadence to motivate the 12×9 registration, again without discovering the later machine.

## 2023: twelve 3×3 blocks stated explicitly

On **12 Oct 2023**, message:

`1162212809568964608`

states:

> “if you put them into 3x3 grids such that they would complete the nine piece puzzle, you get these twelve squares”

The attached rendering uses:

- slash = red;
- dash = blue;
- dot = orange;
- unknown = black.

The important historical fact is not whether that rendering solved anything. It did not. The important fact is that a solver independently connected:

1. the already-solved nine-piece physical sticker background;
2. the 108-cell foreground;
3. a decomposition of that foreground into **twelve 3×3 blocks**.

This restates and makes visually explicit the December-2022 decomposition. Both predate the present typed-machine reconstruction by years.

## 2026: 9×12 and alphabet split sharpen the same geometry

On **10 May 2026**, message:

`1502960920568135761`

argues for a 9×12 rendering because the first 81 cells form a 9×9 slash/dash region and the final 27 form three rows of slash/dot cells. It explicitly observes:

> “This way image could be twelve 3x3 squares, 9 is with "/" and "-", and 3 is with "." and "-".”

The archive then contains an attachment named:

`twelve_3x3_squares.png`

in the immediately following discussion.

This is stronger historical provenance than a generic “108 has factors 9 and 12” observation. It combines the exact **81+27 alphabet boundary** with the already-known 3×3 A–I physical carrier.

## What this upgrades

The present human-solve reconstruction uses:

`108 = 12 × 9`

and registers every nine consecutive foreground residues against the physical A–I layout:

```
I A B
C D E
F G H
```

Experiment 302 already established the physical A–I registration historically.

Experiment 315 now establishes that applying **3×3 framing to the foreground itself** was independently proposed in the historical community by December 2022, including the exact twelve-block decomposition, and was later restated explicitly as twelve 3×3 squares.

Therefore the human-plausibility classification can be sharpened:

- the A–I 3×3 carrier: historically solved and source-recovered;
- the 108 → twelve 3×3 foreground framing: historically attested exploration by Dec 2022 and stated explicitly as twelve squares by Oct 2023;
- the 81+27 → nine primary-like blocks plus three tail blocks split: explicitly articulated by May 2026;
- the later POS3 occupancy grammar, Q4 selector interpretation, recursive address substitution, route shell, and terminal `100`: still present-project deductions.

## What this does not upgrade

The 2023/2026 community geometry did **not** establish:

- one-exception-per-column POS3;
- the primary polarity staircase;
- slash-as-selector-depth code;
- `(q,d,j) -> (q,S(j),j)`;
- `120/012/102`;
- `210`;
- the `14 -> 3 -> 1` collapse;
- terminal `100`.

No old screenshot or message should be counted as an independent statistical validation of those later deductions because it uses the same physical sticker corpus.

## Consequence

Move the “twelve 3×3 foreground frames” step in the human-solve narrative from a merely hindsight-plausible factorization to a historically attested geometric move.

This reduces the discovery burden at the front of the present mechanism without changing any machine theorem or observation.

The next archival question is narrower: whether any pre-current-reconstruction message explicitly noticed the **within-frame column exceptional-position structure**. A positive hit would affect the provenance of POS3 itself; generic 3×3 visual experiments would not.
