#!/usr/bin/env python3
"""Experiment 391: prospective physical predictions from the two 534brn-selected U4 masters."""

from pathlib import Path
import json

from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-391-534brn-target-pair-predictions.json"
OBS=ROOT/"data"/"observations.csv"
TARGET=("112","012","120")

def observed_residues():
    import csv
    with OBS.open(newline="",encoding="utf-8") as fh:
        return {int(r["residue"]) for r in csv.DictReader(fh)}

def serials(residue,limit=648):
    return list(range(residue,limit+1,108))

def main():
    _u3,u4,_u5=machine_layers()
    hits=[m for m in u4 if first_words(m)==TARGET]
    assert len(hits)==2

    obs=observed_residues()
    unknown=[r for r in range(1,109) if r not in obs]
    differing={}
    shared={}
    for r in unknown:
        vals=sorted({m[r-1] for m in hits})
        if len(vals)==1:
            shared[r]=vals[0]
        else:
            differing[r]=vals

    assert differing=={84:[".","/"],102:[".","/"]}
    assert shared[82]=="/"
    assert shared[103]=="/"
    assert shared[45]=="-"

    result={
        "experiment":391,
        "target":"112/012/120",
        "selected_master_count":2,
        "pair_discriminators":{
            str(r):{
                "values":differing[r],
                "physical_serials_le_648":serials(r)
            }
            for r in differing
        },
        "shared_predictions":{
            str(r):{
                "symbol":s,
                "physical_serials_le_648":serials(r)
            }
            for r,s in shared.items()
        },
        "high_value_prospective_checks":{
            "residue_84_or_102":"Either residue identifies which of the two target masters is live.",
            "residue_82":"Both target masters predict slash; U5 instead fixes dot. A physical observation here directly discriminates one-shot target pair from recursive U5.",
            "residue_103":"Both target masters predict slash. The current unverified 427=dot owner claim maps here and would falsify both if physically verified.",
            "residue_45":"Both target masters predict dash, consistent with the existing incumbent invariant; the unverified 369=dot claim would also falsify this target pair."
        }
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
