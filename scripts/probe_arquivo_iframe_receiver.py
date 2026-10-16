#!/usr/bin/env python3
"""Acquire only exact Archive.pt replay iframe resources exposed by dated viewers.

The 2018/2019 *viewer HTML*, already preserved as a GitHub Actions artifact,
specifies the mp_ iframe URLs here. We do not call original site hosts. Raw
archived bytes are saved in the Actions artifact, not committed as Playdead code.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.request

ARCHIVE_HOSTS = {"arquivo.pt", "www.arquivo.pt"}
PATH = "/wayback/"
BASE = "https://arquivo.pt"
SOURCES = {
    "2018-07-19": "20180719141035",
    "2019-03-27": "20190327172747",
}
RESOURCE = "https://playdead.com/js/dist.js"
LIMIT = 1_500_000

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def check(url):
    u=urllib.parse.urlsplit(url)
    if u.scheme!="https" or u.hostname not in ARCHIVE_HOSTS \
       or not u.path.startswith(("/wayback/","/noFrame/replay/")):
        raise ValueError("blocked non-archive URL: "+url[:150])

def plan():
    targets=[]
    for label,stamp in SOURCES.items():
        for mode in ("mp_", "id_"):
            targets.append({"label":label, "mode":mode,
                "url":f"{BASE}{PATH}{stamp}{mode}/{RESOURCE}"})
    # Official Arquivo.pt documentation describes the independent no-frame route.
    targets.append({"label":"2018-07-19","mode":"noFrame",
        "url":f"{BASE}/noFrame/replay/{SOURCES['2018-07-19']}/{RESOURCE}"})
    for task in targets:check(task["url"])
    assert len(targets)==5
    return targets

def fetch(url):
    check(url)
    req=urllib.request.Request(url,headers={
        "User-Agent":"GRA-EDISNI closed-source archive study/1.0",
        "Accept":"application/javascript,text/plain,text/html,*/*"})
    opener=urllib.request.build_opener(SafeRedirect())
    with opener.open(req,timeout=13) as r:
        final=r.geturl();check(final)
        content=r.read(LIMIT+1)
        if len(content)>LIMIT: raise ValueError("oversized archival response")
        return content, {"http_status":r.status,
                         "url":final,"mime":r.headers.get("Content-Type","")}

def inspect(data:bytes,meta:dict):
    txt=data.decode("utf-8",errors="replace")
    html=bool(re.match(r"\s*(?:<!DOCTYPE\s+html|<html)\b",txt,re.I))
    looksjs=bool("jQuery" in txt[:1000] or "/print/index.php" in txt or
                 "changeForInputSuccess" in txt)
    return {"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
            "classification": "archive_viewer_html" if html else
                "javascript_source_candidate" if looksjs else "other_content",
            "print_endpoint_mentions":txt.count("/print/index.php"),
            "print_prepare_mentions":txt.count("/print/prepare.php"),
            "success_handler_mentions":txt.count("changeForInputSuccess"),
            "browser_print_mentions":txt.count("window.print"),
            "inline_sourcemap": "sourceMappingURL=data:application/json;base64," in txt,
            **meta}

def selftest():
    t=plan()
    assert len(t)==5
    for x in ("https://playdead.com/js/dist.js", "https://terminal41.link/foo",
              "http://arquivo.pt/wayback/abc","https://arquivo.pt/textsearch"):
        try:check(x)
        except ValueError:continue
        raise AssertionError("Failed archival host guard")
    assert inspect(b'<!DOCTYPE html><html></html>',{})["classification"]=="archive_viewer_html"
    assert inspect(b'/*! jQuery */ /print/index.php',{})["classification"]=="javascript_source_candidate"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--execute",action="store_true")
    p.add_argument("--out",default="search-output/arquivo-iframe-replay-2026-10-16.json")
    a=p.parse_args()
    selftest()
    tasks=plan()
    if not a.execute:
        print("DRY_RUN_NO_NETWORK",json.dumps(tasks,indent=2));return
    target=Path(a.out);target.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for n,task in enumerate(tasks):
        rec=dict(task)
        try:
            data,meta=fetch(task["url"])
            rec.update(inspect(data,meta))
            file=target.parent / f"arquivo-2018-19-{n}.replay-capture.bin"
            file.write_bytes(data);rec["artifact"]=file.name
        except Exception as exc:
            rec.update({"classification":"archive_unavailable",
                        "error_type":type(exc).__name__,"error":str(exc)[:180]})
        rows.append(rec)
        print("ARCHIVED_IFRAME",rec["label"],rec["mode"],rec["classification"],
              rec.get("bytes",0),rec.get("print_endpoint_mentions",0),
              rec.get("error_type",""),flush=True)
        time.sleep(0.5)
    target.write_text(json.dumps({"source":"exact iframe references from recovered 2018/2019 archival viewer",
        "source_archive_metadata":"historical-receiver-archive-phase2-2026-10-16.json",
        "site_queried":"arquivo.pt only","never_contact_original":True,"results":rows
        },indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
