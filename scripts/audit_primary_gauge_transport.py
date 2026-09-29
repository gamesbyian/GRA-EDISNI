#!/usr/bin/env python3
"""Experiment 282: select the primary completion gauge by local transport.

Experiment 280 exposes two transition-invisible physical gauge bits:
  * q0,d0: move the fixed minority pulse H -> F;
  * q1,d1: move the fixed minority pulse I -> E.

All four gauge settings reproduce the same 14->3->1 transducer, so recursion
cannot choose among them.

This experiment tests an independent physical authoring criterion on the
3x3 lattice of primary frames. Treat each frame's three minority cells as
indistinguishable tokens. For two neighboring (q,d) frames, define transport
cost as the minimum total Manhattan distance required to match the three
tokens between frames.

For each gauge-sensitive frame, compare its summed transport to its orthogonal
neighbors. Also sum transport over every edge of the 3x3 (q,d) frame lattice,
across all six raw primary (x,y) payloads.

No column-occupancy/POS3 condition, selector value, recursion output, terminal,
or hidden-state label enters the score.
"""

from __future__ import annotations

from itertools import permutations, product



def cells_from_word(word):
    return frozenset((int(row), col) for col, row in enumerate(word))


def canonical_frames(x, y):
    words = (
        ("112", "212", f"0{x}0"),
        ("212", "002", "100"),
        (f"1{y}2", "022", "100"),
    )
    return {
        (q, d): cells_from_word(words[q][d])
        for q in range(3)
        for d in range(3)
    }


def apply_gauge(frames, flip_q0d0, flip_q1d1):
    result = dict(frames)

    if flip_q0d0:
        changed = set(result[(0, 0)])
        changed.remove((2, 2))  # H
        changed.add((2, 0))     # F
        result[(0, 0)] = frozenset(changed)

    if flip_q1d1:
        changed = set(result[(1, 1)])
        changed.remove((0, 0))  # I
        changed.add((1, 2))     # E
        result[(1, 1)] = frozenset(changed)

    return result


def transport(left, right):
    left = tuple(left)
    right = tuple(right)
    assert len(left) == len(right) == 3
    return min(
        sum(
            abs(r1 - r2) + abs(c1 - c2)
            for (r1, c1), (r2, c2) in zip(left, perm)
        )
        for perm in permutations(right)
    )


def neighbors(frame):
    q, d = frame
    result = []
    for dq, dd in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        other = (q + dq, d + dd)
        if 0 <= other[0] < 3 and 0 <= other[1] < 3:
            result.append(other)
    return tuple(result)


def local_cost(frames, frame):
    return sum(
        transport(frames[frame], frames[other])
        for other in neighbors(frame)
    )


def lattice_edges():
    edges = []
    for q in range(3):
        for d in range(3):
            if q < 2:
                edges.append(((q, d), (q + 1, d)))
            if d < 2:
                edges.append(((q, d), (q, d + 1)))
    return tuple(edges)


def total_cost(frames):
    return sum(
        transport(frames[left], frames[right])
        for left, right in lattice_edges()
    )


def main() -> None:
    settings = tuple(product((False, True), repeat=2))
    xy = tuple(product((1, 2), (0, 1, 2)))

    local_q0d0 = {}
    local_q1d1 = {}
    totals = {}

    for setting in settings:
        g0, g1 = setting
        local0_values = set()
        local1_values = set()
        total_values = []

        for x, y in xy:
            frames = apply_gauge(canonical_frames(x, y), g0, g1)
            local0_values.add(local_cost(frames, (0, 0)))
            local1_values.add(local_cost(frames, (1, 1)))
            total_values.append(total_cost(frames))

        # Gauge-local costs are independent of x/y because the changed frames
        # touch only fixed neighboring payload structure.
        assert len(local0_values) == 1
        assert len(local1_values) == 1
        local_q0d0[setting] = next(iter(local0_values))
        local_q1d1[setting] = next(iter(local1_values))
        totals[setting] = tuple(total_values)

    assert local_q0d0[(False, False)] == 2
    assert local_q0d0[(False, True)] == 2
    assert local_q0d0[(True, False)] == 6
    assert local_q0d0[(True, True)] == 6

    assert local_q1d1[(False, False)] == 11
    assert local_q1d1[(True, False)] == 11
    assert local_q1d1[(False, True)] == 15
    assert local_q1d1[(True, True)] == 15

    aggregate = {
        setting: sum(values)
        for setting, values in totals.items()
    }
    assert aggregate == {
        (False, False): 172,
        (False, True): 196,
        (True, False): 196,
        (True, True): 220,
    }

    best = min(aggregate.values())
    assert {
        setting
        for setting, value in aggregate.items()
        if value == best
    } == {(False, False)}

    print("Experiment 282")
    print("q0,d0 local transport by gauge:", local_q0d0)
    print("q1,d1 local transport by gauge:", local_q1d1)
    print("aggregate adjacent-frame transport:", aggregate)
    print("RESULT: each gauge flip independently increases local frame-lattice transport by 4")
    print("RESULT: the canonical all-POS3 gauge is the unique minimum-transport representative")
    print("CAUTION: transport smoothness is an authoring-simplicity prior, not a raw observation")


if __name__ == "__main__":
    main()
