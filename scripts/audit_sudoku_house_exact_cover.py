#!/usr/bin/env python3
"""Experiment 377: test the cheapest exact-cover consequence of the 81+27 Sudoku analogy."""

from itertools import product, permutations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiment-377-sudoku-house-exact-cover.json"

# Observation-only one-slash tail completions from Experiment 317, serial classes A..I.
ALLOWED = [
    (0,1,2),  # A
    (2,),     # B
    (0,1,2),  # C
    (1,2),    # D
    (0,),     # E
    (1,),     # F
    (0,2),    # G
    (2,),     # H
    (2,),     # I
]

def row_house(i):
    return {(i,c) for c in range(9)}

def col_house(i):
    return {(r,i) for r in range(9)}

def box_house(i):
    br=(i//3)*3
    bc=(i%3)*3
    return {(r,c) for r in range(br,br+3) for c in range(bc,bc+3)}

HOUSES={"row":row_house,"column":col_house,"box":box_house}

def main():
    selectors=list(product(*ALLOWED))
    assert len(selectors)==36

    records=[]
    exact_total=0

    # Tail positions 0/1/2 may map to row/column/box in any of 3! ways.
    # The community also explicitly raised the 000/I indexing issue, so allow
    # all cyclic index offsets and reversal as a generous registration family.
    for type_perm in permutations(("row","column","box")):
        type_map={d:type_perm[d] for d in range(3)}
        for sign in (1,-1):
            for offset in range(9):
                exact=[]
                best_union=0
                min_overlap=81
                for selector in selectors:
                    chosen=[]
                    for j in range(9):
                        idx=(sign*j+offset)%9
                        kind=type_map[selector[j]]
                        chosen.append(HOUSES[kind](idx))
                    union=set().union(*chosen)
                    overlap=81-len(union)  # nine houses always contain 81 incidences
                    best_union=max(best_union,len(union))
                    min_overlap=min(min_overlap,overlap)
                    if len(union)==81:
                        exact.append("".join(map(str,selector)))
                exact_total += len(exact)
                records.append({
                    "tail_type_map":"".join(x[0].upper() for x in type_perm),
                    "index_sign":sign,
                    "index_offset":offset,
                    "exact_cover_selectors":exact,
                    "best_union_cells":best_union,
                    "minimum_overlap_incidences":min_overlap,
                })

    assert len(records)==108
    assert exact_total==0

    result={
        "experiment":377,
        "historical_cue":"Aug 2026 proposal: 81 Sudoku cells + 27 houses (9 rows, 9 columns, 9 boxes) = 108",
        "tail_completions_tested":len(selectors),
        "house_type_permutations":6,
        "index_registrations_per_type_map":18,
        "total_registration_families":len(records),
        "selector_registration_combinations":len(records)*len(selectors),
        "exact_cover_hits":exact_total,
        "best_union_cells":max(r["best_union_cells"] for r in records),
        "minimum_overlap_incidences":min(r["minimum_overlap_incidences"] for r in records),
        "result":"No observation-compatible one-slash tail completion selects nine Sudoku houses that partition all 81 primary cells under any tested type mapping, cyclic offset, or reversal.",
        "interpretation":"The historically independent 81+27 Sudoku analogy has an exact dimensional match to primary+tail, but its cheapest natural selector consequence fails. Do not use Sudoku houses as a G6 bridge absent a new cue."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
