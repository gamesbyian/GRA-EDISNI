#!/usr/bin/env python3
"""Verify SHA-256 / sizes for the 2026-10-08 INSIDE cover derivative archive.

Source manifest uses relative path names under the conversation recovery root.
The ZIP contains a subset of cover_artifact/ files; verify those members too.
"""
import argparse
import hashlib
import zipfile
from pathlib import Path


def checksum(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(root: Path, manifest: Path, allow_missing=False):
    rows = manifest.read_text(encoding="utf-8").splitlines()
    assert rows[0] == "relative_local_path|size_bytes|sha256", rows[0]
    entries = {}
    for row in rows[1:]:
        path, size, digest = row.split("|")
        assert path not in entries and len(digest) == 64, path
        entries[path] = (int(size), digest)
    found = missing = 0
    for path, (size, digest) in entries.items():
        p = root / path
        if not p.exists():
            if not allow_missing:
                raise FileNotFoundError(str(p))
            missing += 1
            continue
        data = p.read_bytes()
        assert len(data) == size, (path, "size", len(data), size)
        assert checksum(data) == digest, (path, "SHA-256")
        found += 1
    archive = root / "inside-cover-source-audit.zip"
    zip_verified = 0
    if archive.is_file():
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            assert len(names) == len(set(names)), "duplicate ZIP member"
            for name in names:
                assert "cover_artifact/" + name in entries, name
                size, digest = entries["cover_artifact/" + name]
                data = z.read(name)
                assert len(data) == size and checksum(data) == digest, name
                zip_verified += 1
    elif not allow_missing:
        raise FileNotFoundError(str(archive))
    print(f"PASS: {found} files verified, {missing} missing, {zip_verified} ZIP members verified")
    return found, missing, zip_verified


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--allow-missing", action="store_true")
    a = p.parse_args()
    run(a.root, a.manifest, a.allow_missing)


if __name__ == "__main__":
    main()
