#!/usr/bin/env python3
"""Experiment 475: Q1-Q3-only observed registration under masked frame nulls.

All relations are the original Discord Lab's unordered, different-cube
±1 no-wrap pair definitions, restricted to Q1-Q3. The physical
observation mask and observed slash count per primary 9-cell frame
are held fixed, but observed label placements are allowed to shuffle
under two declared structural grammars.

Dependency-free, seeded, finite-sample Monte Carlo. Exploratory.
"""
import argparse
from collections import defaultdict
from itertools import combinations
from math import sqrt
import json
import random

from enumerate_sticker_completion_ensembles import observations, primary_columns
from audit_cube_lab_completion_ensemble import edges


MODES = ("exact", "x", "y", "z")
LAYOUTS = ("IABCDEFGH", "ABCDEFGHI")


def primary_options(observed, frame, strict):
    positions = [j for j in range(9) if 1 + 9 * frame + j in observed]
    slash_count = sum(observed[1+9*frame+j] == "/" for j in positions)
    result = []
    for minority in ("/", "-"):
        majority = "-" if minority == "/" else "/"
        for unusual in combinations(range(9), 3):
            cells = tuple(minority if j in unusual else majority
                          for j in range(9))
            if sum(cells[j] == "/" for j in positions) != slash_count:
                continue
            if strict and not primary_columns(cells):
                continue
            result.append(cells)
    assert result
    return result


def available_pairs(observed):
    return {
        (layout,mode): [
            (a,b) for a,b in edges(layout,mode)
            if a < 81 and b < 81 and a+1 in observed and b+1 in observed
        ]
        for layout in LAYOUTS for mode in MODES
    }


def same_rate(seq, pairs):
    return sum(seq[a] == seq[b] for a,b in pairs) / len(pairs)


def simulate(observed, pairs, n, strict, seed):
    rand = random.Random(seed)
    options = [primary_options(observed,f,strict) for f in range(9)]
    keys = [(layout,axis) for layout in LAYOUTS
            for axis in ("x","y","z")]
    observed_values = ["?" for _ in range(81)]
    for r,v in observed.items():
        if r <= 81:
            observed_values[r-1] = v
    actual = {key:same_rate(observed_values,ps)
              for key,ps in pairs.items()}
    distributions = {key:[] for key in keys}
    for _ in range(n):
        body = tuple(v for opts in options
                     for v in rand.choice(opts))
        rates = {key:same_rate(body,ps) for key,ps in pairs.items()}
        for key in keys:
            layout,axis = key
            distributions[key].append(
                rates[layout,"exact"] - rates[layout,axis])

    scores = {}
    for key in keys:
        layout,axis = key
        vals = distributions[key]
        mean = sum(vals)/n
        sd = sqrt(sum((v-mean)**2 for v in vals)/n)
        difference = actual[layout,"exact"] - actual[layout,axis]
        tail = sum(v >= difference - 1e-12 for v in vals)/n
        scores["%s_%s"%(layout,axis)] = {
            "observed_same_minus_shift":difference,
            "null_mean_difference":mean,
            "null_sd":sd,
            "one_sided_fraction_at_least_observed":tail,
            "z":(difference-mean)/sd
        }

    max_seen = max(row["z"] for row in scores.values())
    candidates = []
    for i in range(n):
        candidates.append(max(
            (distributions[key][i] -
             scores["%s_%s"%key]["null_mean_difference"]) /
            scores["%s_%s"%key]["null_sd"]
            for key in keys
        ))
    return {
        "samples":n,
        "frame_option_counts":list(map(len,options)),
        "observed_rates":{
            "%s_%s"%k:{"matches":sum(observed_values[a]==observed_values[b]
                                  for a,b in p),"pairs":len(p)}
            for k,p in pairs.items()},
        "contrasts":scores,
        "six_comparison_max_Z":{
            "observed":max_seen,
            "upper_tail_fraction":sum(x>=max_seen-1e-12
                                      for x in candidates)/n
        }
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--samples",type=int,default=250000)
    parser.add_argument("--seed",type=int,default=20261008)
    args=parser.parse_args()
    physical,obs=observations()
    assert physical == 84 and len(obs) == 66
    pairs=available_pairs(obs)
    primary_observed=["?" for _ in range(81)]
    for r,v in obs.items():
        if r<=81:primary_observed[r-1]=v
    assert sum(primary_observed[a] == primary_observed[b]
               for a,b in pairs["ABCDEFGHI","exact"]) == 24
    assert len(pairs["ABCDEFGHI","exact"]) == 40
    assert sum(primary_observed[a] == primary_observed[b]
               for a,b in pairs["ABCDEFGHI","x"]) == 16
    assert len(pairs["ABCDEFGHI","x"]) == 47
    result={
        "physical_records":physical,
        "unique_residues":len(obs),
        "scope":"Q1-Q3 only; Q4 not used at all in statistics or null",
        "three_of_nine":simulate(obs,pairs,args.samples,False,args.seed),
        "plus_one_minority_per_physical_column":
            simulate(obs,pairs,args.samples,True,args.seed+1927),
        "limitations":[
            "Statistical operation and coordinate family explored post hoc.",
            "Frame symbol counts are conditioned, not physical placements.",
            "A six-test maximum does not adjust for the broader historical search.",
            "Fitted code grammars supply model nulls, not manufacturing priors."
        ]
    }
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
