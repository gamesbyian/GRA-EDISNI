#!/usr/bin/env python3
"""Validate the CE decoder/recipient atlases and optionally export machine JSON.

Stdlib only; reads the two hand-curated Markdown catalogues without making up
cross-product links or treating each proposed method as independent evidence.

Usage:
    python scripts/check_decoder_receiver_atlas.py
    python scripts/check_decoder_receiver_atlas.py --json /tmp/sticker-readers.json
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CATALOGS = (
    ("receiver", DOCS / "receiving-surface-atlas-2026-10-12.md", "R", 82),
    ("decoder", DOCS / "decoder-operation-atlas-2026-10-12.md", "D", 162),
)
PROGRAM = DOCS / "closed-corpus-reader-bridge-program-2026-10-12.md"
ITEM = re.compile(r"^\| ([RD]\d{3}) \| (.+) \| (.+) \| (.+) \|\s*$")
SECTION = re.compile(r"^## ([RD]\d+)\. (.+)$")
LINK = re.compile(r"\]\(([^)#]+)(?:#[^)]*)?\)")
CAMPAIGN = re.compile(r"^\| \*\*B(\d{2}):")


def parse_catalog(kind: str, path: Path, prefix: str, expected: int) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    group = None
    rows = []
    for line in text.splitlines():
        header = SECTION.fullmatch(line)
        if header:
            group = header.group(2)
            assert header.group(1).startswith(prefix), line
            continue
        match = ITEM.fullmatch(line)
        if not match:
            if re.match(r"^\| [RD]\d{3} \|", line):
                raise ValueError("malformed catalogue row: " + line[:120])
            continue
        code, name, test, provenance = match.groups()
        assert code[0] == prefix and group is not None, (path, code)
        assert all(field.strip() for field in (name, test, provenance)), code
        rows.append({
            "id": code, "kind": kind, "family": group,
            "method": name.strip(), "source_and_test": test.strip(),
            "basis_and_priority": provenance.strip(),
            "source_file": path.relative_to(ROOT).as_posix(),
        })
    want = [f"{prefix}{i:03}" for i in range(1, expected + 1)]
    got = [r["id"] for r in rows]
    assert got == want, f"{path.name}: missing, duplicate or out-of-order IDs: {got}"
    assert len({r["method"] for r in rows}) == len(rows), f"repeated titles: {path}"
    return rows


def verify_links(path: Path):
    text = path.read_text(encoding="utf-8")
    for m in LINK.finditer(text):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        dest = (path.parent / target).resolve()
        assert dest.is_relative_to(ROOT), (path, target)
        assert dest.is_file(), f"broken relative link: {path.name} => {target}"


def audit() -> dict:
    rows = []
    for args in CATALOGS:
        rows.extend(parse_catalog(*args))
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)) == 244
    for _, path, _, _ in CATALOGS:
        verify_links(path)
    verify_links(PROGRAM)
    campaigns = [int(n) for n in CAMPAIGN.findall(PROGRAM.read_text(encoding="utf-8"))]
    assert campaigns == list(range(1, 21)), campaigns
    kinds = Counter(r["kind"] for r in rows)
    families = Counter(f'{r["kind"]}: {r["family"]}' for r in rows)
    return {
        "purpose": "catalogue navigation, NOT an independent evidence score",
        "physical_reference_snapshot": {"records": 84, "residues": 66, "unobserved": 42},
        "items": rows,
        "count": len(rows), "by_kind": dict(sorted(kinds.items())),
        "by_family": dict(sorted(families.items())),
        "source_first_campaign_count": len(campaigns),
        "program": PROGRAM.relative_to(ROOT).as_posix(),
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", type=Path, help="write machine-readable catalogue")
    args = p.parse_args()
    result = audit()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {result['count']} entries to {args.json}")
    else:
        print(json.dumps({k:v for k,v in result.items() if k!="items"}, indent=2))


if __name__ == "__main__":
    main()
