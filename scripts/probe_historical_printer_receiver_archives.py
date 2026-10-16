#!/usr/bin/env python3
"""Bounded, archival-service-only provenance search for two original ARG web files.

NEVER contacts playdead.com or terminal41.link directly. Network probes require
--execute; all service failures are censored rather than "page did not exist".
A one-shot GitHub Action is used because the interactive research container
cannot reach external archival service APIs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "search-output/historical-receiver-archive-2026-10-16.json"
ORIGINALS = {
    "PDJS2018": "http://www.playdead.com/js/dist.js",
    "T41HOP2019": "http://terminal41.link/sys/activate_shutdown_protocol/commit/___________DONE_SD.html",
}
CLEAN_HOSTS = {"archive.org", "web.archive.org", "arquivo.pt",
               "www.arquivo.pt", "index.commoncrawl.org", "data.commoncrawl.org"}
COMMON_CRAWL_INDEXES = ("CC-MAIN-2018-26", "CC-MAIN-2019-47", "CC-MAIN-2020-24")
RANGE_START, RANGE_END = 2016, 2021
MAX_BODY = 1_500_000
UA = "GRA-EDISNI ARG source archaeology/1.0 (small archival-only metadata probe)"
BLOCKS = {401, 403, 429, 503}


class ArchiveOnlyRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        assert_archive_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def assert_archive_url(url: str):
    u = urllib.parse.urlsplit(url)
    if u.scheme != "https" or u.hostname not in CLEAN_HOSTS:
        raise ValueError(f"non-archival or non-HTTPS request blocked: {url[:160]}")
    if u.username or u.password:
        raise ValueError("credential URL prohibited")


def planned() -> list[dict]:
    items = []
    for label, original in ORIGINALS.items():
        # All original URLs are passed only as parameters of archive URLs.
        encoded = urllib.parse.urlencode({"url": original})
        items.append({"label": label, "provider": "wayback_available",
                      "url": "https://archive.org/wayback/available?" + encoded
                             + "&timestamp=2019"})
        items.append({"label": label, "provider": "wayback_cdx",
                      "url": "https://web.archive.org/cdx/search/cdx?"
                             + urllib.parse.urlencode({
                                 "url": original, "output": "json",
                                 "from": str(RANGE_START), "to": str(RANGE_END),
                                 "fl": "timestamp,original,statuscode,mimetype,digest,length",
                                 "limit": "24",
                             })})
        items.append({"label": label, "provider": "arquivo_history",
                      "url": "https://arquivo.pt/textsearch?"
                             + urllib.parse.urlencode({
                                 "versionHistory": original, "maxItems": "10",
                             })})
        for index in COMMON_CRAWL_INDEXES:
            items.append({
                "label": label, "provider": "common_crawl",
                "index": index,
                "url": "https://index.commoncrawl.org/" + index
                       + "-index?" + urllib.parse.urlencode({
                           "url": original, "output": "json", "filter": "status:200",
                       }),
            })
    assert len(items) == 12
    for item in items:
        assert_archive_url(item["url"])
    return items


def extract_captures(task: dict, raw: bytes) -> list[dict]:
    txt = raw.decode("utf-8", errors="replace").strip()
    if not txt:
        return []
    provider = task["provider"]
    if provider == "wayback_cdx":
        rows = json.loads(txt)
        if not isinstance(rows, list) or not rows:
            return []
        head = rows[0]
        need = {"timestamp", "original", "statuscode"}
        if not isinstance(head, list) or not need.issubset(head):
            raise ValueError("unexpected Wayback CDX headers")
        return [dict(zip(head, row)) for row in rows[1:] if len(row) == len(head)]
    if provider == "wayback_available":
        item = json.loads(txt)
        snap = item.get("archived_snapshots", {}).get("closest")
        return [snap] if snap and isinstance(snap, dict) else []
    if provider == "arquivo_history":
        item = json.loads(txt)
        if isinstance(item, list):
            return item[:24]
        if isinstance(item, dict):
            for key in ("response_items", "items", "results"):
                if isinstance(item.get(key), list):
                    return item[key][:24]
            return [] if "error" not in item else [item]
        raise ValueError("unexpected Arquivo response")
    if provider == "common_crawl":
        out = []
        for line in txt.splitlines()[:24]:
            item = json.loads(line)
            if not isinstance(item, dict):
                raise ValueError("unexpected CC response")
            out.append({k: item.get(k) for k in ("url", "timestamp", "status",
                         "mime", "filename", "offset", "length", "digest")})
        return out
    raise ValueError("unrecognized archival service")


def detect_replay(candidate: dict) -> tuple[str, str] | None:
    """Only source-identified archived replay, never a generated live URL."""
    if "url" in candidate:
        url = candidate["url"]
        if isinstance(url, str):
            host = urllib.parse.urlsplit(url).hostname
            if host in {"web.archive.org", "arquivo.pt", "www.arquivo.pt"}:
                return url.replace("http://", "https://", 1), "wayback_or_arquivo_replay"
    if candidate.get("linkToArchive"):
        u = candidate["linkToArchive"]
        if isinstance(u, str) and urllib.parse.urlsplit(u).hostname in {
                "arquivo.pt", "www.arquivo.pt"}:
            return u.replace("http://", "https://", 1), "arquivo_replay"
    if re.fullmatch(r"\d{14}", str(candidate.get("timestamp", ""))) \
            and candidate.get("original", "").startswith(("http://", "https://")):
        ts, original = candidate["timestamp"], candidate["original"]
        return f"https://web.archive.org/web/{ts}id_/{original}", "wayback_exact_replay"
    return None


def safe_archived_request(url: str, max_bytes: int = MAX_BODY):
    assert_archive_url(url)
    opener = urllib.request.build_opener(ArchiveOnlyRedirects())
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "*/*",
    })
    with opener.open(req, timeout=12) as response:
        final = response.geturl()
        assert_archive_url(final)
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError("oversize archive response")
        return {"status": response.status, "url": final,
                "content_type": response.headers.get("Content-Type", "")}, data


def probe(tasks: list[dict], outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    disabled = {}
    results = []
    captured_paths = {}
    for task in tasks:
        provider = task["provider"]
        rec = dict(task)
        if provider in disabled:
            rec.update({"status": "provider_censored_after_block",
                        "reason": disabled[provider]})
            results.append(rec)
            continue
        print("PROBE", rec["label"], provider, rec.get("index", ""), flush=True)
        try:
            meta, raw = safe_archived_request(task["url"], 500_000)
            rec.update({"status": "metadata_received", "http_status": meta["status"],
                        "response_sha256": hashlib.sha256(raw).hexdigest(),
                        "response_bytes": len(raw), "content_type": meta["content_type"],
                        "captures": extract_captures(task, raw)})
            if rec["captures"]:
                print("CAPTURE_INDEX", rec["label"], provider,
                      len(rec["captures"]), flush=True)
            else:
                print("NO_INDEX_HIT", rec["label"], provider, flush=True)
            # The archive API response is preserved, including explicit empty
            # results, for auditing parser/provider failures independently.
            metadata_path = outdir / f'{rec["label"]}-{provider}-{rec.get("index", "default")}.body'
            metadata_path.write_bytes(raw)
        except urllib.error.HTTPError as e:
            rec.update({"status": "http_error", "http_status": e.code,
                        "error": str(e)[:240]})
            if e.code in BLOCKS:
                disabled[provider] = f"HTTP_{e.code}"
        except Exception as e:
            rec.update({"status": "provider_error", "error_type": type(e).__name__,
                        "error": str(e)[:240]})
            if isinstance(e, (TimeoutError, urllib.error.URLError)):
                disabled[provider] = type(e).__name__
        results.append(rec)
        time.sleep(0.5)
    # Safely retrieve at most two independently listed replay candidates,
    # only from Wayback or Arquivo. Never request original hosts.
    for label in ORIGINALS:
        candidates = []
        for r in results:
            if r["label"] == label and r.get("status") == "metadata_received":
                for entry in r.get("captures", []):
                    replay = detect_replay(entry)
                    if replay:
                        candidates.append(replay)
        seen = set()
        for url, provenance in candidates:
            if url in seen:
                continue
            seen.add(url)
            if len(captured_paths.get(label, [])) >= 2:
                break
            cap = {"label": label, "archive_url": url, "provenance": provenance}
            try:
                meta, raw = safe_archived_request(url)
                cap.update({"status": "archive_payload_retrieved",
                            "http_status": meta["status"], "bytes": len(raw),
                            "sha256": hashlib.sha256(raw).hexdigest(),
                            "mime": meta["content_type"]})
                name = f"{label}-{len(captured_paths.get(label, []))}.archive-replay.bin"
                (outdir / name).write_bytes(raw)
                cap["artifact_name"] = name
                captured_paths.setdefault(label, []).append(cap)
            except Exception as e:
                cap.update({"status": "replay_failed",
                            "error": str(e)[:240]})
                captured_paths.setdefault(label, []).append(cap)
            print("REPLAY", label, cap["status"], flush=True)
    return {
        "schema_version": 1,
        "scope": "historical-source retrieval; NOT sticker/owner search",
        "guard": "Archive provider hosts only, no original website HTTP requests",
        "success_not_guaranteed": True,
        "archive_negative_is_not_absence": True,
        "targets": ORIGINALS, "probe_results": results,
        "replays": captured_paths, "provider_blocks": disabled,
    }


def self_test():
    jobs = planned()
    assert len(jobs) == 12 and len({(x["label"], x["provider"], x.get("index"))
                                    for x in jobs}) == 12
    for url in ("https://www.playdead.com/js/dist.js",
                "http://web.archive.org/",
                "https://example.com/a",
                "https://terminal41.link/"):
        try:
            assert_archive_url(url)
        except ValueError:
            pass
        else:
            raise AssertionError(f"live URL guard failed: {url}")
    assert len(extract_captures({"provider": "wayback_cdx"},
                                b'[["timestamp","original","statuscode"],'
                                b'["20180604000000","http://example.org","200"]]')) == 1
    assert not extract_captures({"provider": "wayback_available"},
                                b'{"archived_snapshots":{}}')
    assert detect_replay({"url": "http://web.archive.org/web/20180701000000/http://abc/"})
    assert not detect_replay({"url": "https://www.playdead.com/js/dist.js"})


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--execute", action="store_true")
    p.add_argument("--out", type=Path, default=DEFAULT)
    a = p.parse_args()
    self_test()
    jobs = planned()
    if a.execute:
        results = probe(jobs, a.out.parent / "originals")
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        print("ARCHIVE_PROBE_SUMMARY", json.dumps({
            "metadata_hits": sum(len(x.get("captures", [])) for x in results["probe_results"]),
            "providers_blocked": results["provider_blocks"],
            "replays": {k: [z["status"] for z in v] for k, v in results["replays"].items()},
        }), flush=True)
    else:
        print("DRY_RUN_NO_REQUESTS", json.dumps({
            "tasks": jobs,
            "scope": "archives only, original website never directly queried",
        }, indent=2))


if __name__ == "__main__":
    main()
