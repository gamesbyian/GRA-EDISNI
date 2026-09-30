#!/usr/bin/env python3
"""Experiment 343: alphabet-boundary proof for the known lever password.

Under the historically attested sleeve mapping:
    / -> U
    - -> R
    . -> L

the observed alphabet boundary implies:
    H108 residues 1..81  can only be U/R
    H108 residues 82..108 can only be U/L

This checks whether the known 14-command bunker password, its reverse, or any
cyclic rotation can fit anywhere in that two-zone cyclic carrier even before
consulting individual physical observations.
"""

from __future__ import annotations
import json

CODE="UURLRRRUUURLLL"

def allowed(residue:int)->set[str]:
    return {"U","R"} if residue<=81 else {"U","L"}

def starts(word:str)->list[int]:
    out=[]
    for start in range(1,109):
        if all(word[j] in allowed(((start-1+j)%108)+1) for j in range(len(word))):
            out.append(start)
    return out

def rotations(word:str):
    return [(k,word[k:]+word[:k]) for k in range(len(word))]

def main():
    forward=starts(CODE)
    reverse=starts(CODE[::-1])
    rotated=[{"rotation":k,"word":w,"starts":starts(w)} for k,w in rotations(CODE)]
    reverse_rotated=[{"rotation":k,"word":w,"starts":starts(w)} for k,w in rotations(CODE[::-1])]
    out={
      "mapping":{"/":"U","-":"R",".":"L"},
      "zones":{
        "1-81":["U","R"],
        "82-108":["U","L"],
      },
      "known_bunker_code":CODE,
      "canonical_forward_starts":forward,
      "canonical_reverse_starts":reverse,
      "cyclic_rotations_with_any_start":[x for x in rotated if x["starts"]],
      "reverse_cyclic_rotations_with_any_start":[x for x in reverse_rotated if x["starts"]],
      "result":"The known bunker password cannot occur as any contiguous cyclic H108 window under the sleeve mapping, even with arbitrary start, reversal, and cyclic rotation, regardless of unknown sticker cells."
    }
    assert forward==[]
    assert reverse==[]
    assert not any(x["starts"] for x in rotated)
    assert not any(x["starts"] for x in reverse_rotated)
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
