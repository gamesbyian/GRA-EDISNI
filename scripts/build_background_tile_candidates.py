#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
import cv2,numpy as np
from PIL import Image,ImageFile,UnidentifiedImageError
ImageFile.LOAD_TRUNCATED_IMAGES=False
TILES="ABCDEFGHI"; OUT=384

def tile(n): return TILES[(n-1)%9]

def load_sources(manifest):
    rows={}
    with open(manifest,newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("category")!="derived-community-resize": continue
            n=int(r["serial"]); p=Path(r["path"])
            if p.is_file() and r["tile"]==tile(n):
                rows[n]={"serial":n,"tile":r["tile"],"symbol":r["symbol"].strip(),"path":p}
    return list(rows.values())

def read_img(p):
    try:
        with Image.open(p) as x: x.verify()
        with Image.open(p) as x: rgb=np.asarray(x.convert("RGB"))
        return cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
    except (UnidentifiedImageError,OSError,ValueError,Image.DecompressionBombError):
        return None

def order_quad(pts):
    pts=np.asarray(pts,np.float32).reshape(4,2); s=pts.sum(1); d=np.diff(pts,axis=1).ravel()
    return np.array([pts[np.argmin(s)],pts[np.argmin(d)],pts[np.argmax(s)],pts[np.argmax(d)]],np.float32)

def rectify(img,size=700):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); h,w=g.shape
    best=None
    for pct in (55,65,75):
        th=np.percentile(g,pct); bw=(g>=th).astype(np.uint8)*255
        bw=cv2.morphologyEx(bw,cv2.MORPH_CLOSE,np.ones((11,11),np.uint8),iterations=2)
        cs,_=cv2.findContours(bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in cs:
            area=cv2.contourArea(c); af=area/(h*w)
            if not .18<=af<=.98: continue
            rect=cv2.minAreaRect(c); rw,rh=rect[1]
            if min(rw,rh)<20: continue
            ratio=max(rw,rh)/min(rw,rh)
            if ratio>1.30: continue
            q=order_quad(cv2.boxPoints(rect)); cen=q.mean(0)
            center=((cen[0]-w/2)/w)**2+((cen[1]-h/2)/h)**2
            score=af-2.2*center-.25*(ratio-1)
            if best is None or score>best[0]: best=(score,q)
    if best is None:return None,"no-confident-square"
    dst=np.array([[0,0],[size-1,0],[size-1,size-1],[0,size-1]],np.float32)
    H=cv2.getPerspectiveTransform(best[1],dst)
    return cv2.warpPerspective(img,H,(size,size),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_REPLICATE),"square"

def symbol_mask(symbol,n):
    m=np.zeros((n,n),np.uint8)
    if symbol in ("•","."):
        cv2.circle(m,(n//2,int(.43*n)),int(.20*n),255,-1)
    elif symbol=="-":
        cv2.rectangle(m,(int(.13*n),int(.29*n)),(int(.87*n),int(.58*n)),255,-1)
    else:
        q=np.array([[int(.18*n),int(.77*n)],[int(.48*n),int(.82*n)],
                    [int(.82*n),int(.11*n)],[int(.52*n),int(.08*n)]],np.int32)
        cv2.fillConvexPoly(m,q,255)
    return cv2.dilate(m,np.ones((19,19),np.uint8),1)

def density(sticker,symbol):
    n=sticker.shape[0]; mask=symbol_mask(symbol,n)
    x0,x1=int(.08*n),int(.92*n); y0,y1=int(.06*n),int(.77*n)
    g=cv2.cvtColor(sticker[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY).astype(np.float32)
    v=(mask[y0:y1,x0:x1]==0).astype(np.float32)
    bg=cv2.GaussianBlur(g,(0,0),max(12,min(g.shape)/20))
    ink=cv2.GaussianBlur(np.clip(bg-g,0,50)/50,(0,0),2.0)
    num=cv2.resize(ink*v,(OUT,OUT),interpolation=cv2.INTER_AREA)
    den=cv2.resize(v,(OUT,OUT),interpolation=cv2.INTER_AREA)
    d=np.divide(num,np.maximum(den,.05),out=np.zeros_like(num),where=den>.05)
    return d.astype(np.float32),(den>.82).astype(np.uint8)

def corr(a,va,b,vb):
    m=(va>0)&(vb>0)
    if m.sum()<.2*a.size:return np.nan
    x=a[m].astype(float); y=b[m].astype(float); x-=x.mean(); y-=y.mean()
    z=np.linalg.norm(x)*np.linalg.norm(y)
    return float(np.dot(x,y)/z) if z>1e-9 else np.nan

def align(ref,rv,a,av):
    common=(rv>0)&(av>0)
    if common.sum()<.2*a.size:return None
    x=cv2.GaussianBlur(ref,(0,0),3); y=cv2.GaussianBlur(a,(0,0),3)
    xf=np.where(common,x,np.median(x[common])).astype(np.float32)
    yf=np.where(common,y,np.median(y[common])).astype(np.float32)
    (dx,dy),resp=cv2.phaseCorrelate(xf,yf)
    if abs(dx)>16 or abs(dy)>16 or resp<.03:return None
    M=np.float32([[1,0,-dx],[0,1,-dy]])
    aa=cv2.warpAffine(a,M,(OUT,OUT),flags=cv2.INTER_LINEAR,borderValue=0)
    vv=cv2.warpAffine(av,M,(OUT,OUT),flags=cv2.INTER_NEAREST,borderValue=0)
    return aa,vv,float(dx),float(dy)

def combine(rows):
    st=np.stack([r["img"] for r in rows]); vv=np.stack([r["valid"] for r in rows])>0
    with np.errstate(all="ignore"): med=np.nanmedian(np.where(vv,st,np.nan),axis=0)
    return med,vv.sum(0)

def render(med,sup,n):
    known=np.isfinite(med)&(sup>0); g=np.full(med.shape,127,np.uint8)
    if known.any():
        lo,hi=np.percentile(med[known],[2,98]); hi=max(hi,lo+1e-6)
        g[known]=np.clip((med[known]-lo)/(hi-lo)*255,0,255).astype(np.uint8)
    view=g.copy()
    if (~known).any(): view=cv2.inpaint(view,(~known).astype(np.uint8)*255,5,cv2.INPAINT_TELEA)
    view=cv2.createCLAHE(1.5,(8,8)).apply(view)
    rgba=np.dstack([g,g,g,np.where(known,255,0).astype(np.uint8)])
    support=np.clip(sup/max(1,n)*255,0,255).astype(np.uint8)
    return rgba,support,view,known

def contact(views,out,order):
    sh=np.full((OUT*3+75,OUT*3),245,np.uint8)
    for i,t in enumerate(order):
        if t not in views: continue
        r,c=divmod(i,3); y=r*OUT+25; x=c*OUT
        sh[y:y+OUT,x:x+OUT]=views[t]
        cv2.putText(sh,t,(x+8,y-5),cv2.FONT_HERSHEY_SIMPLEX,.65,20,2,cv2.LINE_AA)
    cv2.imwrite(str(out),sh)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--manifest",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True); a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    src=load_sources(a.manifest); prep={t:[] for t in TILES}; prov=[]
    for s in src:
        im=read_img(s["path"])
        if im is None: prov.append({**s,"status":"decode-reject"}); continue
        z,method=rectify(im)
        if z is None: prov.append({**s,"status":method}); continue
        d,v=density(z,s["symbol"])
        if v.mean()<.55: prov.append({**s,"status":"mask-reject"}); continue
        r={**s,"img":d,"valid":v,"method":method}; prep[s["tile"]].append(r)
    qa={}; views={}; accepted=[]
    for t,rows in prep.items():
        if len(rows)<3: qa[t]={"status":"FAIL","reason":"too-few-prepared","prepared":len(rows)}; continue
        medoids=[]
        for i,x in enumerate(rows):
            cs=[corr(x["img"],x["valid"],y["img"],y["valid"]) for j,y in enumerate(rows) if i!=j]
            cs=[c for c in cs if np.isfinite(c)]; medoids.append(np.median(cs) if cs else -1)
        ri=int(np.argmax(medoids)); ref=rows[ri]
        al=[]
        for r in rows:
            q=align(ref["img"],ref["valid"],r["img"],r["valid"])
            if q is None: prov.append({**r,"status":"align-reject"}); continue
            img,v,dx,dy=q; c=corr(ref["img"],ref["valid"],img,v)
            if not np.isfinite(c) or c<.08: prov.append({**r,"status":"agreement-reject"}); continue
            al.append({**r,"img":img,"valid":v,"corr":c,"dx":dx,"dy":dy})
        if len(al)<3: qa[t]={"status":"FAIL","reason":"too-few-aligned","accepted":len(al)}; continue
        m0,_=combine(al); mv=np.isfinite(m0).astype(np.uint8)
        cs=np.array([corr(np.nan_to_num(m0),mv,r["img"],r["valid"]) for r in al])
        finite=cs[np.isfinite(cs)]; floor=.08
        if len(finite)>=4:
            q=float(np.median(finite)); mad=float(np.median(np.abs(finite-q))); floor=max(.08,q-3.5*max(mad,.015))
        kept=[r for r,c in zip(al,cs) if np.isfinite(c) and c>=floor]
        if len(kept)<3: qa[t]={"status":"FAIL","reason":"too-few-consensus","accepted":len(kept)}; continue
        med,sup=combine(kept); rgba,sup8,view,known=render(med,sup,len(kept))
        cv2.imwrite(str(a.out/f"{t}.png"),rgba); cv2.imwrite(str(a.out/f"{t}-support.png"),sup8)
        cv2.imwrite(str(a.out/f"{t}-enhanced.png"),view); views[t]=view; accepted+=kept
        sy=sorted(set(r["symbol"] for r in kept)); cov=float(known.mean()); c2=float((sup>=2).mean())
        qa[t]={"status":"PASS" if cov>=.72 and len(sy)>=2 else "FAIL","prepared":len(rows),"accepted":len(kept),
               "reference":ref["serial"],"symbols":sy,"coverage_any":round(cov,4),"coverage_2plus":round(c2,4)}
    contact(views,a.out/"physical-layout-contact-sheet.png","IABCDEFGH"); contact(views,a.out/"A-I-contact-sheet.png",TILES)
    (a.out/"qa.json").write_text(json.dumps(qa,indent=2)+"\n",encoding="utf-8")
    with (a.out/"provenance.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["serial","tile","symbol","path","status"])
        ok={(r["serial"],r["tile"]) for r in accepted}
        for s in src:w.writerow([f'{s["serial"]:03d}',s["tile"],s["symbol"],s["path"],"accepted" if (s["serial"],s["tile"]) in ok else "rejected"])
    (a.out/"README.md").write_text("# Candidate A-I masters\n\nReview candidates only. Not promoted automatically.\n\n"+json.dumps(qa,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(qa,indent=2))
    return 0 if all(qa.get(t,{}).get("status")=="PASS" for t in TILES) else 2
if __name__=="__main__": raise SystemExit(main())
