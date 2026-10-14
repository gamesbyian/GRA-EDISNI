#!/usr/bin/env python3
"""Exploratory three-symbol glyph/outline/shadow test for INSIDE CE banners.

All missing cells remain unknown. Models and select-best procedure are repeated
on every matched shuffled control. Uses only Python's standard library.
"""
import argparse
import csv
import json
import random
from functools import lru_cache
from itertools import permutations
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]

# Fixed canonical 3x5 uppercase bitmap font, resampled only by integer nearest
# neighbour. Glyphs/parameters are fixed before score inspection.
FONT = {
'A':['010','101','111','101','101'],
'B':['110','101','110','101','110'],
'C':['011','100','100','100','011'],
'D':['110','101','101','101','110'],
'E':['111','100','110','100','111'],
'F':['111','100','110','100','100'],
'G':['011','100','101','101','011'],
'H':['101','101','111','101','101'],
'I':['111','010','010','010','111'],
'J':['001','001','001','101','010'],
'K':['101','101','110','101','101'],
'L':['100','100','100','100','111'],
'M':['101','111','111','101','101'],
'N':['101','111','111','111','101'],
'O':['010','101','101','101','010'],
'P':['110','101','110','100','100'],
'Q':['010','101','101','111','011'],
'R':['110','101','110','101','101'],
'S':['011','100','010','001','110'],
'T':['111','010','010','010','010'],
'U':['101','101','101','101','111'],
'V':['101','101','101','101','010'],
'W':['101','101','111','111','101'],
'X':['101','101','010','101','101'],
'Y':['101','101','010','010','010'],
'Z':['111','001','010','100','111']
}
SHAPES = {4:[(3,4,6,1),(4,4,5,1)], 6:[(3,5,4,1),(5,5,3,1)]}
OPS = ('outline','shadow','right-edge','bottom-edge')
CODES = {'/':0,'-':1,'.':2,' ':3}
SYMBOLS = '/-.'
CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def physical_master(include_045=False):
    doc = json.loads((ROOT/'data/discord-community-master-108.json').read_text())
    s = list(''.join(doc['rows_12x9']))
    assert len(s)==108
    obs = list(csv.DictReader((ROOT/'data/observations.csv').open(newline='')))
    for o in obs:
        residue = int(o['residue'])%108
        assert s[residue] in (' ',o['symbol'])
        s[residue] = o['symbol']
    assert len(obs)==84
    assert sum(c!=' ' for c in s)==66
    assert {c:s.count(c) for c in '/-.'}=={'/':36,'-':22,'.':8}
    assert s[45]==' ' and s[103]=='.'
    if include_045:
        s[45]='.'  # YouTube comment; NOT physical confirmation
    return ''.join(s)


def rows_for(s,width):
    assert len(s)==108 and 108%width==0
    return [s[i:i+width] for i in range(0,108,width)]


def seam_matrix(rows):
    n=len(rows)
    out=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            sc=sum((1 if a==b else -1) for a,b in zip(rows[i],rows[j]) if a!=' ' and b!=' ')
            out[i][j]=out[j][i]=sc
    return out


def seam_score(order,mat):
    return sum(mat[i][j] for i,j in zip(order,order[1:]))


def improve(order,mat):
    n=len(order)
    while True:
        change=False
        for i in range(n-1):
            for j in range(i+1,n):
                old=new=0
                if i:
                    old += mat[order[i-1]][order[i]]
                    new += mat[order[i-1]][order[j]]
                if j+1<n:
                    old += mat[order[j]][order[j+1]]
                    new += mat[order[i]][order[j+1]]
                if new>old:
                    order[i:j+1]=reversed(order[i:j+1])
                    change=True
                    break
            if change:break
        if not change:return order


