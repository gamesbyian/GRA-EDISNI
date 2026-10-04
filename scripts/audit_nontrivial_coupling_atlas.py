#!/usr/bin/env python3
"""Experiment 407: nontrivial complement-coupling atlas across U2/U4/U5/E2."""

from pathlib import Path
import json

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-407-nontrivial-coupling-atlas.json"

def bit(master,residue):
    return 1 if master[residue-1]=="/" else 0

def variable_positions(masters):
    return [r for r in range(1,109) if len({bit(m,r) for m in masters})>1]

def relations(child,parent_variable):
    child_var=set(variable_positions(child))
    active=[r for r in parent_variable if r in child_var]
    out=[]
    for i,a in enumerate(active):
        for b in active[i+1:]:
            eq=all(bit(m,a)==bit(m,b) for m in child)
            comp=all(bit(m,a)!=bit(m,b) for m in child)
            if eq or comp:
                out.append([a,b,"eq" if eq else "comp"])
    return out

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    _u3,u4,u5=machine_layers()
    e2=[m for m in u4 if first_words(m)==("112","012","120")]
    assert len(e2)==2

    v2=variable_positions(u2)
    v4=variable_positions(u4)
    v5=variable_positions(u5)
    ve=variable_positions(e2)

    r24=relations(u4,v2)
    r45=relations(u5,v4)
    r4e=relations(e2,v4)

    assert r24==[[22,25,"comp"],[84,102,"comp"],[88,106,"comp"],[94,103,"comp"]]
    assert r45==[[22,25,"comp"],[84,102,"comp"],[88,106,"comp"],[91,100,"comp"],[94,103,"comp"]]
    assert r4e==[[84,102,"comp"]]

    result={
        "experiment":407,
        "variable_residue_counts":{"U2":len(v2),"U4":len(v4),"U5":len(v5),"E2":len(ve)},
        "U2_to_U4_nontrivial_relations":r24,
        "U4_to_U5_nontrivial_relations":r45,
        "U4_to_E2_nontrivial_relations":r4e,
        "interpretation":(
            "After excluding fixed-cell trivialities, U4 creates four exact complement couplings. "
            "G6 adds exactly one, residue 91 versus 100. E2 fixes every U4 degree of freedom "
            "except the existing 84/102 complement pair."
        )
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
