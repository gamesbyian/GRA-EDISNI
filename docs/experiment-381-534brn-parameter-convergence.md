# Experiment 381 — parameter convergence around the 534brn one-shot hit

_Status: completed provenance synthesis, 2 Oct 2026._

Experiment 378 initially looked like an exact but three-parameter coincidence:

1. make a 3×3 from the nine URL digits;
2. map `1–3 / 4–6 / 7–9` to ternary `0/1/2`;
3. rotate 90° counter-clockwise.

After Experiments 379–380 and a fresh historical replay, that framing is now too pessimistic.

Each step has **independent pre-machine operation-class provenance**.

## 1. Why a 3×3 at all?

The digits do not come from an arbitrary string elsewhere in the ARG.

They come from the solution to the **nine-piece CE background puzzle**, whose canonical physical carrier is itself a 3×3:

```
I A B
C D E
F G H
```

Then, independently in November 2025, community solvers explicitly noticed that the solved path contains **nine digits** and proposed that those nine numbers might aid the nine sticker sections.

So the 3×3 carrier shape is not being imported after seeing the one-shot target.

What remains free is narrower:

> why map digit-string ordinal 1..9 to 3×3 cell ordinal 1..9 in reading order?

That exact registration is still not documented.

## 2. Why `1–3 / 4–6 / 7–9`?

Experiment 380 resolves this much more strongly.

On 22 May 2026, before the current machine work, the sticker discussion explicitly proposed a **DTMF / old-phone keypad** and attached the standard:

```
1 2 3
4 5 6
7 8 9
```

The Experiment-378 transform is exactly the keypad's **row coordinate**.

This is not merely “equal thirds” anymore.

Even better, the same keypad supplies an equally natural alternative ternary coordinate: **column**.

For `534965398`:

- keypad row → `101 / 211 / 022` → one D4 hit, `112 / 012 / 120`;
- keypad column → `120 / 221 / 221` → **zero** D4 hits.

So the historical keypad cue selectively supports the successful coordinate rather than opening an unconstrained transform buffet.

## 3. Why rotate?

The exact direction is still not independently fixed, but the operation family is no longer alien.

The solved Xbox printer puzzle demonstrably requires a **90-degree rotation** before its Braille layer is read. That is a Playdead-authored precedent for a quarter-turn between registered carrier and secondary readout.

Separately, on 2 Nov 2025, while discussing the sticker foreground and the `534brn` solution, lime8159 explicitly wondered whether the sticker puzzle should be **transposed similar to the 534brn puzzle**.

Neither source tells us “rotate this new keypad-row grid 90° counter-clockwise.” So the direction remains a real free parameter.

But a rigid reorientation of a registered grid now has both solved-ARG and sticker-specific historical provenance.

## Revised status

The three Experiment-378 operations should now be classified as:

| step | old description | revised status |
|---|---|---|
| 3×3 carrier | uncued | source-side 9-piece/9-digit carrier strongly motivated |
| decimal→ternary | uncued equal terciles | exact historical DTMF **row coordinate**; alternative column coordinate fails |
| quarter-turn | uncued D4 choice | 90° rotation is Playdead-demonstrated; exact CCW direction remains uncued |

This is a material upgrade.

## What still blocks promotion

Two exact parameters remain unresolved:

1. **ordinal registration:** digit 1st→cell 1st, 2nd→2nd, ... in 3×3 reading order;
2. **turn direction:** why the successful quarter-turn is CCW rather than CW.

Those are now the highest-value evidence targets.

The candidate should not be called solved until at least one is fixed independently and the other is correspondingly reduced or explained.

## Guardrail

Do not compensate for the remaining uncertainty by testing:

- arbitrary digit permutations;
- arbitrary keypad functions;
- letter portions of the URL as extra keys;
- nonlinear numeric maps;
- semantic interpretations of `112/012/120`.

The present candidate is strong precisely because its operation family is becoming externally constrained. Preserve that advantage.
