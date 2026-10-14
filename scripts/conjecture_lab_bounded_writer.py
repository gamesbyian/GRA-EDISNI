#!/usr/bin/env python3
"""CL-VLEN-16: minimum per-instruction bit-write capacity around A–I tape.

Exact 512-state finite dynamic program; no codebook, no inferred physical mark.
"""
from __future__ import annotations
import argparse,json,random
from pathlib import Path
from collections import Counter
from conjecture_lab_minimal_tape_edits import body,shuffled,min_depth
import itertools

NEIGHBOR={radius:tuple(tuple(y for y in range(512) if (x^y).bit_count()<=radius) for x in range(512)) for radius in (0,1,2,3,4,5)}


def allowed(word):
    return frozenset(v for v in range(512) if all(c=='?' or (((v>>i)&1)==(c=='/')) for i,c in enumerate(word)))


def feasible(words, radius, witness=False):
    states=[allowed(w) for w in words]
    assert len(states[2])==1
    initial=next(iter(states[2]))
    reached={initial:None}
    parents=[]
    for step in range(9):
        target=(3+step)%9  # class D first, then ... I,A,B,C
        available=states[target]
        new={}
        for source in reached:
            for out in (NEIGHBOR[radius][source] if radius<=5 else range(512)):
                if out in available and out not in new:new[out]=source
        if witness:parents.append((target,new))
        if not new:return {'feasible':False,'failed_at':'ABCDEFGHI'[target]}
        reached=new
    found=initial in reached
    result={'feasible':found}
    if found and witness:
        chain=[initial];now=initial
        for target,pr in reversed(parents):
            before=pr[now];chain.append(before);now=before
        chain=list(reversed(chain))
        assert chain[0]==initial and chain[-1]==initial
        result['cycle_C_to_C']=[format(v,'09b')[::-1] for v in chain]
        result['step_change_counts']=[(a^b).bit_count() for a,b in zip(chain,chain[1:])]
    return result


def minimum_total_with_cap(words,k):
    """Exact joint minimum bit flips under global maximal per-step capacity."""
    states=[allowed(w) for w in words]
    initial=next(iter(states[2]))
    costs={initial:0}
    for step in range(9):
        target=states[(3+step)%9]
        result={}
        for current,cost in costs.items():
            for nxt in (NEIGHBOR[k][current] if k<=5 else range(512)):
                if nxt not in target:continue
                d=(current^nxt).bit_count()
                if d>k:continue
                total=cost+d
                if total<result.get(nxt,1000):result[nxt]=total
        costs=result
    return costs.get(initial)

def minimum_edit_completion_witness(words):
    winners=[min_depth(''.join(words[j][t] for j in range(9)))[1] for t in range(9)]
    best=None
    for choice in itertools.product(*winners):
        states=[sum(((choice[t]>>j)&1)<<t for t in range(9)) for j in range(9)]
        changes=[(states[i]^states[(i+1)%9]).bit_count() for i in range(9)]
        metric=(max(changes),sum(changes))
        if best is None or metric<(best[0],best[1]):
            best=(metric[0],metric[1],states,changes)
    assert best is not None
    return {'minimum_possible_max_writes_among_all_global_minimum_edit_completions':best[0], 'total_writes':best[1], 'A_to_I_states':{classid: ''.join('/' if (state>>j)&1 else '-' for j in range(9)) for classid,state in zip('ABCDEFGHI',best[2])},'A_to_B_to_C_to_D_to_E_to_F_to_G_to_H_to_I_to_A_writes':best[3]}

def audit(words,n):
    outcome={}
    for k in range(0,10):
        r=feasible(words,k,False)
        outcome[str(k)]=r
        if r['feasible']:break
    min_budget=next(int(k) for k,v in outcome.items() if v['feasible'])
    outcome[str(min_budget)]=feasible(words,min_budget,True)
    outcome[str(min_budget)]['minimum_total_changes_under_this_cap']=minimum_total_with_cap(words,min_budget)
    outcome['unlimited']={'minimum_total_changes':minimum_total_with_cap(words,9)}
    outcome['global_minimum_edit_example']=minimum_edit_completion_witness(words)
    controls={}
    for frame in (True,False):
        rng=random.Random(20261013+int(frame)+501);budgets=[]
        for _ in range(n):
            trial=shuffled(words,rng,frame)
            for k in range(0,10):
                if feasible(trial,k)['feasible']:
                    budgets.append(k);break
            else:raise RuntimeError('all-nine flip program must be possible')
        controls['original_frame9' if frame else 'same_class']={'n':n,'at_most_observed':sum(x<=min_budget for x in budgets),'median':sorted(budgets)[len(budgets)//2] if budgets else None,'histogram':dict(sorted(Counter(budgets).items()))}
    return {'minimum_per_step_write_capacity':min_budget,'radii_checked':outcome,'control':controls}


def test():
    assert all(len(NEIGHBOR[k][0])==sum(__import__('math').comb(9,j) for j in range(k+1)) for k in range(6))
    assert len(NEIGHBOR[0][3])==1 and NEIGHBOR[0][3][0]==3
    assert feasible(['---------']*9,0)['feasible']
    print('PASS: independently counted Hamming balls and finite state reachability')


def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--nulls',type=int,default=1000);p.add_argument('--test',action='store_true');p.add_argument('--output',default='data/conjecture-lab-bounded-writer-2026-10-13.json');a=p.parse_args()
    if a.test:
        # trivial C-only fixture: other cells equal, is exact for radius 0
        test();return
    result={'status':'DISCOVER: unrestricted per-step bit writes, not an identified codebook','actual':audit(body(a.observations),a.nulls)}
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result)
if __name__=='__main__':main()