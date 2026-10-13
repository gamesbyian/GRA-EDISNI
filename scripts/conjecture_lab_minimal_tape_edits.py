#!/usr/bin/env python3
"""CL-VLEN-14: exactly minimize A..I cyclic bit-writing operations.

Oblivious to tail code: this is a minimal-edit prior, *not an identified
Playdead instruction language*. Full per-depth 2^9 exhaustive completion.
"""
from __future__ import annotations
import argparse,csv,itertools,json,random
from collections import Counter
from pathlib import Path
WORD_COUNT=9
COSTS=[(x^( (x<<1 | x>>8)&511)).bit_count() for x in range(512)]

def body(path):
    seen={};rows=list(csv.DictReader(open(path,encoding='utf8',newline='')))
    for r in rows:
        i=int(r['residue']);s=r['symbol']
        if i in seen and seen[i]!=s:raise ValueError('conflict')
        seen[i]=s
    assert len(rows)==84 and len(seen)==66
    return [''.join(seen.get(1+j+9*t,'?') for t in range(9)) for j in range(9)]

def min_depth(column):
    ones=sum(1<<i for i,v in enumerate(column) if v=='/')
    zeros=sum(1<<i for i,v in enumerate(column) if v=='-')
    options=[v for v in range(512) if v&ones==ones and v&zeros==0]
    assert options
    optimal=min(COSTS[v] for v in options)
    winners=[v for v in options if COSTS[v]==optimal]
    return optimal,winners

def min_results(words, detailed=True):
    depths=[''.join(word[t] for word in words) for t in range(9)]
    outcomes=[min_depth(x) for x in depths]
    result={'minimum_writes':sum(v[0] for v in outcomes),'per_depth_minimum':[v[0] for v in outcomes], 'per_depth_optima':[len(v[1]) for v in outcomes]}
    if detailed:
        predictions={};forced={};alternative=1
        for t,(mincost,winners) in enumerate(outcomes):
            alternative*=len(winners)
            for c in range(9):
                if words[c][t]=='?':
                    probability=sum((w>>c)&1 for w in winners)/len(winners)
                    key=f'{1+c+9*t}'
                    predictions[key]=probability
                    if probability in (0.,1.):forced[key]='/' if probability else '-'
        result['conditional_unobserved_probabilities']=predictions
        result['uniquely_forced_under_minimum_edits']=forced
        result['total_optimal_body_completions']=alternative
        result['per_depth_minimizing_sequences']=[[''.join('/' if (v>>j)&1 else '-' for j in range(9)) for v in w] for _,w in outcomes]
    return result

def shuffled(words, rng, frame):
    flat=[words[j][t] for t in range(9) for j in range(9)]
    groups=[list(range(t*9,(t+1)*9)) for t in range(9)] if frame else [[j+9*t for t in range(9)] for j in range(9)]
    for group in groups:
        pos=[v for v in group if flat[v]!='?'];tokens=[flat[v] for v in pos]
        rng.shuffle(tokens)
        for p,token in zip(pos,tokens):flat[p]=token
    return [''.join(flat[j+9*t] for t in range(9)) for j in range(9)]

def holdout(words):
    results=[]
    for c in range(9):
        for t in range(9):
            observed=words[c][t]
            if observed=='?':continue
            w=[list(word) for word in words];w[c][t]='?'
            p=min_depth(''.join(w[j][t] for j in range(9)))
            probability=sum((state>>c)&1 for state in p[1])/len(p[1])
            actual=int(observed=='/')
            results.append({'residue':1+c+9*t,'actual':observed,'conditional_p_slash':probability,'brier':(probability-actual)**2,'impossible':probability==1-actual})
    return {'n':len(results),'brier':sum(r['brier'] for r in results)/len(results),'zero_probability_wrong':sum(r['impossible'] for r in results),'predictions':results}

def test():
    assert COSTS[0]==0 and COSTS[511]==0
    assert COSTS[1]==2 and COSTS[0b11111]==2
    assert min_depth('?????????')[0]==0 and len(min_depth('?????????')[1])==2
    assert min_depth('/--------')[0]==2 and len(min_depth('/--------')[1])==1
    for x in range(512):
        assert COSTS[x]==sum(bool((x>>j)&1)^bool((x>>((j+1)%9))&1) for j in range(9))
    print('PASS: independent 512-state ring-edit brute and observation mask checks')

def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--output',default='data/conjecture-lab-minimal-tape-edits-2026-10-13.json');p.add_argument('--nulls',type=int,default=10000);p.add_argument('--test',action='store_true')
    a=p.parse_args()
    if a.test:test();return
    words=body(a.observations);actual=min_results(words)
    controls={}
    for frame in (True,False):
        rng=random.Random(20261013+int(frame)+41);values=[]
        for _ in range(a.nulls):
            values.append(min_results(shuffled(words,rng,frame),False)['minimum_writes'])
        controls['native_frame9' if frame else 'within_class']={'trials':a.nulls,'less_or_equal_observed':sum(v<=actual['minimum_writes'] for v in values),'mean':sum(values)/len(values) if values else None,'histogram':dict(sorted(Counter(values).items()))}
    out={'status':'DISCOVER; minimum-cyclic-write hypothesis not an original code','physical':{'observed_unique':66,'body_unique':54,'body_unknown':27},'actual':actual,'holdout':holdout(words),'null_controls':controls}
    Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('Min',actual['minimum_writes'],'solutions',actual['total_optimal_body_completions'],'forced_unknowns',len(actual['uniquely_forced_under_minimum_edits']),'holdout brier',out['holdout']['brier'],'null', {k:(v['less_or_equal_observed'],v['trials']) for k,v in controls.items()})
if __name__=='__main__':main()