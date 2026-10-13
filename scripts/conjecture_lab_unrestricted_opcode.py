#!/usr/bin/env python3
"""CL-VLEN-19: constructive universal 3-op lookup program, a null counterexample.

A command dictionary without native source constraints can always be
hardcoded to the nine photographed partial class states. Demonstrates why
'we found a valid program' is not confirmation of the CE mechanism.
"""
import argparse,json
from pathlib import Path
from conjecture_lab_contextual_feedback import physical,selectors


def domain(word):
    return tuple(x for x in range(512) if all(c=='?' or (((x>>j)&1)==(c=='/')) for j,c in enumerate(word)))

def distinct_completion(words,pin=None):
    choices=[domain(w) for w in words]
    if pin:
        classid,position,slash=pin
        choices[classid]=tuple(x for x in choices[classid] if bool((x>>position)&1)==slash)
    ordering=sorted(range(9),key=lambda i:(len(choices[i]),i))
    assignment=[None]*9
    def search(j,used):
        if j==9:return True
        classid=ordering[j]
        for x in choices[classid]:
            if x in used:continue
            assignment[classid]=x
            if search(j+1,used|{x}):return True
        assignment[classid]=None
        return False
    return assignment if search(0,set()) else None

def make(words,tail):
    select=selectors(tail)
    assert len(select)==18
    state=distinct_completion(words)
    assert state is not None and len(set(state))==9
    opcode=select[0]
    commands={str(k):{} for k in range(3)}
    for i,current in enumerate(state):commands[str(opcode[i])][str(current)]=state[(i+1)%9]
    # Test real cyclic execution of the frozen finite table.
    cursor=state[0]
    for i in range(9):
        assert cursor==state[i]
        cursor=commands[str(opcode[i])][str(cursor)]
    assert cursor==state[0]
    unconstrained=[]
    for c,word in enumerate(words):
        for j,g in enumerate(word):
            if g!='?':continue
            forced=[distinct_completion(words,(c,j,bit)) is not None for bit in (0,1)]
            unconstrained.append({'residue':c+1+9*j,'can_force_dash':forced[0],'can_force_slash':forced[1]})
    assert len(unconstrained)==27
    return {'status':'deliberately overfitted universal three-command lookup; NOT a decoded CE program','source':'data/observations.csv','body_observed':54,'tail_onehot_vectors':18,'complete_native_classes':[''.join('/' if (x>>j)&1 else '-' for j in range(9)) for x in state],'opcodes':opcode,'partial_transition_tables':commands,'entry_count':sum(len(v) for v in commands.values()),'illustrative_naive_dictionary_bits':9*(2+9+9),'missing_bit_forcing_experiment':unconstrained,'both_bit_values_still_possible':sum(v['can_force_dash'] and v['can_force_slash'] for v in unconstrained)}

def test():
    assert distinct_completion(['---------']*9) is None
    fixed=['---------','/--------','-/-------','--/------','---/-----','----/----','-----/---','------/--','-------/-']
    s=distinct_completion(fixed)
    assert s is not None and len(set(s))==9
    assert distinct_completion(fixed,(0,0,True)) is None
    print('PASS: matching needs independent states; pinned contradiction detected')

def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv');p.add_argument('--test',action='store_true');p.add_argument('--output',default='data/conjecture-lab-unrestricted-opcode-2026-10-13.json');a=p.parse_args()
    if a.test:test();return
    words,tail=physical(a.observations)
    r=make(words,tail);Path(a.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print('Program entries',r['entry_count'],'body unknowns compatible with both values',r['both_bit_values_still_possible'])
if __name__=='__main__':main()