#!/usr/bin/env python3
"""Verify core closed-corpus invariants for GRA-EDISNI.

This intentionally uses only the Python standard library. It should fail loudly
if the compact repository state drifts away from the canonical machine.
"""

from itertools import combinations, product


LEGAL_FUNCTIONAL = [
    (1, 0, 1),
    (1, 1, 1),
    (1, 2, 0),
    (2, 0, 2),
    (2, 1, 2),
    (2, 2, 0),
    (2, 2, 2),
]


def physical_states():
    return [(*state, g) for state in LEGAL_FUNCTIONAL for g in (0, 2)]


def latent_register(state):
    x, y, p, g = state
    return {
        22: int(x == 2),
        25: int(x != 2),
        55: int(y == 0),
        58: int(y == 1),
        61: int(y == 2),
        84: int(g == 2),
        102: int(g == 0),
        100: int(p == 0),
        91: int(p != 0),
        94: int(p == 1),
        103: int(p != 1),
        88: int(p == 2),
        106: int(p != 2),
    }


def observer(state):
    x, y, p, g = state
    X = int(x == 2)
    Y = int(y == 2)
    G = int(g == 2)
    P0 = int(p == 0)
    Y1 = int(y == 1)

    same_quarter = (0, 0, X, 1, 0, 0, Y, 0, 0)
    q4_target = (0, 0, X & Y & P0, 1, G, P0, 1 - Y1, 1, 1 - P0)
    return same_quarter + q4_target


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
                previous = seen.get(key)
                if previous is not None and previous != target:
                    valid = False
                    break
                seen[key] = target
            if valid:
                winners.append(indices)
        if winners:
            return size, winners
    raise AssertionError("no observer subset separates target states")


def compose(f, g):
    """Return f after g, with maps encoded as tuples of outputs for 0,1,2."""
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


def rank(mapping):
    return len(set(mapping))


def main():
    states = physical_states()
    assert len(states) == 14
    assert len(set(states)) == 14

    # Arbiter relation.
    expected = {
        (0, 0): {1},
        (0, 1): {0},
        (1, 0): {2},
        (1, 1): {0, 2},
    }
    actual = {}
    for x, y, p, _g in states:
        key = (int(x == 2), int(y == 2))
        actual.setdefault(key, set()).add(p)
    assert actual == expected

    # Latent register: exact size, constant weight, minimum distance 2.
    codes = [latent_register(state) for state in states]
    assert len({tuple(code.items()) for code in codes}) == 14
    assert all(sum(code.values()) == 6 for code in codes)

    def hamming(a, b):
        return sum(a[k] != b[k] for k in a)

    minimum_distance = min(hamming(a, b) for a, b in combinations(codes, 2))
    assert minimum_distance == 2

    # Observer injectivity.
    observations = [observer(state) for state in states]
    assert len(set(observations)) == 14

    names = [f"S{i}" for i in range(1, 10)] + [f"Q{i}" for i in range(1, 10)]

    control_size, control_sets = minimum_observer_subsets(
        states, lambda s: (int(s[0] == 2), int(s[1] == 2), s[2])
    )
    functional_size, functional_sets = minimum_observer_subsets(
        states, lambda s: (s[0], s[1], s[2])
    )
    physical_size, physical_sets = minimum_observer_subsets(states, lambda s: s)

    assert control_size == 3
    assert functional_size == 4
    assert physical_size == 5

    expected_control = {
        ("S3", "S7", "Q3"),
        ("S3", "S7", "Q6"),
        ("S3", "S7", "Q9"),
    }
    expected_functional = {
        ("S3", "S7", "Q3", "Q7"),
        ("S3", "S7", "Q6", "Q7"),
        ("S3", "S7", "Q7", "Q9"),
    }
    expected_physical = {
        ("S3", "S7", "Q3", "Q5", "Q7"),
        ("S3", "S7", "Q5", "Q6", "Q7"),
        ("S3", "S7", "Q5", "Q7", "Q9"),
    }

    def named(subsets):
        return {tuple(names[i] for i in indices) for indices in subsets}

    assert named(control_sets) == expected_control
    assert named(functional_sets) == expected_functional
    assert named(physical_sets) == expected_physical

    # Route / terminal algebra.
    sigma = (1, 2, 0)  # 120
    tau = (1, 0, 2)    # 102
    terminal = (1, 0, 0)  # 100

    s3 = closure({sigma, tau})
    assert len(s3) == 6
    assert all(rank(mapping) == 3 for mapping in s3)

    t3 = closure({sigma, tau, terminal})
    assert len(t3) == 27

    rank_counts = {1: 0, 2: 0, 3: 0}
    for mapping in t3:
        rank_counts[rank(mapping)] += 1
    assert rank_counts == {1: 3, 2: 18, 3: 6}

    # Terminal is the p-order derangement indicator for granted route family.
    granted = {
        0: (1, 2, 0),  # 120
        1: (0, 1, 2),  # 012
        2: (1, 0, 2),  # 102
    }
    derangement_indicator = tuple(
        int(all(mapping[i] != i for i in range(3)))
        for _p, mapping in sorted(granted.items())
    )
    assert derangement_indicator == terminal

    print("OK: 14 physical states")
    print("OK: latent register is constant-weight (13,14,6), d_min=2")
    print("OK: frozen observer minima are 3 / 4 / 5 bits")
    print("OK: route shell generates S3")
    print("OK: route shell + terminal generates full T3 (27 maps)")
    print("OK: terminal 100 equals p-order derangement indicator")


if __name__ == "__main__":
    main()
