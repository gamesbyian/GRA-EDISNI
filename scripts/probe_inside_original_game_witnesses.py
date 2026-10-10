#!/usr/bin/env python3
"""Bounded, source-attributed recovery of the early INSIDE asset screenshots.

A success establishes surviving URL bytes, not a Unity-native source asset
or evidence for an INSIDE CE sticker interpretation. No search/URL guessing.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_MANIFEST = Path("data/original-game-2016-witness-targets.json")

def detect(data: bytes) -> str:
    if data.startswith(bytes.fromhex("89504e470d0a1a0a")): return "png"
    if data.startswith(bytes.fromhex("ffd8ff")): return "jpeg"
    if data.startswith(b"GIF8"): return "gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP": return "webp"
    if b"\0" not in data[:256] and (b"<html" in data[:512].lower() or
                                  b"<!doctype html" in data[:512].lower()):
        return "html"
    return "unrecognized"

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, hosts: set[str]):
        self.hosts = hosts
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = urllib.parse.urlsplit(newurl)
        if new.scheme != "https" or new.hostname not in self.hosts:
            raise ValueError("redirect_outside_allowlist")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def check_manifest(doc: dict) -> None:
    assert doc["schema_version"] == 1
    assert 0 < len(doc["targets"]) <= 20
    ids = set()
    for item in doc["targets"]:
        assert item["id"] not in ids and item["id"].replace("-","").replace("_","").isalnum()
        ids.add(item["id"])
        assert item["kind"] in ("image","html")
        assert item["source_date"] and item["source_reference"] and item["source_context"]
        url = urllib.parse.urlsplit(item["url"])
        assert url.scheme == "https" and url.hostname in doc["allowed_hosts"]
        assert len(item["url"]) < 1024

def probe(doc: dict, out: Path, timeout: float, max_bytes: int) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    files = out / "recovered"
    files.mkdir(exist_ok=True)
    opener = urllib.request.build_opener(SafeRedirect(set(doc["allowed_hosts"])))
    log = {"schema_version": 1,
           "notice": "Retrieval-time URL bytes, not game-native source by inference.",
           "targets": []}
    for item in doc["targets"]:
        row = {k: item[k] for k in
               ("id","url","kind","source_date","source_reference","source_context")}
        try:
            request = urllib.request.Request(
                item["url"],
                headers={"User-Agent": "INSIDE-ARG-historical-image-source-probe/1.0",
                         "Accept": "image/png,image/jpeg,image/webp,image/gif,text/html;q=0.8,*/*;q=0.1"})
            with opener.open(request, timeout=timeout) as response:
                declared = response.headers.get("Content-Length")
                if declared and int(declared) > max_bytes:
                    raise ValueError("declared_size_exceeds_budget")
                data = response.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise ValueError("download_exceeds_budget")
                typ = detect(data)
                row.update(status_code=response.status,final_url=response.url,
                           content_type=response.headers.get("Content-Type",""),
                           media_detected=typ, byte_count=len(data))
                allowed = {"png","jpeg","webp","gif"} if item["kind"] == "image" else {"html"}
                if typ not in allowed:
                    raise ValueError("unexpected_payload_" + typ)
                suffix = "jpg" if typ == "jpeg" else typ
                filename = item["id"] + "." + suffix
                (files / filename).write_bytes(data)
                row.update(
                    result=("recovered_image" if item["kind"] == "image" else
                            "html_capture_not_original_image"),
                    filename="recovered/" + filename,
                    sha256=hashlib.sha256(data).hexdigest())
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError,
                OSError, TimeoutError) as error:
            row.update(result="unavailable_or_rejected", error_type=type(error).__name__,
                       error=str(error)[:300])
        log["targets"].append(row)
    (out / "report.json").write_text(json.dumps(log,indent=2,ensure_ascii=False) + "\n")
    return log

def self_test() -> None:
    assert detect(bytes.fromhex("89504e470d0a1a0a") + b"x") == "png"
    assert detect(bytes.fromhex("ffd8ff") + b"\0") == "jpeg"
    assert detect(b"GIF89a" + b"\0") == "gif"
    assert detect(b"RIFF" + b"\0"*4 + b"WEBP") == "webp"
    assert detect(b"<!doctype html><html></html>") == "html"
    assert detect(b"Forbidden") == "unrecognized"
    doc={"schema_version":1,"allowed_hosts":["example.org"],"targets":[
        {"id":"fixture","url":"https://example.org/abc","kind":"image",
         "source_date":"2016-07-10","source_reference":"test","source_context":"test"}]}
    check_manifest(doc)
    try:
        check_manifest({**doc,"targets":[{**doc["targets"][0],
                                        "url":"http://example.org/abc"}]})
    except AssertionError:
        pass
    else:
        raise AssertionError("HTTP source not rejected")
    print("OK: format detection, refuse error page, URL allowlist")

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest",type=Path,default=DEFAULT_MANIFEST)
    p.add_argument("--output",type=Path,default=Path("original-2016-witnesses"))
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--timeout",type=float,default=12.0)
    p.add_argument("--max-bytes",type=int,default=6_000_000)
    args=p.parse_args()
    if args.self_test: return self_test()
    if not 1 <= args.timeout <= 30 or not 1024 <= args.max_bytes <= 10_000_000:
        p.error("probe budget exceeded")
    doc=json.loads(args.manifest.read_text())
    check_manifest(doc)
    log=probe(doc,args.output,args.timeout,args.max_bytes)
    count=sum(r["result"]=="recovered_image" for r in log["targets"])
    print(f"{count}/{len(log['targets'])} target original-URL images recovered")
    for r in log["targets"]:
        print(f"{r['id']}: {r['result']}: {r.get('sha256',r.get('error',''))}")

if __name__ == "__main__":
    main()
