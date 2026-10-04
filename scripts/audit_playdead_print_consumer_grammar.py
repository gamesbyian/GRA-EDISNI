#!/usr/bin/env python3
"""Experiment 412: audit historical Playdead print-consumer client grammar."""

from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"archive"/"external"/"playdead-unofficial-exports"/"assets"/"print-b58746938d8d0071.txt"
OUT=ROOT/"data"/"experiment-412-playdead-print-consumer-grammar.json"

def main():
    text=SRC.read_text(encoding="utf-8")

    facts={
        "input_selector_present":"$('#mce-EMAIL').val()" in text,
        "endpoint_posts":len(re.findall(r"\$\.post\('/print/index\.php'",text)),
        "persistent_guid":"localStorage.setItem('id', guid())" in text,
        "check_pass":"'check': 'true'" in text or "check: 'true'" in text,
        "blank_only_client_gate":"!/^$|\\s+/.test(s_input)" in text,
        "server_false_rejection":"data == 'false'" in text,
        "second_post_after_success":"var _data = { in: s_input, id: localStorage.getItem('id')}" in text,
    }

    assert facts["input_selector_present"]
    assert facts["endpoint_posts"]==2
    assert facts["persistent_guid"]
    assert facts["check_pass"]
    assert facts["blank_only_client_gate"]
    assert facts["server_false_rejection"]
    assert facts["second_post_after_success"]

    result={
        "experiment":412,
        "source":"archived historical Playdead print JavaScript",
        "facts":facts,
        "client_side_format_constraints":{
            "nonblank_required":True,
            "length_constraint":None,
            "character_class_constraint":None,
            "numeric_constraint":None,
            "ternary_constraint":None,
            "nine_value_constraint":None,
        },
        "protocol":{
            "validation_request":{"endpoint":"/print/index.php","fields":["in","id","check=true"]},
            "content_request":{"endpoint":"/print/index.php","fields":["in","id"]},
            "state_key":"persistent browser-local GUID"
        },
        "interpretation":(
            "The historical consumer is a real arbitrary-text answer validator, but its browser code contributes "
            "almost no syntax information: it rejects only blank/whitespace input and delegates correctness to the "
            "server. It therefore supports the existence of hidden server-side consumers and per-client state, "
            "but cannot independently choose among the sticker project's text, numeric, ternary, or nine-symbol outputs."
        )
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
