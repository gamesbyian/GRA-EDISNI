#!/usr/bin/env python3
"""CL-VLEN-07: native 9-picture 3-choice instructions as a self-contained route.

3x3 background art gives nine nodes, onehot last-three gives three opcodes.
Test if those can form a 9-visit closed tour on the nine-piece print.
Speculative graph semantics; no intentional path claim.
"""
import argparse,csv,itertools,json,statistics
from pathlib import Path

CLASSES='ABCDEFGHI'
BOARDS=('IAB/CDE/FGH','ABC/DEF/GHI')
DIRECTIONS=((0,-1),(-1,0),(1,0)) # community physical lever U/L/R
MOVES=tuple((dx,dy) for dx in (-1,0,1) for dy in (-1,0,1) if (dx,dy)!=(0,0))

def physical(path):
    s=['?']*108;seen={};rows=0
    if path.suffix=='.csv':
        with path.open(newline='') as f:
            for r in csv.DictReader(f):
                i=int(r['residue'])-1;v=r['symbol'];rows+=1
                assert v in ('/','-','.')
                assert i not in seen or seen[i]==v
                seen[i]=v;s[i]=v
    else:
        for t in path.read_text().split():
            i=int(t[:-1])-1;v=t[-1];rows+=1
            assert i not in seen or seen[i]==v
            seen[i]=v;s[i]=v
    assert (rows,len(seen))==(84,66)
    return s

def options(tail):
    out=[]
    for j in range(9):
        marks=[tail[j],tail[j+9],tail[j+18]]
        choices=[i for i in range(3) if marks[i] in ('/','?') and all(m in ('.','?') for n,m in enumerate(marks) if n!=i)]
        out.append(choices)
    return out

def opcodes(opts):
    return itertools.product(*opts) if all(opts) else ()

def geometry(board):
    names=board.replace('/','')
    return {ch:divmod(i,3)[::-1] for i,ch in enumerate(names)}

def travel(board,moves,wrap):
    lookup=geometry(board)
    inverse={v:k for k,v in lookup.items()}
    tr={}
    for c in CLASSES:
        x,y=lookup[c]
        dest=[]
        for dx,dy in moves:
            xx=x+dx; yy=y+dy
            if wrap:xx%=3;yy%=3
            dest.append(inverse.get((xx,yy)))
        tr[c]=dest
    return tr

def hamiltonian(moves,opc,board,wrap=True):
    tr=travel(board,moves,wrap)
    cur='A';visited=set()
    for i in range(9):
        if cur is None or cur in visited:return False
        visited.add(cur)
        cur=tr[cur][opc[CLASSES.index(cur)]]
    return cur=='A' and len(visited)==9

def fast_route(table,opc):
    cur=0;mask=0
    for _ in range(9):
        if cur<0 or mask>>cur&1:return False
        mask|=1<<cur
        cur=table[cur][opc[cur]]
    return cur==0 and mask==511

def compiled(board,moves,wrap):
    ge=geometry(board);rev={v:i for i,c in enumerate(CLASSES) for v in [ge[c]]}
    arr=[]
    for i,c in enumerate(CLASSES):
        x,y=ge[c];to=[]
        for dx,dy in moves:
            X,Y=x+dx,y+dy
            if wrap:X%=3;Y%=3
            to.append(rev.get((X,Y),-1))
        arr.append(to)
    return arr

def choose(tail,boards=('IAB/CDE/FGH',),generic=True):
    opts=options(tail)
    choices=list(opcodes(opts))
    res={}
    if not choices:return {b:{'literal':0,'any_three_moves':0,'witness':None,'options':opts,'tail_completions':0} for b in boards}
    for board in boards:
        literal=0;any3=0;witness=None
        for mov in itertools.permutations(DIRECTIONS):
            t=compiled(board,mov,True)
            for opc in choices:
                if fast_route(t,opc):literal+=1;witness=(board,'literal',mov,opc)
        if generic:
            for mov in itertools.permutations(MOVES,3):
                t=compiled(board,mov,True)
                for opc in choices:
                    if fast_route(t,opc):any3+=1
                    if any3 and witness is None:witness=(board,'general',mov,opc)
        res[board]={'literal':literal,'any_three_moves':any3,'witness':witness,'options':opts,
                    'tail_completions':len(choices)}
    return res

def exact_controls(tail,board):
    known=[i for i,x in enumerate(tail) if x!='?'];nslashes=sum(tail[i]=='/' for i in known)
    tests=[]
    for slash_positions in itertools.combinations(known,nslashes):
        sample=['?']*27
        for i in known:sample[i]='.'
        for i in slash_positions:sample[i]='/'
        tests.append(sample)
    actual=choose(tail,(board,))[board]
    totals=[]
    for sample in tests:
        got=choose(sample,(board,))[board]
        totals.append((got['literal'],got['any_three_moves'],got['tail_completions']))
    return {'exact_permutations':len(tests),'observed':actual,
            'compatible_onehot_count':sum(x[2]>0 for x in totals),
            'literal_ge':sum(x[0]>=actual['literal'] for x in totals),
            'general_ge':sum(x[1]>=actual['any_three_moves'] for x in totals),
            'median_literal':statistics.median(x[0] for x in totals),
            'median_general':statistics.median(x[1] for x in totals)}

def check():
    for board in BOARDS:
        moves=((1,0),(0,1),(1,1))
        table=compiled(board,moves,True)
        for opc in itertools.product(range(3),repeat=5):
            op=opc+(0,0,0,0)
            assert fast_route(table,op)==hamiltonian(moves,op,board,True)
    assert len(MOVES)==8
    return 'compiled transition table agrees with independent geometric walk'

def main():
    p=argparse.ArgumentParser();p.add_argument('--observations',default='data/observations.csv',type=Path);p.add_argument('--test',action='store_true');p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.test:print(check());return
    s=physical(a.observations);tail=s[81:]
    result={'experiment':'CL-VLEN-07','status':'Invented nine-address route model; not a recovered map.',
        'boards':{b:exact_controls(tail,b) for b in BOARDS},'oracle':check()}
    out=json.dumps(result,indent=2,sort_keys=True)
    if a.output:a.output.write_text(out+'\n')
    print(json.dumps({b:{k:v for k,v in result['boards'][b].items() if k!='observed'} for b in BOARDS},indent=2))
if __name__=='__main__':main()