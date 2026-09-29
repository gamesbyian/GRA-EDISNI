#!/usr/bin/env python3
"""Experiment 246: reconstruct primary constraints directly from raw observations.

This audit assumes only the primary POS3 column grammar, then first leaves each
frame's polarity free:
    minority symbol in a frame is either dash or slash.

It asks:
  1. which of the 9 frame polarities are forced by the classified corpus?
  2. after applying the current global polarity rule (minority dash iff d<=q),
     which of the 27 primary payload trits remain unresolved?
  3. does the outer no-self rule add information, or is it already a
     consequence of the corpus under that polarity?

No current payload lattice values are used as search targets.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "observations.csv"

SERIAL_ORDER = "ABCDEFGHI"
PHYSICAL_POSITION = {
    "I": (0, 0),
    "A": (0, 1),
    "B": (0, 2),
    "C": (1, 0),
    "D": (1, 1),
    "E": (1, 2),
    "F": (2, 0),
    "G": (2, 1),
    "H": (2, 2),
}


def load_primary_observations():
    by_column = defaultdict(list)
    with OBSERVATIONS.open(newline="", encoding="utf-8") as fh:
        for record in csv.DictReader(fh):
            residue = int(record["residue"])
            if residue > 81:
                continue

            offset = residue - 1
            q = offset // 27
            d = (offset % 27) // 9
            j = offset % 9
            row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
            by_column[(q, d, col)].append(
                (row, record["symbol"], residue, int(record["serial"]))
            )
    return by_column


def predicted_symbol(row: int, minority_row: int, minority_is_dash: bool) -> str:
    on_minority = row == minority_row
    if on_minority:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def allowed_rows(observations, q: int, d: int, col: int, minority_is_dash: bool):
    allowed = []
    for minority_row in range(3):
        if all(
            predicted_symbol(row, minority_row, minority_is_dash) == symbol
            for row, symbol, _residue, _serial in observations[(q, d, col)]
        ):
            allowed.append(minority_row)
    return tuple(allowed)


def main() -> None:
    observations = load_primary_observations()

    # First leave polarity free independently in each 3x3 frame.
    frame_options = {}
    for q in range(3):
        for d in range(3):
            options = []
            for minority_is_dash in (False, True):
                columns = tuple(
                    allowed_rows(observations, q, d, col, minority_is_dash)
                    for col in range(3)
                )
                if all(columns):
                    options.append((minority_is_dash, columns))
            frame_options[(q, d)] = tuple(options)

    forced_polarity = {
        frame: options[0][0]
        for frame, options in frame_options.items()
        if len(options) == 1
    }
    ambiguous_polarity = {
        frame: options
        for frame, options in frame_options.items()
        if len(options) != 1
    }

    assert len(forced_polarity) == 8
    assert set(ambiguous_polarity) == {(1, 2)}

    expected_forced = {
        (0, 0): True,
        (0, 1): False,
        (0, 2): False,
        (1, 0): True,
        (1, 1): True,
        (2, 0): True,
        (2, 1): True,
        (2, 2): True,
    }
    assert forced_polarity == expected_forced

    # The current global staircase agrees with every forced frame and chooses
    # slash-minority in the sole ambiguous frame q=1,d=2.
    for (q, d), value in forced_polarity.items():
        assert value == (d <= q)
    assert not (2 <= 1)

    # Now apply the staircase and reconstruct every payload trit directly.
    allowed = {}
    for q in range(3):
        for d in range(3):
            for col in range(3):
                allowed[(q, d, col)] = allowed_rows(
                    observations,
                    q,
                    d,
                    col,
                    minority_is_dash=(d <= q),
                )

    singleton = {key: rows[0] for key, rows in allowed.items() if len(rows) == 1}
    unresolved = {key: rows for key, rows in allowed.items() if len(rows) != 1}

    assert len(singleton) == 25
    assert unresolved == {
        (0, 2, 1): (1, 2),
        (2, 0, 1): (0, 1, 2),
    }

    # Every outer column is already forced by raw observations and every one
    # satisfies the no-self condition. It is therefore downstream of the
    # corpus + POS3 + chosen frame polarity, not an additional constraint.
    outer = {
        (q, d, col): allowed[(q, d, col)]
        for q in range(3)
        for d in range(3)
        for col in (0, 2)
    }
    assert len(outer) == 18
    assert all(len(rows) == 1 for rows in outer.values())
    assert all(rows[0] != d for (q, d, _col), rows in outer.items())

    print("Experiment 246")
    print("frame polarity from raw corpus under POS3:")
    for q in range(3):
        print(
            "  ",
            " ".join(
                (
                    "dash"
                    if frame_options[(q, d)][0][0]
                    else "slash"
                )
                if len(frame_options[(q, d)]) == 1
                else "ambig"
                for d in range(3)
            ),
        )

    print("OK: raw corpus forces 8/9 frame polarities")
    print("OK: sole ambiguous frame is q=1,d=2")
    print("OK: d<=q staircase matches all eight forced polarities")
    print("OK: with that polarity, raw corpus forces 25/27 primary trits")
    print("OK: unresolved trits are exactly x=(q0,d2,c1) and y=(q2,d0,c1)")
    print("OK: all 18 outer trits are forced and already satisfy row != depth")
    print("RESULT: outer no-self registration is derived, not an extra premise")


if __name__ == "__main__":
    main()
