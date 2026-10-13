#!/usr/bin/env python3
"""CL-VLEN-05: nine-class, 9-data/3-control checksum and microcode audit.

Exploratory: parity/logic microcode hypotheses, not physically established.
Standard-library; observed.txt is a same-content extraction of data/observations.csv.
In the repository, use --observations data/observations.csv.
"""
import argparse,csv,itertools,json,math,random,statistics
from pathlib import Path

RECORDS=84; UNIQUE=66

def observed(path):
    ss=['?']*108; n=0; seen={}
    if path.suffix=='.csv':
        with path.open(newline='') as f:
            for r in csv.DictReader(f):
                i=int(r['residue'])-1;v=r['symbol'];n+=1
                if i in seen: assert seen[i]==v
                seen[i]=v;ss[i]=v
    else:
        for x in path.read_text().split():
            i=int(x[:-1])-1;v=x[-1];n+=1
            if i in seen: assert seen[i]==v
            seen[i]=v;ss[i]=v
    assert n==RECORDS and len(seen)==UNIQUE
    assert all(c in '/-?' for c in ss[:81]) and all(c in '/.?' for c in ss[81:])
    return ss

def words_to_mask(word,pos,want):
    return bool((word>>pos)&1)==want

ALL=(1<<512)-1
BITMASK=[]
for pos in range(9):
    mask=sum(1<<w for w in range(512) if (w>>pos)&1)
    BITMASK.append((ALL^mask,mask))

def cand_masks(obs):
    # 9 physical class registers, each has 9 input + 3 output positions.
    body=[];tails=[];k=[]
    for j in range(9):
        mask=ALL
        for row in range(9):
            c=obs[j+9*row]
            if c!='?':mask &= BITMASK[row][int(c=='/')]
        body.append(mask)
        tails.append(tuple(-1 if obs[j+9*row]=='?' else int(obs[j+9*row]=='/') for row in range(9,12)))
        k.append(sum(obs[j+9*row]!='?' for row in range(12)))
    return body,tails,k

def f3(name,t):
    a,b,c=t
    if name=='xor':return a^b^c
    if name=='maj':return int((a+b+c)>=2)
    if name=='or':return int(any(t))
    if name=='and':return int(all(t))
    if name=='exact1':return int((a+b+c)==1)
    if name=='same':return int(a==b==c)
    raise ValueError(name)

LAYOUTS=('row','col')
FUNS=('xor','maj','or','and','exact1','same')
MODELS=list(itertools.product(LAYOUTS,range(3),FUNS,(0,1),(0,1)))

def encode(w,model):
    layout,shift,op,invert_body,invert_tail=model
    out=[]
    for tail_index in range(3):
        if layout=='row': sites=[(3*tail_index+u+shift)%9 for u in range(3)]
        else: sites=[(tail_index+3*u+shift)%9 for u in range(3)]
        three=[((w>>r)&1)^invert_body for r in sites]
        out.append(f3(op,three)^invert_tail)
    return tuple(out)

# Body-register bitsets for fixed codeword output values.
TABLE={}
for model in MODELS:
    d=[0]*8
    for w in range(512):
        code=encode(w,model);v=code[0]*4+code[1]*2+code[2]
        d[v]|=1<<w
    TABLE[model]=d
assert all(sum(x.bit_count() for x in tab)==512 for tab in TABLE.values())

def allowed(tail,table):
    mask=0
    for codeword,words in enumerate(table):
        bits=((codeword>>2)&1,(codeword>>1)&1,codeword&1)
        if all(a==-1 or a==b for a,b in zip(tail,bits)):
            mask |= words
    return mask

def evaluate(obs):
    body,tails,k=cand_masks(obs)
    n_body=[m.bit_count() for m in body]
    rows=[]
    for model in MODELS:
        tab=TABLE[model];counts=[];logfactor=0.;failed=[]
        for j in range(9):
            count=(body[j]&allowed(tails[j],tab)).bit_count()
            counts.append(count)
            if not count:failed.append('ABCDEFGHI'[j])
            else:logfactor+=math.log2(count)+k[j]-9
        rows.append((model,counts,None if failed else round(logfactor,9),failed))
    return rows

def select(rows):
    # family-wide fit measures: exact compatibility, best BF, and maximum surviving classes.
    ok=[r for r in rows if r[2] is not None]
    return {'compatible':len(ok),'best_log2_bf':max((r[2] for r in ok),default=None),
        'max_classes':max(9-len(r[3]) for r in rows),
        'best':[[*r[0]],r[2],r[1]] if (r:=max(ok,key=lambda r:r[2],default=None)) else None}

