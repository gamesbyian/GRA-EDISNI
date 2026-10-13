#!/usr/bin/env python3
"""Offline structural triage of local ILSpy-decompiled C#.

Reports hashes, filenames, method spans and candidate features. No source
code, literals, passwords, or complete game files leave the local computer.
This is heuristic DISCOVER work; a hit is NEVER a proven code consumer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re

MAX_FILES = 10_000
MAX_BYTES = 15 * 1024 * 1024
SIGNAL = "printSecretMessage"
KNOWN = {"CheckPassword", "InputCheckAndStateTransition", "OnFastEventEx"}
BAD_DECL = {"if", "for", "foreach", "while", "switch", "catch",
            "using", "lock", "fixed", "return", "sizeof", "nameof", "typeof"}

# Retain exact offsets and newlines. Handle comments, escaped/quoted strings
# and verbatim strings. Modern C# raw strings are not completely parsed.
def mask(source: str, *, preserve_strings: bool = False) -> str:
    out = list(source)
    n, i = len(source), 0
    while i < n:
        if source.startswith("//", i) or source.startswith("/*", i):
            if source.startswith("//", i):
                end = source.find("\n", i)
                end = n if end == -1 else end
            else:
                end = source.find("*/", i+2)
                end = n if end == -1 else end+2
            for k in range(i, end):
                if out[k] != "\n": out[k] = " "
            i = end
            continue
        start, quote, verbatim = i, None, False
        if source.startswith(('$@"', '@$"'), i):
            quote, verbatim = '"', True
            i += 2
        elif source.startswith('@"', i):
            quote, verbatim = '"', True
            i += 1
        elif source.startswith('$"', i):
            quote = '"'
            i += 1
        elif source[i] in ('"', "'"):
            quote = source[i]
        if quote:
            i += 1
            while i < n:
                if verbatim and source[i:i+2] == quote*2:
                    i += 2
                elif source[i] == quote:
                    i += 1
                    break
                elif not verbatim and source[i] == "\\":
                    i += 2
                else:
                    i += 1
            if not preserve_strings:
                for k in range(start, min(n, i)):
                    if out[k] != "\n": out[k] = " "
            continue
        i += 1
    return "".join(out)

# Covers ordinary ILSpy method blocks, not expression-bodied methods, local
# functions with unusual signatures, lambdas or all generic constraints.
DECL = re.compile(
    r"(?m)^[ \t]*(?:(?:public|private|protected|internal|static|sealed|"
    r"override|virtual|unsafe|async|new|partial|extern)\s+)*"
    r"(?:(?:[\w<>\[\].,?]+)\s+)?(?P<name>[A-Za-z_]\w*)\s*"
    r"\([^{};]*\)\s*\{"
)

def method_ranges(code: str):
    result = []
    for m in DECL.finditer(code):
        name = m.group("name")
        if name in BAD_DECL: continue
        open_brace = m.end()-1
        depth, close = 0, None
        for i in range(open_brace, len(code)):
            if code[i] == "{": depth += 1
            elif code[i] == "}":
                depth -= 1
                if depth == 0:
                    close = i+1
                    break
        if close is not None:
            result.append((name, m.start(), open_brace, close))
    result.sort(key=lambda x: (x[1], -(x[3]-x[1])))
    filtered = []
    for candidate in result:
        if not any(candidate[1] >= prev[1] and candidate[3] <= prev[3]
                   for prev in filtered):
            filtered.append(candidate)
    return filtered

def method_features(name: str, source: str, code: str, lo: int, hi: int):
    body = code[lo:hi]
    literals = mask(source[lo:hi], preserve_strings=True)
    pattern = re.compile(r'(?<!\w)"' + re.escape(SIGNAL) + r'"')
    signal_seen = bool(pattern.search(literals))
    features = {
        "length_sensitive": bool(re.search(r"\.(?:Length|Count)\b", body)),
        "prefix_operation": bool(re.search(r"\b(?:Substring|StartsWith|Take)\s*\(", body)),
        "comparison": bool(re.search(r"==|!=|\b(?:Equals|SequenceEqual)\s*\(", body)),
        "reset": bool(re.search(r"\.Clear\s*\(|\bReset\w*\s*\(", body)
                      or re.search(r'\w+\s*=\s*(?:@|\$)?""', literals)),
        "accumulation": bool(re.search(r"\+=|\.(?:Add|Append)\s*\(", body)),
        "signal_api": bool(re.search(r"\b(?:SignalOut|SignalIn|GetOrCreate)\b|"
                                     r"\.(?:Signal|Subscribe|Register|AddListener)\b", body)),
    }
    keys = ("length_sensitive", "prefix_operation", "comparison",
            "reset", "accumulation")
    inferred = all(features[k] for k in keys)
    reasons = []
    if inferred: reasons.append("structural-prefix-validator-candidate")
    if signal_seen: reasons.append("reported-signal-literal")
    if name in KNOWN: reasons.append("historical-method-name")
    if not reasons: return None
    return {
        "method": name,
        "first_line": source.count("\n", 0, lo)+1,
        "last_line": source.count("\n", 0, hi)+1,
        "reasons": reasons,
        "features": features,
        "reported_signal_literal": signal_seen,
        "validated_consumer": False,
    }

def scan(root: Path):
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Supply the local decompiled C# directory")
    examined = skipped = 0
    matches = []
    signal_paths = []
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(parent)/d).is_symlink())
        for filename in sorted(files):
            file = Path(parent)/filename
            if file.suffix.lower() != ".cs" or file.is_symlink() or not file.is_file():
                continue
            examined += 1
            if examined > MAX_FILES: raise ValueError("C# file count cap exceeded")
            if file.stat().st_size > MAX_BYTES: raise ValueError("C# file size cap exceeded")
            original = file.read_bytes()
            try: source = original.decode("utf-8-sig")
            except UnicodeDecodeError:
                skipped += 1
                continue
            code = mask(source)
            hits = [
                hit for name, _start, lo, hi in method_ranges(code)
                if (hit := method_features(name, source, code, lo, hi)) is not None
            ]
            rel = file.relative_to(root).as_posix()
            if hits:
                matches.append({
                    "path": rel,
                    "sha256": hashlib.sha256(original).hexdigest(),
                    "methods": hits,
                })
                if len(matches) > 2000:
                    raise ValueError("Candidate file cap exceeded")
            if re.search(r'(?<!\w)"'+re.escape(SIGNAL)+r'"',
                         mask(source, preserve_strings=True)):
                signal_paths.append(rel)
    return {
        "schema": "inside-managed-consumer-structural-candidates-v1",
        "files_examined": examined,
        "undecodable_files": skipped,
        "matched_files": matches,
        "reported_signal_reference_paths": signal_paths,
        "game_consumer_verified": False,
        "note": "Synthetic tests certify detector only; game binaries not provided.",
        "limitations": [
            "Heuristic lexical pass, not a complete C# compiler or call graph",
            "Expression-bodied methods and some raw/interpolated strings may be missed",
            "A candidate match is not proof of reachable validation logic",
            "No signal reference does not prove absence across uninspected assemblies/scenes",
        ],
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    a = parser.parse_args()
    report = json.dumps(scan(a.source_dir), indent=2, sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")

if __name__ == "__main__":
    main()
