#!/usr/bin/env python3
"""CL-VLEN-04: one-hot tail instructions copying/reversing 3-bit body runs.

Exact observation-only enumeration of alternative body/tail operators, distinct
from the incumbent recursive machine. All opcode meanings are speculative.
"""
from __future__ import annotations
import argparse
import csv
import itertools
import json
import math
import random
from collections import Counter
from pathlib import Path

OPS=('identity','reverse','invert','reverse_invert')
CLASS='ABCDEFGHI'
SITES={'contiguous':((0,1,2),(3,4,5),(6,7,8)),
       'strided':((0,3,6),(1,4,7),(2,5,8))}

def load(path):
    obs={}; n=0
    for row in csv.DictReader(path.open(newline='')):
        r=int(row['residue']);v=row['symbol'];n+=1
        assert 1<=r<=108 and int(row['serial'])%108==r%108
        assert v in ('/','-') if r<=81 else v in ('/','.')
        if row['image_class']:assert row['image_class']==CLASS[(r-1)%9]
        assert r not in obs or obs[r]==v
        obs[r]=v
    return obs,n

def observed_strings(obs):
    b=''.join('?' if i not in obs else ('1' if obs[i]=='/' else '0') for i in range(1,82))
    t=''.join('?' if i not in obs else ('1' if obs[i]=='/' else '0') for i in range(82,109))
    return b,t

def classes(b,t):
    return {n:(b[i::9],t[i::9]) for i,n in enumerate(CLASS)}

def onehot(t):
    return tuple(j for j in range(3) if all(c=='?' or c==('1' if k==j else '0') for k,c in enumerate(t)))

def transform(v,op):
    assert len(v)==3
    if op in ('reverse','reverse_invert'):v=v[::-1]
    if op in ('invert','reverse_invert'):v=''.join('1' if x=='0' else '0' for x in v)
    return v

def compatible(word,mask):return all(x=='?' or x==y for x,y in zip(mask,word))

def construct(seed,selector,layout,direction,mode,op_a,op_b=None,which=1):
    """One class generator: fanout, chain, or one-transform with literal spare."""
    order=[selector,(selector+direction)%3,(selector+2*direction)%3]
    chunks=[None,None,None]
    chunks[selector]=seed
    if mode=='fanout':
        chunks[order[1]]=transform(seed,op_a)
        chunks[order[2]]=transform(seed,op_b)
    elif mode=='chain':
        chunks[order[1]]=transform(seed,op_a)
        chunks[order[2]]=transform(chunks[order[1]],op_b)
    elif mode=='single':
        target=order[which]
        chunks[target]=transform(seed,op_a)
    else:raise ValueError(mode)
    return chunks

def generate_all(model):
    layout,direction,mode,op_a,op_b,which=model
    positions=SITES[layout]
    for selector in range(3):
        for seed in itertools.product('01',repeat=3):
            seed=''.join(seed)
            partial=construct(seed,selector,layout,direction,mode,op_a,op_b,which)
            empties=[i for i,c in enumerate(partial) if c is None]
            for spare in itertools.product(('000','001','010','011','100','101','110','111'),repeat=len(empties)):
                chunks=list(partial)
                for ix,val in zip(empties,spare):chunks[ix]=val
                bits=['?']*9
                for j,inds in enumerate(positions):
                    for k,pos in enumerate(inds):bits[pos]=chunks[j][k]
                yield selector,''.join(bits)

def models():
    for layout in SITES:
        for direction in (1,-1):
            for op_a,op_b in itertools.product(OPS,repeat=2):
                for mode in ('fanout','chain'):
                    yield (layout,direction,mode,op_a,op_b,1)
            for op_a in OPS:
                for which in (1,2):
                    yield (layout,direction,'single',op_a,None,which)
ALL_MODELS=tuple(models())
assert len(ALL_MODELS)==160

# Future: precompute full raw source for all 160 models. 128*24 + 32*192 
PROGRAMS={model:tuple(generate_all(model)) for model in ALL_MODELS}
assert all(len(PROGRAMS[m])==(192 if m[2]=='single' else 24) for m in ALL_MODELS)


def count_with_model(b,t,model):
    cl=classes(b,t)
    paths=PROGRAMS[model]
    count=1
    by_class={}
    for n,(bb,tt) in cl.items():
        options=[(s,word) for s,word in paths if s in onehot(tt) and compatible(word,bb)]
        by_class[n]=len(options)
        count*=len(options)
    return count,by_class

def control_count(b,t):
    return math.prod(2**bb.count('?')*len(onehot(tt)) for bb,tt in classes(b,t).values())

