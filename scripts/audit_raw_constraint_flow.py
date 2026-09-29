#!/usr/bin/env python3
"""Experiment 252: expose constraint flow inside the raw reconstruction.

This script does not introduce a new parent family. It decomposes Experiment
250's 216 -> 20 -> 14 closure to show which unobserved selector freedoms are
removed at each recursive pass and whether the request/grant relation emerges
from the final survivor set.
"""

from __future__ import annotations

from collections import defaultdict

from enumerate_raw_machine import (
    compact_primary_signature,
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    first_pass_surface,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    selector_at_physical_cell,
    terminal_surface,
    SERIAL_ORDER,
)


def selector_letter(selector, letter):
    return selector[SERIAL_ORDER.index(letter)]


def reconstruct():
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    first = []
    for payload in payloads:
        for selector in selectors:
            decoded = tuple(
                decode_dash_pos3(first_pass_surface(payload, selector, q))
                for q in range(3)
            )
            if None not in decoded:
                first.append((payload, selector, decoded))

    final = []
    for payload, selector, decoded in first:
        terminal = decode_dash_pos3(terminal_surface(payload, selector))
        if terminal is not None:
            final.append((payload, selector, decoded, terminal))

    return first, final


def control_core(selector):
    return (
        selector_letter(selector, "A"),
        selector_letter(selector, "D"),
        selector_letter(selector, "G"),
    )


def main():
    first, final = reconstruct()
    assert len(first) == 20
    assert len(final) == 14

    first_c = {selector_letter(selector, "C") for _p, selector, _d in first}
    final_c = {selector_letter(selector, "C") for _p, selector, _d, _t in final}
    assert first_c == {0, 2}
    assert final_c == {0, 2}

    first_cores = {
        control_core(selector)
        for _payload, selector, _decoded in first
    }
    final_cores = {
        control_core(selector)
        for _payload, selector, _decoded, _terminal in final
    }

    assert first_cores == {
        (0, 1, 2),
        (0, 2, 0),
        (1, 1, 0),
        (2, 1, 2),
        (2, 2, 0),
    }
    assert final_cores == {
        (1, 1, 0),
        (2, 1, 2),
        (2, 2, 0),
    }

    # The second pass rejects exactly the first-pass survivors with A=0.
    final_keys = {
        (
            tuple(sorted(payload.items())),
            tuple(sorted(selector.items())),
        )
        for payload, selector, _decoded, _terminal in final
    }
    rejected = [
        (payload, selector, decoded)
        for payload, selector, decoded in first
        if (
            tuple(sorted(payload.items())),
            tuple(sorted(selector.items())),
        )
        not in final_keys
    ]
    assert len(rejected) == 6
    assert all(selector_letter(selector, "A") == 0 for _p, selector, _d in rejected)
    assert all(
        selector_letter(selector, "A") != 0
        for _p, selector, _d, _t in final
    )

    # C is a pure two-valued gauge in the final family: for every primary
    # payload + ADG core combination, both C=0 and C=2 survive.
    gauge_groups = defaultdict(set)
    for payload, selector, _decoded, _terminal in final:
        key = (compact_primary_signature(payload), control_core(selector))
        gauge_groups[key].add(selector_letter(selector, "C"))
    assert all(values == {0, 2} for values in gauge_groups.values())

    # Derive the request/grant compatibility relation directly from final
    # survivors, using only whether the two raw-variable primary ports occupy
    # their high values and the emergent ADG control-core class.
    compatibility = defaultdict(set)
    for payload, selector, _decoded, _terminal in final:
        x, y = compact_primary_signature(payload)
        X = int(x == 2)
        Y = int(y == 2)
        compatibility[(X, Y)].add(control_core(selector))

    assert dict(compatibility) == {
        (0, 0): {(2, 2, 0)},
        (0, 1): {(1, 1, 0)},
        (1, 0): {(2, 1, 2)},
        (1, 1): {(1, 1, 0), (2, 1, 2)},
    }

    print("Experiment 252")
    print("first-pass survivor C values:", sorted(first_c))
    print("first-pass ADG cores:", sorted(first_cores))
    print("second-pass ADG cores:", sorted(final_cores))
    print("second-pass rejected states:", len(rejected))
    print("OK: first pass forces C gauge from {0,1,2} to {0,2}")
    print("OK: second pass rejects exactly A=0 first-pass impostors")
    print("OK: final ADG control cores are exactly 110, 220, 212")
    print("OK: C remains a free binary gauge on every final functional state")
    print("derived request/grant compatibility:")
    for key in sorted(compatibility):
        print(f"  {key} -> {sorted(compatibility[key])}")


if __name__ == "__main__":
    main()
