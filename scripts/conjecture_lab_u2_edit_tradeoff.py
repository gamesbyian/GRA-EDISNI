#!/usr/bin/env python3
"""CL-VLEN-18: compare raw minimum-edit tape to independent conditional U2 one-hot primary family.

Reconstruct U2 primary geometry *from physical observations*, not any model
completed sticker. Historical U2=18 primary ×18 selector =324 states.
"""
from __future__ import annotations
import argparse, itertools, json, math, csv
from collections import Counter
from pathlib import Path
from conjecture_lab_minimal_tape_edits import body,min_results
from conjecture_lab_tape_order_rank import minimum_order


def completed_primary_options(words):
    frames=[''.join(words[j][t] for j in range(9)) for t in range(9)]
    options=[]
    for original in frames:
        frameoptions=[]
        for symbols in itertools.product('/-',repeat=original.count('?')):
            chars=iter(symbols)
            completed=''.join(next(chars) if c=='?' else c for c in original)
            counts=[sum(completed[j+3*p]=='/' for p in range(3)) for j in range(3)]
            if counts in ([1,1,1],[2,2,2]):frameoptions.append(completed)
        options.append(frameoptions)
    assert tuple(map(len,options))==(1,1,2,1,1,3,3,1,1)
    return options


def completed_words(frames):
    return [''.join(frames[t][j] for t in range(9)) for j in range(9)]


def cycle_distribution(words):
    native=minimum_order(words,tuple(range(9)))
    counts=Counter();lower=0;equal=0
    for p in itertools.permutations(range(1,9)):
        if p[0]>p[-1]:continue
        cost=minimum_order(words,(0,)+p);counts[cost]+=1
        if cost<native:lower+=1
        if cost==native:equal+=1
    assert sum(counts.values())==20160
    return {'native_cost':native,'strictly_better_orders':lower,'tied_orders':equal,'rank_percentile_at_most_native':(lower+equal)/20160,'order_min_cost':min(counts),'order_max_cost':max(counts)}


def analyze(words,rank_all=True):
    primary=completed_primary_options(words)
    hist=Counter();orders=[];states=[]
    for combo in itertools.product(*primary):
        complete=completed_words(combo)
        edit=minimum_order(complete,tuple(range(9)))
        hist[edit]+=1
        data={'body':complete,'cycle_edits':edit}
        if rank_all:data['permutation_rank']=cycle_distribution(complete)
        orders.append(data)
    assert len(orders)==18
    raw=min_results(words,True)
    contrasts=[]
    for residue_s,conditional_p in raw['conditional_unobserved_probabilities'].items():
        residue=int(residue_s);index=(residue-1)%9;depth=(residue-1)//9
        u2_p=sum(state['body'][index][depth]=='/' for state in orders)/18
        contrasts.append({'residue':residue,'conditional_min_edit_p_slash':conditional_p,'conditional_U2_p_slash':u2_p,'absolute_difference':abs(u2_p-conditional_p),'fully_opposed':abs(u2_p-conditional_p)==1.0})
    opposed=[v['residue'] for v in contrasts if v['fully_opposed']]
    assert opposed==[8,16,27,33,35,62], opposed
    return {'status':'CONDITIONAL comparison: U2 class grammar not a physical completion','physical':{'observations':84,'known':66,'unknown':42},'u2':{'primary_frame_option_counts':list(map(len,primary)),'primary_count':18,'onehot_tail_count':18,'joint_count':324,'native_class_cycle_edit_histogram_18_primary':dict(sorted(hist.items())),'cycle_min_across_U2':min(hist),'cycle_max_across_U2':max(hist),'extra_writes_above_raw_unconstrained_minimum':min(hist)-raw['minimum_writes']},'raw':{'minimum_edit_cycle':raw['minimum_writes']},'exactly_opposed_missing_residues':opposed,'unobserved_prediction_contrasts':sorted(contrasts,key=lambda x:(-x['absolute_difference'],x['residue'])),'all_18_primary_states':orders}


def test():
    # A single native frame: 3 congruence-depth rails, each exactly one
    # minority / (3 slashes total) OR one minority - (6 slashes total).
    assert len([s for s in itertools.product('/-',repeat=9)
                if [sum(s[j+3*p]=='/' for p in range(3)) for j in range(3)]
                in ([1,1,1],[2,2,2])])==54
    assert '///------' in [''.join(s) for s in itertools.product('/-',repeat=9)
                if [sum(s[j+3*p]=='/' for p in range(3)) for j in range(3)]
                in ([1,1,1],[2,2,2])]
    assert '/--------' not in [''.join(s) for s in itertools.product('/-',repeat=9)
                if [sum(s[j+3*p]=='/' for p in range(3)) for j in range(3)]
                in ([1,1,1],[2,2,2])]
    print('PASS: independently enumerated all 54 permitted full native frames')


def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--output',default='data/conjecture-lab-u2-edit-tradeoff-2026-10-13.json');p.add_argument('--test',action='store_true');a=p.parse_args()
    if a.test:
        test()
        return
    result=analyze(body(a.observations))
    # Optional native-repo cross-check: the original U2 CSV uses little-endian
    # hex over the 42 residue indices from Experiment 365. Not copied here.
    catalog=Path('data/completion-universe-u2-324.csv')
    indexing=Path('data/experiment-365-completion-universe.json')
    if catalog.exists() and indexing.exists():
        unknown=json.loads(indexing.read_text())['unknown_residues']
        assert len(unknown)==42
        native=set()
        with catalog.open(newline='',encoding='utf8') as handle:
            rowset=list(csv.DictReader(handle))
        assert len(rowset)==324
        for row in rowset:
            value=int(row['unknown42_hex'],16)
            filled={i:'/' if (value>>j)&1 else ('-' if i<=81 else '.')
                    for j,i in enumerate(unknown)}
            # A-I class-major body, preserving only the unknown bits in U2
            copy=[list(w) for w in body(a.observations)]
            for i,glyph in filled.items():
                if i<=81:copy[(i-1)%9][(i-1)//9]=glyph
            native.add(tuple(''.join(w) for w in copy))
        expected={tuple(x['body']) for x in result['all_18_primary_states']}
        assert native==expected,(len(native),len(expected))
        result['original_U2_csv_verified_exactly']=True
    else:
        result['original_U2_csv_verified_exactly']=False
    Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('U2 18 primary edit costs',result['u2']['native_class_cycle_edit_histogram_18_primary'])
    print('U2 order rank classes',[(x['cycle_edits'],round(x['permutation_rank']['rank_percentile_at_most_native'],3)) for x in result['all_18_primary_states']])
    print('Six opposite frozen conditional predictions:',result['exactly_opposed_missing_residues'])
if __name__=='__main__':main()