def rank_all(b,t):
    control=control_count(b,t)
    out=[]
    for model in ALL_MODELS:
        n,by=count_with_model(b,t,model)
        # Per class unconditional grammar word pairs = 3*8*2^(3 if single else 0).
        d=len(PROGRAMS[model])**9
        base_d=(512*3)**9
        score=(math.log(n)-math.log(d)-math.log(control)+math.log(base_d)) if n and control else None
        out.append({'model':list(model),'compatible_completions':n,'source_grammar_volume':d,
                    'observed_classes_compatible':sum(x>0 for x in by.values()),
                    'class_counts':by,'log_bayes_factor_vs_onehot_baseline':round(score,9) if score is not None else None})
    best=max((v for v in out if v['log_bayes_factor_vs_onehot_baseline'] is not None),key=lambda v:v['log_bayes_factor_vs_onehot_baseline'],default=None)
    return out,best

def shuffled(b,t,rng,mode):
    a=list(b)
    chunks=[list(range(i,min(i+9,81))) for i in range(0,81,9)] if mode=='frames' else [list(range(i,81,9)) for i in range(9)]
    for inds in chunks:
        known=[k for k in inds if a[k]!='?']
        vals=[a[k] for k in known];rng.shuffle(vals)
        for k,val in zip(known,vals):a[k]=val
    return ''.join(a),t

def nulls(b,t,n):
    _,actual=rank_all(b,t)
    results={}
    for mode in ('frames','classes'):
        rng=random.Random(20261012+(0 if mode=='frames' else 107))
        scores=[];possible=0
        for _ in range(n):
            bb,tt=shuffled(b,t,rng,mode)
            _,best=rank_all(bb,tt)
            if best:
                possible+=1;scores.append(best['log_bayes_factor_vs_onehot_baseline'])
            else:scores.append(None)
        obs=actual['log_bayes_factor_vs_onehot_baseline'] if actual else None
        higher=sum(x is not None and obs is not None and x>=obs-1e-9 for x in scores)
        valid=sorted(x for x in scores if x is not None)
        results[mode]={'n':n,'models_with_any_survivor':possible,'observed_best_log_bayes_factor':obs,
                       'shuffle_median_best_log_bayes_factor':valid[len(valid)//2] if valid else None,
                       'shuffle_ge_actual':higher if obs is not None else None,
                       'null':'fixed physical site mask, early-zone counts preserved within '+mode+', tail unchanged'}
    return results

def tests():
    assert transform('001','reverse')=='100'
    assert transform('001','invert')=='110'
    assert transform('001','reverse_invert')=='011'
    for model in ALL_MODELS:
        programs=PROGRAMS[model]
        assert len(programs)==len(set(programs))
        assert all(len(w)==9 and set(w)<=set('01') and 0<=s<=2 for s,w in programs)
    first=ALL_MODELS[0]
    # Brute force independent one-class membership compares exact generator.
    seed=PROGRAMS[first][0]
    bb=seed[1];tt=''.join('1' if i==seed[0] else '0' for i in range(3))
    assert sum(s in onehot(tt) and compatible(w,bb) for s,w in PROGRAMS[first])==1
    print('Tail-operated triple tests passed')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--observations',type=Path,default=Path('data/observations.csv'))
    parser.add_argument('--output',type=Path,default=Path('data/conjecture-lab-tail-operated-triples-2026-10-12.json'))
    parser.add_argument('--null-replicates',type=int,default=160);parser.add_argument('--test',action='store_true')
    a=parser.parse_args()
    if a.test:tests();return
    obs,n=load(a.observations);b,t=observed_strings(obs)
    ranked,best=rank_all(b,t)
    report={'experiment':'CL-VLEN-04','status':'DISCOVER/DEVELOP only; no external decoder','source':str(a.observations),
        'physical_records':n,'observed_residues':len(obs),'tail_onehot_assignments':math.prod(len(onehot(tt)) for _,tt in classes(b,t).values()),
        'baseline_onehot_completions':control_count(b,t),'model_count':len(ALL_MODELS),'compatible_models':sum(x['compatible_completions']>0 for x in ranked),
        'highest_scoring_model':best,'models':ranked,'matched_nulls':nulls(b,t,a.null_replicates),
        'limitations':['hypothetical across-class one-hot selector applied within a class body; differs from source-registered recursive G5/G6',
            'all operation pairs are invented and compared retrospectively','imputation only inside conditional enumerator; no raw observations altered']}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k in ('model_count','compatible_models','highest_scoring_model','matched_nulls')},indent=2))
if __name__=='__main__':main()