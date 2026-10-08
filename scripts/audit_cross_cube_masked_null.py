#!/usr/bin/env python3
"""Experiment 431: masked cross-cube matches under a grammar-aware randomization.

This is a *retrospective diagnostic*, not a confirmatory p-value. It conditions
on which residue positions are physically observed and on their per-frame
observed slash counts, but deliberately permutes their symbols; holding the
observed symbol at each location fixed would make the statistic tautological.

Primary frames use exactly one minority symbol in each physical column,
with either minority polarity allowed. Q4 uses one slash per A-I depth
stack and retains the number (not locations) of observed slashes.
"""
import argparse
import csv
from itertools import product
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
LETTERS = "ABCDEFGHI"
PHYSICAL = "IAB" + "CDE" + "FGH"
COLS = tuple(tuple(LETTERS.index(PHYSICAL[3*row+col]) for row in range(3))
             for col in range(3))


def load():
    records = 0
    observed = {}
    with (ROOT / "data/observations.csv").open(newline="", encoding="utf8") as fh:
        for row in csv.DictReader(fh):
            records += 1
            r = int(row["residue"])
            symbol = row["symbol"]
            assert r not in observed or observed[r] == symbol
            observed[r] = symbol
    return records, observed


def primary_null_choices(obs, frame):
    visible = [obs.get(frame*9+j+1) for j in range(9)]
    slash_count = sum(s == "/" for s in visible)
    choices = []
    for minority in "/-":
        for rows in product(range(3), repeat=3):
            cells = [("-" if minority == "/" else "/") for _ in range(9)]
            for column, row in enumerate(rows):
                cells[COLS[column][row]] = minority
            if sum(cells[j] == "/" for j, s in enumerate(visible)
                   if s is not None) == slash_count:
                choices.append("".join(cells))
    return choices


def q4_null_choices(obs):
    observed_slash_count = sum(
        obs.get(r) == "/" for r in range(82, 109))
    result = []
    for depths in product(range(3), repeat=9):
        slash_count = sum(
            obs.get(82+9*d+j) is not None and depths[j] == d
            for d in range(3) for j in range(9))
        if slash_count == observed_slash_count:
            result.append(depths)
    return result


def cube_pairs(obs):
    pairs = []
    for q in range(4):
        for q2 in range(q+1, 4):
            for local in range(27):
                a, b = 1+27*q+local, 1+27*q2+local
                if a in obs and b in obs:
                    pairs.append((a-1, b-1, q2 < 3))
    return pairs


def pair_scores(symbols, pairs):
    primary = overall = 0
    for a,b,is_primary in pairs:
        match = symbols[a] == symbols[b]
        overall += match
        if is_primary:
            primary += match
    return overall, primary


def shifted_controls(obs):
    coords = [divmod(PHYSICAL.index(letter), 3) for letter in LETTERS]
    def to_index(x,y):
        return LETTERS.index(PHYSICAL[x*3+y])
    operators = {
        "rot90": lambda x,y: (y, 2-x),
        "rot180": lambda x,y: (2-x,2-y),
        "rot270": lambda x,y: (2-y,x),
        "flip_horizontal": lambda x,y: (x,2-y),
        "flip_vertical": lambda x,y: (2-x,y),
        "diagonal": lambda x,y: (y,x),
        "antidiagonal": lambda x,y: (2-y,2-x),
        "shift_row": lambda x,y: ((x+1)%3,y),
        "shift_column": lambda x,y: (x,(y+1)%3),
    }
    output = {}
    for name,fn in operators.items():
        n = identity = transformed = 0
        for q in range(3):
            for q2 in range(q+1,3):
                for d in range(3):
                    for j,(x,y) in enumerate(coords):
                        mapped = to_index(*fn(x,y))
                        a = 1+27*q+9*d+j
                        b = 1+27*q2+9*d+j
                        c = 1+27*q2+9*d+mapped
                        if all(p in obs for p in (a,b,c)):
                            n += 1
                            identity += obs[a] == obs[b]
                            transformed += obs[a] == obs[c]
        output[name] = {"matched_support_pairs":n,
                        "identity_matches":identity,
                        "transformed_matches":transformed,
                        "difference":identity-transformed}
    return output


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument("--samples", type=int, default=100000)
    argp.add_argument("--seed", type=int, default=20261008)
    args = argp.parse_args()
    records, obs = load()
    assert records == 84 and len(obs) == 66, "Recalibrate after new observation"
    pairs = cube_pairs(obs)
    direct = [obs.get(r, "?") for r in range(1,109)]
    actual = pair_scores(direct, pairs)
    assert len(pairs) == 64 and actual == (33,24)
    assert sum(p[2] for p in pairs) == 40

    primary_choices = [primary_null_choices(obs,frame)
                       for frame in range(9)]
    tails = q4_null_choices(obs)
    assert list(map(len, primary_choices)) == [
        12,12,6,9,12,16,9,12,12]
    assert len(tails) == 6120
    rng = random.Random(args.seed)
    total = pri = tail_sum = ge_total = ge_pri = 0
    for _ in range(args.samples):
        primary = "".join(rng.choice(opts) for opts in primary_choices)
        selected = rng.choice(tails)
        tail = "".join("/" if selected[j] == d else "."
                       for d in range(3) for j in range(9))
        all_score, pri_score = pair_scores(primary+tail, pairs)
        total += all_score
        pri += pri_score
        tail_sum += all_score-pri_score
        ge_total += all_score >= actual[0]
        ge_pri += pri_score >= actual[1]

    output = {
        "physical_records":records,
        "unique_residues":len(obs),
        "matched_coordinate_pairs":len(pairs),
        "observed": {
            "all": {"matches":actual[0],"pairs":64},
            "primary_only": {"matches":actual[1],"pairs":40},
            "cube4_involving": {"matches":actual[0]-actual[1],"pairs":24}
        },
        "null": {
            "family": "observation-mask and per-frame observed census preserved; one minority per physical primary column; one Q4 slash per depth stack",
            "primary_frame_option_counts":list(map(len,primary_choices)),
            "q4_compatible_with_observed_slash_count":len(tails),
            "samples":args.samples, "seed":args.seed,
            "mean_all_matches":total/args.samples,
            "mean_primary_matches":pri/args.samples,
            "mean_cube4_matches":tail_sum/args.samples,
            "fraction_all_ge_observed":ge_total/args.samples,
            "fraction_primary_ge_observed":ge_pri/args.samples
        },
        "matched_support_coordinate_controls":shifted_controls(obs),
        "cautions": [
            "The actual labels are shuffled at observed sites; conditioning on labels would make the score invariant.",
            "These are retrospective model-specific diagnostic tail fractions, not discovery-adjusted p-values.",
            "Cube 4 contributes a different slash/dot alphabet, so a pooled binary-colour match is a fragile statistic.",
            "Matched-support rotations use only primary cubes and do not assert an intended orientation.",
            "More stringent cube-by-letter constraints and multiplicity selection were explored post hoc by the community."
        ]
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
