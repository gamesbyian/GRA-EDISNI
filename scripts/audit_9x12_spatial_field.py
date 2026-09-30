#!/usr/bin/env python3
"""Experiment 326: observation-only 9x12 / 9x9 spatial-field audit."""

from __future__ import annotations
import argparse, csv, json, random
from pathlib import Path

CLASSES = "ABCDEFGHI"
PHYSICAL_FLAT = "IABCDEFGH"  # IAB / CDE / FGH

def load_observations(path: Path) -> dict[int, str]:
    values: dict[int, str] = {}
    with path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r, s = int(row["residue"]), row["symbol"]
            if r in values and values[r] != s:
                raise ValueError(f"conflict at residue {r}: {values[r]!r} vs {s!r}")
            values[r] = s
    return values

def body_grid(values: dict[int, str], order: str) -> list[list[str]]:
    idx = {c:i for i,c in enumerate(CLASSES)}
    cols = [idx[c] for c in order]
    return [[values.get(1+i+9*layer, "?") for i in cols] for layer in range(9)]

def tail_grid(values: dict[int, str], order: str) -> list[list[str]]:
    idx = {c:i for i,c in enumerate(CLASSES)}
    return [[values.get(82+idx[c]+9*t, "?") for t in range(3)] for c in order]

def adjacency_stat(grid: list[list[str]]) -> tuple[dict[str,int], dict[tuple[int,int],str], list[tuple[tuple[int,int],tuple[int,int]]]]:
    known={(r,c):grid[r][c] for r in range(9) for c in range(9) if grid[r][c] in "/-"}
    edges=[]
    for r,c in known:
        for dr,dc in ((1,0),(0,1)):
            q=(r+dr,c+dc)
            if q in known: edges.append(((r,c),q))
    same=sum(known[a]==known[b] for a,b in edges)
    out={"known":len(known),"slash":sum(v=="/" for v in known.values()),
         "dash":sum(v=="-" for v in known.values()),"known_known_edges":len(edges),
         "same_symbol_edges":same}
    return out, known, edges

def permutation_null(grid: list[list[str]], iterations:int, seed:int) -> dict[str,float]:
    stats, known, edges=adjacency_stat(grid)
    coords=list(known)
    labels=["/"]*stats["slash"]+["-"]*stats["dash"]
    obs=stats["same_symbol_edges"]
    rng=random.Random(seed)
    total=total2=ge=le=0
    for _ in range(iterations):
        rng.shuffle(labels)
        lab=dict(zip(coords,labels))
        x=sum(lab[a]==lab[b] for a,b in edges)
        total+=x; total2+=x*x; ge+=x>=obs; le+=x<=obs
    mean=total/iterations
    sd=max(0.0,total2/iterations-mean*mean)**0.5
    return {"iterations":iterations,"seed":seed,"mean_same_symbol_edges":mean,
            "sd_same_symbol_edges":sd,"z":(obs-mean)/sd if sd else 0.0,
            "p_high":(ge+1)/(iterations+1),"p_low":(le+1)/(iterations+1)}

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--observations",default="data/observations.csv")
    ap.add_argument("--iterations",type=int,default=200_000)
    ap.add_argument("--seed",type=int,default=324)
    args=ap.parse_args()
    values=load_observations(Path(args.observations))
    out={"unique_observed_residues":len(values),
         "body_observed_residues":sum(r<=81 for r in values),
         "tail_observed_residues":sum(r>81 for r in values),"layouts":{}}
    for name,order in (("serial_A_to_I",CLASSES),("physical_flat_IAB_CDE_FGH",PHYSICAL_FLAT)):
        grid=body_grid(values,order); tail=tail_grid(values,order)
        stats,_,_=adjacency_stat(grid)
        out["layouts"][name]={"column_order":order,"body_9x9":["".join(x) for x in grid],
                              "tail_9x3_by_class":["".join(x) for x in tail],
                              "adjacency":stats,
                              "permutation_null":permutation_null(grid,args.iterations,args.seed)}
    assert out["unique_observed_residues"]==65
    assert out["body_observed_residues"]==54
    assert out["tail_observed_residues"]==11
    assert out["layouts"]["serial_A_to_I"]["adjacency"]=={"known":54,"slash":32,"dash":22,"known_known_edges":64,"same_symbol_edges":30}
    assert out["layouts"]["physical_flat_IAB_CDE_FGH"]["adjacency"]=={"known":54,"slash":32,"dash":22,"known_known_edges":62,"same_symbol_edges":29}
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
