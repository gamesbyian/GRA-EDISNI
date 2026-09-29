# Minimum primary verification witness

_Status: Experiment 259 support artifact._

This is the exact minimum set of **distinct observed primary H108 residues** that preserves the full Experiment-246 raw reconstruction once the H108/POS3 representation is being tested:

- 8 of 9 frame polarities remain uniquely forced with polarity initially free;
- 25 of 27 primary ternary payload cells remain uniquely forced under the `d<=q` polarity staircase.

The minimum contains **34 residues** and is unique under the exact per-frame subset search.

This is a **verification witness**, not a claim that a human could discover H108 or POS3 from these 34 marks alone.

## Physical layout

A–I physical positions:

```
I A B
C D E
F G H
```

## Minimum witness by frame

| q | d | Minimum residues | Observed marks in residue order |
|---:|---:|---|---|
| 0 | 0 | 2, 3, 4, 5 | B=/, C=-, D=-, E=/ |
| 0 | 1 | 12, 13, 17, 18 | C=-, D=/, H=/, I=- |
| 0 | 2 | 20, 21, 24 | B=/, C=-, F=- |
| 1 | 0 | 29, 30, 31, 32, 36 | B=/, C=/, D=-, E=/, I=/ |
| 1 | 1 | 37, 39, 42, 44 | A=-, C=/, F=/, H=- |
| 1 | 2 | 46, 47, 48 | A=/, B=/, C=/ |
| 2 | 0 | 56, 57, 59 | B=/, C=-, E=/ |
| 2 | 1 | 66, 69, 70, 71 | C=/, F=/, G=-, H=- |
| 2 | 2 | 74, 75, 76, 79 | B=-, C=-, D=/, G=/ |

Global residue tuple:

```
2,3,4,5,
12,13,17,18,
20,21,24,
29,30,31,32,36,
37,39,42,44,
46,47,48,
56,57,59,
66,69,70,71,
74,75,76,79
```

## What each frame minimum means

The frame minima are independent for this reconstruction problem. Each listed subset is the unique smallest subset of observed residues in that frame that preserves:

1. every ternary column value that the full public corpus forces in that frame under the established staircase; and
2. the frame-polarity conclusion when the full corpus forces one.

Minimum sizes by frame are:

```
q0: 4, 4, 3
q1: 5, 4, 3
q2: 3, 4, 4
```

Total: `34`.

## Human-use recommendation

For a human-facing view, do **not** begin by displaying the solved ternary digits. Show these 34 raw slash/dash observations grouped only by the already-motivated H108 quarter/depth frame and physical A–I cell.

Useful staged reveal:

1. show the nine sparse 3×3 frames with only these observed marks;
2. invite the viewer to infer which symbol is the minority pulse in each frame;
3. reveal the eight forced frame polarities;
4. then show the forced minority-row positions column by column;
5. only afterward overlay the compact ternary lattice.

This keeps the visual evidence ahead of the solved notation and makes it possible to judge whether POS3 is genuinely conspicuous rather than merely easy to understand in hindsight.

## Caveat

The 34-residue optimum is conditional on the current representation family. It does not establish that 34 is the smallest corpus from which a fresh solver could independently discover:

- period 108;
- the q/d/j address factorization;
- the physical A–I layout;
- the polarity staircase;
- POS3 itself.

Those are earlier discovery problems and should be tested separately.