def shuffled(obs,rng,by='class'):
    x=obs[:]
    groups=[]
    if by=='class':
        groups.extend([[j+9*r for r in range(9)] for j in range(9)])
        groups.extend([[81+9*r+j for j in range(9)] for r in range(3)])
    elif by=='frame':
        groups.extend([list(range(r*9,(r+1)*9)) for r in range(12)])
    elif by=='region':groups=[list(range(81)),list(range(81,108))]
    else:raise ValueError(by)
    for indices in groups:
        sites=[i for i in indices if x[i]!='?']; vals=[x[i] for i in sites]
        rng.shuffle(vals)
        for i,v in zip(sites,vals):x[i]=v
    return x

def onehold(obs,rows):
    # Unfit a physical mark. Prefer one model per entire training set;
    # posterior probabilities only if some model survives training.
    result=[]
    for pos,c in enumerate(obs):
        if c=='?':continue
        train=obs[:];train[pos]='?'
        fit=evaluate(train)
        survivors=sorted([x for x in fit if x[2] is not None],key=lambda z:-z[2])
        if not survivors:
            result.append({'residue':pos+1,'actual':c,'trained':0,'pred':None,'correct_support':None})
            continue
        chosen=survivors[0][0]
        trial=[]
        for bit in ('/', '-' if pos<81 else '.'):
            tt=train[:];tt[pos]=bit
            try_result=next(x for x in evaluate(tt) if x[0]==chosen)
            trial.append(2**try_result[2] if try_result[2] is not None else 0)
        prob=trial[0]/sum(trial) if sum(trial) else None
        result.append({'residue':pos+1,'actual':c,'trained':len(survivors),'model':list(chosen),'prob_slash':prob,'prob_actual':prob if c=='/' else 1-prob if prob is not None else None})
    available=[x for x in result if x.get('prob_actual') is not None]
    return {'attempted':len(result),'predictive_folds':len(available),'unavailable_folds':len(result)-len(available),
        'wrong_zero_folds':sum(x['prob_actual']==0 for x in available),'brier':round(statistics.mean((1-x['prob_actual'])**2 for x in available),6) if available else None,
        'details':result}

def inspect():
    # Independently verify bitset tabulations vs loop over every nine-bit word.
    for model in MODELS:
        tab=TABLE[model]
        for code in range(8):
            assert tab[code].bit_count()==sum(encode(w,model)==((code>>2)&1,(code>>1)&1,code&1) for w in range(512))
        for t in [(-1,-1,-1),(0,-1,1),(1,0,1)]:
            a=allowed(t,tab)
            assert all(bool((a>>w)&1)==all(k==-1 or k==v for k,v in zip(t,encode(w,model))) for w in range(512))
    assert len(MODELS)==144
    return 'all 144 codeword truth tables x 512 nine-bit inputs tested'

def run(obs,shuffles=200,holdout=False):
    rows=evaluate(obs);base=select(rows)
    rng=random.Random(413027)
    null={}
    for method in ('class','frame','region'):
        xs=[select(evaluate(shuffled(obs,rng,method))) for _ in range(shuffles)]
        ncomp=sum(x['compatible']>=base['compatible'] for x in xs)
        scores=[x['best_log2_bf'] for x in xs if x['best_log2_bf'] is not None]
        null[method]={'replicates':shuffles,'compatible_ge':ncomp,'any_compatible':len(scores),'median_compatible':statistics.median(x['compatible'] for x in xs),
            'best_factor_ge':sum(x>=base['best_log2_bf'] for x in scores) if base['best_log2_bf'] is not None else None,
            'median_best_factor':statistics.median(scores) if scores else None,'ge_classes':sum(x['max_classes']>=base['max_classes'] for x in xs),
            'median_max_classes':statistics.median(x['max_classes'] for x in xs)}
    return {'experiment':'CL-VLEN-05','status':'DISCOVER/DEVELOP not evidence of checksum','physical_records':RECORDS,'unique':UNIQUE,
       'models':len(MODELS),'model_definition':'class 9 body bits, three three-input Boolean checks, by row/col with 3 rotations, six operators, separate input and output polarities',
       'best':base,'failed_alternatives':[(list(m),failed) for m,c,score,failed in rows if failed and len(failed)<=2][:20],
       'null':null,'holdout':onehold(obs,rows) if holdout else None,'unit_tests':inspect()}

def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',type=Path,default=Path('data/observations.csv'))
    p.add_argument('--shuffles',type=int,default=200);p.add_argument('--holdout',action='store_true');p.add_argument('--test',action='store_true')
    p.add_argument('--output',type=Path);a=p.parse_args()
    if a.test:
        print(inspect());return
    result=run(observed(a.observations),a.shuffles,a.holdout)
    s=json.dumps(result,indent=2,sort_keys=True)
    if a.output:a.output.write_text(s+'\n')
    print(s if not a.output else json.dumps({'best':result['best'],'null':result['null'],'holdout':{k:v for k,v in (result['holdout'] or {}).items() if k!='details'}}))

if __name__=='__main__':main()