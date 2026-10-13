#!/usr/bin/env python3
"""CL-VLEN-03: finite-state executable RLE instruction streams.

Synthetic opcode table, not source-discovered. Unary runs of one mark encode
EMIT (length 1), REPEAT (2), REVERSE (3), optional terminal STOP (4). The
opposite-mark run is a positive unary operand (1..cap). Both are maximal runs.
No canonical machine, no guessed sticker cells, no fitted plaintext.
"""
from __future__ import annotations
import argparse
import csv
import functools
import itertools
import json
import math
import random
from pathlib import Path

ORDERS=('serial','reverse','class_major')
LENGTHS=('body','tail','whole')
CAPS=(3,5,9)

def corpus(path):
    obs={};records=0
    for row in csv.DictReader(path.open(newline='')):
        r=int(row['residue']);v=row['symbol'];records+=1
        assert 1<=r<=108 and int(row['serial'])%108==r%108
        assert v in ('/','-') if r<=81 else v in ('/','.')
        assert r not in obs or obs[r]==v
        obs[r]=v
    return obs,records

def build(obs):
    return [''.join('1' if obs.get(i)=='/' else ('?' if i not in obs else '0') for i in range(1,82)),
            ''.join('1' if obs.get(i)=='/' else ('?' if i not in obs else '0') for i in range(82,109))]

def rearrange(s,order):
    if order=='serial':return s
    if order=='reverse':return s[::-1]
    if order=='class_major':
        assert len(s)%9==0
        return ''.join(s[i::9] for i in range(9))
    raise ValueError(order)

def parse_counts(s,opbit='1',cap=5,stop=False,target_output=None):
    """Count *completed* bitstrings that are legal programs, exactly.

    The unique maximal-run parse means each compatible completion is counted
    exactly once; command semantics track history length, not actual values.
    """
    data='0' if opbit=='1' else '1'
    n=len(s)
    ok_op=[[all(x in ('?',opbit) for x in s[i:i+l]) and i+l<=n for l in range(5)] for i in range(n+1)]
    ok_data=[[all(x in ('?',data) for x in s[i:i+l]) and i+l<=n for l in range(cap+1)] for i in range(n+1)]
    @functools.lru_cache(None)
    def dp(pos,outlen):
        if pos==n:
            return int(not stop and outlen>0 and (target_output is None or outlen==target_output))
        total=0
        if stop and outlen>0 and pos+4==n and ok_op[pos][4]:total+=int(target_output is None or outlen==target_output)
        for code in (1,2,3):
            if pos+code>=n or not ok_op[pos][code]:continue
            for m in range(1,min(cap,n-pos-code)+1):
                if not ok_data[pos+code][m]:continue
                if code==1:new_len=outlen+1
                elif code==2:
                    if outlen==0:continue
                    new_len=outlen+m
                else:
                    if outlen<m:continue
                    new_len=outlen
                if target_output is not None and new_len>target_output:continue
                total+=dp(pos+code+m,new_len)
        return total
    count=dp(0,0)
    return count,dp

def build_witness(s,opbit='1',cap=5,stop=False,target_output=None):
    count,dp=parse_counts(s,opbit,cap,stop,target_output)
    if not count:return None
    data='0' if opbit=='1' else '1'
    n=len(s)
    pos=0;output=[];bits='';trace=[]
    while pos<n:
        if stop and len(output)>0 and pos+4==n and all(x in ('?',opbit) for x in s[pos:pos+4]) and (target_output is None or len(output)==target_output):
            bits+=opbit*4;trace.append({'op':'STOP','opcode_run_length':4});pos=n;break
        found=False
        for code in (1,2,3):
            if pos+code>=n or any(x not in ('?',opbit) for x in s[pos:pos+code]):continue
            for m in range(1,min(cap,n-pos-code)+1):
                if any(x not in ('?',data) for x in s[pos+code:pos+code+m]):continue
                if code==1:newlen=len(output)+1
                elif code==2:newlen=len(output)+m if output else -1
                else:newlen=len(output) if len(output)>=m else -1
                if newlen<0 or (target_output is not None and newlen>target_output):continue
                if not dp(pos+code+m,newlen):continue
                before=len(output)
                if code==1:output.append(m);op='EMIT'
                elif code==2:output.extend([output[-1]]*m);op='REPEAT'
                else:output[-m:]=list(reversed(output[-m:]));op='REVERSE'
                bits+=opbit*code+data*m
                trace.append({'op':op,'opcode_run_length':code,'operand_run_length':m,'output_length_before':before,'output_length_after':len(output)})
                pos+=code+m;found=True;break
            if found:break
        if not found:raise AssertionError(('witness DP mismatch',s,pos))
    assert len(bits)==n and all(x=='?' or x==bits[i] for i,x in enumerate(s))
    assert target_output is None or len(output)==target_output
    return {'filled_bits':bits,'program':trace,'output_numbers':output,'note':'one retrospectively synthesized example; not a physical sticker completion'}

