#!/usr/bin/env python3
"""CL09: strictly read-only public archive discovery for historically screenshot-listed
Terminal41 URLs. No requests to current terminal41.link and no guessed login.
Failure does not imply historical nonexistence; no automatic link following to site.
"""
import argparse, concurrent.futures, json, time, urllib.parse, urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

ROUTES=[
"/sys/all_sys_hibernate/",
"/dat/saf_dat_col_BACKUP.html",
"/dat/breachlog_BACKUP.html",
"/dat/breach_contribution_reg_BACKUP.html",
"/sys/printreqstatus_SD_BACKUP.html",
"/sys/terminate_terminal/23/",
]
HOSTS=["http://terminal41.link","http://www.terminal41.link"]
SERVICES=[
"https://archive.org/wayback/available?url=",
"https://web.archive.org/cdx/search/cdx?output=json&filter=statuscode:200&url=",
]
def one(request):
    label,url=request
    started=time.time()
    rq=urllib.request.Request(url,headers={"User-Agent":"INSIDE-research/0.1 (public archival metadata only)"})
    try:
        with urllib.request.urlopen(rq,timeout=10) as resp:
            data=resp.read(10000)
            return {"target":label,"query_url":url,"status":resp.status,
                    "body_excerpt":data.decode("utf8",errors="replace")[:700],
                    "content_type":resp.headers.get("Content-Type"),
                    "elapsed_s":round(time.time()-started,2)}
    except Exception as ex:
        return {"target":label,"query_url":url,"error_type":type(ex).__name__,
                "error":str(ex)[:180],"elapsed_s":round(time.time()-started,2)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="cl09-wayback-route-results.json")
    args=ap.parse_args()
    tasks=[]
    for route in ROUTES:
        for service in SERVICES:
            url=service+urllib.parse.quote(HOSTS[0]+route,safe="")
            tasks.append((route,url))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        result=list(executor.map(one,tasks))
    d={"purpose":"metadata lookups of screenshot attested historic URLs, never the original site",
       "not_a_historical_nonexistence_test":True,"results":result}
    Path(args.output).write_text(json.dumps(d,indent=2)+"\n",encoding="utf8")
    for obj in result:
        print("CL09_ARCHIVE "+json.dumps({k:obj.get(k) for k in
          ["target","status","error_type","body_excerpt"]},ensure_ascii=False)[:700])

if __name__=="__main__":main()
