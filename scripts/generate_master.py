#!/usr/bin/env python3
"""Generate complete H108 foreground masters from the four-bit state model.

State:
    H = (X,Y,Z,G)
Validity:
    Y & Z -> X

Exactly 14 physical states are legal. Each generates one complete 108-symbol
foreground master in native serial order.

Primary alphabet:
    slash "/" and dash "-"
Q4 alphabet:
    slash "/" and dot "."
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass


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


@dataclass(frozen=True)
class HiddenState:
    X: int
    Y: int
    Z: int
    G: int

    def __post_init__(self) -> None:
        for name in ("X", "Y", "Z", "G"):
            value = getattr(self, name)
            if value not in (0, 1):
                raise ValueError(f"{name} must be 0 or 1")
        if self.Y and self.Z and not self.X:
            raise ValueError("forbidden state: validity clause Y & Z -> X fails")

    @property
    def x(self) -> int:
        return 1 + self.X

    @property
    def y(self) -> int:
        return 2 if self.Y else self.Z

    @property
    def g(self) -> int:
        return 2 * self.G

    @property
    def grants(self) -> tuple[int, int, int]:
        P0 = int(self.Y and not self.Z)
        P1 = int((not self.X) and (not self.Y))
        P2 = int(self.X and ((not self.Y) or self.Z))
        if P0 + P1 + P2 != 1:
            raise AssertionError("legal state did not decode to exactly one grant")
        return P0, P1, P2

    @property
    def p(self) -> int:
        P0, P1, P2 = self.grants
        return 0 if P0 else 1 if P1 else 2


def legal_states() -> list[HiddenState]:
    states = []
    for X in (0, 1):
        for Y in (0, 1):
            for Z in (0, 1):
                for G in (0, 1):
                    try:
                        states.append(HiddenState(X, Y, Z, G))
                    except ValueError:
                        pass
    return states


def primary_payload_lattice(state: HiddenState) -> list[list[str]]:
    x = state.x
    y = state.y
    return [
        ["112", "212", f"0{x}0"],
        ["212", "002", "100"],
        [f"1{y}2", "022", "100"],
    ]


def q4_selector_field(state: HiddenState) -> list[list[int]]:
    P0, P1, P2 = state.grants
    A = 2 - P0
    D = 1 + P1
    G_control = 2 * P2
    return [
        [2, A, 2],
        [state.g, D, 0],
        [1, G_control, 2],
    ]


def primary_symbol(state: HiddenState, residue: int) -> str:
    if not 1 <= residue <= 81:
        raise ValueError("primary residue must be in 1..81")

    offset = residue - 1
    q = offset // 27
    d = (offset % 27) // 9
    j = offset % 9

    image_class = SERIAL_ORDER[j]
    physical_row, physical_col = PHYSICAL_POSITION[image_class]
    payload = primary_payload_lattice(state)[q][d]
    minority_row = int(payload[physical_col])

    minority_is_dash = d <= q
    on_minority = physical_row == minority_row

    if on_minority:
        return "-" if minority_is_dash else "/"
    return "/" if minority_is_dash else "-"


def q4_symbol(state: HiddenState, residue: int) -> str:
    if not 82 <= residue <= 108:
        raise ValueError("Q4 residue must be in 82..108")

    offset = residue - 82
    selector_depth = offset // 9
    j = offset % 9

    image_class = SERIAL_ORDER[j]
    physical_row, physical_col = PHYSICAL_POSITION[image_class]
    selected = q4_selector_field(state)[physical_row][physical_col]

    return "/" if selector_depth == selected else "."


def foreground_symbol(state: HiddenState, residue: int) -> str:
    if 1 <= residue <= 81:
        return primary_symbol(state, residue)
    if 82 <= residue <= 108:
        return q4_symbol(state, residue)
    raise ValueError("H108 residue must be in 1..108")


def generate_master(state: HiddenState) -> str:
    return "".join(foreground_symbol(state, residue) for residue in range(1, 109))


def symbol_census(master: str) -> Counter:
    return Counter(master)


def format_state(state: HiddenState) -> str:
    return f"{state.X}{state.Y}{state.Z}{state.G}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state",
        help="four-bit XYZG state, e.g. 0000; omit to list all 14 legal masters",
    )
    args = parser.parse_args()

    if args.state:
        if len(args.state) != 4 or any(ch not in "01" for ch in args.state):
            raise SystemExit("--state must be four bits XYZG")
        try:
            state = HiddenState(*(int(ch) for ch in args.state))
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        master = generate_master(state)
        print(f"state={format_state(state)} x={state.x} y={state.y} p={state.p} g={state.g}")
        print(master)
        print(dict(symbol_census(master)))
        return

    for state in legal_states():
        master = generate_master(state)
        print(
            f"{format_state(state)} "
            f"x={state.x} y={state.y} p={state.p} g={state.g} "
            f"{master}"
        )


if __name__ == "__main__":
    main()
