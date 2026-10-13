#!/usr/bin/env python3
"""Offline, SHA-256-bound metadata inventory of a local INSIDE installation.

No game content, strings, or proprietary code are exported; no network access.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct

CANDIDATES = {
    "assembly-csharp.dll": "gameplay-managed-candidate",
    "assembly-csharp-firstpass.dll": "managed-candidate",
    "gameassembly.dll": "il2cpp-native-candidate",
    "global-metadata.dat": "il2cpp-metadata-candidate",
    "inside.exe": "game-player-candidate",
    "unityplayer.dll": "unity-runtime-candidate",
    "mono.dll": "mono-runtime-candidate",
    "mono-2.0-bdwgc.dll": "mono-runtime-candidate",
}
MAX_CANDIDATES = 512


def identify(first: bytes) -> str:
    if first.startswith(b"MZ"):
        if len(first) < 0x40:
            return "truncated-pe"
        peoff = struct.unpack_from("<I", first, 0x3c)[0]
        if peoff + 0x1a > len(first) or first[peoff:peoff + 4] != b"PE\0\0":
            return "pe-unverified-header"
        optional_off = peoff + 0x18
        magic = struct.unpack_from("<H", first, optional_off)[0]
        if magic not in (0x10b, 0x20b):
            return "pe-unrecognized-optional-header"
        offset = 96 if magic == 0x10b else 112
        clr_dir = optional_off + offset + 14 * 8
        if clr_dir + 8 > len(first):
            return "pe-incomplete-clr-directory"
        va, length = struct.unpack_from("<II", first, clr_dir)
        return "pe-cli-managed" if va and length else "pe-native-or-unmarked"
    if first.startswith(b"\x7fELF"):
        return "elf-native"
    if first[:4] in (b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf", b"\xca\xfe\xba\xbe",
                      b"\xfe\xed\xfa\xce", b"\xce\xfa\xed\xfe"):
        return "mach-o-or-fat"
    if first.startswith(b"UnityFS"):
        return "unityfs-asset"
    if first.startswith(b"BSJB"):
        return "cli-metadata"
    return "unidentified-by-header"


def hash_and_head(path: Path) -> tuple[str, bytes, int]:
    dig = hashlib.sha256()
    size = 0
    head = bytearray()
    with path.open("rb") as f:
        while data := f.read(1024 * 1024):
            dig.update(data)
            size += len(data)
            if len(head) < 8192:
                head.extend(data[:8192 - len(head)])
    return dig.hexdigest(), bytes(head), size


def inspect(root: Path) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Supply a directory, not a URL or executable file")
    paths = []
    for parent, subdirs, filenames in os.walk(root, followlinks=False):
        subdirs[:] = sorted(name for name in subdirs
                            if not (Path(parent) / name).is_symlink())
        for name in sorted(filenames):
            if name.lower() not in CANDIDATES:
                continue
            path = Path(parent) / name
            if path.is_symlink() or not path.is_file():
                continue
            paths.append(path)
            if len(paths) > MAX_CANDIDATES:
                raise ValueError("Too many target files; narrow the supplied root")
    entries = []
    for p in paths:
        sha, head, size = hash_and_head(p)
        entries.append({
            "relative_path": p.relative_to(root).as_posix(),
            "role": CANDIDATES[p.name.lower()],
            "size_bytes": size,
            "sha256": sha,
            "header_kind": identify(head),
        })
    managed = [e for e in entries if e["role"] == "gameplay-managed-candidate"
               and e["header_kind"] == "pe-cli-managed"]
    native = [e for e in entries if e["role"] == "il2cpp-native-candidate"
              and e["header_kind"] == "pe-native-or-unmarked"]
    metadata = [e for e in entries if e["role"] == "il2cpp-metadata-candidate"]
    if managed:
        decision = "managed-gameplay-present; ILSpy is first-pass tool"
    elif native and metadata:
        decision = "IL2CPP-like pair present; Ghidra and metadata tooling possible"
    else:
        decision = "no verified gameplay analysis target; obtain local retail files"
    return {
        "schema": "inside-consumer-binary-intake-v1",
        "input_mode": "user-supplied local directory; offline",
        "data_exported": "relative paths, lengths, digests and signature categories only",
        "consumer_validated": False,
        "sticker_decoder_identified": False,
        "files": entries,
        "route": decision,
        "limitation": "Signatures and hashes alone prove neither version nor CE functionality.",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    report = inspect(a.root)
    content = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