@functools.lru_cache(None)
def denominator(n,cap,stop,target):
    return parse_counts('?'*n,'1',cap,stop,target)[0]

def source_odds(s,cap,stop,opbit,target=None):
    count,_=parse_counts(s,opbit,cap,stop,target)
    den=denominator(len(s),cap,stop,target)
    assert den>0, (len(s),cap,stop,target)
    score=math.log(count)-math.log(den)+s.count('0')*math.log(2)+s.count('1')*math.log(2) if count else None
    return count,den,score

def examine(b,t):
    channels={'body':b,'tail':t,'whole':b+t}
    models=[]
    for chan in LENGTHS:
        for order in ORDERS:
            s=rearrange(channels[chan],order)
            for opbit,cap,stop in itertools.product(('0','1'),CAPS,(False,True)):
                count,den,score=source_odds(s,cap,stop,opbit)
                count14=parse_counts(s,opbit,cap,stop,target_output=14)[0] if count else 0
                den14=denominator(len(s),cap,stop,14)
                score14=(math.log(count14)-math.log(den14)+s.count('0')*math.log(2)+s.count('1')*math.log(2)) if count14 and den14 else None
                models.append({'zone':chan,'order':order,'operator_bit':opbit,'operand_cap':cap,'explicit_stop':stop,
                    'valid_completions':count,'unconstrained_valid_programs':den,
                    'compatible_fraction_of_random_unknown_fillings':(round(count/(2**s.count('?')),8) if count else 0),
                    'log_bayes_factor_vs_uniform_binary':round(score,9) if score is not None else None,
                    'compatible_programs_outputting_14_integers':count14,
                    'unconditional_programs_outputting_14_integers':den14,
                    'log_BF_conditioned_on_14_output_numbers':round(score14,9) if score14 is not None else None})
    return models

def shuffled(b,t,rng):
    def sh(s):
        q=list(s)
        for offset in range(0,len(q),9):
            idx=[i for i in range(offset,min(offset+9,len(q))) if q[i]!='?']
            vals=[q[i] for i in idx];rng.shuffle(vals)
            for i,c in zip(idx,vals):q[i]=c
        return ''.join(q)
    return sh(b),sh(t)

