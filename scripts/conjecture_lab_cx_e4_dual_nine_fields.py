#!/usr/bin/env python3
"""CX-E4: source-class 9+3 suffix, finite row/column readers, D4 transfer audit.

Uses observed H108 marks only. The selected minority rules and source-to-
source transform were picked after seeing this corpus; these are DEVELOP
hypotheses and must not be used to report an independent validation.
"""
import argparse
import csv
import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYSICAL = ("IAB", "CDE", "FGH")
CLASS_ORDER = "GHIABCDEF"


def get_observations(path):
    out = {}
    with Path(path).open(newline="", encoding="utf8") as f:
        for r in csv.DictReader(f):
            n, s = int(r["residue"]), r["symbol"].strip()
            assert 1 <= n <= 108 and s in "/-."
            assert r.get("image_class", "").strip() in ("", "ABCDEFGHI"[(n-1)%9])
            assert n not in out or out[n] == s
            out[n] = s
    return out


def get_grid(marks, quarter):
    source = {CLASS_ORDER[i]:marks.get(quarter*27+16+i, "?")
              for i in range(9)}
    return [[source[c] for c in row] for row in PHYSICAL]


def minority_options(grid, alphabet, axis):
    """One minority in each physical row or column, no fitted rotation."""
    opts=[]
    for minority in alphabet:
        other=next(c for c in alphabet if c!=minority)
        for indices in product(range(3),repeat=3):
            x=[[other]*3 for _ in range(3)]
            for a,b in enumerate(indices):
                if axis=="row":
                    x[a][b]=minority
                else:
                    x[b][a]=minority
            if all(grid[i][j] in ("?",x[i][j])
                   for i in range(3) for j in range(3)):
                opts.append({"minority":minority,"token":"".join(map(str,indices)),
                             "rows":["".join(row) for row in x]})
    return opts


def rotate(g):
    return [[g[2-j][i] for j in range(3)] for i in range(3)]


def mirror(g):
    return [list(reversed(row)) for row in g]


def orientations(g):
    arr=[list(row) for row in g]
    for k in range(4):
        yield f"rot{k*90}", arr
        yield f"rot{k*90}_mirror", mirror(arr)
        arr=rotate(arr)


def evaluate_source_target(source,target,source_alphabet,target_alphabet):
    """Eight D4 orientations times preserve-or-swap binary roles."""
    result=[]
    for label,g in orientations(source):
        for invert in (False,True):
            mapped={}
            for i,sym in enumerate(source_alphabet):
                mapped[sym]=target_alphabet[1-i if invert else i]
            mapped["?"]="?"
            transferred=[[mapped[x] for x in row] for row in g]
            pairs=[(i+1,j+1,transferred[i][j],target[i][j])
                   for i in range(3) for j in range(3)
                   if transferred[i][j]!="?" and target[i][j]!="?"]
            disagreement=[{"row":a,"column":b,"source_transformed":x,"target_observed":y}
                          for a,b,x,y in pairs if x!=y]
            result.append({"orientation":label,"swap_roles":invert,
                           "overlap":len(pairs),"mismatches":len(disagreement),
                           "disagreement_locations":disagreement})
    return sorted(result,key=lambda x:(x["mismatches"],-x["overlap"],
                                      x["orientation"],x["swap_roles"]))


def row_or_column_transfer_forecasts(marks, grids):
    """Conditional exact Q1-row -> Q2-column complemented transpose."""
    a=minority_options(grids[0],"/-","row")
    b=minority_options(grids[1],"/-","column")
    assert len(a)==len(b)==1, (a,b)
    whole_a=[list(row) for row in a[0]["rows"]]
    expected=[["/" if whole_a[j][i]=="-" else "-" for j in range(3)]
              for i in range(3)]
    assert ["".join(row) for row in expected]==b[0]["rows"]
    forecasts=[]
    for q,sol in [(0,a[0]),(1,b[0])]:
        rows=sol["rows"]
        for i,line in enumerate(PHYSICAL):
            for j,cl in enumerate(line):
                serial_j=CLASS_ORDER.index(cl)
                res=q*27+16+serial_j
                if res not in marks:
                    forecasts.append({"residue":res,"image_class":cl,
                                      "conditional_predicted_symbol":rows[i][j],
                                      "from":"Q1 row minority" if q==0 else
                                      "Q2 column minority+transpose complement"})
    return {
        "q1_rows":a[0]["rows"],
        "q2_rows":b[0]["rows"],
        "q1_to_q2_transpose_and_binary_complement":True,
        "frozen_conditional_forecasts":sorted(forecasts,key=lambda x:x["residue"])
    }


