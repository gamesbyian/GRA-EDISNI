#!/usr/bin/env python3
"""Experiment 408: audit the nine-step Terminal41 shutdown confirmation chain.

Tests whether the exact nine-page structure can plausibly consume the robust
nine-symbol sticker feature. It cannot: the pages are a fixed linear redirect
countdown with no input/state branching.
"""

from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"archive"/"external"/"twinysam-inside-arg"/"terminal41.link"/"sys"/"activate_shutdown_protocol"/"commit"
OUT=ROOT/"data"/"experiment-408-terminal41-nine-step-consumer-audit.json"

PATTERN="___________DONE_SD_CONFIRMED_*.html"

def refresh_target(text):
    m=re.search(r'http-equiv="refresh"[^>]*url=([^"\s>]+)',text,re.I)
    return m.group(1) if m else None

def main():
    files=sorted(BASE.glob(PATTERN))
    assert len(files)==9, [p.name for p in files]

    records=[]
    for p in files:
        text=p.read_text(encoding="utf-8",errors="replace")
        records.append({
            "file":p.name,
            "target":refresh_target(text),
            "visible_payload":bool(re.sub(r"<[^>]+>","",text).strip()),
            "form_or_input":bool(re.search(r"<(?:form|input|select|textarea)\b",text,re.I)),
        })

    by_name={r["file"]:r for r in records}
    for n in range(2,10):
        cur=f"___________DONE_SD_CONFIRMED_{n:02d}.html"
        prev=f"___________DONE_SD_CONFIRMED_{n-1:02d}.html"
        assert by_name[cur]["target"]==prev
    assert by_name["___________DONE_SD_CONFIRMED_01.html"]["target"]=="../PROT6y723g90ty9r80234_confirmed_0385729128474.html"
    assert all(not r["form_or_input"] for r in records)

    result={
        "experiment":408,
        "candidate_external_structure":"nine Terminal41 shutdown-confirmation pages",
        "page_count":len(records),
        "records":records,
        "structure":"fixed linear 09->08->...->01->confirmed redirect chain",
        "input_capacity":"none in the nine pages; no forms, inputs, per-step symbol choices, or branch targets",
        "interpretation":(
            "Terminal41 does contain an exact nine-step structure, but it is a deterministic redirect countdown rather "
            "than a nine-slot consumer. It therefore cannot independently consume or validate the Experiment-398 "
            "nine-symbol signature. The cardinality match is closed rather than promoted."
        )
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
