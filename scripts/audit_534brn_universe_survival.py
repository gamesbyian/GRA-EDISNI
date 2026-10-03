#!/usr/bin/env python3
from pathlib import Path
import json

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from enumerate_raw_machine import SERIAL_ORDER, PHYSICAL_LAYOUT

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-390-534brn-universe-survival.json"
TARGET=("112","012","120")

def selector(master):
    out={}
    for j in range(9):
        ds=[d for d in range(3) if master[82+9*d+j-1]=="/"]
        if len(ds)!=1: return None
        out[j]=ds[0]
    return out

def sym(master,q,d,row,col):
    letter=PHYSICAL_LAYOUT[row][col]
    j=SERIAL_ORDER.index(letter)
    return master[(1+27*q+9*d+j)-1]

def decode(surface):
    s=""
    for col in range(3):
        rs=[row for row in range(3) if surface[row][col]=="-"]
        if len(rs)!=1: return None
        s+=str(rs[0])
    return s

def first_words(master):
    sel=selector(master)
    if sel is None: return None
    words=[]
    for q in range(3):
        surface=[]
        for row in range(3):
            rr=[]
            for col in range(3):
                letter=PHYSICAL_LAYOUT[row][col]
                j=SERIAL_ORDER.index(letter)
                rr.append(sym(master,q,sel[j],row,col))
            surface.append(tuple(rr))
        words.append(decode(tuple(surface)))
    if None in words: return None
    return tuple(words)

def summarize(masters):
    counts={}
    hits=[]
    for m in masters:
        w=first_words(m)
        if w is None: continue
        k="/".join(w)
        counts[k]=counts.get(k,0)+1
        if w==TARGET: hits.append(m)
    return {
        "candidate_count":len(masters),
        "g5_valid_count":sum(counts.values()),
        "distinct_g5_objects":len(counts),
        "target_count":len(hits),
        "g5_object_counts":dict(sorted(counts.items())),
        "_hits":set(hits),
    }

def main():
    _summary,u2rows,_unknown=build()
    u2=[m for *_p,m in u2rows]
    u3,u4,u5=machine_layers()
    layers={"U2":u2,"U3":u3,"U4":u4,"U5":u5}
    out={"experiment":390,"fingerprint":"112/012/120","layers":{}}
    hitsets={}
    for name,masters in layers.items():
        s=summarize(masters)
        hitsets[name]=s.pop("_hits")
        out["layers"][name]=s

    assert [out["layers"][x]["candidate_count"] for x in ("U2","U3","U4","U5")]==[648,216,20,14]
    assert [out["layers"][x]["g5_valid_count"] for x in ("U2","U3","U4","U5")]==[20,20,20,14]
    assert [out["layers"][x]["target_count"] for x in ("U2","U3","U4","U5")]==[2,2,2,0]
    assert hitsets["U2"]==hitsets["U3"]==hitsets["U4"]
    assert not hitsets["U5"]

    out["cross_layer"]={
        "same_two_target_masters_U2_U3_U4":True,
        "target_survives_second_recursive_closure":False,
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
