#!/usr/bin/env python3
"""SR-04 domain-bridge preflight; no inferred H108 symbol completions.

Do the natural 81+27 / 9+3 class traces map onto the nine distinct
physical picture tiles without an additional relabeling? No. This script
checks the raw ledger and freezes the distinction for future one-pass
operator prototypes. Requires no nonstdlib packages.
"""
import csv, math
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PHYSICAL=[list("IAB"),list("CDE"),list("FGH")]
EXPECTED_CLASSES="ABCDEFGHI"
def run():
    with (ROOT/"data/observations.csv").open(newline="",encoding="utf8") as f:
        raw=list(csv.DictReader(f))
    unique=defaultdict(set)
    byclass=defaultdict(lambda:{"body":[],"tail":[]})
    for r in raw:
        residue=int(r["residue"])
        assert 1<=residue<=108
        c=r["image_class"].strip() or EXPECTED_CLASSES[(residue-1)%9]
        assert c==EXPECTED_CLASSES[(residue-1)%9],r
        symbol=r["symbol"].strip()
        assert symbol in ("/","-",".")
        assert symbol in ("/","-") if residue<=81 else symbol in ("/",".")
        unique[residue].add(symbol)
        byclass[c]["body" if residue<=81 else "tail"].append(residue)
    assert all(len(v)==1 for v in unique.values()),"conflicting physical symbols"
    assert len(unique)==66,(len(unique),len(raw))
    assert set(byclass)==set(EXPECTED_CLASSES)
    for i,c in enumerate(EXPECTED_CLASSES):
        body=[i+1+9*j for j in range(9)]
        tail=[i+1+9*j for j in range(9,12)]
        assert len(body)==9 and len(tail)==3
        assert set(byclass[c]["body"])<=set(body)
        assert set(byclass[c]["tail"])<=set(tail)
    # Body has nine serial OCCURRENCES of the SAME picture class. They
    # cannot silently become nine DIFFERENT picture classes.
    assert math.factorial(9)==362880
    assert math.factorial(9)//math.factorial(3)**3==1680
    return {"observed_residues":len(unique),"unknown_residues":108-len(unique),
            "source_classes":9,"body_occurrences_per_class":9,
            "tail_occurrences_per_class":3,"body_is_different_classes":False,
            "full_bijections_needed_if_unknown_mapping":362880,
            "ordered_row_partition_conventions":1680,
            "physical_tile_order":["".join(row) for row in PHYSICAL],
            "next_operation":"compare source-fixed one-pass row versus column selector; don't fit a mapping to decoded output"}
if __name__=="__main__":
    print(run())
