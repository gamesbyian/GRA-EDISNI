#!/usr/bin/env python3
"""Experiment 293: derive exact input POS3 from a weaker frame-level parent.

Goal
----
Test whether one-minority-per-column must be supplied directly for the primary
memory, or whether it emerges from weaker physical regularities plus recursive
POS3 closure.

Weakened input grammar
----------------------
1. All nine primary 3x3 frames have one common minority-cell population k.
2. Raw observations must be satisfied under the derived frame polarities.
3. Extend the two strongest raw-supported partial frame repeats from Experiment
   274 to exact equality:
       q0,d1 == q1,d0
       q1,d2 == q2,d2
4. In each external quarter q, aggregate minority counts by physical column
   across its three depth frames. Require only that at least two of the three
   column totals are equal. No pair is named in advance.

No one-per-column rule is imposed on the source frames.

The recursive output type remains dash-POS3, as in the established selector
machine. Ask whether exact input POS3 emerges in the surviving family.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_selectors,
    load_rows,
    q4_selector_candidates,
)


CELLS = tuple((row, col) for row in range(3) for col in range(3))
FRAMES = tuple((q, d) for q in range(3) for d in range(3))


def frame_observations(rows):
    observed = defaultdict(dict)
    for record in rows:
        residue = int(record["residue"])
        if residue > 81:
            continue
        offset = residue - 1
        q = offset // 27
        d = (offset % 27) // 9
        j = offset % 9
        row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
        minority_symbol = "-" if d <= q else "/"
        observed[(q, d)][(row, col)] = record["symbol"] == minority_symbol
    return observed


def candidates_at_weight(observed, weight):
    result = {}
    for frame in FRAMES:
        candidates = []
        for chosen in combinations(CELLS, weight):
            minority = frozenset(chosen)
            if all(
                ((cell in minority) == value)
                for cell, value in observed[frame].items()
            ):
                candidates.append(minority)
        if not candidates:
            return None
        result[frame] = tuple(candidates)
    return result


def enumerate_primary(candidates):
    keys = tuple(sorted(candidates))
    for values in product(*(candidates[key] for key in keys)):
        yield dict(zip(keys, values))


def primary_symbol(payload, residue):
    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9
    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
    minority = (row, col) in payload[(q, d)]
    if minority:
        return "-" if d <= q else "/"
    return "/" if d <= q else "-"


def selector_at(selector, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    return selector[SERIAL_ORDER.index(letter)]


def frame_symbol(payload, q, d, row, col):
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    return primary_symbol(payload, 1 + 27 * q + 9 * d + j)


def first_surface(payload, selector, q):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                q,
                selector_at(selector, row, col),
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def terminal_surface(payload, selector):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                selector_at(selector, row, col),
                selector_at(selector, row, col),
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def exact_column_pos3(payload):
    return all(
        sum((row, col) in payload[(q, d)] for row in range(3)) == 1
        for q, d in FRAMES
        for col in range(3)
    )


def raw_repeat_motifs(payload):
    return (
        payload[(0, 1)] == payload[(1, 0)]
        and payload[(1, 2)] == payload[(2, 2)]
    )


def quarter_column_totals(payload, q):
    return tuple(
        sum(
            sum((row, col) in payload[(q, d)] for row in range(3))
            for d in range(3)
        )
        for col in range(3)
    )


def quarter_has_equal_pair(payload, q):
    a, b, c = quarter_column_totals(payload, q)
    return a == b or a == c or b == c


def recursive_survivors(payloads, selectors):
    survivors = []
    for payload in payloads:
        for selector in selectors:
            first = tuple(
                decode_dash_pos3(first_surface(payload, selector, q))
                for q in range(3)
            )
            if None in first:
                continue
            terminal = decode_dash_pos3(terminal_surface(payload, selector))
            if terminal is None:
                continue
            survivors.append((payload, selector, first, terminal))
    return survivors


def main() -> None:
    rows = load_rows()
    observed = frame_observations(rows)
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    assert len(selectors) == 36

    # If every frame has one common minority population, the raw corpus permits
    # only k=3 or k=4.
    admissible_weights = []
    candidates_by_weight = {}
    for weight in range(10):
        candidates = candidates_at_weight(observed, weight)
        if candidates is not None:
            admissible_weights.append(weight)
            candidates_by_weight[weight] = candidates

    assert admissible_weights == [3, 4]

    payload_counts = {}
    closure_counts = {}
    repeat_counts = {}
    final_counts = {}
    final = {}

    for weight in admissible_weights:
        payloads = list(enumerate_primary(candidates_by_weight[weight]))
        payload_counts[weight] = len(payloads)
        survivors = recursive_survivors(payloads, selectors)
        closure_counts[weight] = len(survivors)

        repeated = [
            item
            for item in survivors
            if raw_repeat_motifs(item[0])
        ]
        repeat_counts[weight] = len(repeated)

        selected = [
            item
            for item in repeated
            if all(
                quarter_has_equal_pair(item[0], q)
                for q in range(3)
            )
        ]
        final_counts[weight] = len(selected)
        final[weight] = selected

    assert payload_counts == {3: 1296, 4: 1152}
    assert closure_counts == {3: 1548, 4: 3676}
    assert repeat_counts == {3: 208, 4: 104}
    assert final_counts == {3: 14, 4: 0}

    canonical = final[3]
    assert all(exact_column_pos3(item[0]) for item in canonical)
    assert Counter(item[3] for item in canonical) == Counter({"100": 14})
    assert Counter(item[2] for item in canonical) == Counter({
        ("102", "002", "120"): 4,
        ("102", "012", "100"): 4,
        ("102", "022", "100"): 6,
    })

    # Prove that all three quarter-balance conditions are necessary inside the
    # repeated-frame k=3 family. Any subset of <=2 leaves noncanonical states.
    repeated3 = [
        item
        for item in recursive_survivors(
            list(enumerate_primary(candidates_by_weight[3])),
            selectors,
        )
        if raw_repeat_motifs(item[0])
    ]
    assert len(repeated3) == 208

    for size in range(3):
        for quarters in combinations(range(3), size):
            selected = [
                item
                for item in repeated3
                if all(
                    quarter_has_equal_pair(item[0], q)
                    for q in quarters
                )
            ]
            assert not (
                len(selected) == 14
                and all(exact_column_pos3(item[0]) for item in selected)
            )

    print("Experiment 293")
    print("raw-compatible common frame weights:", admissible_weights)
    print("raw primary payload counts:", payload_counts)
    print("recursive closure counts:", closure_counts)
    print("after two raw-supported exact repeats:", repeat_counts)
    print("after equal-pair aggregate balance in all three quarters:", final_counts)
    print("weight-3 survivors are exact input POS3:", all(exact_column_pos3(x[0]) for x in canonical))
    print("weight-3 terminal counts:", dict(Counter(x[3] for x in canonical)))
    print("RESULT: exact source POS3 emerges without imposing one minority per input column")
    print("RESULT: common weight 4 is eliminated completely")
    print("RESULT: all three quarter aggregate-balance conditions are necessary in this parent")
    print("CAUTION: uniform frame weight, repeat continuation, and aggregate balance remain authoring-grammar assumptions")


if __name__ == "__main__":
    main()
