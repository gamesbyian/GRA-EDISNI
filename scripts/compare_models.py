#!/usr/bin/env python3
"""Compare the canonical Boolean and independent native implementations exactly.

The two generators are intentionally implemented in separate files and state
languages. This script is the thin comparison layer: it requires equality of
the full set of 108-symbol masters, then infers the state-language bijection
from exact master equality.
"""

from __future__ import annotations

from generate_master import (
    format_state,
    generate_master as generate_boolean_master,
    legal_states as legal_boolean_states,
)
from verify_native_model import (
    NativeState,
    generate_master as generate_native_master,
    legal_native_states,
)


def native_label(state: NativeState) -> str:
    return f"x={state.x},y={state.y},p={state.p},g={state.g}"


def main() -> None:
    boolean_by_master = {
        generate_boolean_master(state): state
        for state in legal_boolean_states()
    }
    native_by_master = {
        generate_native_master(state): state
        for state in legal_native_states()
    }

    assert len(boolean_by_master) == 14
    assert len(native_by_master) == 14
    assert set(boolean_by_master) == set(native_by_master)

    pairs = []
    for master in sorted(boolean_by_master):
        boolean_state = boolean_by_master[master]
        native_state = native_by_master[master]
        pairs.append((format_state(boolean_state), native_label(native_state)))

    assert len(pairs) == 14

    print("OK(compare): Boolean and native generators emit identical 14-master sets")
    print("Exact state bijection inferred from master equality:")
    for boolean_label, native in pairs:
        print(f"  {boolean_label} <-> {native}")


if __name__ == "__main__":
    main()