def nulls(b,t,observed,n=80):
    rng=random.Random(20261012)
    # Score within each region separately: direct comparison of 27,81,108
    best_real={zone:max((m['log_bayes_factor_vs_uniform_binary'] for m in observed if m['zone']==zone and m['log_bayes_factor_vs_uniform_binary'] is not None),default=None) for zone in LENGTHS}
    stats={zone:{'unrestricted':[],'output14':[]} for zone in LENGTHS}
    best_14={zone:max((m['log_BF_conditioned_on_14_output_numbers'] for m in observed if m['zone']==zone and m['log_BF_conditioned_on_14_output_numbers'] is not None),default=None) for zone in LENGTHS}
    for _ in range(n):
        bb,tt=shuffled(b,t,rng)
        probe=examine(bb,tt)
        for zone in LENGTHS:
            score=max((m['log_bayes_factor_vs_uniform_binary'] for m in probe if m['zone']==zone and m['log_bayes_factor_vs_uniform_binary'] is not None),default=None)
            stats[zone]['unrestricted'].append(score)
            score14=max((m['log_BF_conditioned_on_14_output_numbers'] for m in probe if m['zone']==zone and m['log_BF_conditioned_on_14_output_numbers'] is not None),default=None)
            stats[zone]['output14'].append(score14)
    results={}
    for zone in LENGTHS:
        results[zone]={}
        for mode,obs in (('unrestricted',best_real[zone]),('output14',best_14[zone])):
            values=stats[zone][mode]
            valid=sorted(score for score in values if score is not None)
            above=sum(score is not None and obs is not None and score>=obs-1e-9 for score in values)
            results[zone][mode]={'observed_best_log_BF':obs,'replicates':n,
                'null_parsed':len(valid),'null_median_log_BF':valid[len(valid)//2] if valid else None,
                'null_ge_observed':above if obs is not None else None,
                'postselected_exceedance':f'{above+1}/{n+1}' if obs is not None else None,
                'null':'physical-mask-preserving separate nine-site-frame shuffles in 81/27 zones; optimize across same 36 models per region'}
    return results

def independent_complete_parser(bits,opbit,cap,stop,target):
    # Independent event-level semantics oracle, no recursive memo/DP.
    from itertools import groupby
    runs=[(c,len(list(g))) for c,g in groupby(bits)]
    if not runs or runs[0][0]!=opbit:return False
    out=[];i=0
    while i<len(runs):
        v,opcode=runs[i]
        if v!=opbit:return False
        if stop and opcode==4 and i==len(runs)-1:
            return bool(out) and (target is None or target==len(out))
        if i+1>=len(runs):return False
        x,m=runs[i+1]
        if x==opbit or m>cap or opcode not in (1,2,3):return False
        if opcode==1:out.append(m)
        elif opcode==2:
            if not out:return False
            out.extend([out[-1]]*m)
        else:
            if len(out)<m:return False
            out[-m:]=out[-m:][::-1]
        i+=2
    return not stop and bool(out) and (target is None or target==len(out))

def tests():
    # EMIT 2: opcode '1' run followed by operand '00' run.
    assert parse_counts('100','1',3,False)[0]==1
    assert parse_counts('100','1',3,True)[0]==0
    assert parse_counts('11100','1',3,False)[0]==0 # REVERSE before EMIT illegal
    assert parse_counts('1001111','1',3,True)[0]==1 # EMIT2, STOP4
    assert parse_counts('1001111','1',3,True,target_output=1)[0]==1
    assert parse_counts('1001111','1',3,True,target_output=2)[0]==0
    # 1+1 opcode/operand (10), REPEAT2 with operand2 (1100) => outputs [1,1,1].
    assert parse_counts('101100','1',3,False)[0]==1
    witness=build_witness('101100','1',3,False)
    assert witness['output_numbers']==[1,1,1]
    assert parse_counts('??','1',3,False)[0]==1
    assert parse_counts('?????','1',3,False)[0]==3 # three legal full maximal-run programs
    for n in range(1,10):
        words=[''.join(bits) for bits in itertools.product('01',repeat=n)]
        for opbit in ('0','1'):
            for cap in (2,3,5):
                for stop in (False,True):
                    for target in (None,1,3):
                        total=sum(independent_complete_parser(w,opbit,cap,stop,target) for w in words)
                        dp_count=parse_counts('?'*n,opbit,cap,stop,target)[0]
                        assert total==dp_count,(n,opbit,cap,stop,target,total,dp_count)
    print('Streaming RLE tests passed')

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--observations',type=Path,default=Path('data/observations.csv'))
    pa.add_argument('--output',type=Path,default=Path('data/conjecture-lab-streaming-rle-2026-10-12.json'))
    pa.add_argument('--null-replicates',type=int,default=60);pa.add_argument('--test',action='store_true');args=pa.parse_args()
    if args.test:tests();return
    obs,records=corpus(args.observations);b,t=build(obs)
    models=examine(b,t)
    winners={zone:max((m for m in models if m['zone']==zone and m['log_bayes_factor_vs_uniform_binary'] is not None),key=lambda x:x['log_bayes_factor_vs_uniform_binary'],default=None) for zone in LENGTHS}
    witnesses={}
    for zone,m in winners.items():
        if m:
            s=rearrange({'body':b,'tail':t,'whole':b+t}[zone],m['order'])
            witnesses[zone]=build_witness(s,m['operator_bit'],m['operand_cap'],m['explicit_stop'])
    data={'experiment':'CL-VLEN-03','status':'DISCOVER/DEVELOP only; invented streaming unary RLE program; no decoded puzzle',
        'physical_records':records,'unique_positions':len(obs),'unknown_positions':108-len(obs),
        'models':models,'winning_grammars':winners,'invented_program_witnesses':witnesses,
        'postselected_nulls':nulls(b,t,models,args.null_replicates),'run_format':'alternating maximal runs; opcode-run lengths 1=EMIT,2=REPEAT,3=REVERSE, optional final length4=STOP, operand-run positive length 1..cap',
        'modeled_outputs':['integer sequence from operand run lengths','prior operand repetition','reverse last N produced integers'],
        'limitations':['No evidence these opcode lengths are Playdead authored','Best of 12 settings per ordering, 36 per zone; shuffles reselect','Source words are not guessed physical marks','Human-interface and real receiver absent']}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'winning_grammars':winners,'postselected_nulls':data['postselected_nulls']},indent=2))
if __name__=='__main__':main()