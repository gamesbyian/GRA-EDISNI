#!/usr/bin/env python3
"""Adversarial stability audit for the 534brn A/B/P alignment.

Shows that Experiment 337's 238 recovered positions are *conditional on
an edit-distance tie-breaking convention*. Reuses the original normalization
and source data, but varies only tie priorities or the fixed anchor length.

Run: python scripts/audit_534brn_alignment_sensitivity.py
No network; source inputs and the baseline mask are committed under this repo.
"""
from __future__ import annotations
import json
from pathlib import Path
from audit_534brn_loss_map import tokenize, find_ascii, UNKNOWN, TERMINAL
from rebuild_534brn_partial_evidence import CAPTURE, INPUTS, git_blob_sha

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data/534brn-alignment-sensitivity-2026-10-08.json"


def anchor_pairs(left, right, width):
    positions = {}
    for j in range(len(right) - width + 1):
        key = tuple(right[j:j + width])
        if UNKNOWN not in key:
            positions.setdefault(key, []).append(j)
    raw = []
    for i in range(len(left) - width + 1):
        key = tuple(left[i:i + width])
        if UNKNOWN in key:
            continue
        js = positions.get(key, [])
        if len(js) == 1:
            raw.append((i, js[0]))
    result = []
    prev_i = prev_j = -width
    for i, j in raw:
        if i >= prev_i + width and j >= prev_j + width:
            result.append((i, j))
            prev_i, prev_j = i, j
    return result


def edit_gap(left, right, tie):
    n, m = len(left), len(right)
    directions = [bytearray(m + 1) for _ in range(n + 1)]
    previous = list(range(m + 1))
    current = [0] * (m + 1)
    for j in range(1, m + 1):
        directions[0][j] = 2
    for i in range(1, n + 1):
        current[0] = i
        directions[i][0] = 1
        for j in range(1, m + 1):
            a, b = left[i-1], right[j-1]
            sub = previous[j-1] + (0 if a == UNKNOWN or b == UNKNOWN or a == b else 3)
            up = previous[j] + 1
            direction = 0
            if up < sub or (tie == "up" and up == sub):
                sub, direction = up, 1
            across = current[j-1] + 1
            if across < sub or (tie == "left" and across == sub):
                sub, direction = across, 2
            current[j], directions[i][j] = sub, direction
        previous, current = current, previous
    i, j = n, m
    result = []
    while i or j:
        d = directions[i][j]
        if i and j and d == 0:
            i -= 1
            j -= 1
            result.append((i, j))
        elif i and (not j or d == 1):
            i -= 1
            result.append((i, -1))
        else:
            j -= 1
            result.append((-1, j))
    result.reverse()
    return result


def match_map(left, right, ls, le, rs, re, width, tie):
    L, R = left[ls:le], right[rs:re]
    anchors = [(i, j) for i, j in anchor_pairs(L, R, width)
               if i + width < len(L) - len(TERMINAL)
               and j + width < len(R) - len(TERMINAL)]
    anchors.append((len(L) - len(TERMINAL), len(R) - len(TERMINAL)))
    out = {}
    li = ri = 0
    for a, b in anchors:
        for i, j in edit_gap(L[li:a], R[ri:b], tie):
            if i >= 0 and j >= 0:
                out[rs + ri + j] = ls + li + i
        take = len(TERMINAL) if a == len(L) - len(TERMINAL) else width
        for j in range(take):
            out[rs + b + j] = ls + a + j
        li, ri = a + take, b + take
    return out


def audit():
    blobs = {}
    for label in ("A", "B", "P"):
        name, sha, expected_size = INPUTS[label]
        raw = (CAPTURE / name).read_bytes()
        assert len(raw) == expected_size and git_blob_sha(raw) == sha
        blobs[label] = tokenize(raw, label)
    A, B, P = (blobs[k] for k in ("A", "B", "P"))
    aj, bj = find_ascii(A, b"JFIF"), find_ascii(B, b"JFIF")
    ae = find_ascii(A, TERMINAL) + len(TERMINAL)
    be = find_ascii(B, TERMINAL) + len(TERMINAL)
    pe = find_ascii(P, TERMINAL) + len(TERMINAL)
    cases = (("baseline", 12, "diagonal"),
             ("up_tiebreak", 12, "up"), ("left_tiebreak", 12, "left"),
             ("10wide", 10, "diagonal"), ("14wide", 14, "diagonal"))
    results = {}
    candidates = {}
    for name, width, tie in cases:
        mA = match_map(A, B, aj, ae, bj, be, width, tie)
        mP = match_map(P, B, 0, pe, 7387, be, width, tie)
        chosen, conflicts = {}, 0
        for idx in range(bj, be):
            if B[idx] != UNKNOWN:
                continue
            av = A[mA[idx]] if idx in mA else UNKNOWN
            pv = P[mP[idx]] if idx in mP else UNKNOWN
            if av != UNKNOWN and pv != UNKNOWN and av != pv:
                conflicts += 1
            elif av != UNKNOWN or pv != UNKNOWN:
                chosen[idx - bj] = av if av != UNKNOWN else pv
        candidates[name] = chosen
        results[name] = {"fills": len(chosen), "conflicts": conflicts,
                         "offsetsMappedA": len(mA), "offsetsMappedP": len(mP)}
    baseline = candidates["baseline"]
    stable = {pos: value for pos, value in baseline.items()
              if all(candidates[name].get(pos) == value for name, _, _ in cases)}
    changed = {name: sorted(pos for pos, value in baseline.items()
                            if candidates[name].get(pos) != value)
               for name, _, _ in cases[1:]}

    return {"cases": results,
            "baseline_recovered": len(baseline),
            "stable_across_five": len(stable),
            "variable_baseline": len(baseline) - len(stable),
            "changed_by_case": {name: len(pos) for name, pos in changed.items()},
            "stable_position_values_hex": [
                {"offset": pos, "hex": f"{value:02x}"} for pos, value in sorted(stable.items())],
            "changed_positions_by_case": changed}


def main():
    out = audit()
    fixed = json.loads(FROZEN.read_text(encoding="utf-8"))
    for key in ("cases", "baseline_recovered", "stable_across_five",
                "variable_baseline", "changed_by_case"):
        assert out[key] == fixed[key], (key, out[key], fixed[key])
    print(json.dumps(out, indent=2))
    print("PASS: reproduced all five adversarial alignment variants")


if __name__ == "__main__":
    main()
