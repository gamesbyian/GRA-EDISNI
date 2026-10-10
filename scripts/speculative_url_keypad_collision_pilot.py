#!/usr/bin/env python3
"""SR-03 pilot: nine-digit CE URL as a NONBIJECTIVE keypad selector.

Input comes from the physically associated, historically index-recognized
CE background URL, not the unknown sticker foreground. Arithmetic and
D4 variants are exhaustive; no image fitting or candidate fills.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path
PATH="dat/534brn9653f9j8mmd"
EXPECTED="534965398"
GRID=(("I","A","B"),("C","D","E"),("F","G","H"))
def transformations(board):
    flip=lambda a:tuple(tuple(reversed(row)) for row in a)
    rotate=lambda a:tuple(tuple(a[2-j][i] for j in range(3)) for i in range(3))
    x=board
    for i in range(4):
        yield f"r{i*90}",x
        yield f"r{i*90}_mirror",flip(x)
        x=rotate(x)
def run():
    digits="".join(c for c in PATH.split("/")[-1] if c.isdecimal())
    assert digits==EXPECTED and len(digits)==9
    counts=Counter(digits)
    assert dict(sorted(counts.items()))=={"3":2,"4":1,"5":2,"6":1,"8":1,"9":2}
    assert set("123456789")-set(digits)==set("127")
    pos=lambda n:((int(n)-1)//3,(int(n)-1)%3)
    routes=[pos(n) for n in digits]
    from collections import defaultdict
    nodes=defaultdict(list)
    for i,n in enumerate(digits):
        nodes[n].append({"ordinal":i+1,"background":GRID[i//3][i%3],
                         "physical_coord":[i//3,i%3]})
    assert sorted(len(x) for x in nodes.values())==[1,1,1,2,2,2]
    sym=[]
    for label,t in transformations(tuple(tuple(row) for row in GRID)):
        trail="".join(t[i//3][i%3] for i in range(9))
        sym.append({"orientation":label,"background_order":trail})
    assert len(sym)==8 and len({s["background_order"] for s in sym})==8
    return {"source_path":PATH,"digits":digits,"grid_rows":["".join(x) for x in GRID],
            "digit_counts":dict(sorted(counts.items())),"missing_digits":"127",
            "duplicate_digit_classes":"359","distinct_targets":6,
            "nonbijective":True,"digit_keypad_coordinates":routes,
            "physical_repeated_label_classes":dict(nodes),
            "eight_orientation_controls":sym,
            "answer_claim":"none: collision geometry is source-fixed but output/consumer and orientation are not"}
if __name__=="__main__":
    result=run()
    print(json.dumps(result,indent=2))
