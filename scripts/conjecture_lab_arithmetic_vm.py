#!/usr/bin/env python3
"""CL-VLEN-13: three-operand arithmetic-register instruction programs.

A/B/.../I are nine 9-bit register states. Tail triplets choose an immediate
k. The next register is computed from current and previous; arbitrary missing
physical marks are never copied into observations. DISCOVER/DEVELOP only.
"""
import argparse
import csv
import itertools
import json
import random
from collections import Counter
from pathlib import Path

MOD=511
KS=((0,1,2),(-1,0,1),(0,3,6),(0,9,18),(0,27,54))
OPS=('add','subtract','reverse_subtract','xor','rotate_current_add','rotate_current_xor','rotate_previous_add','rotate_previous_xor')


def data(path):
    seen={}
    rows=list(csv.DictReader(open(path,encoding='utf8',newline='')))
    for row in rows:
        i=int(row['residue']);s=row['symbol']
        assert i not in seen or seen[i]==s
        seen[i]=s
    assert len(rows)==84 and len(seen)==66
    body=[''.join(seen.get(1+j+9*i,'?') for i in range(9)) for j in range(9)]
    tail=[''.join(seen.get(82+j+9*i,'?') for i in range(3)) for j in range(9)]
    assert body[2]=='---///-/-'
    return body,tail


def onehot(tail):
    return tuple(itertools.product(*[[j for j in range(3) if all(c=='?' or c==('/' if i==j else '.') for i,c in enumerate(s))] for s in tail]))


def rolled(x,n):
    n=n%9;return ((x<<n)|(x>>(9-n)))&MOD if n else x


def opapply(op,previous,current,k):
    if op=='add':return (current+previous+k)&MOD
    if op=='subtract':return (current-previous+k)&MOD
    if op=='reverse_subtract':return (previous-current+k)&MOD
    if op=='xor':return (current^previous^(k&MOD))&MOD
    if op=='rotate_current_add':return (rolled(current,k)+previous)&MOD
    if op=='rotate_current_xor':return rolled(current,k)^previous
    if op=='rotate_previous_add':return (current+rolled(previous,k))&MOD
    if op=='rotate_previous_xor':return current^rolled(previous,k)
    raise ValueError(op)


def allowed(s):
    return [x for x in range(512) if all(c=='?' or (((x>>i)&1)==(c=='/')) for i,c in enumerate(s))]


def physical_mismatch(x,s):
    return sum(c!='?' and (((x>>i)&1)!=(c=='/')) for i,c in enumerate(s))


def score(body,tail,details=False):
    choices=onehot(tail);assert len(choices)==18
    witness=[];seen_exact=0;min_errors=999
    total=0
    perms=tuple(itertools.permutations(range(3)))
    for reverse in (False,True):
        # start at completely known class C; predecessor is B (known 8) or D (known 5).
        walk=[(2+(-i if reverse else i))%9 for i in range(10)]
        prior=allowed(body[walk[-2]]) # prior to C; reverse: D, forward: B
        assert len(prior) in (2,16)
        seed=allowed(body[2]);assert len(seed)==1
        for op in OPS:
            for shifts in KS:
                for perm in perms:
                    for sel in choices:
                        ks=tuple(shifts[perm[i]] for i in sel)
                        for previous in prior:
                            prev=previous;cur=seed[0]
                            err=0
                            for step in range(9):
                                after=walk[step+1]; here=walk[step]
                                # At the final B→C step the current B state must
                                # *equal* the initial B seed, not merely match its
                                # photographed subset. Otherwise this is no cycle.
                                if step==8: err+=(cur^previous).bit_count()
                                nxt=opapply(op,prev,cur,ks[here]);prev,cur=cur,nxt
                                err+=physical_mismatch(nxt,body[after])
                            total+=1
                            if err <min_errors:
                                min_errors=err;witness=[]
                            if err==min_errors and details and len(witness)<20:
                                witness.append({'errors':err,'op':op,'shifts':shifts,'permutation':perm,'selectors':sel,'reverse':reverse,'initial_previous':previous})
                            if err==0:seen_exact+=1
    return {'programs':total,'exact_survivors':seen_exact,'minimum_bit_mismatch':min_errors,'illustrative_best_fit_models':witness}


def shuffle(body,rng,frames):
    flat=[body[j][t] for t in range(9) for j in range(9)]
    groups=[list(range(t*9,(t+1)*9)) for t in range(9)] if frames else [[j+t*9 for t in range(9)] for j in range(9)]
    for group in groups:
        pos=[v for v in group if flat[v]!='?'];v=[flat[x] for x in pos]
        rng.shuffle(v)
        for x,s in zip(pos,v):flat[x]=s
    return [''.join(flat[j+9*t] for t in range(9)) for j in range(9)]


def test():
    assert rolled(511,7)==511
    assert rolled(1,1)==2
    assert rolled(256,1)==1
    assert rolled(1,9)==1
    # independent execution of an arithmetic two-input recurrence
    for a,b,k in itertools.product((0,1,127,511),(0,7,511),(-1,0,3)):
        assert opapply('add',a,b,k)==((a+b+k)%512)
        assert opapply('xor',a,b,k)==(a^b^(k&511))
        assert opapply('rotate_current_add',a,b,k)==((rolled(b,k)+a)%512)
    print('PASS: independent arithmetic and 9-bit rotate/wrap oracles')


def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--nulls',type=int,default=30);p.add_argument('--test',action='store_true');p.add_argument('--output',default='data/conjecture-lab-arithmetic-vm-2026-10-13.json')
    a=p.parse_args()
    if a.test:test();return
    body,tail=data(a.observations)
    actual=score(body,tail,True)
    controls={}
    for frame in (False,True):
        rng=random.Random(20261013+31+int(frame));scores=[]
        for _ in range(a.nulls):scores.append(score(shuffle(body,rng,frame),tail)['minimum_bit_mismatch'])
        controls['nine_site_frame' if frame else 'same_class']={'trials':a.nulls,'at_most_actual_errors':sum(x<=actual['minimum_bit_mismatch'] for x in scores),'median':sorted(scores)[len(scores)//2] if scores else None,'histogram':dict(sorted(Counter(scores).items()))}
    result={'status':'DISCOVER/DEVELOP; no authorized opcode table; not a decoded sticker', 'physical':{'records':84,'observed_residues':66,'unknown':42}, 'machine':{'operations':OPS,'three_immediate_sets':KS,'opcode_position_permutations':6,'tail_selector_completions':18,'orientations':2},'actual':actual,'matched_controls':controls}
    Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('Actual',actual['programs'],actual['exact_survivors'],actual['minimum_bit_mismatch'],'controls',controls)
if __name__=='__main__':main()