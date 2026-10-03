#!/usr/bin/env python3
"""Experiment 378: test the nine decimal digits in the sticker-derived 534brn URL
against the independently derived one-shot six-state 3x3 family.

The tested decimal->ternary map is the canonical ordered tercile partition
1..3 -> 0, 4..6 -> 1, 7..9 -> 2. The only spatial freedom allowed is D4.
"""

from collections import Counter
from itertools import combinations
from math import factorial
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-378-534brn-one-shot-consumer.json"

DIGITS = "534965398"
GRID = (
    (5,3,4),
    (9,6,5),
    (3,9,8),
)
MIDDLE_COLUMNS = ("002","010","020","110","112","220")

def target(mid):
    return (
        (1,int(mid[0]),2),
        (0,int(mid[1]),2),
        (1,int(mid[2]),0),
    )

TARGETS = {mid: target(mid) for mid in MIDDLE_COLUMNS}

def rot90(a):
    return tuple(tuple(a[r][c] for r in range(2,-1,-1)) for c in range(3))

def mirror_lr(a):
    return tuple(tuple(reversed(row)) for row in a)

def d4(a):
    named=[]
    cur=a
    for k,name in enumerate(("identity","rot90_ccw","rot180","rot270_ccw")):
        named.append((name,cur))
        named.append((name+"_mirror_lr",mirror_lr(cur)))
        cur=rot90(cur)
    # retain first occurrence only
    out=[]
    seen=set()
    for name,g in named:
        if g not in seen:
            seen.add(g)
            out.append((name,g))
    return out

def tercile_digit(d):
    if 1 <= d <= 3:
        return 0
    if 4 <= d <= 6:
        return 1
    if 7 <= d <= 9:
        return 2
    raise ValueError(d)

def map_grid(a, fn):
    return tuple(tuple(fn(v) for v in row) for row in a)

def flatten(a):
    return tuple(v for row in a for v in row)

def main():
    ternary = map_grid(GRID, tercile_digit)

    exact=[]
    for orientation,g in d4(ternary):
        for mid,t in TARGETS.items():
            if g == t:
                exact.append({"orientation":orientation,"middle_column":mid,"grid":["".join(map(str,row)) for row in g]})

    assert exact == [{
        "orientation":"rot90_ccw",
        "middle_column":"112",
        "grid":["112","012","120"],
    }]

    # Union of all D4 images of the six preregistered one-shot states.
    target_orbit=set()
    for t in TARGETS.values():
        for _name,g in d4(t):
            target_orbit.add(flatten(g))
    assert len(target_orbit) == 48

    p_uniform_ternary = len(target_orbit) / (3**9)

    census=Counter(flatten(ternary))
    assert census == Counter({1:4,2:3,0:2})
    total_same_census = factorial(9)//(factorial(4)*factorial(3)*factorial(2))
    census_targets={
        flat for flat in target_orbit
        if Counter(flat)==census
    }
    assert len(census_targets)==8
    p_same_census = len(census_targets)/total_same_census

    # Sensitivity: all 28 monotone 3-bin partitions of decimal 1..9.
    partition_hits=[]
    for a,b in combinations(range(1,9),2):
        def f(d, a=a, b=b):
            return 0 if d <= a else (1 if d <= b else 2)
        g0=map_grid(GRID,f)
        matched=any(flatten(g) in target_orbit for _name,g in d4(g0))
        if matched:
            partition_hits.append([a,b])
    assert partition_hits == [[3,6],[3,7]]

    result={
        "experiment":378,
        "external_artifact":"sticker-background solution URL dat/534brn9653f9j8mmd",
        "historical_cue":"2 Nov 2025 community discussion explicitly noticed nine digits 534965398 and proposed they might aid ordering the nine sticker sections",
        "digit_stream":DIGITS,
        "digit_grid_row_major":["534","965","398"],
        "declared_digit_to_ternary":"1-3 -> 0; 4-6 -> 1; 7-9 -> 2",
        "ternary_grid_row_major":["101","211","022"],
        "exact_one_shot_match":exact[0],
        "one_shot_family":["102/002/120","102/012/100","102/022/100","112/012/100","112/012/120","122/022/100"],
        "d4_target_patterns":len(target_orbit),
        "descriptive_nulls":{
            "uniform_ternary":{
                "space":3**9,
                "hits":len(target_orbit),
                "fraction":p_uniform_ternary
            },
            "fixed_observed_census_0x2_1x4_2x3":{
                "space":total_same_census,
                "hits":len(census_targets),
                "fraction":p_same_census
            }
        },
        "monotone_decimal_partition_sensitivity":{
            "partitions_tested":28,
            "hit_cutpoints":partition_hits,
            "note":"(3,6) is the canonical equal-tercile split. (3,7) is observationally identical here because digit 7 does not occur."
        },
        "interpretation":"A direct sticker-derived external artifact contains exactly nine decimal digits. Under the canonical ordered tercile map of 1..9 into three equal groups, the row-major 3x3 digit grid becomes 101/211/022; rotating 90 degrees counter-clockwise yields 112/012/120, exactly one of the six independently derived one-shot G5 objects. This is a specific externally registered match and materially stronger than generic pattern resemblance, but the decimal-tercile interpretation and row-major gridding remain hypotheses rather than historically documented authorial instructions."
    }

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
