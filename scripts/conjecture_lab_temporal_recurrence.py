#!/usr/bin/env python3
"""CL-VLEN-10: four 27-cell time slices as Boolean order-2 recurrence.

Each location evolves t2=f0(t0,t1); t3=f1(t1,t2). Enumerate all
16 Boolean truth tables, f0==f1 and independent f0/f1 variants,
forward/reverse time, missing raw marks exactly. Exploratory only.
"""
import argparse,csv,itertools,json,math,random,statistics
from pathlib import Path

def corpus(p):
    s=['?']*108;seen={};n=0
    if p.suffix=='.csv':
        with p.open(newline='') as f:
            for r in csv.DictReader(f):
                j=int(r['residue'])-1;v=r['symbol'];n+=1
                assert j not in seen or seen[j]==v
                s[j]=v;seen[j]=v
    else:
        for tok in p.read_text().split():
            j=int(tok[:-1])-1;v=tok[-1];n+=1
            assert j not in seen or seen[j]==v
            s[j]=v;seen[j]=v
    assert n==84 and len(seen)==66
    return s

def func(rule,a,b):return (rule>>((a<<1)|b))&1

def states(rule0,rule1):
    seq=[]
    for a,b in itertools.product(range(2),repeat=2):
        c=func(rule0,a,b);d=func(rule1,b,c);seq.append((a,b,c,d))
    return seq

def actual_bits(s,pos,direction):
    vals=[s[q*27+pos] for q in range(4)]
    if direction=='reverse':vals.reverse()
    return tuple(-1 if x=='?' else int(x=='/') for x in vals)

def compatibility(obs,model):
    direction,f0,f1=model
    hypotheses=states(f0,f1)
    total=1;log_likelihood=0.
    per_cell=[]
    for pos in range(27):
        physical=actual_bits(obs,pos,direction)
        options=sum(all(v==-1 or v==u for v,u in zip(physical,x)) for x in hypotheses)
        if not options:return {'exact_completions':0,'log2_likelihood':None,'log2_bf':None,'impossible_cell':pos+1}
        total*=options
        per_cell.append(options)
        log_likelihood+=math.log2(options)-2
    return {'exact_completions':total,'log2_likelihood':round(log_likelihood,8),
            'log2_bf':round(log_likelihood+66,8),'min_cell_options':min(per_cell)}

COMMON=[(d,i,i) for d in ('forward','reverse') for i in range(16)]
MIXED=[(d,i,j) for d in ('forward','reverse') for i in range(16) for j in range(16)]

def evaluate(s,models):
    matches=[]
    for m in models:
        result=compatibility(s,m)
        if result['exact_completions']:
            matches.append((m,result))
    matches.sort(key=lambda x:(-x[1]['log2_bf'],-x[1]['exact_completions']))
    return {'models':len(models),'compatible':len(matches),
            'best_log2_bf':matches[0][1]['log2_bf'] if matches else None,
            'best':{'model':list(matches[0][0]),'result':matches[0][1]} if matches else None,
            'survivors':[{'model':list(m),'result':x} for m,x in matches[:8]]}

def shuffle(s,rng,mode):
    a=s[:]
    if mode=='frame':blocks=[list(range(i*9,(i+1)*9)) for i in range(12)]
    elif mode=='quarter':blocks=[list(range(i*27,(i+1)*27)) for i in range(4)]
    elif mode=='class':blocks=[[j+9*r for r in range(9)] for j in range(9)]+[list(range(81+9*i,90+9*i)) for i in range(3)]
    else:raise ValueError(mode)
    for ix in blocks:
        sites=[i for i in ix if a[i]!='?'];marks=[a[i] for i in sites];rng.shuffle(marks)
        for i,x in zip(sites,marks):a[i]=x
    return a

def check():
    for a,b in itertools.product(range(16),repeat=2):
        tt=states(a,b);assert len(tt)==4 and len(set(tt))==4
        assert all(t[2]==func(a,t[0],t[1]) and t[3]==func(b,t[1],t[2]) for t in tt)
    assert len(COMMON)==32 and len(MIXED)==512
    # XOR feedback: x2=x0 XOR x1, x3=x1 XOR x2=x0.
    assert all(t[3]==t[0] for t in states(6,6))
    empty=['?']*108
    assert compatibility(empty,('forward',6,6))['exact_completions']==4**27
    return 'all 256 ordered Boolean generator pairs checked against independently computed four-site trajectories'

def run(s,n=200):
    actual={'fixed_step':evaluate(s,COMMON),'changed_step':evaluate(s,MIXED)}
    rng=random.Random(20261013);null={}
    for method in ('frame','quarter','class'):
        stats=[{'fixed_step':evaluate(shuf,COMMON),'changed_step':evaluate(shuf,MIXED)} for shuf in (shuffle(s,rng,method) for _ in range(n))]
        null[method]={}
        for name in ('fixed_step','changed_step'):
            orig=actual[name]
            null[method][name]={
                'replicates':n,
                'compatible_ge':sum(x[name]['compatible']>=orig['compatible'] for x in stats),
                'any_compatible':sum(x[name]['compatible']>0 for x in stats),
                'best_bf_ge':sum(x[name]['best_log2_bf'] is not None and x[name]['best_log2_bf']>=orig['best_log2_bf'] for x in stats) if orig['best_log2_bf'] is not None else None,
                'median_compatible':statistics.median(x[name]['compatible'] for x in stats)}
    return {'experiment':'CL-VLEN-10','status':'DISCOVER/DEVELOP, invented temporal operator not source cue',
            'observed_sites_by_quarter':[sum(x!='?' for x in s[27*i:27*(i+1)]) for i in range(4)],
            'actual':actual,'matched_null':null,'oracle':check()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',type=Path,default=Path('data/observations.csv'));p.add_argument('--nulls',type=int,default=200);p.add_argument('--test',action='store_true');p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.test:print(check());return
    r=run(corpus(a.observations),a.nulls)
    s=json.dumps(r,indent=2,sort_keys=True)
    if a.output:a.output.write_text(s+'\n')
    print(json.dumps({'actual':r['actual'],'matched_null':r['matched_null']},indent=2))
if __name__=='__main__':main()