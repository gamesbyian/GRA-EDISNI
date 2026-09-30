#!/usr/bin/env python3
"""Preserve the historical 846shEE A-I composite as evidence-preserving masters.

This is deliberately conservative. It crops the known A-I tiles from the
historical solved composite, masks the foreground symbol and A-I label, and
writes RGBA masters where masked pixels are transparent. It does NOT invent
replacement background pixels.

Physical layout:
    I A B
    C D E
    F G H
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

LAYOUT = (("I","A","B"),("C","D","E"),("F","G","H"))
SYMBOL = {
    "I":"slash","A":"slash","B":"slash",
    "C":"dash","D":"dash","E":"slash",
    "F":"dash","G":"dot","H":"dash",
}

def scaled(v: int, src: int, dst: int) -> int:
    return int(round(v * dst / src))

def cuts_for_size(w: int, h: int):
    # Coordinates measured from the canonical 1455 x 1536 846shEE image.
    xs = [118, 537, 945, 1335]
    ys = [148, 559, 991, 1384]
    if (w,h)!=(1455,1536):
        xs=[scaled(x,1455,w) for x in xs]
        ys=[scaled(y,1536,h) for y in ys]
    return xs,ys

def evidence_mask(label: str, shape: tuple[int,int]) -> np.ndarray:
    """255 = known/evidenced pixel, 0 = symbol/label deliberately unknown."""
    h,w=shape
    unknown=np.zeros((h,w),np.uint8)
    kind=SYMBOL[label]

    if kind=="slash":
        pts=np.array([
            [0.08,0.84],
            [0.34,0.84],
            [0.83,0.08],
            [0.52,0.08],
        ],np.float32)
        pts[:,0]*=w
        pts[:,1]*=h
        cv2.fillConvexPoly(unknown,pts.astype(np.int32),255)
    elif kind=="dash":
        cv2.rectangle(
            unknown,
            (int(.05*w),int(.37*h)),
            (int(.95*w),int(.64*h)),
            255,-1,
        )
    else:
        cv2.circle(
            unknown,
            (int(.50*w),int(.56*h)),
            int(.22*min(w,h)),
            255,-1,
        )

    # Mask the added A-I label.
    if label in "IAB":
        cv2.rectangle(unknown,(0,0),(int(.15*w),int(.15*h)),255,-1)
    else:
        cv2.rectangle(unknown,(0,int(.80*h)),(int(.18*w),h),255,-1)

    # Conservative fringe around symbol/letter edges.
    unknown=cv2.dilate(unknown,np.ones((7,7),np.uint8),iterations=1)
    return 255-unknown

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("source",type=Path)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--size",type=int,default=512)
    args=ap.parse_args()

    src=np.array(Image.open(args.source).convert("L"))
    h,w=src.shape
    xs,ys=cuts_for_size(w,h)
    args.out.mkdir(parents=True,exist_ok=True)

    views={}
    coverage={}
    for r,row in enumerate(LAYOUT):
        for c,label in enumerate(row):
            crop=src[ys[r]:ys[r+1],xs[c]:xs[c+1]]
            crop=cv2.resize(crop,(args.size,args.size),interpolation=cv2.INTER_LANCZOS4)
            known=evidence_mask(label,crop.shape)
            rgba=np.dstack([crop,crop,crop,known])
            cv2.imwrite(str(args.out/f"{label}.png"),rgba)
            cv2.imwrite(str(args.out/f"{label}-known-mask.png"),known)
            coverage[label]=float(np.mean(known>0))
            # Contact sheet shows unknown pixels as neutral gray, not fabricated texture.
            view=crop.copy()
            view[known==0]=127
            views[label]=view

    sheet=np.full((args.size*3,args.size*3),127,np.uint8)
    for i,label in enumerate("IABCDEFGH"):
        rr,cc=divmod(i,3)
        sheet[rr*args.size:(rr+1)*args.size,cc*args.size:(cc+1)*args.size]=views[label]
        cv2.putText(sheet,label,(cc*args.size+12,rr*args.size+38),
                    cv2.FONT_HERSHEY_SIMPLEX,1.0,255,2,cv2.LINE_AA)
    cv2.imwrite(str(args.out/"physical-layout.png"),sheet)

    readme=[
        "# Evidence-preserving A-I masters from 846shEE",
        "",
        "These files preserve the directly visible background evidence in the historical solved 846shEE composite.",
        "",
        "- A.png through I.png are 512x512 RGBA.",
        "- Transparent pixels are foreground-symbol or added A-I-label regions and are deliberately unknown.",
        "- *-known-mask.png is 255 where the historical composite directly evidences the tile and 0 where it does not.",
        "- physical-layout.png shows the known physical arrangement I-A-B / C-D-E / F-G-H, with unknown areas rendered neutral gray.",
        "- No texture is synthesized or inpainted into unknown regions.",
        "",
        "Source: historical community composite known as 846shEE (originally linked as https://i.imgur.com/846shEE.jpg).",
        "",
        "Known-pixel coverage:",
    ]
    for label in "ABCDEFGHI":
        readme.append(f"- {label}: {coverage[label]:.3%}")
    readme.append("")
    (args.out/"README.md").write_text("\n".join(readme),encoding="utf-8")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
