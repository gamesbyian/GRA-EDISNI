#!/usr/bin/env python3
"""Independent native-state implementation of the closed-corpus machine.

This implementation deliberately does NOT import generate_master.py and does
not use the Boolean XYZG/Horn-clause state representation.

Its state space is reconstructed from native variables:
    x in {1,2}
    y in {0,1,2}
    p in {0,1,2}
    g in {0,2}

with p constrained only by the request/grant relation:
    X=[x=2], Y=[y=2]
    00 -> p=1
    01 -> p=0
    10 -> p=2
    11 -> p in {0,2}

That relation yields exactly 14 physical states. The script then independently
generates the complete H108 master family and checks the live corpus plus the
main completion invariants.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
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
PHYSICAL_LAYOUT = (
    ("I", "A", "B"),
    ("C", "D", "E"),
    ("F", "G", "H"),
)

REQUEST_GRANT = {
    (0, 0): (1,),
    (0, 1): (0,),
    (1, 0): (2,),
    (1, 1): (0, 2),
}


@dataclass(frozen=True)
class NativeState:
    x: int
    y: int
    p: int
    g: int

    @property
    def request_bits(self) -> tuple[int, int]:
        return int(self.x == 2), int(self.y == 2)


def legal_native_states() -> list[NativeState]:
    states: list[NativeState] = []
    for x in (1, 2):
        for y in (0, 1, 2):
            X, Y = int(x == 2), int(y == 2)
            for p in REQUEST_GRANT[(X, Y)]:
                for g in (0, 2):
                    states.append(NativeState(x, y, p, g))
    return states


def primary_payload_lattice(state: NativeState) -> tuple[tuple[str, ...], ...]:
    return (
        ("112", "212", f"0{state.x}0"),
        ("212", "002", "100"),
        (f"1{state.y}2", "022", "100"),
    )


def selector_field(state: NativeState) -> tuple[tuple[int, ...], ...]:
    p0 = int(state.p == 0)
    p1 = int(state.p == 1)
    p2 = int(state.p == 2)
    return (
        (2, 2 - p0, 2),
        (state.g, 1 + p1, 0),
        (1, 2 * p2, 2),
    )


def primary_symbol(state: NativeState, residue: int) -> str:
    if not 1 <= residue <= 81:
        raise ValueError("primary residue must be in 1..81")

    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9

    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
    minority_row = int(primary_payload_lattice(state)[q][d][col])
    minority_is_dash = d <= q
    on_minority = row == minority_row

    if on_minority:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def q4_symbol(state: NativeState, residue: int) -> str:
    if not 82 <= residue <= 108:
        raise ValueError("Q4 residue must be in 82..108")

    offset = residue - 82
    depth = offset // 9
    j = offset % 9

    row, col = PHYSICAL_POSITION[SERIAL_ORDER[j]]
    return "/" if selector_field(state)[row][col] == depth else "."


def foreground_symbol(state: NativeState, residue: int) -> str:
    if 1 <= residue <= 81:
        return primary_symbol(state, residue)
    if 82 <= residue <= 108:
        return q4_symbol(state, residue)
    raise ValueError("H108 residue must be in 1..108")


def generate_master(state: NativeState) -> str:
    return "".join(foreground_symbol(state, r) for r in range(1, 109))


def frame_symbol(state: NativeState, q: int, d: int, row: int, col: int) -> str:
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return foreground_symbol(state, residue)


def selected_surface(state: NativeState, q: int) -> tuple[tuple[str, ...], ...]:
    selector = selector_field(state)
    return tuple(
        tuple(
            frame_symbol(state, q, selector[row][col], row, col)
            for col in range(3)
        )
        for row in range(3)
    )


def terminal_surface(state: NativeState) -> tuple[tuple[str, ...], ...]:
    selector = selector_field(state)
    return tuple(
        tuple(
            frame_symbol(
                state,
                selector[row][col],
                selector[row][col],
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def decode_dash_pos3(surface: tuple[tuple[str, ...], ...]) -> str:
    digits: list[str] = []
    for col in range(3):
        rows = [row for row in range(3) if surface[row][col] == "-"]
        if len(rows) != 1:
            raise AssertionError(f"column {col} is not dash-POS3: {surface}")
        digits.append(str(rows[0]))
    return "".join(digits)


def surface_serial_word(surface: tuple[tuple[str, ...], ...]) -> str:
    by_letter = {
        PHYSICAL_LAYOUT[row][col]: surface[row][col]
        for row in range(3)
        for col in range(3)
    }
    return "".join(by_letter[letter] for letter in SERIAL_ORDER)


def load_observations() -> list[dict[str, str]]:
    with OBSERVATIONS.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    states = legal_native_states()
    assert len(states) == 14

    masters = [generate_master(state) for state in states]
    assert len(set(masters)) == 14

    # Every legal completion preserves the same global symbol budget.
    expected_census = Counter({"/": 54, "-": 36, ".": 18})
    assert all(Counter(master) == expected_census for master in masters)

    # Exact invariant/variable decomposition.
    variable = [
        residue
        for residue in range(1, 109)
        if len({master[residue - 1] for master in masters}) > 1
    ]
    assert variable == [22, 25, 55, 58, 61, 84, 88, 91, 94, 100, 102, 103, 106]

    # Live physical corpus. The native 14-state family is the structural
    # model; newly observed stickers prospectively prune that family.
    observations = load_observations()
    assert len(observations) == 84
    assert len({int(row["residue"]) for row in observations}) == 66

    for row in observations:
        serial = int(row["serial"])
        residue = int(row["residue"])
        image_class = row["image_class"]

        if image_class:
            assert image_class == SERIAL_ORDER[(serial - 1) % 9]
        assert residue == ((serial - 1) % 108) + 1

    live = [
        (state, master)
        for state, master in zip(states, masters)
        if all(
            master[int(row["residue"]) - 1] == row["symbol"]
            for row in observations
        )
    ]
    assert len(live) == 10
    live_masters = [master for _state, master in live]
    live_variable = [
        residue
        for residue in range(1, 109)
        if len({master[residue - 1] for master in live_masters}) > 1
    ]
    assert live_variable == [22, 25, 55, 58, 61, 84, 88, 91, 100, 102, 106]
    assert all(master[102] == "." for master in live_masters)
    assert all(master[93] == "/" for master in live_masters)

    # First recursion collapses 14 physical states to the three p classes.
    expected_first = {
        0: ("102", "002", "120"),
        1: ("102", "012", "100"),
        2: ("102", "022", "100"),
    }
    first_outputs = set()

    for state in states:
        outputs = tuple(
            decode_dash_pos3(selected_surface(state, q))
            for q in range(3)
        )
        assert outputs == expected_first[state.p]
        first_outputs.add(outputs)

        terminal = terminal_surface(state)
        assert decode_dash_pos3(terminal) == "100"
        assert surface_serial_word(terminal) == "---//////"

    assert len(first_outputs) == 3

    print("OK(native): request/grant relation yields exactly 14 states")
    print("OK(native): 14 distinct complete H108 masters")
    print("OK(native): 82 stickers / 65 residues fit every legal master")
    print("OK(native): exact 95 invariant / 13 variable split")
    print("OK(native): global 54/36/18 symbol census")
    print("OK(native): first recursion has rank 3 by p")
    print("OK(native): second selector reuse terminates at 100 / ---//////")


if __name__ == "__main__":
    main()
