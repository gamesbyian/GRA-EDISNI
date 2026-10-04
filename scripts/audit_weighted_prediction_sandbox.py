#!/usr/bin/env python3
"""Experiment 393: safe use of weighted prediction lists as exploratory models."""

from __future__ import annotations
import csv, math, json
from collections import Counter
from pathlib import Path

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers

ROOT=Path(__file__).resolve().parents[1]
OBS=ROOT/"data"/"observations.csv"
PRED=ROOT/"data"/"unobserved-sticker-predictions.csv"
OUT=ROOT/"data"/"experiment-393-weighted-prediction-sandbox.json"

def load_obs():
    with OBS.open(newline="",encoding="utf-8") as fh:
        return {int(r["residue"]):r["symbol"] for r in csv.DictReader(fh)}

def load_pred():
    with PRED.open(newline="",encoding="utf-8") as fh:
        return {int(r["residue"]):r for r in csv.DictReader(fh)}

def modal_master(obs,pred):
    return "".join(
        obs.get(r,pred[r]["preferred_guess"])
        for r in range(1,109)
    )

def support_map(pred):
    out={}
    for r,row in pred.items():
        d={row["preferred_guess"]:int(row["support_of_14"])}
        if row["alternate_symbol"]:
            d[row["alternate_symbol"]]=int(row["alternate_support"])
        out[r]=d
    return out

def canonical_vote_conflicts(master,pred_support):
    return [
        r for r,d in pred_support.items()
        if d.get(master[r-1],0)==0
    ]

def broad_multiplicity_score(master,u2,unknown):
    score=0.0
    for r in unknown:
        counts=Counter(m[r-1] for m in u2)
        score += math.log(counts[master[r-1]]/len(u2))
    return score

def main():
    obs=load_obs(); pred=load_pred()
    summary,u2_rows,unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    u3,u4,u5=machine_layers()
    modal=modal_master(obs,pred)

    # The familiar "preferred guess at every residue" is not a coherent completion.
    membership={
        "U2": modal in set(u2),
        "U3": modal in set(u3),
        "U4": modal in set(u4),
        "U5": modal in set(u5),
    }
    assert not any(membership.values())

    # U2 candidate multiplicity is deliberately combinatorial, not probabilistic.
    # Check whether it even ranks the U4 survivors.
    scores=[broad_multiplicity_score(m,u2,unknown) for m in u4]
    rounded={round(x,12) for x in scores}
    assert len(rounded)==1

    # Canonical 14-state support is downstream of G6. It assigns zero support to
    # residue-82 slash, exactly the value selected by the 534brn one-shot pair.
    ps=support_map(pred)
    assert ps[82]=={".":14}
    target=[m for m in u4 if m[81]=="/"]
    # This includes the externally selected pair plus other pre-G6 masters;
    # the key point is that every such master receives a hard zero from the
    # downstream canonical vote at residue 82.
    assert target
    assert all(82 in canonical_vote_conflicts(m,ps) for m in target)

    result={
        "experiment":393,
        "question":"How may the existing weighted missing-sticker guesses be used safely for exploratory decoding?",
        "modal_synthetic_master":{
            "member_of":membership,
            "conclusion":"The per-residue modal guess sheet is not a legal completion even in broad U2; never treat it as a physical master."
        },
        "u2_combinatorial_weighting":{
            "u4_survivors":len(u4),
            "distinct_scores":len(rounded),
            "conclusion":"Broad U2 candidate multiplicities give the same product score to all 12 U4 survivors; they do not provide a hidden prior ranking."
        },
        "canonical_14_state_weighting":{
            "residue_82_support":ps[82],
            "conclusion":"The 14-state weights encode downstream G6 assumptions. Naively using them as priors would assign zero support to every pre-G6 master with 82=slash, including the active 534brn-selected pair."
        },
        "safe_policy":[
            "Use weighted lists as uncertainty masks and scenario generators, not calibrated probabilities.",
            "Run exploratory operations over coherent ensembles U2/U3/U4/U5 rather than the synthetic modal master.",
            "Report operation stability and survivor counts separately at each universe layer.",
            "For pre-G6 discovery, do not use U5-derived support counts to rank candidates.",
            "A promising operation must survive replay on the broadest universe whose premises it does not itself assume."
        ],
        "recommended_sandbox_panels":{
            "broad_physical":"U2 324",
            "typed_one_shot":"U4 12",
            "recursive":"U5 10",
            "external_selected":"Experiment 390 pair of 2",
            "rival":"frozen row-selector family at residues 84/102"
        }
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
