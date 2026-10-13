#!/usr/bin/env python3
"""CL-VLEN-08: nine 9-bit class registers executing shared 3-command dictionary.

Each class's final-three onehot command transforms its 9-bit body to the
next class's body, cyclic A->B->..->I->A. No source-authored interpreter.
"""
import argparse,csv,itertools,json,random,statistics
from pathlib import Path
CLASSES='ABCDEFGHI';OPS=('id','invert','rot1','rot-1','rot3','rot-3','cw','mirror')
N=9;FULL=(1<<9)-1

def corpus(p):
    s=['?']*108;seen={};count=0
    if p.suffix=='.csv':
        with p.open(newline='') as f:
            for r in csv.DictReader(f):
                j=int(r['residue'])-1;v=r['symbol'];count+=1
                if j in seen:assert seen[j]==v
                s[j]=v;seen[j]=v
    else:
        for tok in p.read_text().split():
            j=int(tok[:-1])-1;v=tok[-1];count+=1
            if j in seen:assert seen[j]==v
            s[j]=v;seen[j]=v
    assert (count,len(seen))==(84,66)
    return s

def command_choices(s):
    out=[]
    for j in range(9):
        triple=[s[j+81],s[j+90],s[j+99]]
        out.append([k for k in range(3) if triple[k] in ('/','?') and all(x in ('.','?') for h,x in enumerate(triple) if h!=k)])
    return out

def bitperm(w,perm):return sum(((w>>i)&1)<<j for i,j in enumerate(perm))

def op(w,name):
    if name=='id':return w
    if name=='invert':return w^FULL
    if name=='rot1':return ((w<<1)&FULL)|(w>>8)
    if name=='rot-1':return (w>>1)|((w&1)<<8)
    if name=='rot3':return ((w<<3)&FULL)|(w>>6)
    if name=='rot-3':return (w>>3)|((w&7)<<6)
    if name=='cw':return bitperm(w,[2,5,8,1,4,7,0,3,6])
    if name=='mirror':return bitperm(w,[2,1,0,5,4,3,8,7,6])
    raise ValueError(name)
TABLE={o:[op(x,o) for x in range(512)] for o in OPS}
DICT=list(itertools.permutations(OPS,3)) # 336

def body_sets(s):
    sets=[]
    for j in range(9):
        known=sum(1<<r for r in range(9) if s[j+9*r]!='?')
        vals=sum(1<<r for r in range(9) if s[j+9*r]=='/')
        sets.append((known,vals))
    return sets

def match(x,mask):return ((x^mask[1])&mask[0])==0

def exact_count(masks,selectors,dictionary):
    if not all(selectors):return 0
    op0,op1,op2=[TABLE[x] for x in dictionary]
    tr=(op0,op1,op2)
    count=0
    for first in range(512):
        if not match(first,masks[0]):continue
        states={first:1}
        for pos in range(9):
            nxt={}
            for state,ways in states.items():
                for cmd in selectors[pos]:
                    val=tr[cmd][state]
                    if pos==8:
                        if val==first:count+=ways
                    elif match(val,masks[pos+1]):nxt[val]=nxt.get(val,0)+ways
            states=nxt
            if pos<8 and not states:break
    return count

def evaluate(s):
    masks=body_sets(s);selectors=command_choices(s)
    vals=[];vmax=0;best=[]
    for dictionary in DICT:
        n=exact_count(masks,selectors,dictionary)
        if n:
            vals.append((list(dictionary),n))
        if n>vmax:vmax=n;best=[(dictionary,n)]
        elif n==vmax and n:best.append((dictionary,n))
    return {'survivor_dictionaries':len(vals),'complete_programs':sum(v for k,v in vals),
            'best_support':vmax,'best':[[list(x),y] for x,y in best[:15]],'top_dictionaries':sorted(vals,key=lambda v:-v[1])[:15],
            'tail_selector_completions':__import__('math').prod(len(x) for x in selectors),
            'body_observed':[v[0].bit_count() for v in masks]}

def shuffle(s,rng,mode):
    x=s[:]
    if mode=='nine':groups=[list(range(i*9,(i+1)*9)) for i in range(9)]
    elif mode=='class':groups=[[j+9*r for r in range(9)] for j in range(9)]
    elif mode=='81':groups=[list(range(81))]
    else:raise ValueError(mode)
    for group in groups:
        idx=[i for i in group if x[i]!='?'];v=[x[i] for i in idx];rng.shuffle(v)
        for i,k in zip(idx,v):x[i]=k
    return x

def check():
    assert len(DICT)==336
    for x in range(512):
        assert op(op(x,'rot1'),'rot-1')==x
        assert op(op(x,'rot3'),'rot-3')==x
        assert op(op(x,'cw'),'cw')==bitperm(x,[8,7,6,5,4,3,2,1,0])
        assert op(op(x,'mirror'),'mirror')==x
    # Independent simple fixture: same register under id command in every class.
    masks=[(FULL,37)]*9;sel=[[0] for _ in range(9)]
    assert exact_count(masks,sel,('id','invert','rot1'))==1
    assert exact_count(masks,sel,('invert','id','rot1'))==0
    return 'all 512 nine-bit register states, inverses and fixed complete programs checked'

def run(s,n=250):
    observed=evaluate(s);rng=random.Random(20261013)
    null={}
    for mode in ('nine','class','81'):
        samples=[evaluate(shuffle(s,rng,mode)) for _ in range(n)]
        null[mode]={'replicates':n,
            'compatible_dictionaries_ge':sum(x['survivor_dictionaries']>=observed['survivor_dictionaries'] for x in samples),
            'whole_programs_ge':sum(x['complete_programs']>=observed['complete_programs'] for x in samples),
            'best_support_ge':sum(x['best_support']>=observed['best_support'] for x in samples),
            'any_compatible':sum(x['survivor_dictionaries']>0 for x in samples),
            'median_programs':statistics.median(x['complete_programs'] for x in samples)}
    return {'experiment':'CL-VLEN-08','status':'Exploratory shared three-command cyclic nine-register machine, not confirmed CE parser',
        'grammars':len(DICT),'ops':list(OPS),'classes':9,'actual':observed,'null':null,'oracle':check()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',type=Path,default=Path('data/observations.csv'));p.add_argument('--test',action='store_true');p.add_argument('--nulls',type=int,default=250);p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.test:print(check());return
    d=run(corpus(a.observations),a.nulls)
    out=json.dumps(d,indent=2,sort_keys=True)
    if a.output:a.output.write_text(out+'\n')
    print(json.dumps({'actual':d['actual'],'null':d['null']},indent=2))
if __name__=='__main__':main()