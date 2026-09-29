#!/usr/bin/env python3
"""Experiment 300: audit historical Sticker Studio prediction heuristics.

This is a dependency-free reimplementation of the prediction-only logic preserved
in archive/discord/2026-09-29/sticker_random_gen_New.py.  It never imports model
filled cells as observations.

The historical rules are evaluated by leave-one-out prediction on the 65 known
H108 residues and compared with the tool's own zone-majority baseline.
"""

from collections import Counter
from math import comb

KNOWN = {
      2:'G',3:'R',4:'R',5:'G',7:'G',9:'G',10:'R',12:'R',13:'G',14:'R',15:'G',17:'G',
     18:'R',19:'R',20:'G',21:'R',23:'R',24:'R',26:'R',29:'G',30:'G',31:'R',32:'G',36:'G',
     37:'R',38:'G',39:'G',40:'G',42:'G',43:'G',44:'R',46:'G',47:'G',48:'G',51:'R',53:'R',
     56:'G',57:'R',59:'G',60:'G',63:'G',65:'G',66:'G',69:'G',70:'R',71:'R',72:'R',74:'R',
     75:'R',76:'G',78:'G',79:'G',80:'G',81:'G',85:'Y',86:'G',89:'Y',90:'Y',92:'Y',95:'Y',
     96:'G',97:'Y',98:'Y',101:'G',108:'G',
}
CELLS=range(1,109)
PERIODS=[54,36,27,18,12,9,6,4]
WEIGHTS={54:1.0,36:.7,27:.6,18:.5,12:.4,9:.4,6:.3,4:.25,3:.2,2:.15}
LINE_WEIGHT=.3

def is_top(n): return n<=81
def same_class(a,b,p): return (a-b)%p==0
def without(n): return {k:v for k,v in KNOWN.items() if k!=n}

def zone_guess(known,n):
    c=Counter(s for k,s in known.items() if is_top(k)==is_top(n))
    return c.most_common(1)[0][0] if c else 'G'

def mod54_guess(known,n):
    bucket=Counter(s for k,s in known.items() if k!=n and same_class(k,n,54))
    if not bucket: return 'G'
    top=bucket.most_common(1)[0][0]
    if is_top(n) and top=='Y':
        others={s:c for s,c in bucket.items() if s!='Y'}
        return max(others,key=others.get) if others else 'G'
    if (not is_top(n)) and top=='R':
        others={s:c for s,c in bucket.items() if s!='R'}
        return max(others,key=others.get) if others else 'G'
    return top

def multi_guess(known,n,min_agree):
    votes=Counter()
    for period in PERIODS:
        colors=[known[p] for p in CELLS if p!=n and p in known and same_class(p,n,period)]
        valid=[c for c in colors if not(is_top(n) and c=='Y') and not((not is_top(n)) and c=='R')]
        if not valid: continue
        cc=Counter(valid)
        if len(cc)==1: votes[next(iter(cc))]+=1
        else: votes[cc.most_common(1)[0][0]]+=.5
    if votes:
        color,score=votes.most_common(1)[0]
        if score>=min_agree: return color
    return None

def _model_add(n,known,zoned,members,weight,totals):
    vals=[known[q] for q in members if q!=n and q in known and (not zoned or is_top(q)==is_top(n))]
    if vals:
        for s in totals:
            totals[s]+=vals.count(s)/len(vals)*weight

def model_predict(n,known,zoned):
    totals={'G':0.0,'R':0.0,'Y':0.0}
    for period,weight in WEIGHTS.items():
        _model_add(n,known,zoned,[q for q in CELLS if same_class(q,n,period)],weight,totals)
    _model_add(n,known,zoned,[q for q in CELLS if same_class(q,n,9)],LINE_WEIGHT,totals)
    _model_add(n,known,zoned,[q for q in CELLS if (q-1)//9==(n-1)//9],LINE_WEIGHT,totals)
    allowed=('G','R') if is_top(n) else ('G','Y')
    for s in totals:
        if s not in allowed: totals[s]=0.0
    if sum(totals.values())<=0: return 'G'
    return max(('G','R','Y'),key=lambda s:totals[s])

def score(rule):
    return {n:rule(without(n),n)==s for n,s in KNOWN.items()}

def exact_mcnemar(model,baseline):
    model_only=sum(model[n] and not baseline[n] for n in KNOWN)
    baseline_only=sum(baseline[n] and not model[n] for n in KNOWN)
    total=model_only+baseline_only
    if total==0: return model_only,baseline_only,1.0
    k=min(model_only,baseline_only)
    p=min(1.0,2*sum(comb(total,i) for i in range(k+1))/(2**total))
    return model_only,baseline_only,p

def main():
    baseline=score(zone_guess)
    rows=[]
    rules={
        'zone_baseline':baseline,
        'mod54':score(mod54_guess),
        'weighted_model_zoned':score(lambda kn,n:model_predict(n,kn,True)),
        'weighted_model_cross_zone':score(lambda kn,n:model_predict(n,kn,False)),
    }
    for name,res in rules.items():
        correct=sum(res.values())
        if name=='zone_baseline':
            rows.append((name,65,correct,correct/65,None,None,None))
        else:
            a,b,p=exact_mcnemar(res,baseline)
            rows.append((name,65,correct,correct/65,a,b,p))

    for threshold in (1,2,3,3.5,4):
        preds={}
        for n,s in KNOWN.items():
            guess=multi_guess(without(n),n,threshold)
            if guess is not None:
                preds[n]=(guess==s)
        correct=sum(preds.values())
        a=sum(preds[n] and not baseline[n] for n in preds)
        b=sum(baseline[n] and not preds[n] for n in preds)
        total=a+b
        p=1.0 if total==0 else min(1.0,2*sum(comb(total,i) for i in range(min(a,b)+1))/(2**total))
        rows.append((f'multi_period_min_{threshold}',len(preds),correct,correct/len(preds) if preds else 0,a,b,p))

    print("rule,coverage,correct,accuracy,rule_only_correct,baseline_only_correct,mcnemar_p")
    for row in rows:
        print(",".join("" if x is None else f"{x:.12g}" if isinstance(x,float) else str(x) for x in row))

    expected={
        'zone_baseline':39,
        'mod54':37,
        'weighted_model_zoned':34,
        'weighted_model_cross_zone':36,
    }
    for name,res in rules.items():
        assert sum(res.values())==expected[name]

    # Historical default multi-period threshold is 2.
    default=[r for r in rows if r[0]=='multi_period_min_2'][0]
    assert default[1:4]==(65,31,31/65)

if __name__=="__main__":
    main()