def q1_q2_fixed_mask_exact_null(g1, g2):
    """Enumerate observed-label permutations under each grid's symbol count.

    Q1 contains 7 observed sites with 2 slashes, Q2 contains 6 with
    4 slashes: C(7,2)*C(6,4)=315 states. This is a descriptive
    after-selection calibration, not corrected for all prior research.
    """
    seen_a=[(i,j) for i in range(3) for j in range(3) if g1[i][j]!="?"]
    seen_b=[(i,j) for i in range(3) for j in range(3) if g2[i][j]!="?"]
    slash_a=sum(x=="/" for row in g1 for x in row)
    slash_b=sum(x=="/" for row in g2 for x in row)
    def relabel(src, spots, chosen):
        z=[row[:] for row in src]
        which=set(chosen)
        for idx,(r,c) in enumerate(spots):
            z[r][c]="/" if idx in which else "-"
        return z
    hist={"any_zero":0,"any_zero_with_six_overlap":0,
          "row_col_unique":0,"row_col_unique_transpose_complement":0}
    total=0
    for ia in combinations(range(len(seen_a)),slash_a):
        a=relabel(g1,seen_a,ia)
        for ib in combinations(range(len(seen_b)),slash_b):
            b=relabel(g2,seen_b,ib)
            total+=1
            tests=evaluate_source_target(a,b,"/-","/-")
            zeros=[x for x in tests if x["mismatches"]==0]
            hist["any_zero"]+=bool(zeros)
            hist["any_zero_with_six_overlap"]+=any(x["overlap"]>=6 for x in zeros)
            oa=minority_options(a,"/-","row")
            ob=minority_options(b,"/-","column")
            unique=len(oa)==len(ob)==1
            hist["row_col_unique"]+=unique
            if unique:
                z=[list(row) for row in oa[0]["rows"]]
                transformed=[["/" if z[j][i]=="-" else "-" for j in range(3)]
                             for i in range(3)]
                hist["row_col_unique_transpose_complement"]+=(
                    transformed==[list(row) for row in ob[0]["rows"]])
    assert total==315, total
    return {"conditional_sample_space":total,
            "fixed_known_masks":True,
            "per_grid_observed_slash_counts":[slash_a,slash_b],
            "event_counts":hist,
            "fractions_of_all":{k:v/total for k,v in hist.items()},
            "conditional_transform_fraction_given_unique_row_col":
               hist["row_col_unique_transpose_complement"]/hist["row_col_unique"],
            "caution":"post-hoc, missing global selection multiplicity"}


def run(path):
    marks=get_observations(path)
    grids=[get_grid(marks,q) for q in range(4)]
    quarters=[]
    for q,g in enumerate(grids):
        alphabet="/." if q==3 else "/-"
        opts={axis:minority_options(g,alphabet,axis)
              for axis in ("row","column")}
        repeated=[]
        for i,cl in enumerate("GHI"):
            a=q*27+16+i
            b=q*27+25+i
            x,y=marks.get(a,"?"),marks.get(b,"?")
            repeated.append({"class":cl,"residues":[a,b],"symbols":[x,y],
                             "relationship":"unknown" if "?" in (x,y)
                               else ("equal" if x==y else "different")})
        quarters.append({
            "quarter":q+1,
            "suffix_first9_classes":CLASS_ORDER,
            "physical_grid":["".join(row) for row in g],
            "row_minority_options":opts["row"],
            "column_minority_options":opts["column"],
            "suffix_last3_repeated_GHI":repeated
        })
    edges=[]
    for q in range(3):
        result=evaluate_source_target(grids[q],grids[q+1],
                                      "/-" if q<3 else "/.",
                                      "/." if q+1==3 else "/-")
        edges.append({
            "quarter_from":q+1,"quarter_to":q+2,
            "all_16_orientation_role_comparisons":len(result),
            "exact_zero_conflict_variants":[x for x in result if x["mismatches"]==0],
            "best_comparison":result[0],
            "best_overlap_among_exact":max((x["overlap"] for x in result
                                          if x["mismatches"]==0),default=None)
        })
    return {
        "status":"observed-only EXPLORE/DEVELOP, after-data operations",
        "physical_unique_residues":len(marks),
        "quarter_suffix_fields":quarters,
        "adjacent_quarter_8D4_x_2role_edges":edges,
        "special_q1_q2_transform":row_or_column_transfer_forecasts(marks,grids),
        "fixed_mask_q1_q2_exact_null":q1_q2_fixed_mask_exact_null(grids[0],grids[1]),
        "interpretation":"A literal same-axis row reader across all second fields is contradicted by Q2; only Q1->Q2 offers an exact D4+role-swap with >=6 overlapping known cells. No universal four-quarter rule established."
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--observations",type=Path,default=ROOT/"data/observations.csv")
    args=p.parse_args()
    print(json.dumps(run(args.observations),indent=2))
