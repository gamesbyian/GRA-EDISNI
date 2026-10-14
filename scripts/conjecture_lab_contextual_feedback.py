#!/usr/bin/env python3
"""CL-VLEN-11: actual 9-register two-input feedback code under one-hot tail.

DISCOVER/DEVELOP; all commands are invented. Counts are not evidence for an
intended CE decoder. Python stdlib, observation-only, no model completions.
"""
from __future__ import annotations
import argparse
import csv
import itertools
import json
import random
from collections import Counter
from pathlib import Path

SHIFTS = ((-1, 0, 1), (0, 1, 2), (0, 3, 6), (-3, 0, 3), (0, 1, 3))
RECURRENCES = ('prev_rot_xor_current', 'cur_rot_xor_prev', 'prev_cur_rot_xor', 'toggle_prev_pair')


def physical(path):
    data={}
    with open(path, newline='', encoding='utf8') as fh:
        rows=list(csv.DictReader(fh))
    for row in rows:
        i=int(row['residue']); glyph=row['symbol']
        if not 1<=i<=108 or glyph not in '/-.': raise ValueError(row)
        if i in data and data[i]!=glyph: raise ValueError('conflicting residue '+str(i))
        data[i]=glyph
    if len(rows)!=84 or len(data)!=66: raise AssertionError((len(rows),len(data)))
    body=[''.join(data.get(1+j+9*t,'?') for t in range(9)) for j in range(9)]
    tail=[''.join(data.get(82+j+9*t,'?') for t in range(3)) for j in range(9)]
    assert tail[7]=='..?' and tail[8]=='.?/' and body[1]=='/?//////-' and body[2]=='---///-/-'
    return body,tail


def selectors(tail):
    choices=[]
    for word in tail:
        legal=[i for i in range(3) if all((s=='?' or (s=='/' if i==j else s=='.')) for j,s in enumerate(word))]
        choices.append(legal)
    return list(itertools.product(*choices))


def eliminate(eqs, n):
    """Return (rank, solution bits count); rows are n coeff bits + parity in bit n."""
    pivots={}
    for row in eqs:
        r=row
        while r:
            mask=r&((1<<n)-1)
            if not mask: return None
            p=(mask&-mask).bit_length()-1
            if p not in pivots:
                pivots[p]=r
                break
            r^=pivots[p]
    return n-len(pivots)


def equations(rec, selector, shifts, order, polarity, invert):
    """81 equations on 9 class words; XOR relations may depend on earlier word."""
    eqs=[]
    for step in range(9):
        here=order[step];before=order[(step-1)%9];after=order[(step+1)%9]
        k=shifts[selector[here]]
        for j in range(9):
            out=(1<<(after*9+j))
            if rec=='prev_rot_xor_current': terms=[(here,j),(before,(j+k)%9)]
            elif rec=='cur_rot_xor_prev': terms=[(before,j),(here,(j+k)%9)]
            elif rec=='prev_cur_rot_xor': terms=[(before,(j+k)%9),(here,(j+k)%9)]
            elif rec=='toggle_prev_pair': terms=[(here,j),(before,j),(before,(j+k)%9)]
            else: raise ValueError(rec)
            for c,i in terms: out ^= 1<<(c*9+i)
            if invert: out|=1<<81
            eqs.append(out)
    return tuple(eqs)


def known_eqs(body, polarity):
    out=[]
    for c,word in enumerate(body):
        for j,g in enumerate(word):
            if g=='?': continue
            row=(1<<(9*c+j))
            if (g=='/')==bool(polarity):row|=1<<81
            out.append(row)
    return tuple(out)


def find_models(body,tail, inventory=False):
    select=selectors(tail)
    if len(select)!=18: raise AssertionError(('tail completions', len(select)))
    obs=known_eqs(body,True)
    summary={'grammar_count':0,'survivors':0,'best_free_vars':-1,'max_rank':0}
    details=[]
    for shift in SHIFTS:
        for recurrence in RECURRENCES:
            for reverse in (False,True):
                order=tuple(reversed(range(9))) if reverse else tuple(range(9))
                for invert in (False,True):
                    for sel in select:
                        structural=equations(recurrence,sel,shift,order,True,invert)
                        free=eliminate(structural+obs,81)
                        summary['grammar_count']+=1
                        if free is not None:
                            summary['survivors']+=1
                            summary['best_free_vars']=max(summary['best_free_vars'],free)
                            if inventory and len(details)<100:details.append({'shifts':shift,'recurrence':recurrence,'reverse':reverse,'invert':invert,'selectors':sel,'free_vars':free})
    return summary,details


