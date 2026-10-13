#!/usr/bin/env python3
"""CL-VLEN-15: exhaust all 20,160 unoriented A–I circular tape orders.

The order comparison is post-hoc exploration; no claim of independently
precommitted authorial choreography.
"""
import argparse,itertools,json
from collections import Counter
from pathlib import Path
from conjecture_lab_minimal_tape_edits import body, min_results

def minimum_order(words,order):
    total=0
    for t in range(9):
        bits=[words[i][t] for i in order if words[i][t]!='?']
        if not bits:continue
        total+=sum(a!=b for a,b in zip(bits,bits[1:]+bits[:1]))
    return total

def all_orders(words):
    hist=Counter(); at_actual=[];better=[]; equal=0;count=0
    observed=minimum_order(words,tuple(range(9)))
    for p in itertools.permutations(range(1,9)):
        if p[0]>p[-1]:continue # choose one representative of reverse equivalence
        order=(0,)+p
        s=minimum_order(words,order)
        hist[s]+=1
        count+=1
        if s==observed:equal+=1
        if s<observed:better.append((''.join('ABCDEFGHI'[x] for x in order),s))
        if s<=observed and len(at_actual)<45:at_actual.append((''.join('ABCDEFGHI'[x] for x in order),s))
    assert count==20160
    return {'native_ABC_cycle_cost':observed,'unoriented_cyclic_orders':count,'number_below_native':len(better),'number_equal_native':equal,'number_at_most_native':sum(v for k,v in hist.items() if k<=observed),'min_possible_cost':min(hist),'histogram':dict(sorted(hist.items())),'first_40_better_alternative_cycles':better[:40],'first_45_at_most_native':at_actual}

def heldout_class_order_ranks(words):
    """Does natural order stay uncommon after removing an entire class?"""
    result={}
    for ignored in range(9):
        subset=[i for i in range(9) if i!=ignored]
        natural=minimum_order(words,subset)
        prefix=subset[0]
        at_most=0;below=0;total=0;hist=Counter()
        for p in itertools.permutations(subset[1:]):
            if p[0]>p[-1]:continue
            order=(prefix,)+p
            score=minimum_order(words,order)
            hist[score]+=1;total+=1
            if score<=natural:at_most+=1
            if score<natural:below+=1
        assert total==2520
        result['ABCDEFGHI'[ignored]]={'native_cost_without_class':natural,'at_most_native':at_most,'strictly_better':below,'circular_orders':total}
    return result


def mosaic_scan_orders(words):
    source=['IAB','CDE','FGH']
    unique={}
    for mirror in (False,True):
        for rotation in range(4):
            matrix=[list(row) for row in source]
            if mirror:matrix=[list(reversed(row)) for row in matrix]
            for _ in range(rotation):matrix=[[matrix[2-c][r] for c in range(3)] for r in range(3)]
            for snake in (False,True):
                scan=''.join(''.join(reversed(row)) if snake and i%2 else ''.join(row) for i,row in enumerate(matrix))
                order=tuple('ABCDEFGHI'.index(x) for x in scan)
                key=min(tuple(order[k:]+order[:k]) for k in range(9))
                reverse=tuple(reversed(order))
                k2=min(tuple(reverse[k:]+reverse[:k]) for k in range(9))
                code=min(key,k2)
                unique[code]={'cost':minimum_order(words,order),'scan':scan,'snake':snake,'rotation':rotation,'mirror':mirror}
    return {'unique_unoriented_scans':len(unique),'scores':sorted(unique.values(),key=lambda x:(x['cost'],x['scan']))}


def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--output',default='data/conjecture-lab-tape-order-rank-2026-10-13.json');a=p.parse_args()
    w=body(a.observations)
    r=all_orders(w)
    r['leave_one_class_out_rank']=heldout_class_order_ranks(w)
    r['mosaic_scans']=mosaic_scan_orders(w)
    assert r['native_ABC_cycle_cost']==min_results(w,False)['minimum_writes']
    Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print({k:r[k] for k in ('native_ABC_cycle_cost','unoriented_cyclic_orders','number_at_most_native','number_below_native','min_possible_cost')})
if __name__=='__main__':main()