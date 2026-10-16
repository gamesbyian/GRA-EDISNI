#!/usr/bin/env python3
"""One-shot archive-only retrieval of 2018/2019 Playdead page HTML.
Never touches live Playdead or Terminal41; never submits passwords or stickers.
"""
import argparse,hashlib,json,re,time,urllib.parse,urllib.request
from html.parser import HTMLParser
from pathlib import Path
UA="GRA-EDISNI historical Playdead web study/1.0"
STAMPS=("20180719141035","20190327172747")
PATHS={"home":"https://playdead.com/",
       "inside":"https://playdead.com/inside/",
       "games_inside":"https://playdead.com/games/inside/",
       "inside_www":"http://www.playdead.com/inside/"}
MAX_BYTES=1400000

def guard(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.hostname not in {"arquivo.pt","www.arquivo.pt"} \
       or not p.path.startswith("/wayback/") or p.username or p.password:
        raise ValueError("non-archive resource blocked: "+url[:130])

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        guard(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

class HTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.forms=[];self.fields=[];self.scripts=[];self.handlers=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="form":self.forms.append({k:d.get(k) for k in ("action","method","id")})
        if tag in {"input","textarea","button","select"}:
            self.fields.append({"tag":tag,"id":d.get("id"),"type":d.get("type"),
                                "name":d.get("name"),"onclick":d.get("onclick")})
        if tag=="script" and d.get("src"):self.scripts.append(d["src"])
        self.handlers.extend([{"event":k,"value":str(v)[:200]} for k,v in attrs
                              if k.startswith("on") and "print" in str(v).lower()])

def analyze(data):
    text=data.decode("utf-8",errors="replace")
    parser=HTML()
    if re.search(r"<html\b",text[:5000],re.I):parser.feed(text)
    t=re.search(r"<title[^>]*>(.*?)</title\s*>",text,re.I|re.S)
    return {"html_detected":bool(re.search(r"<html\b",text[:5000],re.I)),
        "title":t.group(1).strip()[:120] if t else None,
        "printCheck_refs":len(re.findall(r"\bprintCheck\b",text)),
        "printCheck_invocations":len(re.findall(r"\bprintCheck\s*\(",text)),
        "mce_email_mentions":text.count("mce-EMAIL"),
        "print_button_mentions":text.lower().count("print-button"),
        "forms":parser.forms[:12],"fields":parser.fields[:40],
        "scripts":parser.scripts[:35],"print_events":parser.handlers[:30],
        "archive_viewer_iframe_only":("replay_iframe" in text[:3500])}

def plan():
    queries=[{"label":label,"requested_capture":stamp,"original":original,
       "archive_url":f"https://arquivo.pt/wayback/{stamp}id_/{original}"}
       for label,original in PATHS.items() for stamp in STAMPS]
    assert len(queries)==8
    for q in queries:guard(q["archive_url"])
    return queries

def fetch(url):
    guard(url)
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,*/*"})
    with urllib.request.build_opener(SafeRedirect()).open(req,timeout=15) as response:
        guard(response.geturl())
        raw=response.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:raise ValueError("oversize original page")
        return raw,{"status_code":response.status,"final_url":response.geturl(),
                    "mime":response.headers.get("Content-Type","")}

def tests():
    assert len(plan())==8
    for u in ("https://playdead.com/","https://terminal41.link/",
              "http://arquivo.pt/wayback/a","https://arquivo.pt/textsearch"):
        try:guard(u)
        except ValueError:pass
        else:raise AssertionError("live-original leak")
    row=analyze(b"<html><button onclick='printCheck()'></button><input id='mce-EMAIL'></html>")
    assert row["printCheck_invocations"]==1 and row["mce_email_mentions"]==1

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--execute",action="store_true")
    ap.add_argument("--output",default="search-output/playdead-original-2018-html.json")
    args=ap.parse_args();tests()
    if not args.execute:
        print("DRY_RUN_NO_NETWORK",json.dumps(plan(),indent=2));return
    output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
    rows=[]
    for i,item in enumerate(plan()):
        row=dict(item)
        try:
            raw,meta=fetch(item["archive_url"])
            row.update({"result":"archived_bytes","bytes":len(raw),
                        "sha256":hashlib.sha256(raw).hexdigest(),**meta,**analyze(raw)})
            fname=f"playdead-2018-html-{i:02d}.bin"
            (output.parent/fname).write_bytes(raw);row["artifact"]=fname
        except Exception as e:
            row.update({"result":"unavailable_or_provider_error",
                        "exception":type(e).__name__,"detail":str(e)[:190]})
        rows.append(row)
        print("HTML_ARCHIVE",item["label"],item["requested_capture"],row["result"],
              row.get("bytes",0),row.get("mce_email_mentions",0),
              row.get("printCheck_invocations",0),flush=True)
        time.sleep(.6)
    output.write_text(json.dumps({"mode":"original-page archive only",
        "source_fixture":"Experiment 483 original recovered JavaScript",
        "request_count":len(rows),"no_original_web_requests":True,"results":rows},indent=2)+"\n")
if __name__=="__main__":main()