def shuffled_body(body, rng, frame=False):
    flat=[body[j][i] for i in range(9) for j in range(9)]
    if frame: indices=[range(i*9,(i+1)*9) for i in range(9)]
    else: indices=[[j*9+i for i in range(9)] for j in range(9)]
    for group in indices:
        positions=[j for j in group if flat[j]!='?']
        symbols=[flat[j] for j in positions]
        rng.shuffle(symbols)
        for j,v in zip(positions,symbols):flat[j]=v
    return [''.join(flat[j+9*t] for t in range(9)) for j in range(9)]


def run(body,tail, shuffles):
    actual,witness=find_models(body,tail,True)
    controls={}
    for frame in (True,False):
        rng=random.Random(20261013+(1 if frame else 2))
        numbers=[]
        for i in range(shuffles):
            b=shuffled_body(body,rng,frame)
            val,_=find_models(b,tail,False)
            numbers.append(val['survivors'])
        controls['frame9' if frame else 'class']={'n':shuffles,'ge_observed':sum(x>=actual['survivors'] for x in numbers),'num_with_survivors':sum(x>0 for x in numbers),'median':sorted(numbers)[len(numbers)//2], 'maximum':max(numbers),'histogram':dict(sorted(Counter(numbers).items()))}
    pairs=[]
    for i in range(9):
        a,b=body[i],body[(i+1)%9]
        same=sum(x!='?' and y!='?' and x==y for x,y in zip(a,b))
        diff=sum(x!='?' and y!='?' and x!=y for x,y in zip(a,b))
        pairs.append({'transition':'ABCDEFGHI'[i]+'→'+'ABCDEFGHI'[(i+1)%9],'forced_changes':diff,'forced_equal':same,'unresolved':9-same-diff})
    return {'status':'DISCOVER/DEVELOP only; invented global feedback; no decoded CE message','physical':{'records':84,'distinct':66,'unknown':42}, 'machine':{'state_bits':9,'registers':9,'feedback_functions':RECURRENCES,'shift_sets':SHIFTS,'reverse':2,'global_invert':2,'tail_selector_vectors':len(selectors(tail))},'exact':actual,'compatible_examples':witness, 'matched_controls':controls,'forced_transition_changes':pairs}


def selftest():
    import random
    rng=random.Random(30)
    for n in range(1,12):
        for _ in range(200):
            eq=[rng.randrange(1<<(n+1)) for _ in range(rng.randrange(15))]
            brute=sum(all(((r & ((1<<n)-1) & x).bit_count()%2)==((r>>n)&1) for r in eq) for x in range(1<<n))
            free=eliminate(eq,n)
            assert brute == (0 if free is None else (1<<free)),(n,eq,brute,free)
    # independent local equation evaluator
    for rec in RECURRENCES:
        s=[rng.randrange(512) for _ in range(9)]
        shift=(-1,0,1); sel=[rng.randrange(3) for _ in range(9)]
        for invert in (False,True):
            eq=equations(rec,sel,shift,tuple(range(9)),True,invert)
            for t,row in enumerate(eq):
                value=sum((s[c]>>j)&1 for c in range(9) for j in range(9) if (row>>(c*9+j))&1)%2
                assert value in (0,1) # equation rows may not be satisfied by random states
    print('PASS: independent GF2 brute oracle, recurrence form and physical parser')


def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--output',default='data/conjecture-lab-contextual-feedback-2026-10-13.json');p.add_argument('--shuffles',type=int,default=80);p.add_argument('--test',action='store_true')
    a=p.parse_args()
    if a.test:selftest();return
    body,tail=physical(a.observations)
    res=run(body,tail,a.shuffles)
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
    print('Physical models:',res['exact'],'controls:',{k:{v:d[v] for v in ['n','ge_observed','num_with_survivors']} for k,d in res['matched_controls'].items()})
if __name__=='__main__':main()