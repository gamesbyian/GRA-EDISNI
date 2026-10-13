#!/usr/bin/env python3
"""Plan or run a tiny, polite Wayback CDX *metadata-only* INSIDE forum audit.

This does not retrieve full archived pages or search their text. No requests
happen without --execute. Only the hardcoded Wayback CDX host is contacted.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
FORUMS = ROOT / "data/reference/global-gaming-forum-archive-routes.tsv"
CONTROLS = ROOT / "data/reference/inside-ce-archive-positive-controls.tsv"
CDX = "https://web.archive.org/cdx/search/cdx"
HEADERS = ("timestamp", "original", "statuscode", "mimetype", "digest")

def load_rows(path: Path, inventory: str) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    if inventory == "controls":
        return [
            {"label": r["id"], "url": r["original_url"],
             "evidence": r["evidence_type"], "window": r["post_period"]}
            for r in rows
        ]
    indexed = [
        {"label": r["community"], "url": r["original_url"],
         "evidence": r["source_assurance"], "window": "2016-2026",
         "access": r["handling"], "priority": r["priority"]}
        for r in rows
    ]
    # The 483-row inventory is geographical. For a small archive pilot,
    # prioritize actual documentary rescue/archive leads rather than the
    # earliest English sites in original directory order.
    ranks = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    return sorted(indexed, key=lambda r: (
        ranks.get(r["priority"], 9),
        0 if "INSIDE" in r["label"] else 1,
        r["label"]
    ))

def generate(rows: list[dict], *, per_window_limit: int, max_sources: int) -> list[dict]:
    if not 1 <= per_window_limit <= 100:
        raise ValueError("Per-window metadata sample must be 1..100")
    if not 1 <= max_sources <= 50:
        raise ValueError("Maximum source budget must be 1..50")
    selected = rows[:max_sources]
    tasks = []
    for row in selected:
        url = row["url"]
        u = urllib.parse.urlsplit(url)
        if u.scheme not in ("https", "http") or not u.hostname:
            raise ValueError("Expected an original public HTTP(S) URL")
        if row.get("access", "") == "reddit_platform_rights_and_removed_content_policy":
            # Skip platform bulk archives while the access/retention terms
            # are not individually reviewed; case-specific controls still
            # need permission review before execution.
            continue
        for start, end in ((2016, 2020), (2021, 2026)):
            params = {
                "url": url,
                "output": "json",
                "filter": "statuscode:200",
                "from": str(start),
                "to": str(end),
                "fl": ",".join(HEADERS),
                "limit": str(per_window_limit),
            }
            tasks.append({
                "label": row["label"], "source_url": url,
                "window": f"{start}-{end}",
                "evidence": row["evidence"],
                "cdx_url": CDX + "?" + urllib.parse.urlencode(params),
                "status": "planned_unexecuted",
            })
    return tasks

def parse_cdx(data: bytes) -> list[dict]:
    obj = json.loads(data.decode("utf-8"))
    if not isinstance(obj, list):
        raise ValueError("CDX returned an unexpected JSON structure")
    if not obj:
        return []
    header = obj[0]
    if not isinstance(header, list) or not set(HEADERS).issubset(header):
        raise ValueError("CDX metadata header missing expected fields")
    parsed = []
    for r in obj[1:]:
        if not isinstance(r, list) or len(r) != len(header):
            raise ValueError("Malformed CDX record")
        d = dict(zip(header, r))
        parsed.append({field: d[field] for field in HEADERS})
    return parsed

def run(tasks: list[dict], *, delay_seconds: float,
        transport=None) -> list[dict]:
    if delay_seconds < 2.0:
        raise ValueError("Archive request separation must be >= 2 seconds")
    if transport is None:
        transport = urllib.request.urlopen
    out = []
    for idx, task in enumerate(tasks):
        if idx:
            time.sleep(delay_seconds)
        rec = dict(task)
        rec["status"] = "request_started"
        try:
            req = urllib.request.Request(
                task["cdx_url"],
                headers={"Accept": "application/json",
                         "User-Agent": "GRA-EDISNI-research/1.0 public archive metadata"},
            )
            with transport(req, timeout=25) as response:
                raw = response.read(1_500_000)
            captures = parse_cdx(raw)
            rec["status"] = "metadata_sample_received"
            rec["sampled_captures"] = len(captures)
            rec["captures"] = captures
            rec["coverage"] = "bounded_cdx_metadata_sample_not_historical_fulltext"
        except urllib.error.HTTPError as exc:
            rec["status"] = "http_error"
            rec["http_status"] = exc.code
            out.append(rec)
            if exc.code in (401, 403, 429, 503):
                break
            continue
        except (OSError, ValueError, TimeoutError, json.JSONDecodeError) as exc:
            rec["status"] = "request_error"
            rec["error_type"] = type(exc).__name__
            out.append(rec)
            continue
        out.append(rec)
    return out

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory", choices=("controls", "forums"),
                    default="controls")
    ap.add_argument("--execute", action="store_true",
                    help="Explicitly query the Internet Archive CDX API")
    ap.add_argument("--max-sources", type=int, default=6)
    ap.add_argument("--per-window-limit", type=int, default=12)
    ap.add_argument("--delay-seconds", type=float, default=2.0)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    rows = load_rows(CONTROLS if args.inventory == "controls" else FORUMS, args.inventory)
    tasks = generate(rows, per_window_limit=args.per_window_limit,
                     max_sources=args.max_sources)
    if args.execute:
        tasks = run(tasks, delay_seconds=args.delay_seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as fh:
        for r in tasks:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps({
        "inventory": args.inventory, "sources_selected": args.max_sources,
        "tasks_written": len(tasks), "network_requests": len(tasks) if args.execute else 0,
        "execute": args.execute, "output": str(args.output),
        "scope": "archive_capture_metadata_only_not_full_post_search",
    }))

if __name__ == "__main__":
    main()
