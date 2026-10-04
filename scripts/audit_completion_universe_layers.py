#!/usr/bin/env python3
"""Experiment 366: compare invariants and discriminator structure across U2-U5."""

from __future__ import annotations
import itertools, json, math
from pathlib import Path

from build_completion_universe import build
from enumerate_raw_machine import (
    decode_dash_pos3, first_pass_surface, primary_column_candidates,
    enumerate_primary_payloads, q4_selector_candidates, enumerate_selectors,
    terminal_surface, load_rows, generate_master,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-366-universe-layer-audit.json"

def signature_count(masters,residues):
    return len({tuple(m[r-1] for r in residues) for m in masters})

def invariant_map(masters,unknown):
    fixed={}; variable=[]
    for r in unknown:
        values=sorted({m[r-1] for m in masters})
        if len(values)==1: fixed[r]=values[0]
        else: variable.append(r)
    return fixed,variable

def minimum_discriminators(masters,unknown,limit_examples=12):
    _fixed,vars_=invariant_map(masters,unknown)
    lower=math.ceil(math.log2(len(masters)))
    for k in range(lower,len(vars_)+1):
        good=[]
        for residues in itertools.combinations(vars_,k):
            if signature_count(masters,residues)==len(masters):
                good.append(residues)
        if good:
            return {
                "information_lower_bound":lower,
                "minimum_size":k,
                "number_of_minimum_sets":len(good),
                "examples":[list(x) for x in good[:limit_examples]],
            }
    raise AssertionError("no discriminator")

def equivalence_groups(masters,unknown):
    _fixed,vars_=invariant_map(masters,unknown)
    buckets={}
    for r in vars_:
        pattern=tuple(m[r-1]=="/" for m in masters)
        inv=tuple(not x for x in pattern)
        canon=min(pattern,inv)
        buckets.setdefault(canon,[]).append({
            "residue":r,
            "inverted_from_canonical":pattern!=canon,
        })
    return [g for g in buckets.values() if len(g)>1]

def machine_layers():
    rows=load_rows()
    payloads=list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors=list(enumerate_selectors(q4_selector_candidates(rows)))
    u3=[generate_master(p,s) for p in payloads for s in selectors]
    assert len(u3)==108 and len(set(u3))==108

    u4=[]; u5=[]
    for p in payloads:
        for s in selectors:
            master=generate_master(p,s)
            first=tuple(decode_dash_pos3(first_pass_surface(p,s,q)) for q in range(3))
            if None in first:
                continue
            u4.append(master)
            terminal=decode_dash_pos3(terminal_surface(p,s))
            if terminal is not None:
                u5.append(master)
    assert len(u4)==12 and len(set(u4))==12
    assert len(u5)==10 and len(set(u5))==10
    return u3,u4,u5

def main():
    _summary,u2_rows,unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    u3,u4,u5=machine_layers()
    layers={"U2":u2,"U3":u3,"U4":u4,"U5":u5}

    result={"experiment":366,"layers":{}}
    prev_fixed={}
    for name,masters in layers.items():
        fixed,variable=invariant_map(masters,unknown)
        new_fixed={str(r):v for r,v in fixed.items() if r not in prev_fixed}
        result["layers"][name]={
            "candidate_count":len(masters),
            "invariant_unobserved_count":len(fixed),
            "variable_unobserved_count":len(variable),
            "invariant_unobserved":{str(k):v for k,v in fixed.items()},
            "newly_fixed_vs_previous_layer":new_fixed,
            "variable_residues":variable,
            "minimum_discriminator":minimum_discriminators(masters,unknown),
            "equivalence_groups":equivalence_groups(masters,unknown),
        }
        prev_fixed=fixed

    assert result["layers"]["U2"]["invariant_unobserved_count"]==24
    assert result["layers"]["U3"]["newly_fixed_vs_previous_layer"]=={
        "49":"-","50":"-","52":"-","54":"-"
    }
    assert result["layers"]["U4"]["newly_fixed_vs_previous_layer"]=={"93":"."}
    assert result["layers"]["U5"]["newly_fixed_vs_previous_layer"]=={"82":"."}
    assert result["layers"]["U5"]["variable_residues"]==[
        22,25,55,58,61,84,88,91,94,100,102,106
    ]
    assert [result["layers"][x]["minimum_discriminator"]["minimum_size"] for x in ("U2","U3","U4","U5")]==[11,9,6,5]

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
