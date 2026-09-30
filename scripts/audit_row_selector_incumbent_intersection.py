#!/usr/bin/env python3
"""Experiment 331: frozen row-selector rival x incumbent structural intersection."""

from __future__ import annotations
import json
from itertools import product

CLASSES="ABCDEFGHI"
PHYSICAL_POSITION={"I":(0,0),"A":(0,1),"B":(0,2),"C":(1,0),"D":(1,1),"E":(1,2),"F":(2,0),"G":(2,1),"H":(2,2)}
ROW_DOMAINS={"A":{0,1,2},"B":{2},"C":{2},"D":{1,2},"E":{0},"F":{1},"G":{0,2},"H":{2},"I":{2}}

def legal_states():
    out=[]
    for X,Y,Z,G in product((0,1),repeat=4):
        if Y and Z and not X: continue
        out.append((X,Y,Z,G))
    return out

def grants(st):
    X,Y,Z,G=st
    return int(Y and not Z), int((not X) and (not Y)), int(X and ((not Y) or Z))

def q4(st):
    X,Y,Z,G=st; P0,P1,P2=grants(st)
    return {"I":2,"A":2-P0,"B":2,"C":2*G,"D":1+P1,"E":0,"F":1,"G":2*P2,"H":2}

def payload(st):
    X,Y,Z,G=st; x=1+X; y=2 if Y else Z
    return [["112","212",f"0{x}0"],["212","002","100"],[f"1{y}2","022","100"]]

def primary_symbol(st,r):
    off=r-1; q=off//27; d=(off%27)//9; j=off%9
    c=CLASSES[j]; row,col=PHYSICAL_POSITION[c]
    minority=int(payload(st)[q][d][col]); minority_dash=d<=q
    on=row==minority
    return "-" if (on and minority_dash) or ((not on) and not minority_dash) else "/"

def body(st,c):
    i=CLASSES.index(c)
    return [primary_symbol(st,1+i+9*k) for k in range(9)]

def one_exception(xs):
    return xs.count("/") in (1,2)

def q4_symbol(st,r):
    off=r-82; depth=off//9; c=CLASSES[off%9]
    return "/" if depth==q4(st)[c] else "."

def fsym(st,r):
    return primary_symbol(st,r) if r<=81 else q4_symbol(st,r)

def main():
    states=legal_states()
    inc_domains={c:{q4(st)[c] for st in states} for c in CLASSES}
    domain_comparison={}
    for c in CLASSES:
        rd=ROW_DOMAINS[c]; inc=inc_domains[c]
        relation="equal" if rd==inc else "row_superset" if rd>inc else "row_subset" if rd<inc else "overlap"
        domain_comparison[c]={"row":sorted(rd),"incumbent":sorted(inc),"relation":relation}

    shared=[]
    failures=[]
    for st in states:
        sels=q4(st)
        domain_ok=all(sels[c] in ROW_DOMAINS[c] for c in CLASSES)
        line_bad={}
        if domain_ok:
            for c in CLASSES:
                p=sels[c]; line=body(st,c)[3*p:3*p+3]
                if not one_exception(line): line_bad[c]="".join(line)
        if domain_ok and not line_bad:
            shared.append(st)
        else:
            failures.append({"state":"".join(map(str,st)),"domain_ok":domain_ok,"bad_selected_rows":line_bad})

    extra={}
    for r in range(1,109):
        all_symbols={fsym(st,r) for st in states}
        shared_symbols={fsym(st,r) for st in shared}
        if len(all_symbols)>1 and len(shared_symbols)==1:
            extra[str(r)]=next(iter(shared_symbols))

    out={
      "incumbent_states":len(states),
      "domain_comparison":domain_comparison,
      "exact_domain_matches":sum(v["relation"]=="equal" for v in domain_comparison.values()),
      "all_domains_overlap":all(set(v["row"]) & set(v["incumbent"]) for v in domain_comparison.values()),
      "states_matching_row_selector_domain_only":["".join(map(str,s)) for s in states if all(q4(s)[c] in ROW_DOMAINS[c] for c in CLASSES)],
      "states_matching_full_frozen_row_family":["".join(map(str,s)) for s in shared],
      "shared_state_count":len(shared),
      "failures":failures,
      "newly_forced_vs_14_state_incumbent":extra,
    }
    assert out["exact_domain_matches"]==7
    assert out["all_domains_overlap"]
    assert out["states_matching_row_selector_domain_only"]==["0001","0011","0101","1001","1011","1101","1111"]
    assert out["states_matching_full_frozen_row_family"]==["0011","0101","1001","1011","1101","1111"]
    assert extra=={"84":".","102":"/"}
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
