#!/usr/bin/env python3
"""Experiments 413-414: decode the 534brn footer and test the 128 JPEG-header clue."""

from __future__ import annotations

import base64
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"experiment-413-414-534brn-footer-128.json"

UPSTREAM_REPO="gamesbyian/playdead-unofficial-exports"
UPSTREAM_REF="5e5897e2ce70dad5a2bd85e459770637cb36610f"
PATHS={
    "A":"assets/534brn9653f9j8mmd_original-4f038b969c841fd7.html",
    "B":"assets/534brn9653f9j8mmd_1-9014735779444bc3.html",
    "P":"assets/message-630970294e9fb0ce.txt",
}
UNKNOWN=256

def fetch(path):
    quoted=urllib.parse.quote(path)
    url=f"https://api.github.com/repos/{UPSTREAM_REPO}/contents/{quoted}?ref={UPSTREAM_REF}"
    req=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json"})
    with urllib.request.urlopen(req) as response:
        data=json.load(response)
    return base64.b64decode(data["content"])

def tokenize(blob,label):
    out=[]
    i=0
    while i<len(blob):
        if label in {"B","P"} and blob[i:i+3]==b"\xef\xbf\xbd":
            out.append(UNKNOWN); i+=3; continue
        v=blob[i]; i+=1
        if label=="A" and v==0x3F:
            out.append(UNKNOWN); continue
        if v in (0x0D,0x0A):
            continue
        out.append(v)
    return out

def footer_decode():
    raw="pe^!02un"
    rotated="".join({
        "n":"u","u":"n","2":"s","0":"o","!":"l","^":"v","e":"e","p":"d"
    }[ch] for ch in reversed(raw))
    assert rotated=="unsolved"
    dot_runs=[8,2,1]
    numeral="".join(str(x) for x in reversed(dot_runs))
    assert numeral=="128"
    return rotated,numeral

def sof_candidates(tokens):
    # Under the documented lossy text transform:
    # - bytes >=0x80 become UNKNOWN
    # - NUL 0x00 becomes space 0x20
    # A baseline SOF0 segment with dimensions in 128..255 therefore appears:
    # ?? ?? 20 11 08 20 ?? 20 ?? 03 01 22 20 02 11 01 03 11 01 ...
    hits=[]
    for i in range(len(tokens)-20):
        t=tokens
        if (
            t[i]==UNKNOWN and t[i+1]==UNKNOWN and
            t[i+2]==0x20 and t[i+3]==0x11 and t[i+4]==0x08 and
            t[i+5]==0x20 and t[i+6]==UNKNOWN and
            t[i+7]==0x20 and t[i+8]==UNKNOWN and
            t[i+9]==0x03 and
            t[i+10:i+19]==[0x01,0x22,0x20,0x02,0x11,0x01,0x03,0x11,0x01]
        ):
            hits.append(i)
    return hits

def main():
    rotated,numeral=footer_decode()
    blobs={k:fetch(v) for k,v in PATHS.items()}
    tokens={k:tokenize(v,k) for k,v in blobs.items()}
    candidates={k:sof_candidates(v) for k,v in tokens.items()}

    assert candidates["A"]==[7503]
    assert candidates["B"]==[7520]
    assert candidates["P"]==[133]

    result={
        "experiment_pair":[413,414],
        "footer":{
            "raw_text":"pe^!02un",
            "raw_dot_run_lengths":[8,2,1],
            "rotation":"180-degree / upside-down glyph reading",
            "decoded_word":rotated,
            "reversed_dot_run_digits":numeral,
            "decoded_message":"128 UNSOLVED",
        },
        "jpeg_header":{
            "sof0_shaped_candidate_count_each":{"A":1,"B":1,"P":1},
            "candidate_offsets_tokenized":candidates,
            "normalized_pattern":"?? ?? 20 11 08 20 ?? 20 ?? 03 01 22 20 02 11 01 03 11 01",
            "interpretation":[
                "20 11 is consistent with a 0x0011 SOF0 segment length after NUL->space corruption.",
                "08 is standard 8-bit sample precision.",
                "height and width each appear as 0x00?? with the low byte lost because it is >=0x80.",
                "the three captures therefore constrain both dimensions independently to 128..255.",
                "the component descriptor is consistent with 3 components and 2x2 luma / 1x1 chroma sampling."
            ],
            "dimension_range":[128,255],
        },
        "cross_evidence":{
            "historical_footer_reading_first_noted":"12 Apr 2026 community message proposed reading the footer as '128 unsolved'",
            "historical_jpeg_forensics":"20 Dec 2025 community analysis independently placed each dimension in 128..255 and noted behavior suggestive of roughly 64 MCU-like groups / near-128 geometry",
            "new_connection":"The footer's 128 lands exactly on the surviving SOF dimension boundary; this is a source-native numeric clue to test against the damaged JPEG header."
        },
        "conclusion":(
            "The footer is not random debris: a 180-degree reading yields '128 UNSOLVED'. "
            "Independently, all three damaged JPEG capture families contain one identical SOF0-shaped header "
            "whose lost height/width low bytes constrain each dimension to 128..255. This makes 128 a strong "
            "candidate image-dimension clue. It does not yet prove both dimensions are 128; axis/square status "
            "must be established separately before writing 128x128 into the evidence stream."
        )
    }

    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
