#!/usr/bin/env python3
"""CL09: original-vs-rendition damaged 534brn A byte and alignment audit.

The genuinely preserved A is Git blob ce55c03, 12140 bytes.
The former connector rendition is f9cdbd1, 12150 bytes.
Recompute the exact old and new B/P/A alignment-supported candidate
positions without treating heuristic edit alignment as uniquely correct.

All source bytes are local; no network and no guessed original JPEG bytes.
"""
from __future__ import annotations
import argparse
from collections import Counter
from difflib import SequenceMatcher
import hashlib
import json
from pathlib import Path

from audit_534brn_loss_map import UNKNOWN,TERMINAL,find_ascii,make_map,tokenize
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"archive"/"external"/"terminal41-534brn"
CAPTURES={
    "original_a":("A-original-capture.bin","ce55c03ee972954f6e80f55a1a279bb85024f99b",12140),
    "rendition_a":("A-connector-rendition-not-original.bin","f9cdbd18bbd8713adee89ad93a3551b6310fd7ba",12150),
    "b":("B-original-capture.bin","f12c02c49f4c3f7589419fe8e20d655f7b95a9f4",16922),
    "p":("P-partial-capture.bin","9580913d043ca3efd54a01a38a9cff5767ea8ee7",8760),
}
FROZEN=ROOT/"data"/"534brn-canonical-partial-evidence-2026-10-08.json"

def blob_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def load():
    res={}
    for tag,(name,sha,size) in CAPTURES.items():
        raw=(D/name).read_bytes()
        assert len(raw)==size and blob_sha(raw)==sha,(tag,len(raw),blob_sha(raw))
        res[tag]=raw
    return res

def align(A,B,P):
    AT,BT,PT=(tokenize(x,l) for x,l in ((A,"A"),(B,"B"),(P,"P")))
    a_j=find_ascii(AT,b"JFIF")
    b_j=find_ascii(BT,b"JFIF")
    a_end=find_ascii(AT,TERMINAL)+len(TERMINAL)
    b_end=find_ascii(BT,TERMINAL)+len(TERMINAL)
    p_end=find_ascii(PT,TERMINAL)+len(TERMINAL)
    ma=make_map(AT,BT,a_j,a_end,b_j,b_end)
    mp=make_map(PT,BT,0,p_end,7387,b_end)
    statuses=[]
    hexes=[]
    rec={}
    conflicts={}
    counter=Counter()
    for i in range(b_j,b_end):
        base=BT[i]
        ai=ma.get(i)
        pi=mp.get(i)
        av=AT[ai] if ai is not None else UNKNOWN
        pv=PT[pi] if pi is not None else UNKNOWN
        if base !=UNKNOWN:
            tag,val="B",base
        elif av!=UNKNOWN and pv!=UNKNOWN and av!=pv:
            tag,val="C",UNKNOWN
            conflicts[i-b_j]={"a":f"{av:02x}","p":f"{pv:02x}"}
        elif av!=UNKNOWN and pv!=UNKNOWN:
            tag,val="D",av
        elif av!=UNKNOWN:
            tag,val="A",av
        elif pv!=UNKNOWN:
            tag,val="P",pv
        else:
            tag,val="U",UNKNOWN
        statuses.append(tag)
        hx="??" if val==UNKNOWN else f"{val:02x}"
        hexes.append(hx)
        counter[tag]+=1
        if tag in "APD":rec[i-b_j]=(hx,tag)
    assert len(statuses)==len(hexes)==12052
    return {"counts":dict(counter),"statuses":statuses,"hexes":hexes,
            "recoveries":rec,"conflicts":conflicts,
            "tokens_original_a":len(AT),
            "original_a_unknown_tokens":sum(t==UNKNOWN for t in AT),
            "a_original_jfif_to_footer_token_span":a_end-a_j}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",help="Full comparison JSON")
    a=ap.parse_args()
    raw=load()
    old=align(raw["rendition_a"],raw["b"],raw["p"])
    new=align(raw["original_a"],raw["b"],raw["p"])
    frozen=json.loads(FROZEN.read_text(encoding="utf8"))
    assert old["counts"]==frozen["counts"]
    assert old["recoveries"]=={int(x["offset"]):(x["byte"],x["source"]) for x in frozen["recovered_sites"]}
    assert old["conflicts"]=={int(x["offset"]):{"a":x["a"],"p":x["p"]} for x in frozen["conflicts"]}
    sm=SequenceMatcher(None,raw["original_a"],raw["rendition_a"],autojunk=False)
    ops=[{"operation":typ,"original_span":[i,j],"rendition_span":[k,l],
          "original_hex":raw["original_a"][i:j][:45].hex(),
          "rendition_hex":raw["rendition_a"][k:l][:45].hex()}
         for typ,i,j,k,l in sm.get_opcodes() if typ!="equal"]
    altered=[{"offset":i,"original_hex":old["hexes"][i],"true_hex":new["hexes"][i],
              "rendition_status":old["statuses"][i],"original_status":new["statuses"][i]}
             for i in range(12052)
             if old["hexes"][i]!=new["hexes"][i] or
                old["statuses"][i]!=new["statuses"][i]]
    old_sites=set(old["recoveries"])
    new_sites=set(new["recoveries"])
    change={
        "source_authentication":{
            k:{"git_blob_sha":blob_sha(v),"bytes":len(v)}
            for k,v in raw.items()
        },
        "original_a_known_token_count":new["tokens_original_a"]-new["original_a_unknown_tokens"],
        "former_rendition_a_token_count":old["tokens_original_a"],
        "original_a_unknown_token_count":new["original_a_unknown_tokens"],
        "original_a_jfif_to_footer_tokens":new["a_original_jfif_to_footer_token_span"],
        "rendition_a_jfif_to_footer_tokens":old["a_original_jfif_to_footer_token_span"],
        "old_counts":old["counts"],
        "true_original_counts":new["counts"],
        "old_candidate_fills":len(old_sites),
        "original_a_candidate_fills":len(new_sites),
        "shared_candidate_offsets":len(old_sites & new_sites),
        "candidate_offsets_lost":len(old_sites-new_sites),
        "candidate_offsets_gained":len(new_sites-old_sites),
        "identical_byte_and_status_fills":sum(old["recoveries"][i]==new["recoveries"][i] for i in old_sites&new_sites),
        "status_or_byte_changed_positions":len(altered),
        "change_positions":altered[:400],
        "binary_edit_operations":ops[:30],
        "binary_edit_operation_count":len(ops),
        "old_conflicts":len(old["conflicts"]),
        "original_conflicts":len(new["conflicts"]),
        "shared_conflict_positions":len(set(old["conflicts"])&set(new["conflicts"])),
        "claim_scope":"Selected edit-map candidates, not uniquely recovered original entropy bytes; true A now source-authenticated.",
    }
    if a.output:Path(a.output).write_text(json.dumps(change,indent=2)+"\n",encoding="utf8")
    print("CL09_TRUE_A_RESULT="+json.dumps({k:v for k,v in change.items()
        if k not in ("change_positions","binary_edit_operations")},separators=(",",":")))

if __name__=="__main__":
    main()
