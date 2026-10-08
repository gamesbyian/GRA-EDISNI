#!/usr/bin/env python3
"""Experiment 453: exact cube × A-I-class label-shuffle null.

Unknown cells remain unknown. Within every cube and A-I class, shuffle
only the observed foreground symbols, retaining their symbol counts.
All distinct shuffles are enumerated, not sampled.

The 66-residue CSV has 16 variable groups and 331,776 total assignments.
All-pair matches share observations and need the exact permutation null,
not a binomial approximation.
"""
from collections import Counter
from itertools import permutations
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]


def read_observations():
    by_residue = {}
    physical = 0
    with (ROOT / "data" / "observations.csv").open(newline="", encoding="utf8") as fh:
        for row in csv.DictReader(fh):
            physical += 1
            r, symbol = int(row["residue"]), row["symbol"]
            assert r not in by_residue or by_residue[r] == symbol
            by_residue[r] = symbol
    return physical, by_residue


def exact_test():
    physical, obs = read_observations()
    assert physical == 84 and len(obs) == 66
    source = ["?"] * 109
    for r,v in obs.items():
        source[r] = v
    groups = []
    for cube in range(4):
        for j in range(9):
            sites = [1+27*cube+9*d+j for d in range(3)
                     if 1+27*cube+9*d+j in obs]
            labels = [obs[r] for r in sites]
            if len(set(labels)) < 2:
                continue
            choices = sorted(set(permutations(labels)))
            groups.append((sites, choices))
    pairs = []
    for a in range(4):
        for b in range(a+1,4):
            for local in range(27):
                p, q = 1+27*a+local, 1+27*b+local
                if p in obs and q in obs:
                    pairs.append((p,q,b < 3))
    def score():
        all_matches = primary_matches = 0
        for p,q,primary in pairs:
            match = source[p] == source[q]
            all_matches += match
            if primary:
                primary_matches += match
        return all_matches,primary_matches

    actual = score()
    assert actual == (33,24)
    assert len(pairs) == 64 and sum(primary for _,_,primary in pairs) == 40
    hist_all, hist_primary = Counter(), Counter()

    def visit(i):
        if i == len(groups):
            all_match, primary_match = score()
            hist_all[all_match] += 1
            hist_primary[primary_match] += 1
            return
        sites, possibilities = groups[i]
        for labels in possibilities:
            for site, symbol in zip(sites, labels):
                source[site] = symbol
            visit(i+1)

    visit(0)
    total = sum(hist_all.values())
    assert len(groups) == 16 and total == 331776
    above_all = sum(n for k,n in hist_all.items() if k >= actual[0])
    above_primary = sum(n for k,n in hist_primary.items() if k >= actual[1])
    assert above_all == 20112 and above_primary == 38784
    def mean(hist):
        return sum(k*n for k,n in hist.items()) / total

    return {
        "physical_records":physical,
        "unique_residues":len(obs),
        "variable_cube_letter_groups":len(groups),
        "total_exact_label_assignments":total,
        "observed":{"all":list(actual[:1])+[64],
                    "primary":[actual[1],40],
                    "q4_involving":[actual[0]-actual[1],24]},
        "null":{"all_mean_matches":mean(hist_all),
                "primary_mean_matches":mean(hist_primary),
                "all_ge_observed":above_all,
                "all_upper_tail_fraction":above_all/total,
                "primary_ge_observed":above_primary,
                "primary_upper_tail_fraction":above_primary/total},
        "histogram_all":dict(sorted(hist_all.items())),
        "histogram_primary":dict(sorted(hist_primary.items())),
        "limitations":[
            "retrospective null after the statistic and geometry were explored",
            "the 64 pairs reuse observations and must not be treated as independent",
            "does not imply the four-cube readout is the intended decoding operation",
            "different within-cube primary/Q4 alphabet distributions remain relevant"
        ]
    }


if __name__ == "__main__":
    print(json.dumps(exact_test(), indent=2))
