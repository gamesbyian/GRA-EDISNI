#!/usr/bin/env python3
"""CX-E6: EXACT source-mask/quarter-census/rail-conditioned XOR null.

The observed 66-residue H108 freeze has 4×27 quarters, with columns
5 and 15 slash in every quarter. Keep the physical observation mask
and each quarter's total slash count fixed. Keep those two *observed*
slash rails fixed. Randomly assign the remaining observed slash marks
within each quarter, separately. For the 12 G/H/I triples in the
proposed 4/9/(9+3) segmentation, calculate whether the 16 Boolean
functions permit at least one completion of every missing bit.

This script computes an EXACT rational probability for the particular
after-selected event 'GHI uniquely implies XOR'; a full 84-subset
look-elsewhere diagnostic is optional deterministic Monte Carlo.
Neither is a corrected p-value for the entire prior experiment history.
"""
import argparse
import csv
import json
import math
import random
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/"data/conjecture-lab-h108-66-residue-freeze-2026-10-09.csv"
CLASSES="ABCDEFGHI"
RAILS=(5,15)


def load(path):
    marks={}
    with Path(path).open(newline="",encoding="utf8") as f:
        for row in csv.DictReader(f):
            n=int(row["residue"]);s=row["symbol"].strip()
            assert 1<=n<=108 and s in "/-."
            assert row.get("image_class","").strip() in ("",CLASSES[(n-1)%9])
            assert n not in marks or marks[n]==s
            marks[n]=s
    assert len(marks)==66
    return marks


# [a,b,c] take 0=non-slash, 1=slash, None=unobserved.
ALL_FUNCTIONS=(1<<16)-1
def function_mask(a,b,c):
    val=0
    for rule in range(16):
        if any(
            (a is None or a==x) and (b is None or b==y) and
            (c is None or c==((rule>>(2*x+y))&1))
            for x in range(2) for y in range(2)
        ):
            val|=(1<<rule)
    return val


# Fixed 3^3 helper, keeps exact and simulated methods identical.
TRIPLE_MASK={(a,b,c):function_mask(a,b,c)
             for a,b,c in product((None,0,1),repeat=3)}


def available_indices(obs,q):
    lo=q*27
    rail=[lo+r for r in RAILS]
    assert all(obs.get(n)=="/" for n in rail)
    nonrail=[n for n in range(lo+1,lo+28) if n in obs and n not in rail]
    k=sum(obs[n]=="/" for n in nonrail)
    target=[n for n in nonrail if (n-1)%9 in (6,7,8)]
    return nonrail,k,target


def class_mask(binary,q,cl):
    offset=CLASSES.index(cl)+1
    nums=[q*27+offset+9*j for j in range(3)]
    return TRIPLE_MASK[tuple(binary.get(i) for i in nums)]


def exact_selected_ghi(obs):
    quarter_dists=[]
    sample_sizes=[]
    for q in range(4):
        observed,k,target=available_indices(obs,q)
        m,n=len(observed),len(target)
        dist=Counter()
        for vals in product((0,1),repeat=n):
            r=sum(vals)
            weight=math.comb(m-n,k-r) if 0<=k-r<=m-n else 0
            if not weight:continue
            local=dict(zip(target,vals))
            mask=ALL_FUNCTIONS
            for cl in "GHI":
                mask &= class_mask(local,q,cl)
            dist[mask]+=weight
        assert sum(dist.values())==math.comb(m,k)
        sample_sizes.append({
            "quarter":q+1,
            "observed_nonrail":m,
            "observed_nonrail_slash":k,
            "observed_ghi":n,
            "distinct_16function_masks":len(dist)
        })
        quarter_dists.append(dist)
    ways=Counter({ALL_FUNCTIONS:1})
    for qdist in quarter_dists:
        nxt=Counter()
        for prior,n1 in ways.items():
            for current,n2 in qdist.items():
                nxt[prior & current]+=n1*n2
        ways=nxt
    denominator=math.prod(math.comb(x["observed_nonrail"],
                                   x["observed_nonrail_slash"])
                          for x in sample_sizes)
    assert sum(ways.values())==denominator
    xor=Fraction(ways[1<<6],denominator)
    anyunique=Fraction(sum(c for mask,c in ways.items()
                           if mask and mask&(mask-1)==0),denominator)
    return {
        "condition":"real observed 66-residue mask; quarter slash counts; rails 5/15 fixed slash",
        "quarter_inputs":sample_sizes,
        "distinct_terminal_function_masks":len(ways),
        "total_equal_weight_observed_mark_assignments":denominator,
        "unique_xor_exact":{
            "numerator":xor.numerator,
            "denominator":xor.denominator,
            "probability":float(xor)},
        "any_unique_boolean_exact":{
            "numerator":anyunique.numerator,
            "denominator":anyunique.denominator,
            "probability":float(anyunique)}
    }


