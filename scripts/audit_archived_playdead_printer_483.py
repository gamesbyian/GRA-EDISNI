#!/usr/bin/env python3
"""Experiment 483: pin recovered printer-era client bytes and runtime/source-map split.

CLI: python scripts/audit_archived_playdead_printer_483.py --source ORIGINAL_JS
Offline CI verifies the recorded evidence/protocol schema without committing
copyrighted third-party full JS. No source download or live website requests.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"data/experiment-483-original-printer-client.json"

def load():
    d=json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert d["experiment"]==483
    assert len(d["primary_sources"])==3
    assert d["primary_sources"][1]["sha256"]==d["primary_sources"][2]["sha256"]
    assert d["original_printer_client"]["input_selector"]=="#mce-EMAIL"
    req=d["original_printer_client"]["request_program"]
    assert [x["path"] for x in req]==[
        "/print/prepare.php","/print/index.php","/print/index.php"]
    assert [x["payload_keys"] for x in req]==[
        ["in","id","check","url"],["in","id","check","url"],["in","id"]]
    assert d["original_printer_client"]["empty_input"]["request_count"]==1
    assert d["original_printer_client"]["nonempty_rejected"]["request_count"]==2
    assert d["original_printer_client"]["nonempty_unrejected"]["request_count"]==3
    return d

def check_source(data, d):
    actual=hashlib.sha256(data).hexdigest()
    assert actual==d["primary_sources"][1]["sha256"],actual
    assert len(data)==d["primary_sources"][1]["bytes"]
    s=data.decode("utf-8")
    start=s.find("var printCheck = function()")
    assert start>0
    compiled=s[:s.index("//# sourceMappingURL=")]
    assert compiled.count("/print/prepare.php")==1
    assert compiled.count("/print/index.php")==2
    assert "var s_input = $('#mce-EMAIL').val()" in compiled
    assert "if (s_input != \"\")" in compiled
    assert "url: window.location.pathname" in compiled
    assert "check: 'true'" in compiled
    assert "localStorage.getItem('id')" in compiled
    assert compiled.count("printCheck") == 1, "button invocation must be separately source-proven"
    assert "window.print()" in compiled
    assert "if (data == 'false')" in compiled
    assert "var _data = { in: s_input, id: localStorage.getItem('id')}" in compiled
    assert compiled.index("$.post('/print/prepare.php', data)") < compiled.index(
        "$.post('/print/index.php', data)") < compiled.index(
        "$.post('/print/index.php', _data)")
    m=re.search(r"//# sourceMappingURL=data:application/json(?:;charset=[^;]+)?;base64,([A-Za-z0-9+/=]+)",s)
    assert m
    sm=json.loads(base64.b64decode(m.group(1)))
    assert len(sm["sources"])==d["sourcemap"]["module_count"]
    idx=sm["sources"].index("3_print.js")
    printer=sm["sourcesContent"][idx]
    assert len(printer)==d["sourcemap"]["printer_module_chars"]
    assert printer.count("/print/prepare.php")==0
    assert printer.count("/print/index.php")==2
    assert "window.location.pathname" not in printer
    assert r"if (!/^$|\s+/.test(s_input))" in printer
    assert "if (s_input != \"\")" not in printer
    return {"source_sha256":actual,"bytes":len(data),
            "source_map_modules":len(sm["sources"]),"mapped_printer_module":sm["sources"][idx],
            "runtime_preparation_post_calls":1,"runtime_index_post_calls":2,
            "source_map_stale_for_print_protocol":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,help="local original 2018/2019 id_ replay JS bytes")
    a=p.parse_args()
    d=load()
    if not a.source:
        print("PASS experiment 483: offline historic-client fixture and three-request protocol verified; pass --source for raw byte and embedded-map checks")
    else:
        print(json.dumps(check_source(a.source.read_bytes(),d),indent=2))
if __name__=="__main__":main()
