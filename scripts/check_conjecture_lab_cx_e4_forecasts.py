#!/usr/bin/env python3
"""Read-only prospective check of the frozen CX-E4 Q1/Q2 predictions.

This compares the 9-Oct-2026 five-symbol forecast *as originally frozen*
to current physical observations. It never regenerates predictions from a
now-augmented corpus or writes to data/observations.csv.
"""
import argparse
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"data/conjecture-lab-cx-e4-transport-predictions-2026-10-09.json"


def run(physical_path, fixture_path):
    fixture=json.loads(Path(fixture_path).read_text(encoding="utf8"))
    assert fixture["id"]=="CX-E4-v1"
    predictions=fixture["forecasts"]
    assert [p["residue"] for p in predictions]==[16,22,45,49,50]
    known={}
    with Path(physical_path).open(newline="",encoding="utf8") as f:
        for row in csv.DictReader(f):
            residue=int(row["residue"])
            symbol=row["symbol"].strip()
            assert 1<=residue<=108 and symbol in "/-."
            assert known.get(residue,symbol)==symbol
            known[residue]=symbol
    checks=[]
    for p in predictions:
        residue=p["residue"]
        actual=known.get(residue)
        expected=p["predicted_symbol"]
        checks.append({
            "residue":residue,
            "frozen_symbol":expected,
            "observed":actual,
            "status":"unobserved" if actual is None else
                ("matched" if actual==expected else "falsified"),
            "prior_frame_rival_allowed":p["frame_rival_allowed"],
            "discriminator":p.get("discriminator",False)
        })
    return {
        "model_id":fixture["id"],
        "current_physical_unique_residues":len(known),
        "predictions":checks,
        "matches":sum(p["status"]=="matched" for p in checks),
        "falsifications":sum(p["status"]=="falsified" for p in checks),
        "unknown":sum(p["status"]=="unobserved" for p in checks),
        "warning":"after-data selection; new observations are prospective only if the model is never refitted"
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--observations",type=Path,default=ROOT/"data/observations.csv")
    p.add_argument("--frozen",type=Path,default=FIXTURE)
    args=p.parse_args()
    print(json.dumps(run(args.observations,args.frozen),indent=2))