def trial_mask(known,classes):
    mask=ALL_FUNCTIONS
    for q in range(4):
        for cl in classes:
            mask &= class_mask(known,q,cl)
    return mask


def scan_null(obs, trials, seed):
    rng=random.Random(seed)
    options=[available_indices(obs,q) for q in range(4)]
    combos=list(combinations(CLASSES,3))
    counts=Counter()
    unique_counts=[]
    for t in range(trials):
        # Rails must remain observed slashes even when scanning all
        # 84 class subsets (E/F include rail coordinates). Omitting
        # them would make the subset-selection null spuriously loose.
        sample={q*27+col:1 for q in range(4) for col in RAILS}
        for observed,k,_ in options:
            winners=set(rng.sample(observed,k))
            for n in observed:
                sample[n]=int(n in winners)
        masks={}
        for cl in CLASSES:
            mask=ALL_FUNCTIONS
            for q in range(4):
                mask &= class_mask(sample,q,cl)
            masks[cl]=mask
        selected=masks["G"]&masks["H"]&masks["I"]
        counts["GHI_uniquely_XOR"]+=selected==(1<<6)
        any_xor=0
        for a,b,c in combos:
            mask=masks[a]&masks[b]&masks[c]
            any_xor+=mask==(1<<6)
        unique_counts.append(any_xor)
        counts["any_of_84_uniquely_XOR"]+=bool(any_xor)
        counts["three_or_more_uniquely_XOR"]+=any_xor>=3
        counts["number_of_unique_XOR_subsets_total"]+=any_xor
    return {
        "seed":seed,"trials":trials,
        "GHI_uniquely_XOR_frequency":counts["GHI_uniquely_XOR"]/trials,
        "any_of_84_uniquely_XOR_frequency":counts["any_of_84_uniquely_XOR"]/trials,
        "at_least_three_frequency":counts["three_or_more_uniquely_XOR"]/trials,
        "mean_number_of_84_unique_XOR_subsets":
            counts["number_of_unique_XOR_subsets_total"]/trials,
        "comparison":"selection-aware heuristic Monte Carlo, NOT corrected full-project p-value"
    }


def observed_subsets(obs):
    binary={n:int(v=="/") for n,v in obs.items()}
    combos=list(combinations(CLASSES,3))
    unique_xor=["".join(x) for x in combos if trial_mask(binary,x)==(1<<6)]
    assert unique_xor==["AHI","DHI","GHI"]
    return {"n_three_class_subsets":len(combos),
            "observed_unique_xor_subsets":unique_xor,
            "observed_count":len(unique_xor)}


def run(path,draws=0,seed=20261009):
    obs=load(path)
    result={
        "research_mode":"retrospective null calibration, no CE evidence promoted",
        "frozen_residues":len(obs),
        "exact":exact_selected_ghi(obs),
        "observed":observed_subsets(obs),
    }
    assert result["exact"]["unique_xor_exact"]["numerator"]==16267037
    assert result["exact"]["unique_xor_exact"]["denominator"]==128648520
    if draws:
        result["scan_84_subsets"]=scan_null(obs,draws,seed)
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--observations",type=Path,default=FROZEN)
    p.add_argument("--draws",type=int,default=0,
                   help="optional seeded 84-subset scan, e.g. 20000")
    p.add_argument("--seed",type=int,default=20261009)
    args=p.parse_args()
    print(json.dumps(run(args.observations,args.draws,args.seed),indent=2))
