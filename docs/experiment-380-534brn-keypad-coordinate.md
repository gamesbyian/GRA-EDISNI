# Experiment 380 — the 534brn tercile map is the historical DTMF-keypad row coordinate

_Status: completed bounded external-consumer audit, 2 Oct 2026._

Experiment 379 left three uncued choices in the otherwise exact Experiment-378 hit:

1. arrange the nine URL digits as a 3×3;
2. reduce decimal values by `1–3→0, 4–6→1, 7–9→2`;
3. rotate 90° counter-clockwise.

The second choice now has an independent historical interpretation.

## The historical cue predates the machine

On 22 May 2026, the sticker discussion explicitly proposed an **old telephone / DTMF keypad** as a model for the sticker puzzle. A DTMF keypad image was attached.

The standard layout shown in that archived image is:

```
1 2 3
4 5 6
7 8 9
```

This predates the current POS3/G5 machine work.

Therefore the Experiment-378 reduction:

```
1 2 3 -> 0
4 5 6 -> 1
7 8 9 -> 2
```

has a much less ad-hoc interpretation:

> it is simply the **row coordinate** of a historically proposed 3×3 keypad.

## The useful control: keypad column

A keypad supplies two equally immediate ternary coordinates:

- row;
- column.

For the independently sticker-derived URL digits:

`534965398`

the keypad coordinates are:

### Row coordinate

```
5 3 4   ->   1 0 1
9 6 5        2 1 1
3 9 8        0 2 2
```

or `101 / 211 / 022`.

Under D4 square symmetries, exactly one orientation hits the six-state one-shot family:

```
112 / 012 / 120
```

the same Experiment-378 hit.

### Column coordinate

The equally natural keypad column stream is:

`120 / 221 / 221`

Under all D4 symmetries, it produces **zero** one-shot-family hits.

That discrimination is important. The historical keypad cue does not merely create a large new transform family in which something happens to fit. Of the two native ternary coordinates supplied by the cue, the row coordinate is the one that hits; the column coordinate does not.

## Epistemic effect

Experiment 378's decimal-to-ternary step should no longer be described merely as an “equal-tercile numeric binning.”

It is exactly the row coordinate of an independently proposed sticker-puzzle keypad.

This upgrades one of the three remaining registration choices from uncued to **historically licensed operation-level evidence**.

It still does not prove authorial intent. The May-2026 keypad discussion was a community hypothesis, not a Playdead instruction.

## What remains

Two questions remain before the `534brn` hit can be promoted beyond active candidate:

- Why should the nine URL digits be registered into the nine cells in string/read order?
- Why should the resulting 3×3 be rotated specifically 90° counter-clockwise?

The first has some source-side plausibility because the URL comes from a solved nine-piece 3×3 sticker background puzzle, but the digit-to-cell correspondence is not explicitly documented.

The second is now the sharpest free parameter.

A 90° rotation is a demonstrated INSIDE ARG operation in the solved Xbox printer puzzle, but cross-puzzle precedent licenses the operation family, not the direction. That should be recorded separately rather than silently counted as confirmation.

## Guardrail

Do not test arbitrary keypad functions, telephone texting, DTMF frequencies, or other digit encodings.

The exact historical cue tested here supplies only keypad **row and column position**. Those two coordinates have now been exhausted.
