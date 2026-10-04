#!/usr/bin/env python3
"""Experiment 399: literal 9+3 binary-number profile across completion ensembles.

This follows the May-2026 historical proposal literally: each 12-cell class word
is split into a 9-bit primary number and a 3-bit tail number. It does not assign
semantic meaning to those numbers.
"""

from pathlib import Path
import json

from build_completion_universe import build
from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-399-literal-9plus3-number-profile.json"
SERIAL="ABCDEFGHI"
NATIVE="IABCDEFGH"

def class_word(master,j):
    return "".join(master[j+9*k] for k in range(12))

def binary_value(symbols,reverse=False):
    bits=[1 if ch=="/" else 0 for ch in symbols]
    if reverse:
        bits=list(reversed(bits))
    value=0
    for bit in bits:
        value=(value<<1)|bit
    return value

def class_profile(masters,reverse=False):
    rows=[]
    for letter in NATIVE:
        j=SERIAL.index(letter)
        bodies=set()
        tails=set()
        pairs=set()
        for master in masters:
            word=class_word(master,j)
            body=binary_value(word[:9],reverse)
            tail=binary_value(word[9:],reverse)
            bodies.add(body)
            tails.add(tail)
            pairs.add((body,tail))
        rows.append({
            "class":letter,
            "body_values":sorted(bodies),
            "tail_values":sorted(tails),
            "pair_count":len(pairs),
        })
    return rows

def main():
    _summary,u2_rows,_unknown=build()
    u2=[m for *_prefix,m in u2_rows]
    _u3,u4,u5=machine_layers()
    e2=[m for m in u4 if first_words(m)==("112","012","120")]
    assert len(e2)==2

    result={
        "experiment":399,
        "historical_model":"first nine marks encode a larger binary number; final three marks encode a smaller binary number",
        "bit_mapping":"slash=1; non-slash=0",
        "endianness_status":"historical proposal did not fix bit significance, so forward and reversed readings are both reported",
        "forward":{
            "U2":class_profile(u2,False),
            "U4":class_profile(u4,False),
            "U5":class_profile(u5,False),
            "E2":class_profile(e2,False),
        },
        "reversed":{
            "U2":class_profile(u2,True),
            "U4":class_profile(u4,True),
            "U5":class_profile(u5,True),
            "E2":class_profile(e2,True),
        },
    }

    e2f=result["forward"]["E2"]
    expected={
        "I":([357],[1]),
        "A":([302],[4]),
        "B":([382],[1]),
        "C":([58],[1,4]),
        "D":([151],[1]),
        "E":([311],[4]),
        "F":([407],[2]),
        "G":([369],[4]),
        "H":([129],[1]),
    }
    for row in e2f:
        bodies,tails=expected[row["class"]]
        assert row["body_values"]==bodies
        assert row["tail_values"]==tails

    result["E2_forward_profile"]={
        "I":[357,1],
        "A":[302,4],
        "B":[382,1],
        "C":{"body":58,"tail":[1,4]},
        "D":[151,1],
        "E":[311,4],
        "F":[407,2],
        "G":[369,4],
        "H":[129,1],
    }
    result["E2_reverse_profile"]={
        row["class"]:{
            "body":row["body_values"][0] if len(row["body_values"])==1 else row["body_values"],
            "tail":row["tail_values"][0] if len(row["tail_values"])==1 else row["tail_values"],
        }
        for row in result["reversed"]["E2"]
    }
    result["key_observation"]=(
        "The externally selected E2 pair fixes all nine 9-bit body numbers exactly. "
        "Its only remaining literal 9+3 ambiguity is class C's 3-bit tail value, "
        "1 versus 4 in forward bit order, corresponding exactly to the known "
        "residue-102 versus residue-84 slash ambiguity."
    )
    result["interpretation"]=(
        "The May-2026 9+3 binary-number proposal becomes a sharply constrained numeric profile under E2, "
        "but no independent downstream artifact is known to consume the resulting nine large/small number pairs. "
        "Preserve the profile as a frozen derived surface and do not search arbitrary books, ciphers, serial-address "
        "schemes, or numeric transforms until an external consumer supplies that operation."
    )

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
