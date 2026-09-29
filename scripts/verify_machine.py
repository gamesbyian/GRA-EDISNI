#!/usr/bin/env python3
"""Verify the compact closed-corpus machine against the checked-in corpus."""

from __future__ import annotations

import csv
from collections import Counter
from itertools import combinations
from pathlib import Path

from generate_master import (
    PHYSICAL_POSITION,
    SERIAL_ORDER,
    HiddenState,
    foreground_symbol,
    generate_master,
    legal_states,
    primary_payload_lattice,
    q4_selector_field,
)

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "observations.csv"

PHYSICAL_LAYOUT = (
    ("I", "A", "B"),
    ("C", "D", "E"),
    ("F", "G", "H"),
)


def latent_register(state: HiddenState):
    p = state.p
    return {
        22: state.X,
        25: 1 - state.X,
        55: int(state.y == 0),
        58: int(state.y == 1),
        61: int(state.y == 2),
        84: state.G,
        102: 1 - state.G,
        100: int(p == 0),
        91: int(p != 0),
        94: int(p == 1),
        103: int(p != 1),
        88: int(p == 2),
        106: int(p != 2),
    }


def observer(state: HiddenState):
    P0, _P1, _P2 = state.grants
    Y1 = int(state.y == 1)
    same_quarter = (0, 0, state.X, 1, 0, 0, state.Y, 0, 0)
    q4_target = (
        0,
        0,
        state.X & state.Y & P0,
        1,
        state.G,
        P0,
        1 - Y1,
        1,
        1 - P0,
    )
    return same_quarter + q4_target


def compose(f, g):
    return tuple(f[g[i]] for i in range(3))


def closure(generators):
    known = set(generators)
    changed = True
    while changed:
        changed = False
        snapshot = tuple(known)
        for f in snapshot:
            for g in snapshot:
                h = compose(f, g)
                if h not in known:
                    known.add(h)
                    changed = True
    return known


def map_rank(mapping):
    return len(set(mapping))


def frame_symbol(state: HiddenState, q: int, d: int, row: int, col: int) -> str:
    letter = PHYSICAL_LAYOUT[row][col]
    j = SERIAL_ORDER.index(letter)
    residue = 1 + 27 * q + 9 * d + j
    return foreground_symbol(state, residue)


def selected_surface(state: HiddenState, q: int):
    selector = q4_selector_field(state)
    return [
        [frame_symbol(state, q, selector[row][col], row, col) for col in range(3)]
        for row in range(3)
    ]


def decode_dash_one_hot(surface) -> str:
    digits = []
    for col in range(3):
        rows = [row for row in range(3) if surface[row][col] == "-"]
        assert len(rows) == 1, f"column {col} is not dash-one-hot: {surface}"
        digits.append(str(rows[0]))
    return "".join(digits)


def terminal_surface(state: HiddenState):
    selector = q4_selector_field(state)
    return [
        [
            frame_symbol(state, selector[row][col], selector[row][col], row, col)
            for col in range(3)
        ]
        for row in range(3)
    ]


def surface_serial_word(surface) -> str:
    by_letter = {
        PHYSICAL_LAYOUT[row][col]: surface[row][col]
        for row in range(3)
        for col in range(3)
    }
    return "".join(by_letter[letter] for letter in SERIAL_ORDER)


def load_observations():
    with OBSERVATIONS.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def minimum_observer_subsets(states, target_fn):
    outputs = [observer(state) for state in states]
    targets = [target_fn(state) for state in states]

    for size in range(19):
        winners = []
        for indices in combinations(range(18), size):
            seen = {}
            valid = True
            for output, target in zip(outputs, targets):
                key = tuple(output[i] for i in indices)
                if key in seen and seen[key] != target:
                    valid = False
                    break
                seen[key] = target
            if valid:
                winners.append(indices)
        if winners:
            return size, winners
    raise AssertionError("no observer subset separates target states")


