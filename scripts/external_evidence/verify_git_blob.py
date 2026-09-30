#!/usr/bin/env python3
"""Verify a file using Git blob SHA-1 semantics."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("expected")
    parser.add_argument("--size", type=int)
    args = parser.parse_args()

    data_size = args.path.stat().st_size
    actual = git_blob_sha1(args.path)
    if args.size is not None and data_size != args.size:
        raise SystemExit(
            f"size mismatch: expected {args.size}, got {data_size}: {args.path}"
        )
    if actual.lower() != args.expected.lower():
        raise SystemExit(
            f"Git blob SHA-1 mismatch: expected {args.expected}, got {actual}: {args.path}"
        )
    print(f"OK {args.path} size={data_size} git_blob_sha1={actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
