# Experiment 361 — literal Xbox envelope transfer to H108

_Status: completed bounded historical-mechanism test, 2 Oct 2026._

## Why this test exists

Experiment 360 showed that optimizing sticker row order by generic same-symbol continuity does not improve held-out sticker prediction. That leaves one much better-motivated ordering question: can the **actual ordering mechanism used in the solved Xbox printer puzzle** transfer to the sticker rows?

The preserved 30 Jun 2018 Discord reconstruction is unusually explicit. Solvers observed that:

- the slash characters formed the visible outer dome/circle;
- for correctly placed rows, the first slash from the left was mirrored at the same position from the right;
- dashes filled the exterior/background;
- dots and dashes inside the slash envelope were treated as payload;
- row order was adjusted to preserve a smooth boundary/staircase rather than to maximize payload similarity.

This experiment tests only that literal structural premise. It does not search for a new sticker-specific rule.

## Frozen literal envelope

For a row of width `W`, choose an envelope depth `k` from the left edge.

The historical mechanism requires:

- cell `k` is slash;
- cell `W-1-k` is slash;
- every cell outside those two boundary positions is dash;
- cells inside the boundary are unrestricted payload.

Unknown sticker cells remain unknown and may take whatever value is necessary.

This is intentionally generous. It does **not** require:

- a unique depth;
- smooth depth progression across rows;
- a circle/dome;
- no extra interior slashes;
- any semantic image.

A row is rejected only if **no** mirrored slash-envelope depth can accommodate its physically observed cells.

## Formats tested

The same observed H108 corpus is tested in the two obvious rectangular views:

1. `12×9`: twelve consecutive 9-residue sequence rows;
2. `9×12`: nine A-I class traces.

No model-filled cells are used.

## Results

### 12×9

Observed rows and compatible envelope depths:

| row | trace | compatible k |
|---:|---|---|
| 1 | `?/--/?/?/` | 0 |
| 2 | `-?-/-/?/-` | 1 |
| 3 | `-/-?--?-?` | none |
| 4 | `?//-/???/` | 0 |
| 5 | `-///?//-?` | none |
| 6 | `///??-?-?` | 0 |
| 7 | `?/-?//??/` | 0 |
| 8 | `?//??/---` | none |
| 9 | `?--/?////` | 0 |
| 10 | `???./??..` | none |
| 11 | `?.??./..?` | 0 |
| 12 | `?/??????/` | 0 |

Only **8/12** rows are compatible. Even restricting to the first nine slash/dash rows, **3/9** rows fail before the tail is considered.

### 9×12

| class trace | trace | compatible k |
|---|---|---|
| A | `?--?-/??????` | 0,3,5 |
| B | `/?//////-?./` | 0 |
| C | `---///-/-???` | none |
| D | `-/?-/???/.??` | 1 |
| E | `/--/??/??/.?` | 0 |
| F | `?/-?/-///?/?` | 0,1 |
| G | `/???/??-/?.?` | 0 |
| H | `?/-?--?-/..?` | 0 |
| I | `/-?/??/-/.?/` | 0 |

Only **8/9** class traces are compatible; class C is already impossible.

## Interpretation

The literal Xbox ordering channel does not transfer to either sticker layout.

This matters because it closes the strongest historically grounded version of “sort the sticker rows like the printer puzzle.” The failure occurs before any visual fitting or optimized order is attempted:

- the 12×9 body already contains rows incompatible with a slash boundary / dash exterior;
- the 9×12 transpose also contains an incompatible class trace;
- therefore no row permutation can rescue the literal envelope rule, because permutation changes row order but not the incompatible contents of each row.

The broader lesson from the printer puzzle still survives: Playdead has used one symbol layer as registration structure and another as payload. But the stickers do not reuse the Xbox registration grammar verbatim.

Future ordering work should therefore require one of:

1. an independently evidenced **different** sticker-native registration feature;
2. an archival source describing a distinct sticker-specific ordering operation;
3. a preregistered operation derived from another solved INSIDE puzzle, followed by blind predictive validation.

Do not soften the Xbox rule post hoc by changing boundary symbol, exterior symbol, row width, or cyclic offset merely to make H108 fit. Those would be new hypothesis families.

## Historical provenance

Primary archived discussion:

- Playdead Unofficial Discord, ARG / solving, 30 Jun 2018, especially 16:24–18:10 local export timestamps.
- Preserved in `gamesbyian/playdead-unofficial-exports`, `Playdead Unofficial - ARG - solving [461275582970462209].txt`.

Key operational statements recovered there include the mirrored first-slash criterion, the slash dome as ordering structure, dash exterior/background, and explicit row moves to smooth the boundary.

## Reproducibility

Run:

```bash
python scripts/audit_xbox_envelope_transfer.py
```

The script writes `data/experiment-361-xbox-envelope-transfer.json`.
