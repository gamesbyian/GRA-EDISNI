#!/usr/bin/env python3
"""Experiment 261: local parsimony at the sole unresolved primary frame.

Experiment 246 leaves exactly one frame polarity unresolved directly by raw
observations under exact POS3: q=1,d=2.

Experiment 247 selects the current completion because d<=q is the unique
minimum-L1 bounded threshold rule. This experiment asks a simpler local human
question:

    how many exact-POS3 payload completions does each polarity admit in that
    one ambiguous frame?

No global threshold family is used here.
"""

from __future__ import annotations

from functools import reduce
from operator import mul

from audit_primary_leave_one_out import (
    allowed_rows,
    build_columns,
    load_rows,
)


def completion_count(columns, q, d, minority_is_dash):
    options = tuple(
        allowed_rows(columns, q, d, col, minority_is_dash)
        for col in range(3)
    )
    count = reduce(mul, (len(values) for values in options), 1)
    return count, options


def main() -> None:
    rows = load_rows()
    columns = build_columns(rows)

    # First confirm that q=1,d=2 is the only frame with two viable polarities.
    ambiguous = []
    for q in range(3):
        for d in range(3):
            viable = []
            for polarity in (False, True):
                count, options = completion_count(columns, q, d, polarity)
                if count:
                    viable.append((polarity, count, options))
            if len(viable) > 1:
                ambiguous.append(((q, d), tuple(viable)))

    assert len(ambiguous) == 1
    frame, viable = ambiguous[0]
    assert frame == (1, 2)

    by_polarity = {
        polarity: (count, options)
        for polarity, count, options in viable
    }

    # Current staircase at q=1,d=2 has d>q, so minority symbol is slash
    # (minority_is_dash=False).
    current_count, current_options = by_polarity[False]
    alternate_count, alternate_options = by_polarity[True]

    assert current_count == 1
    assert current_options == ((1,), (0,), (0,))

    assert alternate_count == 2
    assert alternate_options == ((2,), (1, 2), (2,))

    print("Experiment 261")
    print("sole polarity-ambiguous frame:", frame)
    print(
        "current slash-minority completion:",
        current_count,
        "payload(s)",
        current_options,
    )
    print(
        "alternate dash-minority completion:",
        alternate_count,
        "payload(s)",
        alternate_options,
    )
    print("RESULT: current polarity is the unique locally fully-determined completion")
    print("RESULT: alternate polarity retains one unresolved ternary column bit")
    print("CAUTION: this is local parsimony, not a proof that parsimony was the authoring rule")


if __name__ == "__main__":
    main()
