# SR-03 pilot: repeated-label routing instead of nine-tile permutation

9 October 2026. First executable pilot of the [36-candidate speculative revival portfolio](speculative-revival-portfolio-2026-10-09.md).

The physical CE background mosaic is linked to the path dat/534brn9653f9j8mmd. The full path was partially read from the artwork, then matched against a website index in April 2020 (Experiment 465). It contains **exactly nine decimal digits in order: 534965398**.

Under the direct keypad map 1–9, these are **not** nine different destinations:

| Digit class | Occurrences | Index type |
| --- | ---: | --- |
| 3, 5, 9 | Twice each | Three repeated destinations |
| 4, 6, 8 | Once each | Three singleton destinations |
| 1, 2, 7 | None | Three absent destinations |

Thus nine values address **six unique targets**, and any theory treating the digits as an ordinary nine-cell *permutation* must introduce an additional disambiguating rule. It is more economical to keep the collisions and test whether they are intended **revisit/overlay/repeated-transmission** instructions.

The source-fixed original 3×3 background layout is:

    I A B
    C D E
    F G H

A strict 1–9 phone keypad offers row and column addresses for each digit, but the URL does **not** independently tell us which of the eight D4 physical orientations to choose, whether read positions and target positions both refer to this board, what should happen when a target is visited twice, or which output receives the resulting six-target route.

The [source-only prototype](../scripts/speculative_url_keypad_collision_pilot.py) verifies the nine digits, six targets, 3+3 repeated/singleton partitions, native keypad coordinates, and all eight unique physical rotations/reflections. It does **not** read sticker foreground symbols or fit any missing H108 cells.

## What to do next

Specify at most three operation families before scoring any H108 output: (a) ordinary revisit/update, (b) repeated-address XOR/toggle, (c) repeated-address selection with a second independent symbol. Each must have the same baseline and fixed physical orientation convention. If all three remain underdetermined, do not call it a decoder.

Most importantly, test the source-native domain mismatch identified by Experiment 319: a URL digit may refer to a physical **background tile** (nine possible classes), but the nine positions of a *single class's body word* are **time/serial occurrences**, not background classes. The literal physical IAB/CDE/FGH coordinates cannot be silently assigned to occurrence slots.

**Status:** genuine, source-fixed address collisions; no evidence yet that they are an intended foreground operation or a six-address endgame.
