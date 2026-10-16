#!/usr/bin/env python3
"""Experiment 484: audit date-pinned archived original Playdead page wiring.

Checks the immutable source-URL, SHA and observed input structure registry.
Can optionally re-audit downloaded archival files from the original GHA ZIP.
Does not contact any website or require third-party original files in repo.
"""
from __future__ import annotations
import argparse,hashlib,json,re,zipfile
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"data/experiment-484-playdead-original-page-html.json"
PRINTER=ROOT/"data/experiment-483-original-printer-client.json"

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags=[]
    def handle_starttag(self,tag,attrs):
        self.tags.append((tag,dict(attrs)))
    def has_attr(self,tag,key,val):
        return any(t==tag and d.get(key)==val for t,d in self.tags)
    def handler(self):
        return any(d.get("onclick")=="printCheck()" and d.get("class")=="print-button-wrapper"
                   for t,d in self.tags if t=="div")

def load():
    data=json.loads(REG.read_text(encoding="utf8"))
    parent=json.loads(PRINTER.read_text(encoding="utf8"))
    assert data["experiment"]==484 and data["prior_experiment"]==parent["experiment"]==483
    sources=data["observations"]
    assert len(sources)==4 and len(set(x["sha256"] for x in sources))==4
    actual={x["label"]:x for x in sources}
    assert actual["home_actual_2019"]["capture_utc"]=="2019-03-27T17:27:02Z"
    assert actual["games_inside_actual_2018"]["capture_utc"]=="2018-07-19T14:09:51Z"
    assert actual["inside_redirect_actual_2025"]["capture_utc"]=="2025-10-09T10:48:55Z"
    assert actual["home_actual_2019"]["parse"]["print_content_id"]=="print-content"
    assert actual["home_actual_2019"]["parse"]["newsletter_external_destination_domain"]=="playdead.us3.list-manage.com"
    assert actual["games_inside_actual_2018"]["parse"]["email_input_id"] is None
    assert actual["games_inside_actual_2018"]["parse"]["print_content_id"] is None
    assert actual["games_inside_actual_2019"]["parse"]["email_input_id"] is None
    assert all(x["bytes"]>0 and len(x["sha256"])==64 for x in sources)
    assert all(x["actual_replay"].startswith("https://arquivo.pt/wayback/") for x in sources)
    assert data["no_original_live_requests"] and data["no_sticker_search"]
    return data

def verify_raw(raw:bytes,item:dict):
    assert hashlib.sha256(raw).hexdigest()==item["sha256"]
    assert len(raw)==item["bytes"]
    parser=Tags();parser.feed(raw.decode("utf-8",errors="replace"))
    kind=item["label"]
    if kind in {"home_actual_2019","games_inside_actual_2018","games_inside_actual_2019"}:
        assert parser.handler(),kind
        assert any(t=="script" and d.get("src","").endswith("/js/dist.js") for t,d in parser.tags)
    if kind=="home_actual_2019":
        assert parser.has_attr("input","id","mce-EMAIL")
        assert parser.has_attr("div","id","print-content")
        assert parser.has_attr("form","id","mc-embedded-subscribe-form")
        assert any(t=="form" and "list-manage.com" in d.get("action","") for t,d in parser.tags)
    if kind.startswith("games_inside_"):
        assert not parser.has_attr("input","id","mce-EMAIL")
        assert not parser.has_attr("div","id","print-content")

def main():
    arg=argparse.ArgumentParser()
    arg.add_argument("--zip",type=Path,help="downloaded GitHub Actions ZIP containing authentic archive replay bytes")
    a=arg.parse_args();data=load()
    if a.zip:
        filemap={"home_actual_2019":"playdead-2018-html-00.bin",
                 "games_inside_actual_2018":"playdead-2018-html-04.bin",
                 "games_inside_actual_2019":"playdead-2018-html-05.bin",
                 "inside_redirect_actual_2025":"playdead-2018-html-02.bin"}
        with zipfile.ZipFile(a.zip) as z:
            for item in data["observations"]:
                verify_raw(z.read(filemap[item["label"]]),item)
        print("PASS Experiment 484: original archived page bytes/DOM structures verified")
    else:
        print("PASS Experiment 484: 2018/2019 source provenance and 2025 replay exclusion are internally consistent")

if __name__=="__main__":main()
