#!/usr/bin/env python3
"""Exploratory CE banner orientation and row-order optimizer.

Only observed symbols contribute to scores. Spaces are never imputed.
This is an unfitted visual-continuity exercise, NOT a proposed decoder.
"""
import argparse
import csv
import json
import math
import random
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (3, 4, 6, 9, 12, 18, 27, 36)
PALETTE = {'/': '#41474e', '-': '#cb3936', '.': '#edbe31', ' ': '#fafafa'}


def master(include_045=False):
    base = json.loads((ROOT / 'data/discord-community-master-108.json').read_text())
    s = list(''.join(base['rows_12x9']))
    assert len(s) == 108
    for obs in csv.DictReader((ROOT / 'data/observations.csv').open()):
        i = int(obs['residue']) % 108
        assert s[i] in (' ', obs['symbol']), (i, s[i], obs['symbol'])
        s[i] = obs['symbol']
    assert sum(x != ' ' for x in s) == 66
    assert s[103] == '.' and s[45] == ' '
    if include_045:
        s[45] = '.'  # unconfirmed YouTube comment, never physical evidence
    return ''.join(s)


def rows_for(s, width):
    assert len(s) == 108 and 108 % width == 0
    return [s[i:i + width] for i in range(0, 108, width)]


def seam_matrix(rows):
    n = len(rows)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            v = 0
            for a, b in zip(rows[i], rows[j]):
                if a != ' ' and b != ' ':
                    v += 1 if a == b else -1
            matrix[i][j] = matrix[j][i] = v
    return matrix


def score(order, m):
    return sum(m[i][j] for i, j in zip(order, order[1:]))


def exact_path(m):
    """Held-Karp exact optimum for a symmetric Hamiltonian path, n<=12."""
    n = len(m)
    assert n <= 12
    dp = {(1 << i, i): (0, -1) for i in range(n)}
    for mask in range(1, 1 << n):
        for j in range(n):
            if not (mask & (1 << j)):
                continue
            old = dp.get((mask, j))
            if old is None:
                continue
            for k in range(n):
                if mask & (1 << k):
                    continue
                nxt = (mask | (1 << k), k)
                val = old[0] + m[j][k]
                if nxt not in dp or val > dp[nxt][0]:
                    dp[nxt] = (val, j)
    full = (1 << n) - 1
    j = max(range(n), key=lambda i: dp[(full, i)][0])
    val = dp[(full, j)][0]
    order = []
    mask = full
    while j != -1:
        order.append(j)
        prev = dp[(mask, j)][1]
        mask ^= 1 << j
        j = prev
    return val, order[::-1], True


def improve(order, m):
    """Deterministic 2-opt path improvement; differences computed at boundaries."""
    n = len(order)
    while True:
        improved = False
        for i in range(n - 1):
            for j in range(i + 1, n):
                old = new = 0
                if i:
                    old += m[order[i - 1]][order[i]]
                    new += m[order[i - 1]][order[j]]
                if j + 1 < n:
                    old += m[order[j]][order[j + 1]]
                    new += m[order[i]][order[j + 1]]
                if new > old:
                    order[i:j + 1] = reversed(order[i:j + 1])
                    improved = True
                    break
            if improved:
                break
        if not improved:
            return order


def heuristic_path(m, seed, restarts=12):
    n = len(m)
    rng = random.Random(seed)
    options = [list(range(n)), list(reversed(range(n)))]
    for start in range(n):
        used = {start}
        order = [start]
        while len(order) < n:
            choices = []
            for j in range(n):
                if j in used:
                    continue
                choices.append((m[j][order[0]], j, 0))
                choices.append((m[order[-1]][j], j, 1))
            _, j, side = max(choices)
            if side:
                order.append(j)
            else:
                order.insert(0, j)
            used.add(j)
        options.append(order)
    for _ in range(restarts):
        a = list(range(n))
        rng.shuffle(a)
        options.append(a)
    best = None
    for a in options:
        a = improve(a[:], m)
        val = score(a, m)
        if best is None or val > best[0]:
            best = (val, a)
    return best[0], best[1], False


def optimize(m, seed):
    return exact_path(m) if len(m) <= 12 else heuristic_path(m, seed)


def matched_shuffle(rows, rng):
    out = []
    for r in rows:
        idx = [i for i, c in enumerate(r) if c != ' ']
        vals = [r[i] for i in idx]
        rng.shuffle(vals)
        chars = list(r)
        for i, c in zip(idx, vals):
            chars[i] = c
        out.append(''.join(chars))
    return out


def render(rows, order, caption, scale=19):
    w, n = len(rows[0]), len(rows)
    left, top, pad = 44, 45, 12
    width, height = left + w * scale + pad, top + n * scale + pad
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="12" y="23" font-family="sans-serif" font-size="13">{caption}</text>']
    for y, ri in enumerate(order):
        parts.append(f'<text x="{left-8}" y="{top+y*scale+14}" text-anchor="end" font-family="monospace" font-size="10">{ri+1}</text>')
        for x, c in enumerate(rows[ri]):
            parts.append(f'<rect x="{left+x*scale}" y="{top+y*scale}" width="{scale}" height="{scale}" fill="{PALETTE[c]}" stroke="#ccc" stroke-width=".5"/>')
    return ''.join(parts) + '</svg>'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--include-045', action='store_true')
    p.add_argument('--controls', type=int, default=120)
    p.add_argument('--widths', type=int, nargs='+', default=list(WIDTHS))
    p.add_argument('--out', default='out/banner-row-search')
    args = p.parse_args()
    assert args.controls >= 1
    assert all(w in WIDTHS for w in args.widths)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    s = master(args.include_045)
    rng = random.Random(20261014)
    result = {
        'mode': 'DISCOVER', 'include_unconfirmed_045': args.include_045,
        'master': s, 'controls_per_width': args.controls,
        'objective': 'For adjacent rows, +1 if both known and same, -1 if both known and different, zero if either unknown',
        'null': 'Shuffle only known symbols within each original row: preserve the missing mask and each row symbol counts',
        'results': []}
    for w in args.widths:
        rows = rows_for(s, w)
        n = len(rows)
        natural = list(range(n))
        m = seam_matrix(rows)
        best, order, exact = optimize(m, 20261014 + w)
        nulls = []
        for i in range(args.controls):
            r = matched_shuffle(rows, rng)
            value, _, _ = optimize(seam_matrix(r), 20261014 + w + i)
            nulls.append(value)
        ge = sum(x >= best for x in nulls)
        rec = {
            'width': w, 'height': n, 'row_permutations': str(math.factorial(n)),
            'method': 'exact' if exact else 'heuristic lower bound',
            'original': score(natural, m), 'candidate_score': best,
            'order_1_based': [x + 1 for x in order],
            'null_mean': round(mean(nulls), 4), 'null_ge_count': ge,
            'null_ge_fraction': round(ge / len(nulls), 4),
            'null_p_plus_one': round((ge + 1) / (len(nulls) + 1), 4),
            'null_max': max(nulls)}
        result['results'].append(rec)
        (out / f'width-{w:02}-original.svg').write_text(render(rows, natural, f'original {w} x {n}'))
        (out / f'width-{w:02}-candidate.svg').write_text(render(rows, order, f'seam-fit {w} x {n}'))
        print(f'{w}x{n}: observed {rec["original"]}, optimized {best}, matched null >= observed {ge}/{len(nulls)}')
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
