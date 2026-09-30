#!/usr/bin/env python3
"""Experiment 329: exploratory one-exception selected-line audit.

Uses only physical observations plus the observation-compatible one-slash tail
family from Experiment 317. The one-exception criterion was introduced after
the row/column replay, so this is exploratory and must not be counted as a
preregistered confirmation of POS3.
"""

from __future__ import annotations
import argparse, csv, json
from itertools import product
from pathlib import Path

CLASSES="ABCDEFGHI"
ALLOWED={"A":[0,1,2],"B":[2],"C":[0,1,2],"D":[1,2],"E":[0],"F":[1],"G":[0,2],"H":[2],"I":[2]}

def load(path:Path)->dict[int,str]:
    out={}
    with path.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s: raise ValueError(f"conflict at residue {r}")
            out[r]=s
    return out

def possible_one_exception(line:list[str])->bool:
    u=[i for i,x in enumerate(line) if x=="?"]
    for bits in product("/-",repeat=len(u)):
        a=line[:]
        for i,b in zip(u,bits): a[i]=b
        if a.count("/") in (1,2): return True
    return False

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    args=ap.parse_args()
    obs=load(Path(args.observations))
    body={c:[obs.get(1+i+9*k,"?") for k in range(9)] for i,c in enumerate(CLASSES)}
    def row(c,p): return body[c][3*p:3*p+3]
    def col(c,p): return [body[c][p],body[c][p+3],body[c][p+6]]

    details={}
    for c in CLASSES:
        details[c]={"allowed_tail_positions":ALLOWED[c],
                    "rows":{str(p):{"trace":"".join(row(c,p)),"one_exception_possible":possible_one_exception(row(c,p))} for p in ALLOWED[c]},
                    "columns":{str(p):{"trace":"".join(col(c,p)),"one_exception_possible":possible_one_exception(col(c,p))} for p in ALLOWED[c]}}

    assignments=[]
    for picks in product(*(ALLOWED[c] for c in CLASSES)):
        a=dict(zip(CLASSES,picks))
        assignments.append({
            "selector":"".join(str(a[c]) for c in CLASSES),
            "row_ok":all(possible_one_exception(row(c,a[c])) for c in CLASSES),
            "column_ok":all(possible_one_exception(col(c,a[c])) for c in CLASSES),
        })
    row_ok=[x for x in assignments if x["row_ok"]]
    col_ok=[x for x in assignments if x["column_ok"]]
    row_allowed={c:sorted({int(x["selector"][i]) for x in row_ok}) for i,c in enumerate(CLASSES)}

    out={"tail_assignments_tested":len(assignments),"row_one_exception_survivors":len(row_ok),
         "column_one_exception_survivors":len(col_ok),"row_surviving_positions":row_allowed,
         "details":details,
         "prospective_C_tail":{"residues":[84,93,102],"symbols":"../"},
         "status":"exploratory: criterion introduced after row/column outputs were already inspected"}
    assert len(assignments)==36
    assert len(row_ok)==12
    assert len(col_ok)==0
    assert row_allowed=={"A":[0,1,2],"B":[2],"C":[2],"D":[1,2],"E":[0],"F":[1],"G":[0,2],"H":[2],"I":[2]}
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
