#!/usr/bin/env python3
"""Experiment 313: exhaust reused cell-local translations of both address coordinates.

This fills the natural gap between:
- Experiment 310: reused cell-local depth translations only,
- Experiment 309: both q/depth translations but only on the second pass, and
- Experiments 303-305: both coordinates transformed globally rather than per cell.

At every physical A-I cell j choose one translation

    F_j(q,S) = (q + a_j, S + b_j) mod 3

with (a_j,b_j) in F3^2, and reuse that same F_j on both passes.

Full physical family:
    9^9 = 387,420,489 operations.

The search is exact but quotient-compressed by physical column. Each column
has three cells, hence 9^3 = 729 local translation triples. Local triples with
identical q0/q1/q2/terminal signatures over all 216 raw-compatible machines are
collapsed with multiplicity. The three columns have 230, 729, and 47 distinct
signatures respectively, leaving 7,880,490 quotient combinations.

No target state count, terminal, survivor family, route words, or canonical
operation is used as a filter.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    enumerate_primary_payloads,
    enumerate_selectors,
    frame_symbol,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
)

TRANSLATIONS = tuple(product(range(3), repeat=2))
IDENTITY = (0, 0)


def is_permutation(word):
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def route_shells(families):
    families = tuple(sorted(families))
    if len(families) != 3:
        return []
    result = []
    for choices in product(range(3), repeat=3):
        routes = tuple(families[index][choices[index]] for index in range(3))
        if all(is_permutation(word) for word in routes) and len(set(routes)) == 3:
            result.append((choices, routes))
    return result


def raw_candidates(rows):
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    result = [(payload, selector) for payload in payloads for selector in selectors]
    assert len(payloads) == 6
    assert len(selectors) == 36
    assert len(result) == 216
    return result


def physical_columns():
    return tuple(
        tuple(SERIAL_ORDER.index(PHYSICAL_LAYOUT[row][col]) for row in range(3))
        for col in range(3)
    )


def column_signature(candidates, js, local_translations):
    """Per candidate: q0,q1,q2,terminal row digits; 3 means invalid."""
    signatures = []
    for payload, selector in candidates:
        digits = []

        for q in range(3):
            dash_rows = []
            for row, (j, (q_offset, d_offset)) in enumerate(
                zip(js, local_translations)
            ):
                physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
                s = selector[j]
                if frame_symbol(
                    payload,
                    (q + q_offset) % 3,
                    (s + d_offset) % 3,
                    physical_row,
                    physical_col,
                ) == "-":
                    dash_rows.append(row)
            digits.append(dash_rows[0] if len(dash_rows) == 1 else 3)

        dash_rows = []
        for row, (j, (q_offset, d_offset)) in enumerate(
            zip(js, local_translations)
        ):
            physical_row, physical_col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
            s = selector[j]
            if frame_symbol(
                payload,
                (s + q_offset) % 3,
                (s + d_offset) % 3,
                physical_row,
                physical_col,
            ) == "-":
                dash_rows.append(row)
        digits.append(dash_rows[0] if len(dash_rows) == 1 else 3)

        signatures.append(tuple(digits))
    return tuple(signatures)


def signature_counts(candidates, js):
    counts = Counter()
    representatives = {}
    for local in product(TRANSLATIONS, repeat=3):
        signature = column_signature(candidates, js, local)
        counts[signature] += 1
        cost = sum(pair != IDENTITY for pair in local)
        key = (cost, local)
        if signature not in representatives or key < representatives[signature][0]:
            representatives[signature] = (key, local)
    assert sum(counts.values()) == 9 ** 3
    return counts, representatives


def valid_mask(signature):
    mask = 0
    for index, digits in enumerate(signature):
        if 3 not in digits:
            mask |= 1 << index
    return mask


def operation_label(columns, representatives, sigs):
    local_by_j = [IDENTITY] * 9
    for js, reps, signature in zip(columns, representatives, sigs):
        local = reps[signature][1]
        for j, translation in zip(js, local):
            local_by_j[j] = translation

    parts = []
    for j, (q_offset, d_offset) in enumerate(local_by_j):
        if (q_offset, d_offset) != IDENTITY:
            parts.append(f"{SERIAL_ORDER[j]}:({q_offset},{d_offset})")
    return "+".join(parts) if parts else "canonical"


def main() -> None:
    candidates = raw_candidates(load_rows())
    columns = physical_columns()

    counts_and_reps = [signature_counts(candidates, js) for js in columns]
    counts = [item[0] for item in counts_and_reps]
    representatives = [item[1] for item in counts_and_reps]

    assert [len(item) for item in counts] == [230, 729, 47]
    quotient_combinations = 230 * 729 * 47
    assert quotient_combinations == 7_880_490

    tables = [
        [
            (valid_mask(signature), multiplicity, signature)
            for signature, multiplicity in counter.items()
        ]
        for counter in counts
    ]

    state_distribution = Counter()
    total_operations = 0
    maximum_states = -1
    high_state_records = []

    for i, (mask0, count0, sig0) in enumerate(tables[0]):
        for j, (mask1, count1, sig1) in enumerate(tables[1]):
            mask01 = mask0 & mask1
            for k, (mask2, count2, sig2) in enumerate(tables[2]):
                multiplicity = count0 * count1 * count2
                total_operations += multiplicity
                mask = mask01 & mask2
                states = mask.bit_count()
                state_distribution[states] += multiplicity
                maximum_states = max(maximum_states, states)

                if states >= 14:
                    high_state_records.append(
                        (
                            states,
                            i,
                            j,
                            k,
                            multiplicity,
                            mask,
                            sig0,
                            sig1,
                            sig2,
                        )
                    )

    assert total_operations == 9 ** 9 == 387_420_489
    assert maximum_states == 24
    assert len(high_state_records) == 1_340
    assert Counter(item[0] for item in high_state_records) == Counter(
        {14: 840, 16: 280, 18: 80, 20: 80, 22: 20, 24: 40}
    )

    # Canonical is known to be route-capable with 14 states. Therefore only
    # >=14-state operations can improve or tie the routed maximum.
    route_records = []
    for (
        states,
        i,
        j,
        k,
        multiplicity,
        mask,
        sig0,
        sig1,
        sig2,
    ) in high_state_records:
        survivor_indices = [
            index for index in range(len(candidates)) if (mask >> index) & 1
        ]
        families = set()
        terminals = Counter()

        for index in survivor_indices:
            first = tuple(
                "".join(
                    str(signature[index][q])
                    for signature in (sig0, sig1, sig2)
                )
                for q in range(3)
            )
            families.add(first)
            terminal = "".join(
                str(signature[index][3]) for signature in (sig0, sig1, sig2)
            )
            terminals[terminal] += 1

        shells = route_shells(families)
        if shells:
            route_records.append(
                (
                    states,
                    i,
                    j,
                    k,
                    multiplicity,
                    mask,
                    frozenset(families),
                    terminals,
                    tuple(shells),
                    (sig0, sig1, sig2),
                )
            )

    assert route_records
    maximum_route_states = max(item[0] for item in route_records)
    assert maximum_route_states == 14

    route_max = [item for item in route_records if item[0] == 14]
    route_max_operations = sum(item[4] for item in route_max)

    assert len(route_records) == 11
    assert len(route_max) == 11
    assert route_max_operations == 396

    route_max_classes = Counter()
    route_max_representatives = {}

    for item in route_max:
        (
            _states,
            _i,
            _j,
            _k,
            multiplicity,
            mask,
            families,
            terminals,
            shells,
            sigs,
        ) = item
        key = (
            mask,
            families,
            tuple(sorted(terminals.items())),
            shells,
        )
        route_max_classes[key] += multiplicity

        label = operation_label(columns, representatives, sigs)
        previous = route_max_representatives.get(key)
        if previous is None or (label.count("+"), label) < (
            previous.count("+"),
            previous,
        ):
            route_max_representatives[key] = label

    assert len(route_max_classes) == 10
    assert sorted(route_max_classes.values()) == [
        36, 36, 36, 36, 36, 36, 36, 36, 36, 72
    ]

    canonical_signatures = tuple(
        column_signature(candidates, js, (IDENTITY, IDENTITY, IDENTITY))
        for js in columns
    )
    canonical_record = next(item for item in route_max if item[9] == canonical_signatures)
    canonical_key = (
        canonical_record[5],
        canonical_record[6],
        tuple(sorted(canonical_record[7].items())),
        canonical_record[8],
    )

    assert canonical_record[7] == Counter({"100": 14})
    assert canonical_record[8] == (
        ((2, 1, 0), ("120", "012", "102")),
    )
    assert route_max_classes[canonical_key] == 36

    canonical_column_multiplicities = [
        counter[signature]
        for counter, signature in zip(counts, canonical_signatures)
    ]
    assert canonical_column_multiplicities == [3, 1, 12]
    assert 3 * 1 * 12 == 36

    # Resolve those 36 exact-operation gauges back into physical cell moves.
    canonical_options = []
    for js, target_signature in zip(columns, canonical_signatures):
        options = []
        for local in product(TRANSLATIONS, repeat=3):
            if column_signature(candidates, js, local) == target_signature:
                options.append(local)
        canonical_options.append(options)

    assert canonical_options[0] == [
        ((0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, 0), (1, 0)),
        ((0, 0), (0, 0), (2, 0)),
    ]
    assert canonical_options[1] == [
        ((0, 0), (0, 0), (0, 0)),
    ]
    assert canonical_options[2] == [
        ((b, db), (e, 0), (h, dh))
        for b, db in ((0, 0), (1, 2))
        for e in range(3)
        for h, dh in ((0, 0), (1, 2))
    ]

    # In physical letters this is:
    #   F: arbitrary q translation, depth unchanged;
    #   E: arbitrary q translation, depth unchanged;
    #   B/H independently: identity or (q+1, depth-1).
    # A/D/G and I/C remain fixed. These options produce exactly the same
    # q0/q1/q2/terminal signatures over all 216 raw-compatible candidates.

    # The canonical observational class is the only route-max class with the
    # canonical 14 physical states, invariant 100, and canonical route shell.
    for key in route_max_classes:
        if key == canonical_key:
            continue
        mask, _families, terminal_profile, shells = key
        assert not (
            mask == canonical_record[5]
            and terminal_profile == (("100", 14),)
            and shells == canonical_record[8]
        )

    print("Experiment 313")
    print("reused cell-local 2D translation family:", total_operations)
    print("column signature counts:", [len(item) for item in counts])
    print("quotient combinations:", quotient_combinations)
    print("maximum retained raw states:", maximum_states)
    print(">=14-state signature combinations:", len(high_state_records))
    print("route-capable >=14-state signature combinations:", len(route_records))
    print("maximum route-capable states:", maximum_route_states)
    print("route-max physical operations:", route_max_operations)
    print("route-max observational classes:", len(route_max_classes))
    print("route-max class multiplicities:", sorted(route_max_classes.values()))
    print("canonical-equivalent physical operations:", route_max_classes[canonical_key])
    print("canonical column gauge multiplicities:", canonical_column_multiplicities)
    print("canonical exact gauges: F q+=0/1/2; E q+=0/1/2; B/H each identity or (q+1,d-1)")
    print("simplest route-max representatives:")
    for key, multiplicity in sorted(
        route_max_classes.items(),
        key=lambda item: route_max_representatives[item[0]],
    ):
        print(
            " ",
            route_max_representatives[key],
            "x",
            multiplicity,
            "terminal",
            dict(key[2]),
        )
    print("RESULT: 24-state local-translation siblings exist but are route-degenerate")
    print("RESULT: routed retention still tops out at 14 states")
    print("RESULT: 396 physical route-max rules collapse to 10 observational classes")
    print("RESULT: exactly one route-max class preserves canonical states, route shell, and invariant 100")
    print("RESULT: that canonical class contains 36 exact local translation gauges")


if __name__ == "__main__":
    main()
