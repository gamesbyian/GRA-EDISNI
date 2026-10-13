#!/usr/bin/env python3
"""CL-VLEN-06: direct 4 x 27 carrier, elementary cellular automata.

Raw slash vs non-slash physical mark; 27-cell cyclic/open 1D automata;
all 256 Wolfram ECA rules. No claimed intended ECA operation.
"""
import argparse,itertools,json,statistics,random,csv
from pathlib import Path
import numpy as np
MASK=(1<<27)-1

def raw(path):
    s=['?']*108;seen={};total=0
    if path.suffix=='.csv':
        with path.open(newline='') as f:
            for r in csv.DictReader(f):
                i=int(r['residue'])-1;v=r['symbol'];total+=1
                if i in seen: assert seen[i]==v
                seen[i]=v;s[i]=v
    else:
        for t in path.read_text().split():
            i=int(t[:-1])-1;v=t[-1];total+=1
            if i in seen:assert seen[i]==v
            seen[i]=v;s[i]=v
    assert (total,len(seen))==(84,66)
    return s

def masks(ss):
    out=[]
    for i in range(4):
        s=ss[27*i:27*(i+1)]
        k=sum((1<<j) for j,c in enumerate(s) if c!='?')
        b=sum((1<<j) for j,c in enumerate(s) if c=='/')
        out.append((k,b))
    return out

def seed_states(seed):
    known,bits=seed
    unknown=[i for i in range(27) if not (known>>i)&1]
    codes=np.arange(1<<len(unknown),dtype=np.uint32)
    s=np.full(codes.shape,bits,dtype=np.uint32)
    for j,i in enumerate(unknown):s|=((codes>>j)&1).astype(np.uint32)<<np.uint32(i)
    return s

def step(state,rule,topology):
    if topology=='cyclic':
        left=((state<<np.uint32(1))| (state>>np.uint32(26)))&np.uint32(MASK)
        right=((state>>np.uint32(1)) | ((state &np.uint32(1))<<np.uint32(26)))&np.uint32(MASK)
    else:
        left=(state<<np.uint32(1))&np.uint32(MASK)
        right=state>>np.uint32(1)
    inverse=np.uint32(MASK)
    output=np.zeros_like(state,dtype=np.uint32)
    for x in range(8):
        if (rule>>x)&1:
            out = (left if (x&4) else (left^inverse)) & (state if (x&2) else (state^inverse)) & (right if (x&1) else (right^inverse))
            output|=out
    return output

def independent_step(s,rule,topology):
    out=0
    for i in range(27):
        l=((s>>((i-1)%27))&1) if topology=='cyclic' or i>0 else 0
        c=(s>>i)&1
        rr=((s>>((i+1)%27))&1) if topology=='cyclic' or i<26 else 0
        neighborhood=(l<<2)|(c<<1)|rr
        out|=((rule>>neighborhood)&1)<<i
    return out

def check():
    r=random.Random(99)
    for topology in ('cyclic','open'):
        for rule in range(256):
            s=np.array([r.randrange(1<<27) for _ in range(4)],dtype=np.uint32)
            t=step(s,rule,topology)
            assert list(map(int,t))==[independent_step(int(x),rule,topology) for x in s]
    assert len(seed_states((MASK,123)))==1 and seed_states((MASK,123))[0]==123
    assert len(seed_states((MASK^(1<<2),123)))==2
    return 'all 256 ECA rules on both cyclic/open 27-cell topologies verified against scalar oracle'

def test_direction(mm,direction,topology):
    order=list(range(4)) if direction=='forward' else list(range(3,-1,-1))
    seeds=seed_states(mm[order[0]])
    expected=sum(mm[i][0].bit_count() for i in order[1:])
    best=-1;winner=None;support=0;best_witness=None
    for rule in range(256):
        s=seeds
        wrong=np.zeros(len(seeds),dtype=np.uint16)
        for idx in order[1:]:
            s=step(s,rule,topology)
            k,b=mm[idx]
            wrong+=np.bitwise_count((s^np.uint32(b))&np.uint32(k)).astype(np.uint16)
        score=expected-int(wrong.min())
        if score>best:
            best=score;winner=rule;support=int(np.count_nonzero(wrong==0));best_witness=int(seeds[int(wrong.argmin())]);
        elif score==best:
            support+=int(np.count_nonzero(wrong==0))
    return {'best_matches':best,'comparisons':expected,'best_errors':expected-best,
            'first_best_rule':winner,'sample_seed':best_witness,'exact_program_count':support if best==expected else 0,
            'seed_candidates':len(seeds)}

def shuffle(ss,rng,kind):
    ss=ss[:]
    if kind=='frame':groups=[list(range(9*i,9*i+9)) for i in range(12)]
    elif kind=='quarter':groups=[list(range(27*i,27*i+27)) for i in range(4)]
    elif kind=='class':groups=[[j+9*r for r in range(9)] for j in range(9)]+[list(range(81+9*r,90+9*r)) for r in range(3)]
    else:raise ValueError(kind)
    for group in groups:
        idx=[i for i in group if ss[i]!='?'];vv=[ss[i] for i in idx];rng.shuffle(vv)
        for i,v in zip(idx,vv):ss[i]=v
    return ss

def analyze(ss,nulls=100,directions=('forward',),topologies=('cyclic','open')):
    mm=masks(ss)
    actual={(direction,topology):test_direction(mm,direction,topology) for direction in directions for topology in topologies}
    rng=random.Random(20261013)
    controls={}
    for kind in ('frame','quarter'):
        comparisons=[]
        for _ in range(nulls):
            m=masks(shuffle(ss,rng,kind))
            scores=[test_direction(m,d,t)['best_errors'] for d,t in actual]
            # Minimize physically contradictory marks across the predeclared family.
            comparisons.append(min(scores))
        obsmin=min(x['best_errors'] for x in actual.values())
        controls[kind]={'replicates':nulls,'best_at_least_as_good':sum(x<=obsmin for x in comparisons),
                        'median_best_errors':statistics.median(comparisons),'observed_best_errors':obsmin}
    return {'experiment':'CL-VLEN-06','note':'Exploratory 4x27 ECA programs. No source clue to ECA rule, topology, time direction. Failed exact models are narrow negatives.',
            'four_quarter_marks':[m[0].bit_count() for m in mm],
            'rules':256,'topologies':list(topologies),'directions':list(directions),
            'actual':{':'.join(key):v for key,v in actual.items()},'matched_controls':controls,'oracle':check()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',type=Path,default=Path('data/observations.csv'))
    p.add_argument('--nulls',type=int,default=100);p.add_argument('--reverse',action='store_true');p.add_argument('--test',action='store_true');p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.test:print(check());return
    result=analyze(raw(a.observations),a.nulls,('forward','reverse') if a.reverse else ('forward',))
    s=json.dumps(result,indent=2,sort_keys=True)
    if a.output:a.output.write_text(s+'\n')
    print(s)
if __name__=='__main__':main()