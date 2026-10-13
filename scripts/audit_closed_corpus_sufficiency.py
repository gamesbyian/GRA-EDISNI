#!/usr/bin/env python3
"""Closed-corpus sampling and binary erasure-capacity audit (no decoder assumed).

Run: python scripts/audit_closed_corpus_sufficiency.py
     python scripts/audit_closed_corpus_sufficiency.py --json

The uniform null is EXACT for 84 distinct physical serials drawn without
replacement. The band-conditioned null is also exact, but conditions on the
observed number of serials in each successive 108-serial block. Neither null
models the real historical/social sticker discovery process.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / 'data' / 'observations.csv'
PERIOD = 108
ENDPOINTS = (597, 600, 621, 648)  # scenarios, NOT confirmed edition sizes


def load_serials(path: Path) -> list[int]:
    with path.open(newline='', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    serials = [int(row['serial']) for row in rows]
    assert len(serials) == len(set(serials)), 'duplicate physical serial records'
    observed = {}
    for row, serial in zip(rows, serials):
        r = (serial - 1) % PERIOD + 1
        assert int(row['residue']) == r, (serial, row['residue'])
        symbol = row['symbol']
        assert symbol in ('/', '-') if r <= 81 else symbol in ('/', '.')
        if r in observed:
            assert observed[r] == symbol, ('contradictory repeated residue', r)
        observed[r] = symbol
    return serials


def uniform_coverage_distribution(total: int, sampled: int, period: int = PERIOD) -> dict[int, float]:
    """P(number of occupied residues | uniform sampled distinct serials).

    Exact integer generating-function DP: for each residue with multiplicity c,
    choose j physical copies in comb(c,j) ways; j>0 occupies one residue.
    """
    if not 0 <= sampled <= total:
        raise ValueError((total, sampled))
    capacities = [(total - r) // period + 1 for r in range(1, min(total, period) + 1)]
    dp = {(0, 0): 1}
    for cap in capacities:
        nxt = defaultdict(int)
        for (drawn, occupied), ways in dp.items():
            for count in range(min(cap, sampled-drawn)+1):
                nxt[drawn+count, occupied+(count > 0)] += ways*math.comb(cap, count)
        dp = nxt
    denominator = math.comb(total, sampled)
    counts = {occupied: ways for (drawn, occupied), ways in dp.items() if drawn == sampled}
    assert sum(counts.values()) == denominator
    return {k: v / denominator for k, v in sorted(counts.items())}


def band_conditioned_distribution(total: int, sampled_in_bands: tuple[int, ...], period: int = PERIOD) -> dict[int, float]:
    """Exact P(occupied residues | count from each successive period block).

    For these endpoints the first five blocks contain all 108 residues; the
    last block contains residues 1..(total-5*108). Exchangeability within
    those two residue categories permits a small 2D hypergeometric DP.
    """
    assert len(sampled_in_bands) == 6 and 5*period < total <= 6*period
    short = total - 5*period
    other = period - short
    assert all(0 <= n <= (period if i < 5 else short)
               for i, n in enumerate(sampled_in_bands))
    dp = {(0, 0): 1.0}  # occupied in short-block class vs remainder
    for block, count in enumerate(sampled_in_bands):
        size = period if block < 5 else short
        denom = math.comb(size, count)
        nxt = defaultdict(float)
        for (a, b), weight in dp.items():
            free_a = short-a
            free_b = other-b if block < 5 else 0
            old = a+b if block < 5 else a
            for newly_a in range(max(0, count-free_b-old), min(count, free_a)+1):
                for newly_b in range(max(0, count-newly_a-old), min(free_b, count-newly_a)+1):
                    reused = count-newly_a-newly_b
                    if 0 <= reused <= old:
                        ways = (math.comb(free_a, newly_a)
                                * math.comb(free_b, newly_b)
                                * math.comb(old, reused))
                        nxt[a+newly_a, b+newly_b] += weight*ways/denom
        dp = nxt
    out = defaultdict(float)
    for (a, b), p in dp.items():
        out[a+b] += p
    assert abs(sum(out.values())-1) < 1e-10, sum(out.values())
    return dict(sorted(out.items()))


def summarize(dist: dict[int, float], actual: int) -> dict[str, float]:
    mean = sum(k*p for k, p in dist.items())
    variance = sum((k-mean)**2*p for k, p in dist.items())
    return {'mean_unique': mean, 'sd_unique': math.sqrt(variance),
            'p_at_least_actual': sum(p for k,p in dist.items() if k >= actual)}


def random_binary_linear_rank_probability(known_cells: int, payload_bits: int) -> float:
    """Hypothetical known dense random binary linear generator; not CE evidence.

    If the code maps k data bits to 108 printed bits and m columns survive,
    probability that the selected m-by-k binary submatrix has full rank k.
    This establishes mathematical feasibility for *some* codebooks, not that
    Playdead used such a code or that its generator can be inferred.
    """
    if payload_bits > known_cells or payload_bits < 0:
        return 0.0
    return math.prod(1-2.0**(i-known_cells) for i in range(payload_bits))


def audit(path: Path = OBS) -> dict:
    serials = load_serials(path)
    observed = len({(s-1)%PERIOD for s in serials})
    # Intentional frozen-corpus guard: redo the calculations after new finds.
    assert (len(serials), observed, max(serials)) == (84, 66, 597)
    bands = tuple(sum((s-1)//PERIOD == i for s in serials) for i in range(6))
    assert bands == (19, 18, 17, 19, 10, 1)
    seen_residues = [(s-1)%PERIOD for s in serials]
    repeats = Counter(seen_residues)
    assert sum(n>1 for n in repeats.values()) == 16
    assert sum(n*(n-1)//2 for n in repeats.values()) == 20

    endpoints = {}
    for total in ENDPOINTS:
        flat = uniform_coverage_distribution(total, len(serials))
        conditioned = band_conditioned_distribution(total, bands)
        endpoints[str(total)] = {
            'uniform_without_replacement': summarize(flat, observed),
            'conditioned_on_108_serial_band_counts': summarize(conditioned, observed),
        }

    # Synthetic exhaustive combinatorial positive control, N=6: residues 1,2,3 repeated twice.
    tiny = uniform_coverage_distribution(total=6, sampled=2, period=3)
    assert abs(tiny[1]-3/15)<1e-12 and abs(tiny[2]-12/15)<1e-12
    assert abs(random_binary_linear_rank_probability(1, 1)-0.5)<1e-12

    return {
        'research_mode': 'DEVELOP; observation-only sampling nulls / hypothetical linear-code counterfactual',
        'physical_records': len(serials), 'distinct_h108_residues': observed,
        'unobserved_h108_residues': PERIOD-observed, 'repeated_residue_groups': 16,
        'replication_pairs': 20, 'serial_band_counts': bands,
        'endpoints_are_scenarios_not_confirmed': endpoints,
        'linear_code_full_rank_examples_m66': {
            str(k):random_binary_linear_rank_probability(observed, k)
            for k in (50, 60, 62, 64, 65, 66)
        },
        'raw_binary_completions': 2**(PERIOD-observed),
        'warning': 'Conditional coding feasibility is not evidence for a CE decoder, parity format or intended solvability.'
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--json', action='store_true', help='machine-readable output')
    args = p.parse_args()
    result = audit()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print('84 records; 66 distinct H108 residues; 42 unseen; 16 repeated groups; 20 replication pairs')
        for endpoint, row in result['endpoints_are_scenarios_not_confirmed'].items():
            u = row['uniform_without_replacement']
            c = row['conditioned_on_108_serial_band_counts']
            print(f'N={endpoint}: expected={u["mean_unique"]:.3f} '
                  f'P(coverage>=66)={u["p_at_least_actual"]:.4%}; '
                  f'band-conditional={c["p_at_least_actual"]:.4%}')
        print('Hypothetical random GF(2) code, 60-bit payload and 66-bit observation: '
              f'{result["linear_code_full_rank_examples_m66"]["60"]:.4%} full-rank')


if __name__ == '__main__':
    main()
