# Experiment 405 — native class-word Morse is also a hard negative

_Status: completed bounded Morse replay, 4 Oct 2026._

Experiment 404 closed ordinary serial-order Morse with slash separators.

A fair objection is that the sticker foreground has a much stronger native representation than one flat 108-character line:

```
9 classes × 12 positions
```

The game assets themselves use names such as `MORSE_Dot`, `MORSE_Dash`, and `MORSE_Slash`, while historical solvers explicitly wondered whether slash separated Morse letters or words.

So test the obvious rearranged version before closing the lane.

## Frozen family

For each of the nine A-I class words:

- preserve its native 12-position order;
- slash is the separator;
- remaining dash/dot marks become Morse dot/dash;
- test both polarities;
- accept International Morse A-Z and 0-9.

No permutation of classes or positions is needed for this test.

## Result

Across:

```
648 U2 completions
×
2 Morse polarities
```

completions in which all nine class words parse legally:

```
0
```

The failure is again completely local and invariant.

Class H is identical in every U2 completion:

```
-/------/../
```

Splitting on slash gives:

```
-
------
..
```

The middle token always contains six marks.

Under either polarity it becomes six dots or six dashes.

Neither is an A-Z Morse letter or a decimal Morse digit.

## Consequence

The two cheapest Morse carriers are now closed:

1. flat serial H108 order;
2. native 9×12 class-word order.

Both fail because of model-independent long-token witnesses.

That makes “the symbols are called Morse in the game assets” useful historical context, but not a decoder for the CE foreground under the natural registrations.

## Reopening trigger

Do not try additional sticker rearrangements merely to make Morse legal.

Reopen only if an external source supplies the traversal or grouping.
