#!/usr/bin/env python3
"""Experiment 298: exhaustive audit of the historical Discord Column Shift Tool.

The historical HTML transform is frozen under archive/discord/2026-09-29/.
This script reimplements only that transform and evaluates four structural scores
chosen before inspecting winners:

1. orthogonal coherence: equal known R/G neighbors at distance 1;
2. 3x3 purity: majority-symbol count summed over the nine 3x3 blocks;
3. 180-degree agreement: equal known R/G cells under half-turn pairing;
4. period-3 agreement: equal known R/G cells separated by three rows/columns.

Unknown cells are ignored by every score.  The tail-derived admissible family is
enumerated exhaustively (65,536 vectors).  Exact score distributions for the
full unrestricted 8^9 shift family are computed by dynamic programming /
factorization, so no Monte Carlo null is needed.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
import math

GRID = [
    ["G","K","G","R","R","G","K","G","K"],
    ["G","R","K","R","G","R","G","K","G"],
    ["R","R","G","R","K","R","R","K","R"],
    ["K","K","G","G","R","G","K","K","K"],
    ["G","R","G","G","G","K","G","G","R"],
    ["K","G","G","G","K","K","R","K","R"],
    ["K","K","G","R","K","G","G","K","K"],
    ["G","K","G","G","K","K","G","R","R"],
    ["R","K","R","R","G","K","G","G","G"],
    ["G","K","K","K","Y","G","K","K","Y"],
    ["Y","K","Y","K","K","Y","G","Y","Y"],
    ["K","K","K","G","K","K","K","K","K"],
]

NCOLS = 9
NROWS_TOP = 9


def bottom_bits(c: int) -> list[int | None]:
    out: list[int | None] = []
    for r in range(9, 12):
        v = GRID[r][c]
        out.append(1 if v == "Y" else 0 if v == "G" else None)
    return out


def valid_shifts_for_column(c: int) -> list[int]:
    bits = bottom_bits(c)
    valid: list[int] = []
    for s in range(8):
        candidate = [(s >> 2) & 1, (s >> 1) & 1, s & 1]
        if all(observed is None or observed == proposed
               for observed, proposed in zip(bits, candidate)):
            valid.append(s)
    return valid


VALID = [valid_shifts_for_column(c) for c in range(NCOLS)]


def shifted_col(c: int, s: int) -> tuple[str, ...]:
    col = tuple(GRID[r][c] for r in range(NROWS_TOP))
    if s == 0:
        return col
    return col[-s:] + col[:-s]


STATES = {(c, s): shifted_col(c, s) for c in range(9) for s in range(8)}


def transformed_grid(shifts: tuple[int, ...]) -> list[list[str]]:
    return [[STATES[(c, shifts[c])][r] for c in range(9)] for r in range(9)]


def orthogonal_coherence(shifts: tuple[int, ...]) -> int:
    grid = transformed_grid(shifts)
    score = 0
    for r in range(9):
        for c in range(9):
            if grid[r][c] == "K":
                continue
            for dr, dc in ((0, 1), (1, 0)):
                rr, cc = r + dr, c + dc
                if rr < 9 and cc < 9 and grid[rr][cc] != "K":
                    score += grid[r][c] == grid[rr][cc]
    return score


def block_purity(shifts: tuple[int, ...]) -> int:
    grid = transformed_grid(shifts)
    score = 0
    for br in range(3):
        for bc in range(3):
            values = [
                grid[r][c]
                for r in range(br * 3, br * 3 + 3)
                for c in range(bc * 3, bc * 3 + 3)
                if grid[r][c] != "K"
            ]
            if values:
                counts = Counter(values)
                score += max(counts.values())
    return score


def half_turn_agreement(shifts: tuple[int, ...]) -> int:
    grid = transformed_grid(shifts)
    score = 0
    seen: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for r in range(9):
        for c in range(9):
            rr, cc = 8 - r, 8 - c
            key = tuple(sorted(((r, c), (rr, cc))))
            if key in seen:
                continue
            seen.add(key)
            a, b = grid[r][c], grid[rr][cc]
            if a != "K" and b != "K":
                score += a == b
    return score


def period3_agreement(shifts: tuple[int, ...]) -> int:
    grid = transformed_grid(shifts)
    score = 0
    for dr, dc in ((0, 3), (3, 0)):
        for r in range(9 - dr):
            for c in range(9 - dc):
                a, b = grid[r][c], grid[r + dr][c + dc]
                if a != "K" and b != "K":
                    score += a == b
    return score


SCORES = {
    "orthogonal_coherence": orthogonal_coherence,
    "block_3x3_purity": block_purity,
    "half_turn_agreement": half_turn_agreement,
    "period3_agreement": period3_agreement,
}


def counter_stats(counter: Counter[int]) -> dict[str, float | int]:
    n = sum(counter.values())
    mean = sum(score * count for score, count in counter.items()) / n
    variance = sum((score - mean) ** 2 * count for score, count in counter.items()) / n
    return {
        "n": n,
        "mean": mean,
        "sd": math.sqrt(variance),
        "min": min(counter),
        "max": max(counter),
    }


def convolve(a: Counter[int], b: Counter[int]) -> Counter[int]:
    out: Counter[int] = Counter()
    for x, cx in a.items():
        for y, cy in b.items():
            out[x + y] += cx * cy
    return out


def unrestricted_orthogonal_distribution() -> Counter[int]:
    def vertical(c: int, s: int) -> int:
        col = STATES[(c, s)]
        return sum(col[r] != "K" and col[r + 1] != "K" and col[r] == col[r + 1]
                   for r in range(8))

    def horizontal(c: int, left: int, right: int) -> int:
        a, b = STATES[(c, left)], STATES[(c + 1, right)]
        return sum(a[r] != "K" and b[r] != "K" and a[r] == b[r] for r in range(9))

    dp = {s: Counter({vertical(0, s): 1}) for s in range(8)}
    for c in range(1, 9):
        nxt = {s: Counter() for s in range(8)}
        for s in range(8):
            for previous, dist in dp.items():
                add = horizontal(c - 1, previous, s) + vertical(c, s)
                for score, count in dist.items():
                    nxt[s][score + add] += count
        dp = nxt
    out: Counter[int] = Counter()
    for dist in dp.values():
        out.update(dist)
    return out


def purity_for_three_columns(columns: tuple[int, int, int], shifts: tuple[int, int, int]) -> int:
    cols = [STATES[(c, s)] for c, s in zip(columns, shifts)]
    score = 0
    for br in range(3):
        values = [
            col[r]
            for col in cols
            for r in range(br * 3, br * 3 + 3)
            if col[r] != "K"
        ]
        if values:
            score += max(Counter(values).values())
    return score


def unrestricted_purity_distribution() -> Counter[int]:
    parts: list[Counter[int]] = []
    for columns in ((0, 1, 2), (3, 4, 5), (6, 7, 8)):
        parts.append(Counter(
            purity_for_three_columns(columns, shifts)
            for shifts in product(range(8), repeat=3)
        ))
    return convolve(convolve(parts[0], parts[1]), parts[2])


def mirror_pair(c1: int, s1: int, c2: int, s2: int) -> int:
    a, b = STATES[(c1, s1)], STATES[(c2, s2)]
    return sum(a[r] != "K" and b[8 - r] != "K" and a[r] == b[8 - r]
               for r in range(9))


def unrestricted_half_turn_distribution() -> Counter[int]:
    parts: list[Counter[int]] = []
    for c1, c2 in ((0, 8), (1, 7), (2, 6), (3, 5)):
        parts.append(Counter(
            mirror_pair(c1, s1, c2, s2)
            for s1 in range(8)
            for s2 in range(8)
        ))
    center = Counter()
    for s in range(8):
        col = STATES[(4, s)]
        center[sum(col[r] != "K" and col[8-r] != "K" and col[r] == col[8-r]
                   for r in range(5))] += 1
    parts.append(center)
    out = parts[0]
    for part in parts[1:]:
        out = convolve(out, part)
    return out


def unrestricted_period3_distribution() -> Counter[int]:
    def vertical3(c: int, s: int) -> int:
        col = STATES[(c, s)]
        return sum(col[r] != "K" and col[r + 3] != "K" and col[r] == col[r + 3]
                   for r in range(6))

    def horizontal3(c: int, s1: int, s2: int) -> int:
        a, b = STATES[(c, s1)], STATES[(c + 3, s2)]
        return sum(a[r] != "K" and b[r] != "K" and a[r] == b[r] for r in range(9))

    parts: list[Counter[int]] = []
    for columns in ((0, 3, 6), (1, 4, 7), (2, 5, 8)):
        dist: Counter[int] = Counter()
        for shifts in product(range(8), repeat=3):
            score = sum(vertical3(c, s) for c, s in zip(columns, shifts))
            score += horizontal3(columns[0], shifts[0], shifts[1])
            score += horizontal3(columns[1], shifts[1], shifts[2])
            dist[score] += 1
        parts.append(dist)
    return convolve(convolve(parts[0], parts[1]), parts[2])


NULLS = {
    "orthogonal_coherence": unrestricted_orthogonal_distribution,
    "block_3x3_purity": unrestricted_purity_distribution,
    "half_turn_agreement": unrestricted_half_turn_distribution,
    "period3_agreement": unrestricted_period3_distribution,
}


def main() -> None:
    admissible_count = math.prod(len(values) for values in VALID)
    assert [len(values) for values in VALID] == [2, 8, 4, 4, 4, 2, 4, 4, 2]
    assert admissible_count == 65536

    admissible_distributions = {name: Counter() for name in SCORES}
    winners = {name: [] for name in SCORES}

    for shifts in product(*VALID):
        shifts = tuple(shifts)
        for name, score_fn in SCORES.items():
            score = score_fn(shifts)
            admissible_distributions[name][score] += 1

    result = {
        "admissible_shift_options": VALID,
        "admissible_count": admissible_count,
        "unrestricted_count": 8 ** 9,
        "scores": {},
    }

    for name, dist in admissible_distributions.items():
        best = max(dist)
        winning_vectors = []
        for shifts in product(*VALID):
            shifts = tuple(shifts)
            if SCORES[name](shifts) == best:
                winning_vectors.append(list(shifts))
                if len(winning_vectors) >= 12:
                    break

        null = NULLS[name]()
        assert sum(null.values()) == 8 ** 9
        tail_count = sum(count for score, count in null.items() if score >= best)
        tail_fraction = tail_count / (8 ** 9)
        any_in_65536 = 1.0 - (1.0 - tail_fraction) ** admissible_count

        result["scores"][name] = {
            "admissible": counter_stats(dist),
            "admissible_best": best,
            "admissible_best_count": dist[best],
            "example_best_vectors": winning_vectors,
            "unrestricted": counter_stats(null),
            "unrestricted_tail_at_or_above_admissible_best": tail_fraction,
            "chance_at_least_one_such_score_in_65536_unrestricted_draws": any_in_65536,
        }

    expected = {
        "orthogonal_coherence": (40, 42),
        "block_3x3_purity": (41, 42),
        "half_turn_agreement": (16, 17),
        "period3_agreement": (39, 41),
    }
    for name, (admissible_best, unrestricted_best) in expected.items():
        assert result["scores"][name]["admissible_best"] == admissible_best
        assert result["scores"][name]["unrestricted"]["max"] == unrestricted_best

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
