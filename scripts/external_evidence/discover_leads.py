#!/usr/bin/env python3
"""Extract URLs from acquired text/JSON/HTML and report untracked leads."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urldefrag


URL_RE = re.compile(r"https?://[^\s\"'<>\]\)]+", re.IGNORECASE)


def canonical(url: str) -> str:
    return urldefrag(url.rstrip(".,;:!?"))[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--manifest", type=Path, default=Path("data/external-acquisition-targets.json"))
    parser.add_argument("--output", type=Path, default=Path("evidence-work/untracked-leads.json"))
    args = parser.parse_args()

    tracked = {
        canonical(s["url"])
        for s in json.loads(args.manifest.read_text(encoding="utf-8"))["sources"]
    }

    found: dict[str, set[str]] = {}
    for root in args.roots:
        paths = [root] if root.is_file() else list(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.stat().st_size > 25 * 1024 * 1024:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for raw in URL_RE.findall(text):
                url = canonical(raw)
                if url not in tracked:
                    found.setdefault(url, set()).add(str(path))

    payload = {
        "schema_version": 1,
        "count": len(found),
        "leads": [
            {"url": url, "found_in": sorted(paths)}
            for url, paths in sorted(found.items())
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"{len(found)} untracked URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
