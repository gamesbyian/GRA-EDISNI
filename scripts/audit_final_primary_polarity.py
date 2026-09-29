#!/usr/bin/env python3
"""Experiment 277: derive the final primary frame polarity from recursion.

Under exact primary POS3, raw observations force the exceptional-symbol
polarity of eight of the nine (q,d) frames. Only q=1,d=2 admits both:
  * canonical slash-minority;
  * alternate dash-minority.

Earlier work preferred slash-minority by local determinacy and the compact
d<=q staircase. This experiment removes that global completion rule.

For each of the two raw-compatible q=1,d=2 polarities:
  1. enumerate every exact-POS3 primary completion consistent with raw marks;
  2. combine with all 36 raw-compatible Q4 selectors;
  3. apply the canonical first selector substitution;
  4. require only valid dash-POS3 on all three first-pass surfaces.

The second pass and terminal are measured afterwards but are not needed if one
branch already fails first-pass closure.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


AMBIGUOUS_FRAME = (1, 2)


def build_observations(rows):
    by_column = defaultdict(list)
    for record in rows:
        residue = int(record["residue"])
        if residue > 81:
            continue
        offset = residue - 1
        q = offset // 27
        d = (offset % 27) // 9
        j = offset % 9
        row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
        by_column[(q, d, col)].append((row, record["symbol"]))
    return by_column


def predicted_symbol(row, minority_row, minority_is_dash):
    if row == minority_row:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def primary_candidates(rows, ambiguous_minority_is_dash):
    observed = build_observations(rows)
    candidates = {}
    for q in range(3):
        for d in range(3):
            minority_is_dash = d <= q
            if (q, d) == AMBIGUOUS_FRAME:
                minority_is_dash = ambiguous_minority_is_dash
            for col in range(3):
                allowed = tuple(
                    minority_row
                    for minority_row in range(3)
                    if all(
                        predicted_symbol(
                            row,
                            minority_row,
                            minority_is_dash,
                        ) == symbol
                        for row, symbol in observed[(q, d, col)]
                    )
                )
                if not allowed:
                    raise AssertionError(
                        f"no POS3 completion for {(q, d, col)}"
                    )
                candidates[(q, d, col)] = allowed
    return candidates


def enumerate_primary(candidates):
    keys = tuple(sorted(candidates))
    for values in product(*(candidates[key] for key in keys)):
        yield dict(zip(keys, values))


def minority_is_dash(q, d, ambiguous_minority_is_dash):
    if (q, d) == AMBIGUOUS_FRAME:
        return ambiguous_minority_is_dash
    return d <= q


def primary_symbol(payload, residue, ambiguous_minority_is_dash):
    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9
    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
    return predicted_symbol(
        row,
        payload[(q, d, col)],
        minority_is_dash(q, d, ambiguous_minority_is_dash),
    )


def selector_at(selector, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    return selector[SERIAL_ORDER.index(letter)]


def frame_symbol(payload, q, d, row, col, ambiguous_minority_is_dash):
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return primary_symbol(payload, residue, ambiguous_minority_is_dash)


def first_surface(payload, selector, q, ambiguous_minority_is_dash):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                q,
                selector_at(selector, row, col),
                row,
                col,
                ambiguous_minority_is_dash,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def terminal_surface(payload, selector, ambiguous_minority_is_dash):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                selector_at(selector, row, col),
                selector_at(selector, row, col),
                row,
                col,
                ambiguous_minority_is_dash,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def run_branch(rows, selectors, ambiguous_minority_is_dash):
    candidates = primary_candidates(rows, ambiguous_minority_is_dash)
    payloads = list(enumerate_primary(candidates))

    first_survivors = []
    final_survivors = []

    for payload in payloads:
        for selector in selectors:
            first = tuple(
                decode_dash_pos3(
                    first_surface(
                        payload,
                        selector,
                        q,
                        ambiguous_minority_is_dash,
                    )
                )
                for q in range(3)
            )
            if None in first:
                continue
            first_survivors.append((payload, selector, first))

            terminal = decode_dash_pos3(
                terminal_surface(
                    payload,
                    selector,
                    ambiguous_minority_is_dash,
                )
            )
            if terminal is None:
                continue
            final_survivors.append((payload, selector, first, terminal))

    return payloads, first_survivors, final_survivors


def main() -> None:
    rows = load_rows()
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    assert len(selectors) == 36

    # False = slash is the minority symbol at q=1,d=2, matching d<=q.
    canonical = run_branch(rows, selectors, False)
    alternate = run_branch(rows, selectors, True)

    canonical_payloads, canonical_first, canonical_final = canonical
    alternate_payloads, alternate_first, alternate_final = alternate

    assert len(canonical_payloads) == 6
    assert len(alternate_payloads) == 12

    assert len(canonical_first) == 20
    assert len(canonical_final) == 14
    assert Counter(item[3] for item in canonical_final) == Counter({"100": 14})

    assert len(alternate_payloads) * len(selectors) == 432
    assert len(alternate_first) == 0
    assert len(alternate_final) == 0

    print("Experiment 277")
    print("raw Q4 selectors:", len(selectors))
    print("canonical slash-minority raw primary payloads:", len(canonical_payloads))
    print("canonical first-pass survivors:", len(canonical_first))
    print("canonical final survivors:", len(canonical_final))
    print("canonical terminal counts:", dict(Counter(item[3] for item in canonical_final)))
    print("alternate dash-minority raw primary payloads:", len(alternate_payloads))
    print("alternate raw candidate machines:", len(alternate_payloads) * len(selectors))
    print("alternate first-pass survivors:", len(alternate_first))
    print("alternate final survivors:", len(alternate_final))
    print("RESULT: first-pass recursive POS3 closure uniquely selects slash-minority at q=1,d=2")
    print("RESULT: all nine primary frame polarities are therefore derived from raw POS3 + recursion")
    print("RESULT: the global d<=q staircase becomes a compact description of the derived pattern, not a supplied completion rule")


if __name__ == "__main__":
    main()
