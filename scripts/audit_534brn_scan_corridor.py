#!/usr/bin/env python3
"""Experiment 417: recover the damaged 534brn JPEG scan corridor."""

from __future__ import annotations
import base64, json, urllib.parse, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-417-534brn-scan-corridor.json"
REPO="gamesbyian/playdead-unofficial-exports"
REF="5e5897e2ce70dad5a2bd85e459770637cb36610f"
PATHS={
 "A":"assets/534brn9653f9j8mmd_original-4f038b969c841fd7.html",
 "B":"assets/534brn9653f9j8mmd_1-9014735779444bc3.html",
 "P":"assets/message-630970294e9fb0ce.txt",
}
UNKNOWN=256
FOOTER=b"pe^!02un"

def fetch(path):
    u=f"https://api.github.com/repos/{REPO}/contents/{urllib.parse.quote(path)}?ref={REF}"
    req=urllib.request.Request(u,headers={"Accept":"application/vnd.github+json"})
    with urllib.request.urlopen(req) as rsp:
        d=json.load(rsp)
    return base64.b64decode(d["content"])

def tokenize(blob,label):
    out=[]; i=0
    while i<len(blob):
        if label in {"B","P"} and blob[i:i+3]==b"\xef\xbf\xbd":
            out.append(UNKNOWN); i+=3; continue
        v=blob[i]; i+=1
        if label=="A" and v==0x3f:
            out.append(UNKNOWN); continue
        if v in (0x0d,0x0a): continue
        out.append(v)
    return out

def find_seq(tokens,seq):
    seq=list(seq)
    return [i for i in range(len(tokens)-len(seq)+1) if tokens[i:i+len(seq)]==seq]

def sos_hits(tokens):
    pattern=[UNKNOWN,UNKNOWN,0x20,0x0c,0x03,0x01,0x20,0x02,0x11,0x03,0x11,0x20,0x3f,0x20]
    return find_seq(tokens,pattern)

def dri_hits(tokens,end):
    # FF DD 00 04 interval_hi interval_lo under the lossy transform.
    return [
        i for i in range(end-5)
        if tokens[i]==UNKNOWN and tokens[i+1]==UNKNOWN
        and tokens[i+2]==0x20 and tokens[i+3]==0x04
    ]

def main():
    tokens={k:tokenize(fetch(p),k) for k,p in PATHS.items()}
    result={"experiment":417,"captures":{}}

    for label,t in tokens.items():
        footer=find_seq(t,FOOTER)
        assert len(footer)==1
        f=footer[0]
        eoi_candidate=(f-2,f)
        assert t[f-2:f]==[UNKNOWN,UNKNOWN]

        sos=sos_hits(t)
        rec={
            "token_count":len(t),
            "footer_offset":f,
            "eoi_shaped_candidate":[f-2,f-1],
            "two_unknowns_immediately_before_footer":True,
            "sos_hits":sos,
        }
        if sos:
            assert len(sos)==1
            rec["entropy_start"]=sos[0]+14
            rec["entropy_end_exclusive"]=f-2
            rec["normalized_entropy_token_span"]=(f-2)-(sos[0]+14)
            rec["dri_shaped_hits_before_sos"]=dri_hits(t,sos[0])
        result["captures"][label]=rec

    assert result["captures"]["B"]["sos_hits"]==[7975]
    assert result["captures"]["P"]["sos_hits"]==[580]
    assert result["captures"]["B"]["dri_shaped_hits_before_sos"]==[]
    assert result["captures"]["P"]["dri_shaped_hits_before_sos"]==[]

    result["interpretation"]=(
        "B and P each contain one exact baseline-SOS-shaped sequence. In all A/B/P captures the final two "
        "normalized tokens immediately before the footer are unknown/unknown, exactly the corruption shape expected "
        "for JPEG EOI FF D9. This bounds the entropy corridor without guessing pixels. No DRI-shaped segment is found "
        "before SOS in B or P, so there is no obvious restart-interval shortcut for counting MCUs; the next dimension "
        "test requires entropy/Huffman structural decoding rather than restart-marker counting."
    )
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