def seam_order(mat,seed,restarts=16):
    n=len(mat)
    rng=random.Random(seed)
    options=[]
    for start in range(n):
        used={start}
        order=[start]
        while len(order)<n:
            choices=[]
            for j in range(n):
                if j in used:continue
                choices.append((mat[j][order[0]],j,0))
                choices.append((mat[order[-1]][j],j,1))
            _,j,side=max(choices)
            if side:order.append(j)
            else:order.insert(0,j)
            used.add(j)
        options.append(order)
    for _ in range(restarts):
        order=list(range(n))
        rng.shuffle(order)
        options.append(order)
    best=(-10**6,None)
    for order in options:
        order=improve(order[:],mat)
        v=seam_score(order,mat)
        if v>best[0]:best=(v,order)
    return best


def rotate_landscape(rows,order):
    selected=[rows[i] for i in order]
    h=len(selected)
    w=len(selected[0])
    return [''.join(selected[h-1-x][y] for x in range(h)) for y in range(w)]


@lru_cache(None)
def glyph(ch,gw,gh):
    raw=FONT[ch]
    return tuple(tuple(raw[min(4,(y*5)//gh)][min(2,(x*3)//gw)]=='1'
                       for x in range(gw)) for y in range(gh))


@lru_cache(None)
def roles(ch,gw,gh,op):
    bits=glyph(ch,gw,gh)
    r=[[2]*gw for _ in range(gh)]
    for y in range(gh):
        for x in range(gw):
            if op=='outline':
                if bits[y][x]:r[y][x]=0
                elif any(0<=x+dx<gw and 0<=y+dy<gh and bits[y+dy][x+dx]
                         for dx,dy in ((-1,0),(1,0),(0,-1),(0,1))):
                    r[y][x]=1
            elif op=='shadow':
                if bits[y][x]:r[y][x]=0
                elif y>0 and x>0 and bits[y-1][x-1]:r[y][x]=1
            elif op=='right-edge':
                if bits[y][x]:r[y][x]=1 if x+1==gw or not bits[y][x+1] else 0
            elif op=='bottom-edge':
                if bits[y][x]:r[y][x]=1 if y+1==gh or not bits[y+1][x] else 0
    return tuple(tuple(q) for q in r)


def score_canvas(canvas):
    H=len(canvas)
    W=len(canvas[0])
    assert H*W==108
    matrix=[[CODES[c] for c in row] for row in canvas]
    best=None
    for direction in (0,1):
        view=matrix if direction==0 else [list(reversed(row)) for row in matrix]
        for gw,gh,n,sep in SHAPES[H]:
            length=gw*n+sep*(n-1)
            for left in range(W-length+1):
                for top in range(H-gh+1):
                    for op in OPS:
                        for actual in permutations(range(3)):
                            bg=actual[2]
                            baseline=sum(c==bg for row in view for c in row if c!=3)
                            total=baseline
                            word=[]
                            # Glyph footprints never overlap. Score as baseline
                            # all-background + each independently fitted slot.
                            for slot in range(n):
                                x0=left+slot*(gw+sep)
                                best_slot=(-10**6,'?')
                                for ch in CHARS:
                                    template=roles(ch,gw,gh,op)
                                    delta=0
                                    for y in range(gh):
                                        row=view[top+y]
                                        glyphrow=template[y]
                                        for x in range(gw):
                                            observed=row[x0+x]
                                            if observed==3:continue
                                            predicted=actual[glyphrow[x]]
                                            delta += (observed==predicted)-(observed==bg)
                                    if delta>best_slot[0]:best_slot=(delta,ch)
                                total+=best_slot[0]
                                word.append(best_slot[1])
                            if best is None or total>best['matches']:
                                best={'matches':total,'word':''.join(word),
                                      'direction':'LR' if direction==0 else 'RL',
                                      'glyph':f'{gw}x{gh}x{n}+gap{sep}',
                                      'operation':op,
                                      'roles':{'core':SYMBOLS[actual[0]],
                                               'accent':SYMBOLS[actual[1]],
                                               'background':SYMBOLS[actual[2]]},
                                      'margin':[left,top]}
    return best


def support(canvas,rec):
    rows=canvas if rec['direction']=='LR' else [r[::-1] for r in canvas]
    gw,gh,n=map(int,rec['glyph'].split('+')[0].split('x'))
    sep=int(rec['glyph'].split('gap')[-1])
    expected=[['background']*len(rows[0]) for _ in rows]
    for idx,ch in enumerate(rec['word']):
        block=roles(ch,gw,gh,rec['operation'])
        x0=rec['margin'][0]+idx*(gw+sep)
        for y in range(gh):
            for x in range(gw):
                expected[rec['margin'][1]+y][x0+x]=('core','accent','background')[block[y][x]]
    totals={name:0 for name in ('core','accent','background')}
    matched=dict(totals)
    for y,row in enumerate(rows):
        for x,value in enumerate(row):
            if value==' ':continue
            category=expected[y][x]
            totals[category]+=1
            matched[category]+=value==rec['roles'][category]
    assert sum(matched.values())==rec['matches']
    return {'observed_positions_by_expected_role':totals,'correct_by_expected_role':matched}


def matched_shuffle(rows,rng):
    result=[]
    for row in rows:
        idx=[i for i,c in enumerate(row) if c!=' ']
        values=[row[i] for i in idx]
        rng.shuffle(values)
        s=list(row)
        for i,value in zip(idx,values):s[i]=value
        result.append(''.join(s))
    return result


def search(rows,seed):
    natural=list(range(len(rows)))
    _,optimized=seam_order(seam_matrix(rows),seed)
    a=score_canvas(rotate_landscape(rows,natural))
    b=score_canvas(rotate_landscape(rows,optimized))
    if a['matches']>=b['matches']:
        a['order']='natural'
        a['row_permutation_1based']=[i+1 for i in natural]
        return a
    b['order']='seam-optimized'
    b['row_permutation_1based']=[i+1 for i in optimized]
    return b


def do_case(width,include_045,controls,seed=20261014):
    rows=rows_for(physical_master(include_045),width)
    observed=search(rows,seed+width)
    canvas=rotate_landscape(rows,[i-1 for i in observed['row_permutation_1based']])
    observed['support']=support(canvas,observed)
    rng=random.Random(seed+width*100+int(include_045))
    null=[]
    for i in range(controls):
        shuffled=matched_shuffle(rows,rng)
        # The full multi-model/reading-direction/row-order search is
        # repeated for each control. No best-fit correction omitted.
        null.append(search(shuffled,seed+width+i+1)['matches'])
    ge=sum(x>=observed['matches'] for x in null)
    return {'portrait':f'{width}x{108//width}',
            'sideways':f'{108//width}x{width}',
            'include_unconfirmed_045':include_045,
            'observed':observed,'null_controls':controls,
            'null_mean':round(mean(null),3),
            'null_ge':ge,'null_ge_fraction':round(ge/controls,4),
            'null_min':min(null),'null_max':max(null),
            'null_scores':null}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--controls',type=int,default=150)
    p.add_argument('--widths',type=int,nargs='+',default=[4,6])
    p.add_argument('--include-045',action='store_true')
    p.add_argument('--out',default='out/multisymbol-glyph-results.json')
    args=p.parse_args()
    assert args.controls>0 and all(width in SHAPES for width in args.widths)
    cases=[]
    for width in args.widths:
        row=do_case(width,args.include_045,args.controls)
        print(row['portrait'],args.include_045,row['observed']['word'],
              row['observed']['matches'],'null >=',row['null_ge'],
              '/',args.controls,flush=True)
        cases.append(row)
    dest=Path(args.out)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps({
        'mode':'DISCOVER',
        'source':'66 physically confirmed H108 positions (8 dots), plus optional UNCONFIRMED 045 dot',
        'models':list(OPS),
        'font':'fixed 3x5 uppercase A-Z, resampled to 3x4/4x4/3x5/5x5',
        'roles':'6 permutations of slash/dash/dot to core/accent/background',
        'selection':'max glyph match over all letters, fixed geometric families, 4 morphology operators, 6 symbol roles, 2 directions, natural or seam-optimized row order',
        'unknown':'unknown positions never imputed or scored',
        'null':'shuffle only known marks within each original row; preserve original unknown mask and slash/dash/dot counts per row',
        'interpretation':'exploratory fit, not a decoded word or inferential proof',
        'cases':cases},indent=2)+'\n')


if __name__=='__main__':
    main()
