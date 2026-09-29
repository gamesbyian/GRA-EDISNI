#!/usr/bin/env python3
"""Experiment 262: raw-first POS3 cue on the 34-residue minimum witness.

Use only the unique Experiment-259 witness and the natural presentation as
nine consecutive 9-residue frames (1-9, 10-18, ..., 73-81). Do not use q/d
labels, the compact ternary lattice, or the global d<=q staircase to select
frame polarity.

For each frame, test both possible exact-POS3 polarities and count compatible
payload completions.

Human-style local rule:
  * reject a polarity with zero exact-POS3 completions;
  * if both survive, prefer the polarity with fewer local completions.

Question: does that local determinacy rule recover the same nine frame
polarities as the established staircase?
"""

from __future__ import annotations

from functools import reduce
from operator import mul

from audit_primary_leave_one_out import allowed_rows, build_columns, load_rows


WITNESS = (
    2, 3, 4, 5,
    12, 13, 17, 18,
    20, 21, 24,
    29, 30, 31, 32, 36,
    37, 39, 42, 44,
    46, 47, 48,
    56, 57, 59,
    66, 69, 70, 71,
    74, 75, 76, 79,
)


def completion_count(columns, q, d, polarity):
    options = tuple(
        allowed_rows(columns, q, d, col, polarity)
        for col in range(3)
    )
    return reduce(mul, (len(values) for values in options), 1), options


def main() -> None:
    rows = [
        record
        for record in load_rows()
        if int(record["residue"]) in WITNESS
    ]
    columns = build_columns(rows)

    table = []
    for frame in range(9):
        q, d = divmod(frame, 3)
        slash_minority = completion_count(columns, q, d, False)
        dash_minority = completion_count(columns, q, d, True)

        viable = [
            (count, polarity, options)
            for polarity, (count, options) in (
                (False, slash_minority),
                (True, dash_minority),
            )
            if count > 0
        ]
        assert viable

        viable.sort(key=lambda item: (item[0], item[1]))
        best_count, best_polarity, best_options = viable[0]

        # No ties in local completion count on the minimum witness.
        if len(viable) > 1:
            assert viable[1][0] > best_count

        expected = d <= q
        assert best_polarity == expected

        table.append(
            (
                frame + 1,
                slash_minority[0],
                dash_minority[0],
                best_polarity,
                best_count,
                best_options,
            )
        )

    # Eight frames have only one viable polarity. The sole two-polarity frame
    # is frame 6 (q=1,d=2), where local determinacy is 1 versus 8.
    assert sum((slash > 0) + (dash > 0) == 1 for _f, slash, dash, *_ in table) == 8
    ambiguous = [row for row in table if row[1] > 0 and row[2] > 0]
    assert len(ambiguous) == 1
    assert ambiguous[0][0] == 6
    assert (ambiguous[0][1], ambiguous[0][2]) == (1, 8)

    print("Experiment 262")
    print("frame | slash-minority completions | dash-minority completions | selected")
    for frame, slash, dash, polarity, count, _options in table:
        label = "dash-minority" if polarity else "slash-minority"
        print(f"{frame:>5} | {slash:>27} | {dash:>26} | {label} ({count})")

    print("RESULT: 8/9 frames have exactly one viable polarity")
    print("RESULT: frame 6 resolves locally by 1 completion versus 8")
    print("RESULT: local minimum-completion polarity matches d<=q in all 9 frames")
    print("CAUTION: local parsimony is a human solve heuristic, not an authoring axiom")


if __name__ == "__main__":
    main()
