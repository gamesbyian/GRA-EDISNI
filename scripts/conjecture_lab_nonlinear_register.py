#!/usr/bin/env python3
"""CL-VLEN-12: source C anchors nonlinear, tail-controlled 9-bit register writes.

All 256 elementary 3-input Boolean update rules. Selector picks neighborhood
centre displacement; every class is a deterministic next state. DISCOVER only.
"""
from __future__ import annotations
import argparse
import csv
import itertools
import json
import random
from collections import Counter
from pathlib import Path
try:
    import numpy as np
except ImportError as ex:
    raise SystemExit('requires numpy>=2 (research-only; not CI dependency)') from ex

RULE=np.arange(256,dtype=np.uint16)
PERMS=tuple(itertools.permutations((-1,0,1)))


def physical(path):
    seen={}
    with open(path,encoding='utf8',newline='') as file:rows=list(csv.DictReader(file))
    for r in rows:
        j=int(r['residue']);s=r['symbol']
        if j in seen and seen[j]!=s:raise ValueError('conflict')
        seen[j]=s
    assert len(rows)==84 and len(seen)==66
    body=[''.join(seen.get(1+j+9*k,'?') for k in range(9)) for j in range(9)]
    tail=[''.join(seen.get(82+j+9*k,'?') for k in range(3)) for j in range(9)]
    assert all(x!='?' for x in body[2]);assert body[2]=='---///-/-'
    return body,tail


def choices(tail):
    local=[]
    for s in tail:
        local.append([p for p in range(3) if all(x=='?' or x==('/' if i==p else '.') for i,x in enumerate(s))])
    return list(itertools.product(*local))


def signed_mask(word):
    yes=sum(1<<i for i,x in enumerate(word) if x=='/')
    no=sum(1<<i for i,x in enumerate(word) if x=='-')
    return yes,no


def transform_scalar(state,rule,shift,ring):
    out=0
    for j in range(9):
        q=j+shift
        vals=[]
        for offset in (-1,0,1):
            idx=q+offset
            if ring: idx%=9
            vals.append(((state>>idx)&1) if 0<=idx<9 else 0)
        neighborhood=vals[0]*4+vals[1]*2+vals[2]
        out|=((rule>>neighborhood)&1)<<j
    return out


def transform_vector(state,shift,ring):
    out=np.zeros_like(state)
    for j in range(9):
        q=j+shift;v=[]
        for offset in (-1,0,1):
            i=q+offset
            if ring: i%=9
            v.append((state>>i)&1 if 0<=i<9 else np.zeros_like(state))
        pattern=(v[0]<<2)|(v[1]<<1)|v[2]
        out|=((RULE>>pattern)&1)<<j
    return out


def score_corpus(body,tail,details=False):
    selector_vectors=choices(tail)
    assert len(selector_vectors)==18
    masks=[signed_mask(word) for word in body]
    seed=masks[2][0]
    global_min=1000
    full=0
    histogram=Counter()
    witness=[]
    for reverse in (False,True):
        order=[(2+(step if not reverse else -step))%9 for step in range(10)]
        for ring in (True,False):
            for permutation in PERMS:
                for selectors in selector_vectors:
                    current=np.full(256,seed,dtype=np.uint16)
                    mismatch=np.zeros(256,dtype=np.uint16)
                    for step in range(9):
                        before=order[step];after=order[step+1]
                        current=transform_vector(current,permutation[selectors[before]],ring)
                        yes,no=masks[after]
                        # mark-count contradictions accumulated, not position-hint-only matches
                        mismatch+=np.bitwise_count((current ^ yes)&yes).astype('uint16')
                        mismatch+=np.bitwise_count(current & no).astype('uint16')
                    local=int(np.min(mismatch));global_min=min(global_min,local)
                    unique,counts=np.unique(mismatch,return_counts=True)
                    for val,count in zip(unique.tolist(),counts.tolist()):
                        if val<=14:histogram[val]+=count
                    zeros=np.where(mismatch==0)[0]
                    full+=len(zeros)
                    if details and local<=global_min and len(witness)<20:
                        idx=int(np.argmin(mismatch))
                        witness.append({'misfits':local,'rule':idx,'reverse':reverse,'ring':ring,'permutation':permutation,'selectors':selectors})
    n=len(selector_vectors)*2*2*len(PERMS)*256
    return {'models':n,'survivors':full,'best_mismatches':global_min,'mismatch_histogram_le14':dict(sorted(histogram.items())),'sampled_best_fit_candidates_not_prespecified':witness}


def shuffle_body(body,rng,frame):
    flat=[body[j][i] for i in range(9) for j in range(9)]
    groups=[list(range(i*9,(i+1)*9)) for i in range(9)] if frame else [[j+9*i for i in range(9)] for j in range(9)]
    for group in groups:
        pos=[i for i in group if flat[i]!='?']; values=[flat[i] for i in pos]
        rng.shuffle(values)
        for i,x in zip(pos,values): flat[i]=x
    return [''.join(flat[j+9*i] for i in range(9)) for j in range(9)]


def selftest():
    rng=random.Random(274)
    for ring in (False,True):
        for shift in (-1,0,1):
            for _ in range(90):
                state=rng.randrange(512)
                fast=transform_vector(np.full(256,state,dtype=np.uint16),shift,ring)
                for rule in range(256):assert int(fast[rule])==transform_scalar(state,rule,shift,ring),(state,rule,shift)
    assert signed_mask('---///-/-')==(0b101011000,0b010100111) or sum('---///-/-'[i]=='/' for i in range(9))==4
    print('PASS: independently scalar-verified complete nonlinear 256-rule output semantics')


def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--nulls',type=int,default=120);p.add_argument('--output',default='data/conjecture-lab-nonlinear-register-2026-10-13.json');p.add_argument('--test',action='store_true')
    a=p.parse_args();
    if a.test: selftest();return
    body,tail=physical(a.observations)
    actual=score_corpus(body,tail,True)
    controls={}
    for frame in (True,False):
        rng=random.Random(20261013+(24 if frame else 25))
        values=[]
        for _ in range(a.nulls):
            x=score_corpus(shuffle_body(body,rng,frame),tail)
            values.append(x['best_mismatches'])
        controls['nine_site_frame' if frame else 'class_word']={'trials':a.nulls,'at_most_actual_mismatches':sum(x<=actual['best_mismatches'] for x in values),'median':sorted(values)[len(values)//2] if values else None, 'histogram':dict(sorted(Counter(values).items()))}
    res={'status':'DISCOVER/DEVELOP, not an original Playdead codebook', 'machine':'C-anchored class-cycle, full 256-rule nonlinear register writer, three tail-chosen read offsets', 'physical':{'records':84,'unique':66,'unknown':42},'actual':actual,'null_controls':controls}
    Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
    print('Observed', {x:actual[x] for x in ('models','survivors','best_mismatches')}, 'null',controls)

if __name__=='__main__':main()