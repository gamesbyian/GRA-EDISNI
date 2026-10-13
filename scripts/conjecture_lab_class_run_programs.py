#!/usr/bin/env python3
"""CL-VLEN-02: class-local run opcodes and inter-class copy/reverse programs.

DISCOVER/DEVELOP: no recovery of intended codebook. Uses ONLY observed
physical sticker evidence. No legacy machine completions or semantic target.
Deterministic standard library; run with --test or --output FILE.
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

CLASS_NAMES = 'ABCDEFGHI'
RUN_SETS = ((1,2,3),(2,3,4),(3,4,5),(4,5,6),(2,4,6),(1,3,5),(3,5,7))
FEATURES = ('run_count','longest_run','first_run')
PERMS = tuple(itertools.permutations((0,1,2)))
ORDERS = (('alphabetical','ABCDEFGHI'),('alphabetical_reverse','IHGFEDCBA'),('artwork','IABCDEFGH'),('artwork_reverse','HGFEDCBAI'))
# Physical assembled art order IAB/CDE/FGH read row-major is I A B C D E F G H.
OPERATORS = ('literal','copy','reverse')
CHUNKS = {'whole9':tuple(range(9)), **{f'triplet_{k}':tuple(range(3*k,3*k+3)) for k in range(3)},
          **{f'rail_{k}':tuple(range(k,9,3)) for k in range(3)}}
BODY_WORDS = tuple(format(i,'09b') for i in range(512))
COMP = tuple(i^511 for i in range(512))
REVERSE = tuple(int(x[::-1],2) for x in BODY_WORDS)

def load(path: Path):
    observed = {}
    records = 0
    with path.open(newline='') as fh:
        for row in csv.DictReader(fh):
            records += 1
            r = int(row['residue'])
            symbol=row['symbol']
            assert 1 <= r <= 108 and int(row['serial'])%108 == r%108
            assert symbol in ('-','/','.')
            if r <= 81: assert symbol in ('-','/')
            else: assert symbol in ('/','.')
            if row['image_class']: assert row['image_class']==CLASS_NAMES[(r-1)%9]
            assert r not in observed or observed[r]==symbol, ('conflicting sticker',r)
            observed[r]=symbol
    return observed,records

def physical_zones(observed):
    first=''.join('?' if i not in observed else ('1' if observed[i]=='/' else '0') for i in range(1,82))
    tail=''.join('?' if i not in observed else ('1' if observed[i]=='/' else '0') for i in range(82,109))
    return first,tail

def get_classes(body,tail):
    return {n:(body[i::9],tail[i::9]) for i,n in enumerate(CLASS_NAMES)}

def valid_onehot(t):
    return tuple(s for s in range(3) if all(c=='?' or c==('1' if k==s else '0') for k,c in enumerate(t)))

def fits(w,p):return all(x=='?' or x==y for x,y in zip(p,w))

def run_features(w):
    runs=[]; last=w[0]; size=0
    for c in w:
        if c!=last:
            runs.append(size); size=0;last=c
        size+=1
    runs.append(size)
    return (len(runs),max(runs),runs[0])

WORD_PROFILES = tuple(run_features(w) for w in BODY_WORDS)
UNCONDITIONAL_HIST=tuple(Counter(f[k] for f in WORD_PROFILES) for k in range(3))
CHUNK_VALUES={n:tuple(int(''.join(BODY_WORDS[i][k] for k in pos),2) for i in range(512))
              for n,pos in CHUNKS.items()}

def local_hists(classes):
    output={}
    for name,(b,t) in classes.items():
        words=[i for i,w in enumerate(BODY_WORDS) if fits(w,b)]
        h=[]
        for k in range(3):h.append(Counter(WORD_PROFILES[i][k] for i in words))
        output[name]={'mask':b,'tail':t,'selectors':valid_onehot(t),'nwords':len(words),'hist':h,'words':words}
    return output

def local_model_count(stats,feature_idx,op_values):
    joint=1
    for name in CLASS_NAMES:
        a=stats[name]
        s=sum(a['hist'][feature_idx][op_values[x]] for x in a['selectors'])
        joint*=s
        if not joint:return 0
    return joint

def local_unconditioned(feature_idx,op_values):
    return sum(UNCONDITIONAL_HIST[feature_idx][v] for v in op_values)**9

def score_count(observed_count,unconditioned_count):
    return -math.inf if not observed_count else math.log(observed_count)-math.log(unconditioned_count)

def class_reference_count(stats,order,mapping,polarity=False,chunk='whole9'):
    # RLE-signature copy/reverse may invert every bit while retaining run lengths.
    # For subword modes only the specified three-symbol lane is constrained;
    # all six other body marks are freely transmitted literal payload.
    chunks=CHUNK_VALUES[chunk]
    revbits=tuple(int(format(x,f'0{len(CHUNKS[chunk])}b')[::-1],2) for x in range(1<<len(CHUNKS[chunk])))
    mask=(1<<len(CHUNKS[chunk]))-1
    dp=[0]*512
    for j,name in enumerate(order):
        entry=stats[name]
        allowed={mapping[s] for s in entry['selectors']}
        if not allowed:return 0
        if j==0:
            if 'literal' not in allowed:return 0
            dp=[int(i in entry['words']) for i in range(512)]
            continue
        total=sum(dp)
        bins=[0]*(mask+1)
        for i,x in enumerate(dp):
            if x:bins[chunks[i]]+=x
        nxt=[0]*512
        for i in entry['words']:
            v=0
            key=chunks[i]
            if 'literal' in allowed:v+=total
            if 'copy' in allowed:v+=bins[key]
            if 'reverse' in allowed:v+=bins[revbits[key]]
            if polarity:
                if 'copy' in allowed:v+=bins[key^mask]
                if 'reverse' in allowed:v+=bins[revbits[key]^mask]
            nxt[i]=v
        dp=nxt
    return sum(dp)

REF_DENOMS={}
def ref_denominator(order,mapping,polarity,chunk):
    # Denominators are source grammar volumes, independent of observed masks.
    key=(order,mapping,polarity,chunk)
    if key not in REF_DENOMS:
        empty={n:{'selectors':(0,1,2),'words':list(range(512))} for n in CLASS_NAMES}
        REF_DENOMS[key]=class_reference_count(empty,order,mapping,polarity,chunk)
    return REF_DENOMS[key]

def baseline_onehot(stats):
    count=1
    for n in CLASS_NAMES:
        count*=stats[n]['nwords']*len(stats[n]['selectors'])
    return count

def best_model(body,tail,*,families=('local','referential')):
    stats=local_hists(get_classes(body,tail))
    base=baseline_onehot(stats)
    base_den=(512*3)**9
    models=[]
    if 'local' in families:
        for feature_idx,feature in enumerate(FEATURES):
            for group in RUN_SETS:
                for assignment in itertools.permutations(group):
                    count=local_model_count(stats,feature_idx,assignment)
                    denom=local_unconditioned(feature_idx,assignment)
                    score=score_count(count,denom)-score_count(base,base_den)
                    models.append((score,'local',feature,list(assignment),count,denom))
    if 'referential' in families:
        for order_id,order in ORDERS:
            for m in itertools.permutations(OPERATORS):
                for chunk in CHUNKS:
                    for polar in (False,True):
                        count=class_reference_count(stats,order,m,polar,chunk)
                        denom=ref_denominator(order,m,polar,chunk)
                        score=score_count(count,denom)-score_count(base,base_den)
                        models.append((score,'reference',order_id,list(m),chunk,polar,count,denom))
    # Pick strongest fully specified model, then minimize tie reliance using stable family order.
    chosen=max(models,key=lambda m:m[0])
    return {'base_count':base,'base_denominator':base_den,'models':models,'best':chosen,
            'num_positive':sum(x[0]!=-math.inf for x in models), 'nmodels':len(models), 'stats':stats}

def frame_shuffle(body,tail,rng,by='serial_frame'):
    # Preserve each observed mask location, and either every 9-site serial frame's
    # exact observed 0/1 census, or each nine-occurrence image-class trace.
    a=list(body);t=list(tail)
    for region in (a,):  # freeze physically observed class-tail opcode constraints in null
        if by=='serial_frame':
            groups=[list(range(k,min(k+9,len(region)))) for k in range(0,len(region),9)]
        elif by=='image_class':
            groups=[list(range(k,len(region),9)) for k in range(9)]
        else:raise ValueError(by)
        for group in groups:
            sites=[i for i in group if region[i]!='?']
            vals=[region[i] for i in sites];rng.shuffle(vals)
            for i,v in zip(sites,vals):region[i]=v
    return ''.join(a),''.join(t)

def deterministic_nulls(body,tail,n=300,seed=20261012):
    initial=best_model(body,tail)
    results={}
    for mode in ('serial_frame','image_class'):
        rng=random.Random(seed+(0 if mode=='serial_frame' else 101))
        null=[]
        for _ in range(n):
            a,b=frame_shuffle(body,tail,rng,by=mode)
            null.append(best_model(a,b)['best'][0])
        observed=initial['best'][0]
        results[mode]={'iterations':n,'nonzero_models_shuffles':sum(x!=-math.inf for x in null),'seed':seed+(0 if mode=='serial_frame' else 101),
                       'observed_best_log_bayes_factor':round(observed,7) if observed!=-math.inf else None,
                       'median_null_log_bayes_factor':round(sorted(null)[n//2],7) if sorted(null)[n//2]!=-math.inf else None,
                       'null_max':round(max(null),7) if max(null)!=-math.inf else None,
                       'ge_count':sum(x>=observed-1e-12 for x in null),
                       'post_selection_tail_fraction':f"{1+sum(x>=observed-1e-12 for x in null)}/{n+1}",
                       'conditioned_on':'same physical observed mask, mark counts per '+mode}
    return results

def specified_model_count(body,tail,spec):
    stats=local_hists(get_classes(body,tail))
    if spec[1]=='local':
        return local_model_count(stats,FEATURES.index(spec[2]),spec[3])
    order=dict(ORDERS)[spec[2]]
    return class_reference_count(stats,order,spec[3],spec[5],spec[4])

def heldout_prediction_audit(observed):
    """Choose model afresh *without* each physically known residue and score it.

    One-hot baseline is the same class-tail assumption, without run/program
    constraints. Both models use uniform probabilities on compatible completions.
    These are retrospective known-site predictions, NOT future unseen holdouts.
    """
    outcomes=[]
    selection_counts=Counter()
    for residue in sorted(observed):
        training=dict(observed)
        actual=training.pop(residue)
        body,tail=physical_zones(training)
        fit=best_model(body,tail)
        if fit['num_positive']==0:
            outcomes.append({'residue':residue,'physical':actual,'failure':'no legal training model'});
            continue
        chosen=fit['best'];selection_counts[str(chosen[1:6])]+=1
        forced=[]
        for bit in ('0','1'):
            cb=list(body);ct=list(tail)
            if residue<=81:cb[residue-1]=bit
            else:ct[residue-82]=bit
            cb=''.join(cb);ct=''.join(ct)
            forced.append({'bit':bit,'numerator':specified_model_count(cb,ct,chosen),
                           'baseline_count':baseline_onehot(local_hists(get_classes(cb,ct)))})
        numerator=sum(o['numerator'] for o in forced)
        denominator=sum(o['baseline_count'] for o in forced)
        assert numerator>0 and denominator>0
        p1=forced[1]['numerator']/numerator
        p1base=forced[1]['baseline_count']/denominator
        actual_bit=int(actual=='/')
        predicted_prob=p1 if actual_bit else 1-p1
        base_prob=p1base if actual_bit else 1-p1base
        outcomes.append({'residue':residue,'class':CLASS_NAMES[(residue-1)%9],
                         'zone':'body' if residue<=81 else 'tail',
                         'physical':actual,'model_selected':list(chosen[:6]),
                         'P_slash_model':round(p1,8),'P_slash_onehot_baseline':round(p1base,8),
                         'model_correct_probability':round(predicted_prob,8),
                         'baseline_correct_probability':round(base_prob,8)})
    points=[r for r in outcomes if 'P_slash_model' in r]
    def summarise(key):
        out={}
        for zone in ('body','tail','all'):
            subset=[r for r in points if zone=='all' or r['zone']==zone]
            if not subset:continue
            probs=[r[key] for r in subset]
            out[zone]={'n':len(probs),'mean_probability_actual':round(sum(probs)/len(probs),6),
                       'strict_majority_correct':sum(p>0.5 for p in probs),
                       'strict_majority_wrong':sum(p<0.5 for p in probs),
                       'indeterminate_p05':sum(p==0.5 for p in probs),
                       'falsified_zero_probability':sum(p==0 for p in probs),
                       'mean_brier':round(sum((1-p)**2 for p in probs)/len(probs),7),
                       'mean_log_loss':round(sum(-math.log(max(p,1e-15)) for p in probs)/len(probs),6)}
        return out
    return {'scope':'66 retrospective leave-one-known-residue-out folds; model chosen fresh per fold; hypothesis family and reader may still be historically selected',
            'model_summary':summarise('model_correct_probability'),
            'onehot_baseline_summary':summarise('baseline_correct_probability'),
            'unparsable_folds':sum('failure' in r for r in outcomes),
            'selected_model_histogram':dict(selection_counts),
            'per_residue':outcomes}

def leave_one_class_out_audit(observed):
    """Hold out all class-A/I physical marks at once, including control marks."""
    results=[]
    for class_name in CLASS_NAMES:
        removed={r:char for r,char in observed.items() if CLASS_NAMES[(r-1)%9]==class_name}
        train={r:char for r,char in observed.items() if r not in removed}
        body,tail=physical_zones(train)
        fit=best_model(body,tail)
        if not fit['num_positive']:
            results.append({'class':class_name,'failure':'no training-compatible model'})
            continue
        selected=fit['best']
        evaluated=[]
        for residue,char in sorted(removed.items()):
            vals=[]
            for bit in ('0','1'):
                cb=list(body);ct=list(tail)
                if residue<=81:cb[residue-1]=bit
                else:ct[residue-82]=bit
                a,b=''.join(cb),''.join(ct)
                vals.append((specified_model_count(a,b,selected),baseline_onehot(local_hists(get_classes(a,b)))))
            model_den=vals[0][0]+vals[1][0]
            base_den=vals[0][1]+vals[1][1]
            assert model_den>0 and base_den>0
            actual=int(char=='/')
            prob_model=vals[actual][0]/model_den
            prob_base=vals[actual][1]/base_den
            evaluated.append({'residue':residue,'actual':char,'P_actual_model':round(prob_model,8),'P_actual_baseline':round(prob_base,8)})
        results.append({'class':class_name,'n':len(evaluated),'selected_model':selected[:6],
                        'sites':evaluated})
    flattened=[r for z in results for r in z.get('sites',())]
    def numbers(k):
        p=[r[k] for r in flattened]
        return {'n':len(p),'brier':round(sum((1-x)**2 for x in p)/len(p),7),
                'mean_actual_probability':round(sum(p)/len(p),7),
                'wrong_confident':sum(x==0 for x in p),
                'mean_clipped_log_loss':round(-sum(math.log(max(x,1e-15)) for x in p)/len(p),6)}
    return {'scope':'nine retrospective entire-A-I-class folds, no marks from tested class in model fitting or score',
            'model':numbers('P_actual_model'),'onehot_baseline':numbers('P_actual_baseline'),'folds':results}

def serial_class_details(body,tail):
    classes=get_classes(body,tail)
    out={}
    for n,(b,t) in classes.items():
        words=[i for i,x in enumerate(BODY_WORDS) if fits(x,b)]
        runs=Counter(WORD_PROFILES[i][0] for i in words)
        runslong=Counter(WORD_PROFILES[i][1] for i in words)
        selectors=valid_onehot(t)
        out[n]={'body':b,'tail':t,'body_residues':[i+1+9*k for k in range(9) for i in [CLASS_NAMES.index(n)]],
                'tail_residues':[82+i+9*k for k in range(3) for i in [CLASS_NAMES.index(n)]],
                'unknown_body':b.count('?'),'unknown_tail':t.count('?'),'candidate_selectors':list(selectors),
                'number_of_body_completions':len(words),'run_count_histogram':dict(sorted(runs.items())),
                'longest_run_histogram':dict(sorted(runslong.items()))}
    return out

def frozen_witnesses(body,tail,best,limit=12):
    # Local model only: count potential symbol predictions conditional on the
    # highly postselected "best" model; no training/test independence.
    stats=local_hists(get_classes(body,tail)); witness={}
    if best[1]!='local':return witness
    feature=FEATURES.index(best[2]);op=best[3]
    for n in CLASS_NAMES:
        b,t=get_classes(body,tail)[n];
        words=stats[n]['words']
        options=[(w,s) for s in stats[n]['selectors'] for w in words if WORD_PROFILES[w][feature]==op[s]]
        if not options:return {}
        for j,char in enumerate(b):
            if char=='?' and len({BODY_WORDS[w][j] for w,_ in options})==1:
                residue=1+CLASS_NAMES.index(n)+9*j
                witness[str(residue)]={'symbol':'/' if BODY_WORDS[options[0][0]][j]=='1' else '-', 'class':n,'status':'RETROSPECTIVE FIT, NOT PROSPECTIVE'}
        for j,char in enumerate(t):
            if char=='?' and len({int(s==j) for _,s in options})==1:
                residue=82+CLASS_NAMES.index(n)+9*j
                witness[str(residue)]={'symbol':'/' if options[0][1]==j else '.', 'class':n,'status':'RETROSPECTIVE FIT, NOT PROSPECTIVE'}
    return dict(list(sorted(witness.items(),key=lambda x:int(x[0])))[:limit])

def test():
    assert [run_features(w) for w in ('000000000','010101010','001110011','111000111')]==[(1,9,9),(9,1,1),(4,3,2),(3,3,3)]
    assert valid_onehot('.?.'.replace('.','0'))==(1,)
    # Tiny domain independently enumerated brute-force cross-instruction equality.
    assert REVERSE[int('100001000',2)]==int('000100001',2)
    a={n:{'selectors':(2,), 'words':[int('100001000',2)]} for n in CLASS_NAMES}
    # Two-class manual oracle: second body is previous, reverse, or independent.
    for mode in (False,True):
        order='AB'
        for mp in itertools.permutations(OPERATORS):
            first_s=mp.index('literal')
            for second_s in (0,1,2):
                st={'A':{'selectors':(first_s,), 'words':[8,12]},
                    'B':{'selectors':(second_s,), 'words':[8,12,3,COMP[8],REVERSE[8],COMP[REVERSE[8]],REVERSE[12],COMP[12],COMP[REVERSE[12]]]}}
                expected=0
                for w1 in st['A']['words']:
                    for w2 in set(st['B']['words']):
                        op=mp[second_s]
                        expected+=int(op=='literal' or (op=='copy' and (w2==w1 or (mode and w2==COMP[w1]))) or
                                      (op=='reverse' and (w2==REVERSE[w1] or (mode and w2==COMP[REVERSE[w1]]))))
                assert class_reference_count(st,order,mp,mode,'whole9')==expected,(mp,second_s,mode)
    # Class-by-class exact combinatorics; full assignments of missing marks.
    classes=get_classes('?'*81,'?'*27)
    st=local_hists(classes)
    assert baseline_onehot(st)==(512*3)**9
    assert sum(UNCONDITIONAL_HIST[0].values())==512
    # No signal in data may cause an inferred unknown to be entered into observations.
    p=Path(__file__).resolve().parents[1]/'data/observations.csv'
    if p.exists():
        observed,records=load(p)
        b,t=physical_zones(observed)
        assert len(observed)==66 and b.count('?')==27 and t.count('?')==15
        assert valid_onehot(get_classes(b,t)['D'][1])==(1,)
    print('CL-VLEN-02 tests passed')

def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--observations',type=Path,default=Path('data/observations.csv'))
    pa.add_argument('--output',type=Path,default=Path('data/conjecture-lab-class-run-programs-2026-10-12.json'))
    pa.add_argument('--null-replicates',type=int,default=300)
    pa.add_argument('--test',action='store_true')
    args=pa.parse_args()
    if args.test:test();return
    observed,records=load(args.observations)
    b,t=physical_zones(observed)
    actual=best_model(b,t)
    summary={'experiment':'CL-VLEN-02','mode':'DISCOVER/DEVELOP; NOT decoded or independent validation',
             'source':str(args.observations),'physical_records':records,'distinct_residues':len(observed),
             'missing_residues':108-len(observed),'tail_onehot_assignments':math.prod(len(valid_onehot(a)) for _,a in get_classes(b,t).values()),
             'baseline_onehot_allowed_completions':actual['base_count'],
             'tested_families':{'local':len(FEATURES)*len(RUN_SETS)*len(PERMS),'reference':len(ORDERS)*len(PERMS)*len(CHUNKS)*2},
             'positive_models':actual['num_positive'],'tested_models':actual['nmodels'],
             'best_model':actual['best'] if actual['num_positive'] else None,
             'top_models':[v for v in sorted(actual['models'],key=lambda x:x[0],reverse=True) if v[0]!=-math.inf][:25],
             'all_models':[[None if v == -math.inf else v for v in m] for m in actual['models']],'classes':serial_class_details(b,t),
             'nulls':deterministic_nulls(b,t,n=args.null_replicates),
             'postselected_witnesses':frozen_witnesses(b,t,actual['best']) if actual['num_positive'] else {},
             'retrospective_leave_one_out':heldout_prediction_audit(observed),
             'retrospective_leave_one_class_out':leave_one_class_out_audit(observed),
             'limitations':['Labels and score families invented after reading prior experiment history.',
                'Best-of-family null is descriptive selection control; not an authorial-intent probability.',
                'Unknown physical marks are summed over uniformly, not reconstructed.',
                'No external receiving artifact or semantic target used.',
                'H108 symbol assumptions are not data about actual serial endpoints.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k in ('experiment','physical_records','distinct_residues','tested_models','positive_models','best_model','top_models','nulls','tail_onehot_assignments')},indent=2,allow_nan=False))
if __name__=='__main__':main()