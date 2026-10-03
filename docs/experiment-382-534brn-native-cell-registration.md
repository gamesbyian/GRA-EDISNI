# Experiment 382 — native serial geometry fixes the 534brn digit-to-cell registration

_Status: completed bounded registration audit, 2 Oct 2026._

Experiment 381 left two exact free parameters behind the `534brn` one-shot hit:

1. why digit-string ordinal should map directly to the nine 3×3 cells;
2. why the successful quarter-turn should be counter-clockwise.

The first of those is now much less free than it appeared.

## The solved CE background already numbers its 3×3

The canonical solved background layout is:

```
I A B
C D E
F G H
```

The community labels A-I are arbitrary names assigned after discovery.

But the sticker serial numbers themselves supply a native modulo-9 coordinate:

```
serial mod 9 = 0  1  2  3  4  5  6  7  8
class          I  A  B  C  D  E  F  G  H
```

Therefore the solved physical 3×3 is exactly:

```
0 1 2
3 4 5
6 7 8
```

in row-major order.

This is not reconstructed from the current machine. It is a property of the solved nine-piece background puzzle plus sticker serial numbering.

There is even explicit historical support. On 10 Aug 2026, eropkol noted that the first class should probably be `000 = I`, not `001 = A`, specifically because I is the top-left tile of the first sticker puzzle.

## Consequence for the nine URL digits

The sticker-background solution produces the nine-digit sequence:

`534965398`

If those nine ordered digits are associated with the nine native serial classes `0..8`, their physical placement is automatically the solved row-major 3×3.

Applying the independently licensed DTMF-row coordinate then gives:

```
1 0 1
2 1 1
0 2 2
```

This is exactly the Experiment-378 input grid.

So the controversial step is no longer:

> “take a string and arbitrarily pour it into a 3×3.”

It can instead be stated:

> associate the nine ordered values with the nine native serial residue classes, whose solved physical positions are already 0..8 row-major.

That is a much cleaner registration.

## Control: community alphabetic order

There is another obvious ordering one might have used: assign the digits to the community labels `A,B,...,I` and then render them in the solved physical layout `IAB/CDE/FGH`.

That produces keypad-row grid:

```
2 1 0
1 2 1
1 0 2
```

or `210/121/102`.

Under all eight rigid symmetries of the square, that control produces **zero** hits on the six Experiment-374 one-shot states.

The native serial-modulo-9 registration produces the unique known hit.

## Epistemic effect

The digit-ordinal→cell parameter should be downgraded from a substantive free transform to a **native registration choice with independent physical/historical support**.

There is still one semantic assumption:

> the nine URL digits are intended to be associated in sequence with the nine native background classes.

The Nov-2025 community observation that the nine digits might aid the nine sticker sections supports that operation class, but does not prove Playdead intended it.

Still, the geometry no longer needs to be invented.

## Remaining bottleneck

The dominant unresolved parameter is now the quarter-turn:

```
101 / 211 / 022
    ↓ 90° CCW
112 / 012 / 120
```

Experiment 381 already establishes that 90° reorientation is a demonstrated INSIDE ARG operation family and that transposition was independently discussed around `534brn`.

What is still missing is an independent reason for the **specific direction/orientation**.

That is now the cleanest falsification target in this lane.