def main():
    states = legal_states()
    assert len(states) == 14
    masters = [generate_master(state) for state in states]
    assert len(set(masters)) == 14

    # Every complete master has the same global census.
    for master in masters:
        assert Counter(master) == Counter({"/": 54, "-": 36, ".": 18})

    # Exact invariant / variable split.
    variable = []
    invariant = []
    for residue in range(1, 109):
        values = {master[residue - 1] for master in masters}
        (variable if len(values) > 1 else invariant).append(residue)

    expected_variable = [22, 25, 55, 58, 61, 84, 88, 91, 94, 100, 102, 103, 106]
    assert variable == expected_variable
    assert len(invariant) == 95

    # Checked-in physical corpus.
    observations = load_observations()
    assert len(observations) == 82
    assert len({int(row["residue"]) for row in observations}) == 65

    for row in observations:
        serial = int(row["serial"])
        residue = int(row["residue"])
        symbol = row["symbol"]
        image_class = row["image_class"]

        assert image_class == SERIAL_ORDER[(serial - 1) % 9]
        assert residue == ((serial - 1) % 108) + 1
        for master in masters:
            assert master[residue - 1] == symbol

    # Latent register.
    codes = [latent_register(state) for state in states]
    assert all(sum(code.values()) == 6 for code in codes)

    def hamming(a, b):
        return sum(a[k] != b[k] for k in a)

    assert min(hamming(a, b) for a, b in combinations(codes, 2)) == 2

    # Observer injectivity and optimal logical 4-bit decoding.
    observations18 = [observer(state) for state in states]
    assert len(set(observations18)) == 14
    for state, out in zip(states, observations18):
        S3 = out[2]
        S7 = out[6]
        Q5 = out[9 + 4]
        Q7 = out[9 + 6]
        Q9 = out[9 + 8]
        X = S3
        Y = S7
        G = Q5
        Z = (1 - Q7) | (S3 & S7 & Q9)
        assert (X, Y, Z, G) == (state.X, state.Y, state.Z, state.G)

    # Raw-query minima from Experiment 198.
    assert minimum_observer_subsets(
        states, lambda s: (s.X, s.Y, s.p)
    )[0] == 3
    assert minimum_observer_subsets(
        states, lambda s: (s.x, s.y, s.p)
    )[0] == 4
    assert minimum_observer_subsets(
        states, lambda s: (s.X, s.Y, s.Z, s.G)
    )[0] == 5

    # First recursion and route state.
    expected_first = {
        0: ("102", "002", "120"),
        1: ("102", "012", "100"),
        2: ("102", "022", "100"),
    }
    expected_route = {0: "120", 1: "012", 2: "102"}

    first_families = set()
    for state in states:
        outputs = tuple(decode_dash_one_hot(selected_surface(state, q)) for q in range(3))
        assert outputs == expected_first[state.p]
        first_families.add(outputs)

        q = 2 - state.p
        assert outputs[q] == expected_route[state.p]

        terminal = terminal_surface(state)
        assert decode_dash_one_hot(terminal) == "100"
        assert surface_serial_word(terminal) == "---//////"

    assert len(first_families) == 3

    # S3 / T3 algebraic characterization.
    sigma = (1, 2, 0)      # 120
    tau = (1, 0, 2)        # 102
    terminal_map = (1, 0, 0)  # 100

    s3 = closure({sigma, tau})
    assert len(s3) == 6
    assert all(map_rank(mapping) == 3 for mapping in s3)

    t3 = closure({sigma, tau, terminal_map})
    assert len(t3) == 27
    rank_counts = Counter(map_rank(mapping) for mapping in t3)
    assert rank_counts == Counter({2: 18, 3: 6, 1: 3})

    # Terminal 100 is the p-order derangement indicator.
    granted = {
        0: (1, 2, 0),
        1: (0, 1, 2),
        2: (1, 0, 2),
    }
    derangement_indicator = tuple(
        int(all(mapping[i] != i for i in range(3)))
        for _p, mapping in sorted(granted.items())
    )
    assert derangement_indicator == terminal_map

    print("OK: 14 legal four-bit physical states")
    print("OK: all 14 complete masters are distinct")
    print("OK: 82 physical stickers / 65 H108 residues match every legal master")
    print("OK: exact 95 invariant / 13 variable residue split")
    print("OK: global 54/36/18 symbol census")
    print("OK: latent register weight 6, d_min=2")
    print("OK: frozen observer recovers optimal XYZG state")
    print("OK: raw observer minima 3 / 4 / 5")
    print("OK: first recursion has rank 3 in hidden-state dependence")
    print("OK: second selector reuse terminates at frame9 / 100 / ---//////")
    print("OK: S3 route algebra and 27-map T3 closure")


if __name__ == "__main__":
    main()
