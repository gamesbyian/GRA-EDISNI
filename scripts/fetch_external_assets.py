#!/usr/bin/env python3
"""Fetch external binary assets declared in data/canonical-binary-asset-manifest.json.

Downloads raw GitHub assets, verifies their exact Git blob SHA-1, and writes a
machine-readable fetch report. Standard-library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/canonical-binary-asset-manifest.json")
    parser.add_argument("--output", default="external-assets")
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--max-bytes", type=int, default=0, help="0 means unlimited")
    parser.add_argument("--limit", type=int, default=0, help="0 means unlimited")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    categories = set(args.category)

    selected = []
    for asset in manifest["assets"]:
        if categories and asset["category"] not in categories:
            continue
        if args.max_bytes and asset["size_bytes"] > args.max_bytes:
            continue
        selected.append(asset)
        if args.limit and len(selected) >= args.limit:
            break

    report = {
        "manifest": args.manifest,
        "selected": len(selected),
        "downloaded": 0,
        "verified": 0,
        "failed": [],
        "files": [],
    }

    for i, asset in enumerate(selected, start=1):
        rel = Path(asset["path"])
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"[{i}/{len(selected)}] {asset['path']}")
        try:
            req = Request(asset["raw_url"], headers={"User-Agent": "GRA-EDISNI-asset-fetcher/1"})
            with urlopen(req, timeout=120) as resp:
                data = resp.read()
            report["downloaded"] += 1

            actual = git_blob_sha(data)
            expected = asset["blob_sha"]
            if actual != expected:
                raise ValueError(f"Git blob SHA mismatch: expected {expected}, got {actual}")

            if len(data) != asset["size_bytes"]:
                raise ValueError(
                    f"Size mismatch: expected {asset['size_bytes']}, got {len(data)}"
                )

            dest.write_bytes(data)
            report["verified"] += 1
            report["files"].append({
                "path": asset["path"],
                "bytes": len(data),
                "blob_sha": actual,
                "output": str(dest),
            })
        except Exception as exc:
            report["failed"].append({"path": asset["path"], "error": str(exc)})

    report_path = output / "fetch-report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "selected": report["selected"],
        "downloaded": report["downloaded"],
        "verified": report["verified"],
        "failed": len(report["failed"]),
        "report": str(report_path),
    }, indent=2))

    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
