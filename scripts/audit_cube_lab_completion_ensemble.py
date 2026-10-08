#!/usr/bin/env python3
"""Experiment 459: full cube-lab relation rates over all 324 exact masters.

Faithfully copies the independent lab's cross-cube pairing definitions:
all unordered cross-cube pairs, |axis separation|=1, no wrap; the
flat-column relation uses same A-I letter but a different depth.
Full candidate statistics are *model-conditioned*, not independently
confirmed matches to new stickers.
"""
from itertools import product
from collections import Counter
import json
from enumerate_sticker_completion_ensembles import (
    observations, primary_frame_choices, primary_columns, q4_choices,
    make_master,
)

MODES = ("exact", "x", "y", "z", "flat")
LAYOUTS = ("IABCDEFGH", "ABCDEFGHI")
LETTERS = "ABCDEFGHI"


def edges(layout, mode):
    cells = []
    def co(r):
        slot = layout.index(LETTERS[(r-1)%9])
        return ((r-1)//27, ((r-1)%27)//9, slot%3, slot//3, (r-1)%9)
    for a in range(1,109):
        ac,az,ax,ay,al = co(a)
        for b in range(a+1,109):
            bc,bz,bx,by,bl = co(b)
            if ac == bc:
                continue
            dz,dx,dy = abs(az-bz),abs(ax-bx),abs(ay-by)
            yes = (
                (mode=="exact" and (dz,dx,dy)==(0,0,0)) or
                (mode=="x" and (dz,dx,dy)==(0,1,0)) or
                (mode=="y" and (dz,dx,dy)==(0,0,1)) or
                (mode=="z" and (dz,dx,dy)==(1,0,0)) or
                (mode=="flat" and al==bl and dz!=0)
            )
            if yes:
                cells.append((a-1,b-1))
    return cells


def main():
    physical, obs = observations()
    assert physical==84 and len(obs)==66
    frames = [
        [x for x in primary_frame_choices(obs,f) if primary_columns(x)]
        for f in range(9)
    ]
    tails = list(product(*q4_choices(obs)))
    masters = [make_master(ff, selectors)
               for ff in product(*frames) for selectors in tails]
    assert len(masters)==324

    result={}
    for layout in LAYOUTS:
        es={m:edges(layout,m) for m in MODES}
        rates={m:[] for m in MODES}
        for master in masters:
            for mode in MODES:
                matches=sum(master[a]==master[b] for a,b in es[mode])
                rates[mode].append(matches/len(es[mode]))
        same=rates["exact"]
        comparisons={}
        for mode in MODES:
            a=rates[mode]
            comparisons[mode]={"pairs_per_complete_master":len(es[mode]),
                               "minimum_rate":min(a),"maximum_rate":max(a),
                               "mean_rate":sum(a)/len(a)}
            if mode!="exact":
                contrasts=[x-y for x,y in zip(same,a)]
                comparisons[mode].update({
                    "same_spot_minus_shift_min":min(contrasts),
                    "same_spot_minus_shift_max":max(contrasts),
                    "same_spot_minus_shift_mean":sum(contrasts)/len(contrasts),
                    "masters_with_same_spot_better":sum(d>0 for d in contrasts)})
        result[layout]=comparisons

    assert all(result[layout][mode]["masters_with_same_spot_better"]==324
               for layout in LAYOUTS for mode in MODES if mode!="exact")
    print(json.dumps({
        "physical_records":physical,"unique_residues":len(obs),
        "complete_candidate_masters":len(masters),"layouts":result,
        "interpretation":"The one-minority-per-column model itself makes"
        " exact alignment superior across all 324 full sequences; no"
        " independent proof of intended cube registration is obtained."
    },indent=2))


if __name__=="__main__":
    main()
