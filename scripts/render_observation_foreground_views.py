#!/usr/bin/env python3
"""Render observation-only 12x9, 9x12, 9x9+tail, and per-class 3x3+tail SVG views."""
from __future__ import annotations
import csv
from pathlib import Path

CLASSES="ABCDEFGHI"

def load(path:Path)->dict[int,str]:
    out={}
    with path.open(newline="",encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            r=int(row["residue"]); s=row["symbol"]
            if r in out and out[r]!=s: raise ValueError(f"conflict at residue {r}")
            out[r]=s
    return out

def mark(sym:str,x:float,y:float,sz:float)->str:
    if sym=="/": return f'<line x1="{x+sz*.22}" y1="{y+sz*.78}" x2="{x+sz*.78}" y2="{y+sz*.22}" stroke="black" stroke-width="2"/>'
    if sym=="-": return f'<line x1="{x+sz*.2}" y1="{y+sz*.5}" x2="{x+sz*.8}" y2="{y+sz*.5}" stroke="black" stroke-width="2"/>'
    if sym==".": return f'<circle cx="{x+sz*.5}" cy="{y+sz*.5}" r="{sz*.07}" fill="black"/>'
    return f'<text x="{x+sz*.5}" y="{y+sz*.62}" text-anchor="middle" font-size="{sz*.42}" fill="#888">?</text>'

def main()->None:
    vals=load(Path("data/observations.csv"))
    body={c:[vals.get(1+i+9*k,"?") for k in range(9)] for i,c in enumerate(CLASSES)}
    tail={c:[vals.get(82+i+9*k,"?") for k in range(3)] for i,c in enumerate(CLASSES)}
    sz=32
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="920" viewBox="0 0 1200 920">','<rect width="1200" height="920" fill="white"/>',
       '<style>text{font-family:system-ui,sans-serif}.title{font-size:24px;font-weight:700}.sub{font-size:15px}.lab{font-size:13px;font-weight:600}.cell{fill:white;stroke:#bbb;stroke-width:1}</style>',
       '<text x="40" y="40" class="title">Observation-only 9×12 / 9+3 foreground views</text>',
       '<text x="40" y="65" class="sub">Only physically observed marks are drawn. “?” means unknown. No model-filled cells.</text>',
       '<text x="40" y="105" class="lab">12×9 conventional registration view</text>']
    for r in range(12):
        for c in range(9):
            x,y=40+c*sz,120+r*sz; sym=vals.get(1+r*9+c,"?")
            s.append(f'<rect class="cell" x="{x}" y="{y}" width="{sz}" height="{sz}"/>'+mark(sym,x,y,sz))
    x2=390; s.append(f'<text x="{x2}" y="105" class="lab">9×12 transposed class traces</text>')
    for r,name in enumerate(CLASSES):
        s.append(f'<text x="{x2-20}" y="{142+r*sz}" text-anchor="end" class="lab">{name}</text>')
        arr=body[name]+tail[name]
        for c,sym in enumerate(arr):
            x,y=x2+c*sz,120+r*sz
            s.append(f'<rect class="cell" x="{x}" y="{y}" width="{sz}" height="{sz}"/>'+mark(sym,x,y,sz))
        s.append(f'<line x1="{x2+9*sz}" y1="{120+r*sz}" x2="{x2+9*sz}" y2="{120+(r+1)*sz}" stroke="black" stroke-width="2"/>')
    y3,x3=550,40; s.append(f'<text x="{x3}" y="{y3-15}" class="lab">Collective 9×9 body, columns A→I</text>')
    for r in range(9):
        for c in range(9):
            x,y=x3+c*sz,y3+r*sz; sym=vals.get(1+c+9*r,"?")
            s.append(f'<rect class="cell" x="{x}" y="{y}" width="{sz}" height="{sz}"/>'+mark(sym,x,y,sz))
    px,py,mini=390,550,24; s.append(f'<text x="{px}" y="{py-15}" class="lab">Per-class 3×3 body + 3-cell tail</text>')
    for i,name in enumerate(CLASSES):
        gx,gy=px+(i%3)*250,py+(i//3)*115
        s.append(f'<text x="{gx}" y="{gy+18}" class="lab">{name}</text>')
        for k,sym in enumerate(body[name]):
            rr,cc=divmod(k,3); x,y=gx+24+cc*mini,gy+2+rr*mini
            s.append(f'<rect class="cell" x="{x}" y="{y}" width="{mini}" height="{mini}"/>'+mark(sym,x,y,mini))
        for k,sym in enumerate(tail[name]):
            x,y=gx+112+k*mini,gy+26
            s.append(f'<rect class="cell" x="{x}" y="{y}" width="{mini}" height="{mini}"/>'+mark(sym,x,y,mini))
    s.append('</svg>')
    out=Path("artifacts/foreground-views/observation-only-9x12.svg")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n".join(s),encoding="utf-8")

if __name__=="__main__":
    main()
