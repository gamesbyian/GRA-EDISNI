#!/usr/bin/env python3
"""CL-VLEN-14b: predictive holdout and matched controls for minimal tape edits.

This is separate from retrospective rank: no retrospective fit counts as forecast.
"""
import argparse,json,random
from collections import Counter
from pathlib import Path
from conjecture_lab_minimal_tape_edits import body,holdout,shuffled,min_results

def baseline(words):
    labels=[q for w in words for q in w if q!='?'];n=len(labels); slash=labels.count('/')
    briers=[]
    for w in words:
        for g in w:
            if g=='?':continue
            a=int(g=='/');p=(slash-a+1)/(n+1)
            briers.append((p-a)**2)
    return sum(briers)/len(briers)

def audit(words,n):
    actual=holdout(words)
    controls={}
    for frame in (True,False):
        rng=random.Random(20261013+123+int(frame));scores=[]
        for _ in range(n):scores.append(holdout(shuffled(words,rng,frame))['brier'])
        controls['original_frame9' if frame else 'within_class']={'replicates':n,'null_brier_mean':sum(scores)/len(scores),'null_brier_median':sorted(scores)[len(scores)//2],'at_most_actual_error':sum(v<=actual['brier'] for v in scores),'minimum':min(scores),'maximum':max(scores)}
    return {'status':'exploratory, not prospective','holdout':{'n':actual['n'],'brier':actual['brier'],'impossible':actual['zero_probability_wrong'],'Laplace_smoothed_global_prevalence_baseline_brier':baseline(words)},'controls':controls}

def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--nulls',type=int,default=1000);p.add_argument('--output',default='data/conjecture-lab-tape-holdout-2026-10-13.json');a=p.parse_args()
    result=audit(body(a.observations),a.nulls)
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result)
if __name__=='__main__':main()