# Experiment 377 — bounded Sudoku-house exact-cover test

_Status: completed historical-consumer audit, 2 Oct 2026._

A surprisingly specific historical proposal appears in the August 2026 sticker discussion.

The community independently noticed that ordinary Sudoku has:

- 81 cells;
- 27 houses;
- those houses split into 9 rows, 9 columns and 9 3×3 boxes.

That gives the same 81+27 split as the sticker foreground.

This is much stronger than a generic “maybe Sudoku” resemblance because the tail itself is three groups of nine positions. It therefore suggests a concrete interpretation:

> tail position 0/1/2 chooses one of three house families; A-I chooses house index 0..8.

That proposal predates Experiments 373–375 and is independent of the current machine.

## Cheapest falsifiable consequence

If the nine tail selectors choose nine Sudoku houses, the cleanest structural expectation is that the chosen houses form an exact cover of the 81-cell primary grid:

- nine houses;
- nine cells per house;
- every primary cell covered once;
- no overlaps and no gaps.

This requires no foreground plaintext or machine output.

Experiment 317 leaves exactly 36 observation-compatible one-slash tail assignments.

To avoid winning on a registration convention, the audit exhausts:

- all 6 mappings of tail positions 0/1/2 to row/column/box;
- both forward and reversed A-I house indexing;
- all 9 cyclic index offsets.

That is 108 registration families and 3,888 selector×registration combinations.

## Result

**Zero exact covers.**

The best case covers only 75 of the 81 cells, necessarily creating at least six duplicate incidences elsewhere.

So even after granting generous indexing freedom, no observation-compatible tail completion behaves as a selector choosing a mixed set of Sudoku houses that partitions the primary 81 cells.

## Interpretation

The historical Sudoku proposal remains interesting as an independently discovered **81+27 dimensional analogy**.

Its cheapest natural consumer, however, is dead.

That matters for G6 because Sudoku initially looked like a possible external bridge between two ternary levels. It does not supply one under the simplest exact-cover reading.

Do not widen into arbitrary Sudoku solving rules, digit assignments, clue generation, or visual scoring. Those would add large discretionary families after the clean structural test already failed.

## Consequence

The G6 repeat/cross-axis problem remains open.

The best-supported endpoint without a new cue is still Experiment 374's one-shot six-state object.
