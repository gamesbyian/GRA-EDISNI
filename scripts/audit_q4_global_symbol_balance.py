#!/usr/bin/env python3
"""Experiment 281: select the Q4 polarity gauge by whole-master symbol balance.

Experiment 260 factorizes the recursively closed Q4 polarity family into:
  * an 8-word 14-state/100 gauge cube;
  * the same cube with D toggled, yielding 12-state/110 siblings.

Experiment 270 selects the authored all-slash polarity as the unique locally
homogeneous / minimum-domain-wall representative.

This experiment asks for an independent global physical discriminator.

Under exact primary POS3 and the derived d<=q frame polarity:
  * every primary frame has 3 minority and 6 majority cells;
  * six frames are dash-minority and three are slash-minority;
  * therefore the 81-cell primary always contains 45 slash + 36 dash.

For Q4, each slash-exception stack contributes 1 slash + 2 dots, while each
dot-exception stack contributes 2 slash + 1 dot.

Thus a Q4 polarity word with k dot-exception stacks has whole-master census:
    slash = 54 + k
    dash  = 36
    dot   = 18 - k

The exact 3:2:1 whole-master ratio occurs iff k=0.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from audit_q4_pos3_polarity import DOT, SLASH, local_options, q4_observations
from audit_q4_polarity_gauge import mask_for
from enumerate_raw_machine import load_rows


TARGET = Counter({"/": 54, "-": 36, ".": 18})


def whole_census(polarity):
    k = sum(symbol == DOT for symbol in polarity)
    return Counter({
        "/": 54 + k,
        "-": 36,
        ".": 18 - k,
    })


def main() -> None:
    rows = load_rows()
    options = local_options(q4_observations(rows))

    raw_compatible = []
    for polarity in product((SLASH, DOT), repeat=9):
        if all(
            any(
                symbol == polarity[j]
                for _depth, symbol, _pattern in options[j]
            )
            for j in range(9)
        ):
            raw_compatible.append(polarity)

    assert len(raw_compatible) == 256

    balanced = [
        polarity
        for polarity in raw_compatible
        if whole_census(polarity) == TARGET
    ]
    assert len(balanced) == 1
    assert mask_for(balanced[0]) == 0
    assert all(symbol == SLASH for symbol in balanced[0])

    census_distribution = Counter(
        sum(symbol == DOT for symbol in polarity)
        for polarity in raw_compatible
    )

    # Raw compatibility fixes one stack polarity, so the 256 words form an
    # 8-free-bit cube: binomial distribution over dot-exception count.
    assert census_distribution == Counter({
        0: 1,
        1: 8,
        2: 28,
        3: 56,
        4: 70,
        5: 56,
        6: 28,
        7: 8,
        8: 1,
    })

    print("Experiment 281")
    print("raw-compatible Q4 polarity words:", len(raw_compatible))
    print("dot-exception-count distribution:", dict(sorted(census_distribution.items())))
    print("target whole-master census:", dict(TARGET))
    print("3:2:1-balanced polarity words:", len(balanced))
    print("balanced polarity mask:", mask_for(balanced[0]))
    print("RESULT: whole-master 54/36/18 = 3:2:1 balance uniquely selects all-slash Q4 polarity")
    print("RESULT: every nonzero dot-exception gauge changes slash/dot census and breaks the ratio")
    print("CAUTION: global symbol balance is an authoring-simplicity criterion, not a directly observed complete-master census")


if __name__ == "__main__":
    main()
