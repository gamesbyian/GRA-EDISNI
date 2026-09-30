#!/usr/bin/env python3
"""Assemble the widest practical sticker-photo corpus for A-I tile reconstruction.

The community sticker ledger is the authority for serial/source association.  This
script copies every raw/edited sticker image from a checked-out community repo and,
optionally, follows every external URL on each numbered sticker row.  Supported
social pages are attempted with gallery-dl; ordinary HTML pages are inspected for
OpenGraph/Twitter images and inline image URLs.  Every saved file is renamed with
its sticker serial so the downstream master builder can classify it safely.

Failures are recorded, never silently discarded.
"""
from __future__ import annotations
import argparse, csv, hashlib, html, re, shutil, subprocess, urllib.parse, urllib.request
from pathlib import Path

ROW_RE = re.compile(r"^- \[(\d{3})\].*$", re.M)
URL_RE = re.compile(r"https?://[^\s)<>]+")
IMG_EXTS={".jpg",".jpeg",".png",".webp",".gif",".tif",".tiff"}
META_IMAGE_RE=re.compile(r'''(?:property|name)=["'](?:og:image|twitter:image(?::src)?)["'][^>]+content=["']([^"']+)["']|content=["']([^"']+)["'][^>]+(?:property|name)=["'](?:og:image|twitter:image(?::src)?)["']''',re.I)
IMG_SRC_RE=re.compile(r'''<img[^>]+src=["']([^"']+)["']''',re.I)

def sha256(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def ledger_rows(text:str):
    lines=text.splitlines()
    for line in lines:
        m=re.match(r"^- \[(\d{3})\]",line)
        if not m: continue
        serial=int(m.group(1))
        urls=[u.rstrip(".,;") for u in URL_RE.findall(line)]
        yield serial,line,urls

def copy_repo_images(repo:Path,out:Path,records:list[dict]):
    root=repo/"images"/"stickers"
    if not root.exists(): return
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in IMG_EXTS: continue
        m=re.search(r"(?<!\d)(\d{3})(?!\d)",p.stem)
        if not m: continue
        serial=int(m.group(1)); rel=p.relative_to(root)
        dest=out/f"{serial:03d}"/"community-repo"/rel
        dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
        records.append({"serial":serial,"kind":"community-repo","url":"","path":str(dest),"status":"ok","sha256":sha256(dest),"note":str(rel)})

def run_gallery(url:str,serial:int,out:Path,records:list[dict],timeout:int):
    if shutil.which("gallery-dl") is None: return False
    d=out/f"{serial:03d}"/"gallery-dl"; d.mkdir(parents=True,exist_ok=True)
    try:
        p=subprocess.run(["gallery-dl","--dest",str(d),"--filename",f"{serial:03d}_{{num:03}}.{{extension}}",url],
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
    except subprocess.TimeoutExpired:
        records.append({"serial":serial,"kind":"gallery-dl","url":url,"path":"","status":"timeout","sha256":"","note":""}); return True
    files=[x for x in d.rglob("*") if x.is_file() and x.suffix.lower() in IMG_EXTS]
    if files:
        for x in files: records.append({"serial":serial,"kind":"gallery-dl","url":url,"path":str(x),"status":"ok","sha256":sha256(x),"note":""})
        return True
    records.append({"serial":serial,"kind":"gallery-dl","url":url,"path":"","status":f"exit-{p.returncode}","sha256":"","note":(p.stdout or "")[-600:].replace("\n"," ")})
    return p.returncode==0

def fetch_html_images(url:str,serial:int,out:Path,records:list[dict],timeout:int):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 sticker-research/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=timeout) as r:
            ctype=r.headers.get_content_type()
            data=r.read(12*1024*1024)
            final=r.geturl()
    except Exception as e:
        records.append({"serial":serial,"kind":"html","url":url,"path":"","status":"fetch-failed","sha256":"","note":repr(e)[:500]}); return
    if ctype.startswith("image/"):
        ext=".jpg" if "jpeg" in ctype else "."+ctype.split("/")[-1].replace("svg+xml","svg")
        if ext in IMG_EXTS:
            d=out/f"{serial:03d}"/"direct"; d.mkdir(parents=True,exist_ok=True)
            p=d/f"{serial:03d}_direct{ext}"; p.write_bytes(data)
            records.append({"serial":serial,"kind":"direct","url":url,"path":str(p),"status":"ok","sha256":sha256(p),"note":final})
        return
    text=data.decode("utf-8","ignore")
    candidates=[]
    for m in META_IMAGE_RE.finditer(text):
        candidates.append(next(g for g in m.groups() if g))
    candidates += IMG_SRC_RE.findall(text)
    seen=set()
    for i,raw in enumerate(candidates[:40]):
        iu=urllib.parse.urljoin(final,html.unescape(raw))
        if iu in seen or not iu.startswith(("http://","https://")): continue
        seen.add(iu)
        try:
            rq=urllib.request.Request(iu,headers={"User-Agent":"Mozilla/5.0","Referer":final})
            with urllib.request.urlopen(rq,timeout=min(timeout,20)) as rr:
                ct=rr.headers.get_content_type()
                if not ct.startswith("image/") or "svg" in ct: continue
                b=rr.read(15*1024*1024)
            ext=".jpg" if "jpeg" in ct else "."+ct.split("/")[-1]
            if ext not in IMG_EXTS: continue
            d=out/f"{serial:03d}"/"html"; d.mkdir(parents=True,exist_ok=True)
            p=d/f"{serial:03d}_{i:03d}{ext}"; p.write_bytes(b)
            records.append({"serial":serial,"kind":"html-image","url":iu,"path":str(p),"status":"ok","sha256":sha256(p),"note":url})
        except Exception:
            continue

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--community-repo",type=Path,required=True)
    ap.add_argument("--out",type=Path,default=Path(".tmp/background-tile-corpus"))
    ap.add_argument("--harvest-web",action="store_true")
    ap.add_argument("--timeout",type=int,default=35)
    args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    ledger=args.community_repo/"stickers.md"
    text=ledger.read_text(encoding="utf-8",errors="replace")
    records=[]; copy_repo_images(args.community_repo,args.out,records)
    if args.harvest_web:
        for serial,line,urls in ledger_rows(text):
            for url in urls:
                host=urllib.parse.urlparse(url).netloc.lower()
                # Repository image links are already copied exactly; Discord/private links are not public-web acquisition.
                if "github.com" in host or "discord" in host or "discordapp" in host: continue
                handled=run_gallery(url,serial,args.out,records,args.timeout)
                if not handled: fetch_html_images(url,serial,args.out,records,args.timeout)
    manifest=args.out/"source-manifest.csv"
    fields=["serial","kind","url","path","status","sha256","note"]
    with manifest.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(records)
    ok=[r for r in records if r["status"]=="ok" and r["path"]]
    print(f"records={len(records)} usable_images={len(ok)} serials={len(set(r['serial'] for r in ok))}")
if __name__=="__main__": main()
