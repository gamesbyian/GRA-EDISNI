#!/usr/bin/env python3
"""Experiment 399: historical 9+3 binary-number representation over coherent completions."""

from pathlib import Path
import json

from audit_completion_universe_layers import machine_layers
from audit_534brn_universe_survival import first_words

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-399-nine-plus-three-numeric-surface.json"
SERIAL="ABCDEFGHI"

def class_word(master,j):
    return "".join(master[j+9*k] for k in range(12))

def bits_to_int(bits):
    value=0
    for ch in bits:
        value=value*2+(1 if ch=="/" else 0)
    return value

def pair(master,j):
    word=class_word(master,j)
    return (bits_to_int(word[:9]),bits_to_int(word[9:]))

def per_class_support(masters):
    out={}
    for j,letter in enumerate(SERIAL):
        body=sorted({pair(m,j)[0] for m in masters})
        tail=sorted({pair(m,j)[1] for m in masters})
        out[letter]={"body_9bit_values":body,"tail_3bit_values":tail}
    return out

def main():
    _u3,u4,u5=machine_layers()
    e2=[m for m in u4 if first_words(m)==("112","012","120")]
    assert len(e2)==2

    result={
        "experiment":399,
        "historical_operation":"interpret each native 12-cell class word as first-nine binary value plus last-three binary value, exactly as proposed in May 2026",
        "bit_convention":"slash=1; dash/dot=0; leftmost position is most-significant bit",
        "ranges":{"body":"0..511","tail":"0..7"},
        "U4_support":per_class_support(u4),
        "U5_support":per_class_support(u5),
        "E2_support":per_class_support(e2),
    }

    expected_body={
        "A":[302],"B":[382],"C":[58],"D":[151],"E":[311],
        "F":[407],"G":[369],"H":[129],"I":[357],
    }
    for letter,vals in expected_body.items():
        assert result["E2_support"][letter]["body_9bit_values"]==vals

    expected_tail={
        "A":[4],"B":[1],"C":[1,4],"D":[1],"E":[4],
        "F":[2],"G":[4],"H":[1],"I":[1],
    }
    for letter,vals in expected_tail.items():
        assert result["E2_support"][letter]["tail_3bit_values"]==vals

    result["E2_body_vector_A_to_I"]=[302,382,58,151,311,407,369,129,357]
    result["E2_tail_vector_A_to_I"]=["4","1","1|4","1","4","2","4","1","1"]
    result["interpretation"]=(
        "The historical 9+3 numeric representation is a legitimate compact surface for future consumers. "
        "For the externally selected pair, all nine 9-bit body numbers are already fixed; the only remaining "
        "numeric ambiguity is class C's one-hot tail value, exactly the residue-84/residue-102 physical fork. "
        "The tail never spans 0..7 in live completions because its one-slash structure restricts it to one-hot "
        "values 1,2,4. No specific book/page/domain consumer is independently identified, so these numbers are "
        "preserved as a robust representation rather than decoded semantically."
    )

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
