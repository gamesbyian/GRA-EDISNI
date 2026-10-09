#!/usr/bin/env python3
"""Historical sticker/terminal41 source-cue census in original public Discord export.

Input: exact pinned 5MB Playdead Unofficial archive, NOT community summary.
No physical code symbols, missing-cell completions, semantics or proposed
decoder evaluated. Source-only historical conversations and timestamps.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

EXPECTED_BLOB_SHA="1889cc948f86f5a4455de0d7310b15cdb1b88b5c"
TOPICS = {
    "sticker_or_foreground":r"sticker|foreground|ce code|collector.s edition",
    "534brn_endpoint":r"534brn|5345rn|pe\^!02un|128 unsolved",
    "pixel_registration":r"overla[y|p]|pixel|color layers?|colour layers?|registration|align|rotation|rotate",
    "jpeg_recovery":r"jpe?g|jfif|corrupt|image repair|image data|broken image",
    "operation_instruction":r"solve|decoder|decode|decrypt|method|mapping|transform|instruction|step",
    "placement":r"serial|9 pieces?|tile|background|pattern|grid|position|rows?|columns?",
}
PAT={k:re.compile(v,re.I) for k,v in TOPICS.items()}
DATE=re.compile(r"(?:2018|2019|2020|2021|2022|2023|2024|2025|2026)[-/][01]?\d[-/][0-3]?\d")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("--out",default="/tmp/cl09-discord-history.json")
    a=p.parse_args()
    b=Path(a.source).read_bytes()
    git_blob=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    assert git_blob==EXPECTED_BLOB_SHA,(git_blob,len(b))
    s=b.decode("utf-8",errors="replace")
    lines=s.splitlines()
    found=[]
    for i,line in enumerate(lines):
        matched=[k for k,v in PAT.items() if v.search(line)]
        if not matched:continue
        focused=("534brn_endpoint" in matched or
                 "sticker_or_foreground" in matched and
                 ("pixel_registration" in matched or "jpeg_recovery" in matched or
                  "placement" in matched or "operation_instruction" in matched))
        if not focused:continue
        context="\n".join(lines[max(0,i-4):min(len(lines),i+6)])
        hints={k:sum(bool(v.search(t)) for t in lines[max(0,i-4):min(len(lines),i+6)])
               for k,v in PAT.items()}
        if not (hints["sticker_or_foreground"] or hints["534brn_endpoint"]):continue
        found.append({"line":i+1,"matches":matched,"hints":hints,"snippet":context[:1400]})
    # High-level source-only selection; no target-reading.
    unique=[]
    used=set()
    for z in found:
        canon=re.sub(r"\s+"," ",z["snippet"])[-450:]
        if canon in used:continue
        used.add(canon)
        score=4*z["hints"]["534brn_endpoint"]+3*z["hints"]["sticker_or_foreground"]+\
              z["hints"]["jpeg_recovery"]+z["hints"]["pixel_registration"]+\
              z["hints"]["placement"]
        z["score"]=score
        unique.append(z)
    rank=sorted(unique,key=lambda z:(-z["score"],z["line"]))
    result={
        "source_repository":"gamesbyian/playdead-unofficial-exports",
        "source_path":"Playdead Unofficial - ARG - solving [461275582970462209].txt",
        "source_git_blob_sha":git_blob,
        "bytes":len(b),"lines":len(lines),"total_focus_hits":len(found),
        "unique_context_snippets":len(unique),
        "sample_first_30_focus_hits":sorted(unique,key=lambda z:z["line"])[:30],
        "ranked_top_125":rank[:125],
        "interesting_2020_2021": [
            z for z in sorted(unique,key=lambda z:z["line"])
            if re.search(r"(2020|2021)",z["snippet"])
            and z["hints"]["534brn_endpoint"]
        ][:100],
    }
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    compact={"sha":git_blob,"bytes":len(b),"lines":len(lines),
             "hits":len(found),"unique":len(unique),
             "top":[{"line":z["line"],"score":z["score"],
                     "excerpt":z["snippet"][:380]}
                    for z in rank[:32]]}
    print("CL09_RESULT="+json.dumps(compact,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
