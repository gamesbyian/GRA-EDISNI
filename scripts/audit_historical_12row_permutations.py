#!/usr/bin/env python3
"""Experiment 347: exact historical 12-row permutation audit."""

from __future__ import annotations

import csv
import os
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / os.environ.get("GRA_EDISNI_OBSERVATIONS_FILE", "data/observations.csv")
OUT = ROOT / "data" / "experiment-347-historical-12row-permutation-audit.json"
N = 12
FULL = (1 << N) - 1
SAMPLE_CAP = 20


def load_rows():
    rows = [["?"] * 9 for _ in range(N)]
    dot_rows = set()
    with OBS.open(newline="", encoding="utf-8") as fh:
        for rec in csv.DictReader(fh):
            residue = int(rec["residue"])
            symbol = rec["symbol"]
            r = (residue - 1) // 9
            c = (residue - 1) % 9
            old = rows[r][c]
            if old != "?" and old != symbol:
                raise AssertionError(f"conflict at residue {residue}: {old} vs {symbol}")
            rows[r][c] = symbol
            if symbol == ".":
                dot_rows.add(r)
    return rows, tuple(sorted(dot_rows))


def edge_score(a, b):
    match = mismatch = known = 0
    for x, y in zip(a, b):
        if x == "?" or y == "?":
            continue
        known += 1
        if x == y:
            match += 1
        else:
            mismatch += 1
    return match - mismatch, match, mismatch, known


def path_score(order, w):
    return sum(w[a][b] for a, b in zip(order, order[1:]))


def exact_distribution(w):
    dp = {}
    for last in range(N):
        dp[(1 << last, last)] = Counter({0: 1})
    for size in range(1, N):
        current = [(k, v) for k, v in dp.items() if k[0].bit_count() == size]
        for (mask, last), hist in current:
            for nxt in range(N):
                bit = 1 << nxt
                if mask & bit:
                    continue
                key = (mask | bit, nxt)
                dest = dp.setdefault(key, Counter())
                delta = w[last][nxt]
                for score, count in hist.items():
                    dest[score + delta] += count
    total = Counter()
    for last in range(N):
        total.update(dp[(FULL, last)])
    return total


def max_dp_by_start(w):
    all_start = {}
    for start in range(N):
        best = {(1 << start, start): (0, 1)}
        for size in range(1, N):
            states = [(k, v) for k, v in best.items() if k[0].bit_count() == size]
            for (mask, last), (score, count) in states:
                for nxt in range(N):
                    bit = 1 << nxt
                    if mask & bit:
                        continue
                    key = (mask | bit, nxt)
                    cand = score + w[last][nxt]
                    if key not in best or cand > best[key][0]:
                        best[key] = (cand, count)
                    elif cand == best[key][0]:
                        best[key] = (cand, best[key][1] + count)
        all_start[start] = best
    return all_start


def sample_max_paths(w, global_max, dp_by_start):
    out = []
    for start in range(N):
        best = dp_by_start[start]
        for end in range(N):
            state = (FULL, end)
            if state not in best or best[state][0] != global_max:
                continue

            @lru_cache(maxsize=None)
            def backtrack(mask, last):
                if mask == (1 << start) and last == start:
                    return ((start,),)
                target = best[(mask, last)][0]
                prev_mask = mask ^ (1 << last)
                paths = []
                for prev in range(N):
                    if not (prev_mask & (1 << prev)):
                        continue
                    prev_state = (prev_mask, prev)
                    if prev_state not in best:
                        continue
                    if best[prev_state][0] + w[prev][last] != target:
                        continue
                    for p in backtrack(prev_mask, prev):
                        paths.append(p + (last,))
                        if len(paths) >= SAMPLE_CAP:
                            return tuple(paths)
                return tuple(paths)

            for p in backtrack(FULL, end):
                out.append(p)
                if len(out) >= SAMPLE_CAP:
                    return out
    return out


def main():
    rows, dot_rows = load_rows()
    assert dot_rows == (9, 10), f"historical endpoint prereg expected exactly rows 10/11, got {dot_rows}"

    details = [[None] * N for _ in range(N)]
    w = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            s, m, mm, k = edge_score(rows[i], rows[j])
            w[i][j] = w[j][i] = s
            details[i][j] = details[j][i] = {"net": s, "matches": m, "mismatches": mm, "known": k}

    canonical = tuple(range(N))
    canonical_score = path_score(canonical, w)

    hist = exact_distribution(w)
    assert sum(hist.values()) == 479001600
    global_max = max(hist)
    exact_max_count = hist[global_max]
    tail_ge_canonical = sum(count for score, count in hist.items() if score >= canonical_score)

    dp_by_start = max_dp_by_start(w)
    max_from_dp = max(
        dp_by_start[start][(FULL, end)][0]
        for start in range(N)
        for end in range(N)
        if (FULL, end) in dp_by_start[start]
    )
    assert max_from_dp == global_max

    dot_endpoint_max_count = 0
    for start in dot_rows:
        end = dot_rows[1] if start == dot_rows[0] else dot_rows[0]
        state = (FULL, end)
        if state in dp_by_start[start] and dp_by_start[start][state][0] == global_max:
            dot_endpoint_max_count += dp_by_start[start][state][1]

    samples = sample_max_paths(w, global_max, dp_by_start)

    result = {
        "experiment": 347,
        "input": "data/observations.csv",
        "row_definition": "twelve consecutive 9-residue rows of H108",
        "known_counts_by_row": [sum(x != "?" for x in row) for row in rows],
        "observed_dot_rows_1_based": [r + 1 for r in dot_rows],
        "canonical_order_1_based": [i + 1 for i in canonical],
        "canonical_score": canonical_score,
        "score_min": min(hist),
        "score_max": global_max,
        "exact_max_order_count_directed": exact_max_count,
        "max_orders_with_dot_rows_as_both_endpoints_directed": dot_endpoint_max_count,
        "max_dot_endpoint_fraction": dot_endpoint_max_count / exact_max_count,
        "fraction_all_orders_scoring_at_least_canonical": tail_ge_canonical / 479001600,
        "exact_score_histogram": {str(k): hist[k] for k in sorted(hist)},
        "sample_max_orders_1_based": [[x + 1 for x in p] for p in samples],
        "adjacency_net_matrix": w,
        "interpretation_guardrail": "optimized orders are not semantic evidence without independent agreement; historical dot-row endpoint criterion was frozen before analysis"
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
