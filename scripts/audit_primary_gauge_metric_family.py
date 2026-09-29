#!/usr/bin/env python3
"""Experiment 283: test primary-gauge transport across a metric continuum.

Experiment 282 selects the zero primary gauge by Manhattan transport between
neighboring primary frames. To test whether that result depends on one chosen
distance formula, let a diagonal token move cost lambda in [1,2], while an
orthogonal move costs 1.

lambda=1 is Chebyshev-like: a diagonal is as cheap as an orthogonal step.
lambda=2 is Manhattan: a diagonal costs two orthogonal steps.

For each pair of three-cell frames, minimum matching cost is the lower envelope
of six affine functions A + B*lambda. We enumerate all matching-line
intersections, partition [1,2] exactly using Fractions, and determine the
aggregate gauge winner on every open interval plus every breakpoint.

No POS3 occupancy, selector, recursion output, or terminal enters the score.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

from audit_primary_gauge_transport import (
    apply_gauge,
    canonical_frames,
    lattice_edges,
)


SETTINGS = tuple(product((False, True), repeat=2))
XY = tuple(product((1, 2), (0, 1, 2)))


def move_coeff(left, right):
    dr = abs(left[0] - right[0])
    dc = abs(left[1] - right[1])
    diagonal = min(dr, dc)
    axial = max(dr, dc) - diagonal
    return axial, diagonal


def matching_lines(left, right):
    left = tuple(left)
    right = tuple(right)
    result = set()
    for perm in permutations(right):
        axial = 0
        diagonal = 0
        for a, b in zip(left, perm):
            aa, dd = move_coeff(a, b)
            axial += aa
            diagonal += dd
        result.add((axial, diagonal))
    return tuple(sorted(result))


def line_value(line, lam):
    axial, diagonal = line
    return Fraction(axial) + Fraction(diagonal) * lam


def edge_cost(left, right, lam):
    return min(line_value(line, lam) for line in matching_lines(left, right))


def aggregate_cost(setting, lam):
    total = Fraction(0)
    for x, y in XY:
        frames = apply_gauge(canonical_frames(x, y), *setting)
        total += sum(
            edge_cost(frames[a], frames[b], lam)
            for a, b in lattice_edges()
        )
    return total


def breakpoints():
    points = {Fraction(1), Fraction(2)}
    for setting in SETTINGS:
        for x, y in XY:
            frames = apply_gauge(canonical_frames(x, y), *setting)
            for a, b in lattice_edges():
                lines = matching_lines(frames[a], frames[b])
                for l1 in lines:
                    for l2 in lines:
                        a1, b1 = l1
                        a2, b2 = l2
                        if b1 == b2:
                            continue
                        lam = Fraction(a2 - a1, b1 - b2)
                        if Fraction(1) <= lam <= Fraction(2):
                            points.add(lam)
    return tuple(sorted(points))


def winners_at(lam):
    costs = {setting: aggregate_cost(setting, lam) for setting in SETTINGS}
    best = min(costs.values())
    return costs, {
        setting
        for setting, value in costs.items()
        if value == best
    }


def main() -> None:
    points = breakpoints()

    # Check every exact breakpoint and one exact rational sample inside each
    # interval. Lower envelopes cannot change winner between breakpoints.
    tests = list(points)
    tests.extend(
        (left + right) / 2
        for left, right in zip(points, points[1:])
    )
    tests = tuple(sorted(set(tests)))

    zero = (False, False)
    endpoint_tie = {(False, False), (False, True)}

    for lam in tests:
        _costs, winners = winners_at(lam)
        if lam == 1:
            assert winners == endpoint_tie
        else:
            assert winners == {zero}

    costs1, _ = winners_at(Fraction(1))
    costs2, _ = winners_at(Fraction(2))
    assert costs1 == {
        (False, False): 158,
        (False, True): 158,
        (True, False): 170,
        (True, True): 170,
    }
    assert costs2 == {
        (False, False): 172,
        (False, True): 196,
        (True, False): 196,
        (True, True): 220,
    }

    print("Experiment 283")
    print("metric breakpoints in [1,2]:", [str(point) for point in points])
    print("exact tests:", len(tests))
    print("lambda=1 costs:", costs1)
    print("lambda=2 costs:", costs2)
    print("RESULT: zero gauge is uniquely minimum for every lambda in (1,2]")
    print("RESULT: at lambda=1 only the q1,d1 gauge flip becomes tied")
    print("RESULT: q0,d0 gauge flip is rejected across the entire metric family")
    print("CAUTION: geometric transport remains an authoring prior, not a raw observation")


if __name__ == "__main__":
    main()
