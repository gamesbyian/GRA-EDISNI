#!/usr/bin/env python3
"""Experiment 247: audit the sole unresolved primary frame-polarity bit.

Experiment 246 leaves one frame polarity unresolved directly by raw stickers:
    q=1, d=2

This audit declares a bounded parent family before selecting the completion:
    polarity(q,d) = [a*q + b*d + c >= 0]

with small integer coefficients. Primitive coefficient triples are deduplicated
by positive gcd. Complexity is L1 coefficient cost |a|+|b|+|c|.

The eight corpus-forced frame polarities are the only fit constraints.
"""

from __future__ import annotations

from math import gcd

FORCED = {
    (0, 0): 1,
    (0, 1): 0,
    (0, 2): 0,
    (1, 0): 1,
    (1, 1): 1,
    (2, 0): 1,
    (2, 1): 1,
    (2, 2): 1,
}
AMBIGUOUS = (1, 2)


def primitive(a: int, b: int, c: int) -> tuple[int, int, int]:
    divisor = gcd(gcd(abs(a), abs(b)), abs(c))
    if divisor == 0:
        return a, b, c
    return a // divisor, b // divisor, c // divisor


def value(coeffs, q: int, d: int) -> int:
    a, b, c = coeffs
    return int(a * q + b * d + c >= 0)


def cost(coeffs) -> int:
    return sum(abs(v) for v in coeffs)


def main() -> None:
    candidates = {}
    for a in range(-4, 5):
        for b in range(-4, 5):
            for c in range(-8, 9):
                if a == 0 and b == 0:
                    continue
                coeffs = primitive(a, b, c)
                if coeffs in candidates:
                    continue
                if all(value(coeffs, q, d) == expected for (q, d), expected in FORCED.items()):
                    candidates[coeffs] = value(coeffs, *AMBIGUOUS)

    assert set(candidates.values()) == {0, 1}

    by_completion = {
        completion: sorted(
            (cost(coeffs), coeffs)
            for coeffs, result in candidates.items()
            if result == completion
        )
        for completion in (0, 1)
    }

    current = by_completion[0]
    alternate = by_completion[1]

    assert current[0] == (2, (1, -1, 0))
    assert alternate[0] == (3, (2, -1, 0))

    # The current staircase is the sole primitive threshold rule at global
    # minimum cost among all rules fitting the eight observed polarities.
    global_min = min(cost_value for cost_value, _coeffs in current + alternate)
    global_winners = [
        (coeffs, completion)
        for coeffs, completion in candidates.items()
        if cost(coeffs) == global_min
    ]
    assert global_min == 2
    assert global_winners == [((1, -1, 0), 0)]

    print("Experiment 247")
    print(f"primitive threshold rules fitting 8 forced frames: {len(candidates)}")
    print(
        "current completion q=1,d=2 -> slash minority:",
        f"best={current[0][1]} cost={current[0][0]}",
    )
    print(
        "alternate completion q=1,d=2 -> dash minority:",
        f"best={alternate[0][1]} cost={alternate[0][0]}",
    )
    print("OK: current completion is unique minimum-L1 threshold rule")
    print("OK: minimum rule is q-d>=0, exactly d<=q")


if __name__ == "__main__":
    main()
