#!/usr/bin/env python3
"""CL-VLEN-17: one-hot opcode address footprint on cyclic 9×9 sticker states.

Tests whether three tail-selected commands can each operate on a *fixed* set
of k bit addresses. No source authorized such a stencil. DISCOVER/DEVELOP.
"""
import argparse,itertools,json,random
from collections import Counter
from pathlib import Path
from conjecture_lab_contextual_feedback import physical,selectors
from conjecture_lab_minimal_tape_edits import min_depth,shuffled


def forced_masks(body):
    return [sum(1<<j for j,(a,b) in enumerate(zip(body[i],body[(i+1)%9])) if a!='?' and b!='?' and a!=b) for i in range(9)]


def assignment_footprint(delta,selection):
    masks=[0,0,0]
    for i,op in enumerate(selection): masks[op]|=delta[i]
    return {'per_opcode_write_masks':masks,'per_opcode_sizes':[m.bit_count() for m in masks], 'maximum_fixed_opcode_address_footprint':max(m.bit_count() for m in masks)}


def minimum_address_masks(masks,tail):
    choices=selectors(tail)
    if len(choices)!=18:raise ValueError('expected one-hot selector family')
    candidates=[(assignment_footprint(masks,sel),sel) for sel in choices]
    best=min(candidates,key=lambda x:(x[0]['maximum_fixed_opcode_address_footprint'],sum(x[0]['per_opcode_sizes']),x[1]))
    return {'minimum_maximum_fixed_opcode_site_count':best[0]['maximum_fixed_opcode_address_footprint'], 'witness_selector_positions':best[1], 'witness_writable_sites_zero_based':[ [j for j in range(9) if mask&(1<<j)] for mask in best[0]['per_opcode_write_masks']], 'all_18_results':[{'selectors':sel,'required_max_writable_sites':r['maximum_fixed_opcode_address_footprint']} for r,sel in candidates]}


def minimum_edit_optima(body,tail):
    winner_lists=[min_depth(''.join(body[j][t] for j in range(9)))[1] for t in range(9)]
    combos=0;counter=Counter();best=None
    for choice in itertools.product(*winner_lists):
        states=[sum(((choice[t]>>c)&1)<<t for t in range(9)) for c in range(9)]
        d=[states[i]^states[(i+1)%9] for i in range(9)]
        assert sum(x.bit_count() for x in d)==20
        for sel in selectors(tail):
            result=assignment_footprint(d,sel)
            k=result['maximum_fixed_opcode_address_footprint']
            combos+=1;counter[k]+=1
            if best is None or (k,sum(result['per_opcode_sizes']))<best[0]:
                best=((k,sum(result['per_opcode_sizes'])),sel,d,result)
    return {'minimum_body_optima':len(list(itertools.product(*winner_lists))),'joint_body_selector_cases':combos, 'smallest_maximum_opcode_footprint':best[0][0], 'smallest_sum_opcode_footprint_with_best_max':best[0][1], 'best_selector_vector':best[1], 'best_opcode_masks':[format(v,'09b') for v in best[3]['per_opcode_write_masks']], 'max_footprint_histogram':dict(sorted(counter.items()))}


def analyze(body,tail,nulls):
    forced=forced_masks(body)
    actual=minimum_address_masks(forced,tail)
    controls={}
    for frame in (True,False):
        rng=random.Random(20261013+int(frame)+822);scores=[]
        for _ in range(nulls):
            sample=shuffled(body,rng,frame)
            scores.append(minimum_address_masks(forced_masks(sample),tail)['minimum_maximum_fixed_opcode_site_count'])
        controls['original_frame9' if frame else 'within_class']={'samples':nulls,'at_most_actual_footprint':sum(v<=actual['minimum_maximum_fixed_opcode_site_count'] for v in scores),'median':sorted(scores)[len(scores)//2] if scores else None,'histogram':dict(sorted(Counter(scores).items()))}
    return {'status':'conditional one-hot and cyclic-class tape; no identified Playdead grammar', 'physical':'84 reports / 66 unique H108 residues', 'forced_B_to_C_write_indices_0based':[j for j in range(9) if forced[1]&(1<<j)],'observed_forced_transition_masks':[format(v,'09b') for v in forced],'raw_forced_opcode_address_footprint':actual,'conditional_minimum_20_write_opcode_footprint':minimum_edit_optima(body,tail),'matched_controls':controls}


def test():
    fake=[0b010,0b100,0b001]
    assert assignment_footprint(fake,(0,0,2))['per_opcode_write_masks']==[0b110,0,1]
    assert assignment_footprint(fake,(0,0,2))['maximum_fixed_opcode_address_footprint']==2
    for delta in range(512):
        assert assignment_footprint([delta]*9,(0,1,2,0,1,2,0,1,2))['maximum_fixed_opcode_address_footprint']==delta.bit_count()
    print('PASS: independent mask union, bit count and fixed-opcode address semantics')


def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--nulls',type=int,default=10000);p.add_argument('--test',action='store_true');p.add_argument('--output',default='data/conjecture-lab-opcode-address-footprint-2026-10-13.json');a=p.parse_args()
    if a.test:test();return
    body,tail=physical(a.observations);result=analyze(body,tail,a.nulls)
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('forced',result['raw_forced_opcode_address_footprint']['minimum_maximum_fixed_opcode_site_count'],'min_edit',result['conditional_minimum_20_write_opcode_footprint']['smallest_maximum_opcode_footprint'],'controls',result['matched_controls'])
if __name__=='__main__':main()