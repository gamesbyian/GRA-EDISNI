#!/usr/bin/env python3
"""Offline inspection of locally decompiled C# candidate consumer entrypoints.

Outputs source-file digests, paths, line numbers and pre-frozen search terms.
No decompiled source content is exported; hits are NOT verified validators.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re

TERMS = {
    "printer_research": ("PrintingPaperEasterEgg", "SecretType", "morseConvert"),
    "known_game_interactions": ("SecretBunker", "CodeSequence", "Lever", "SecretEnding"),
    "candidate_validation": ("ValidateCode", "CheckCode", "InputSequence", "Password"),
    "state_handoff": ("GetControllerReward", "controllerInput", "unreadMessages"),
}
TOTAL_CAP = 10_000


def scan(root: Path) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Expected local directory of decompiled C# files")
    records = []
    inspected = 0
    totals = {k: 0 for k in TERMS}
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(parent) / d).is_symlink())
        for filename in sorted(files):
            if not filename.lower().endswith(".cs"):
                continue
            f = Path(parent) / filename
            if f.is_symlink() or not f.is_file():
                continue
            inspected += 1
            if inspected > TOTAL_CAP:
                raise ValueError("C# file count exceeds cap; narrow root")
            data = f.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            try:
                source = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                continue
            hits = []
            for i, line in enumerate(source.splitlines(), 1):
                for group, keys in TERMS.items():
                    for key in keys:
                        if re.search(r"(?<![A-Za-z0-9_])" + re.escape(key) +
                                     r"(?![A-Za-z0-9_])", line, re.I):
                            hits.append({"line": i, "group": group, "term": key})
                            totals[group] += 1
            if hits:
                records.append({
                    "source_relative_path": f.relative_to(root).as_posix(),
                    "sha256": digest,
                    "hits": hits,
                })
    return {
        "schema": "inside-decompiled-consumer-hits-v1",
        "input": "user-supplied, locally decompiled C#; no source exported",
        "files_examined": inspected,
        "matched_files": len(records),
        "totals": totals,
        "matches": records,
        "validated_entrypoint": False,
        "limitation": "Keyword sightings are leads, not path or accepted-input verification.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    opts = parser.parse_args()
    result = json.dumps(scan(opts.source_dir), indent=2, sort_keys=True) + "\n"
    if opts.output:
        opts.output.parent.mkdir(parents=True, exist_ok=True)
        opts.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
