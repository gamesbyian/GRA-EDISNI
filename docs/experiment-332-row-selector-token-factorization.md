# Experiment 332 — 3×3×2 token factorization of the frozen row-selector family

_Status: completed structural factorization, 30 Sep 2026._

## Question

The original Pigpen suggestion was attractive because it combines a 3x3 spatial grid with a secondary distinction. The frozen Experiment-329 row family now supplies a concrete way to ask what information such a reading would actually carry, without choosing letters.

For each class:

1. the one-slash tail chooses one of three body rows;
2. the selected row has one exceptional mark;
3. the position of that exception chooses one of three columns;
4. the exceptional mark itself is either slash or dash.

That gives a native token:

```
(row, column, exceptional-symbol)
```

with cardinality:

```
3 × 3 × 2 = 18
```

## Observation-only token uncertainty

Exhausting only physically compatible completions gives:

| class | possible 3×3×2 tokens |
|---|---:|
| A | 9 |
| B | **1** |
| C | **1** |
| D | 5 |
| E | **1** |
| F | 2 |
| G | 5 |
| H | 2 |
| I | **1** |

Four classes are already completely determined under the frozen family:

```
B = (row 2, column 2, exceptional dash)
C = (row 2, column 1, exceptional slash)
E = (row 0, column 0, exceptional slash)
I = (row 2, column 1, exceptional dash)
```

C and I are particularly neat structurally: they occupy the same 3x3 coordinate and differ only in the binary exceptional-symbol layer.

## Pigpen relationship

This is the first version of the Pigpen idea with exact dimensional bookkeeping rather than visual resemblance.

The ordinary tic-tac-toe portion of a Pigpen alphabet consists of two 3x3 grids:

```
9 positions × 2 variants = 18 symbols
```

The frozen row family independently exposes exactly the same abstract carrier size:

```
9 spatial coordinates × 2 exceptional-symbol polarities = 18 tokens
```

So there is a clean **isomorphism in carrier structure** between the row-selector code and Pigpen's two 3x3-grid families.

That does not establish the conventional Pigpen alphabet mapping. No letters have been assigned here.

## Important limitation

A standard 26-letter Pigpen alphabet also needs the two X-grid families for the remaining eight letters.

The current row-selector carrier has only 18 states. Nothing in the frozen rule supplies an independent grid-vs-X family bit or an additional 8-state carrier.

Therefore:

> the current 3x3x2 mechanism could naturally model the 18-symbol tic-tac-toe half of Pigpen, but it is **not by itself a complete 26-letter Pigpen alphabet**.

A full Pigpen claim now needs an independently evidenced second geometric family. Inventing one to obtain S-Z would be overfitting.

## Why this matters

This sharply separates two ideas that had been bundled together:

- **3x3 spatial code + binary layer:** now concretely supported as a structural description of the frozen row-selector family;
- **standard Pigpen alphabet:** still unestablished.

The useful next question is whether another sticker-native or ARG-native feature supplies a genuine second family/mode, not whether one can visually massage the 18 tokens into letters.

## Reproducibility

```bash
python scripts/audit_row_selector_token_factorization.py
```
