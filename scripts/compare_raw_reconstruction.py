#!/usr/bin/env python3
"""Compare Experiment 250's raw-constraint survivors to both prior generators."""

from __future__ import annotations

from enumerate_raw_machine import (
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    first_pass_surface,
    generate_master as generate_raw_master,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    terminal_surface,
)
from generate_master import (
    generate_master as generate_boolean_master,
    legal_states as legal_boolean_states,
)
from verify_native_model import (
    generate_master as generate_native_master,
    legal_native_states,
)


def raw_survivor_masters():
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))

    masters = set()
    for payload in payloads:
        for selector in selectors:
            first = tuple(
                decode_dash_pos3(first_pass_surface(payload, selector, q))
                for q in range(3)
            )
            if None in first:
                continue
            terminal = decode_dash_pos3(terminal_surface(payload, selector))
            if terminal is None:
                continue
            masters.add(generate_raw_master(payload, selector))

    return masters


def main() -> None:
    raw = raw_survivor_masters()
    boolean = {
        generate_boolean_master(state)
        for state in legal_boolean_states()
    }
    native = {
        generate_native_master(state)
        for state in legal_native_states()
    }

    assert len(raw) == 14
    assert raw == boolean
    assert raw == native

    print("OK(compare-raw): raw-constraint reconstruction emits exactly 14 masters")
    print("OK(compare-raw): raw set equals canonical Boolean set exactly")
    print("OK(compare-raw): raw set equals independent native set exactly")


if __name__ == "__main__":
    main()
