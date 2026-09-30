#!/usr/bin/env python3
"""Synchronize a canonical physical-sticker image archive from the community corpus.

Only serials explicitly present in stickers.md are eligible. Root-level
images/stickers/<serial>.* files are preserved as community-accepted source
evidence. images/stickers/edited/<serial>.* files are preserved separately as
derived/reference material and never counted as independent photographs.

The output manifest is the authority future analysis should consume.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

ROW_RE = re.compile(
    r"^- \[(?P<serial>\d{3})\].*?\(symb:\s*(?P<symbol>[^ ]+)\s+img:\s*(?:\[[A-I]\]\([^)]*\)|(?P<tile>[A-I]))",
    re.M,
)
SERIAL_RE = re.compile(r"^(\d{3})(?:[-_.].*)?$")
IMAGE_EXTS={".jpg",".jpeg",".png",".webp",".gif",".tif",".tiff"}

def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()

def parse_ledger(text: str) -> dict[int,dict]:
    rows={}
    for line in text.splitlines():
        m=re.match(r"^- \[(\d{3})\].*?\(symb:\s*([^ ]+)\s+img:\s*(?:\[([A-I])\]\([^)]*\)|([A-I]))", line)
        if not m:
            continue
        serial=int(m.group(1))
        rows[serial]={
            "serial": serial,
            "symbol": m.group(2),
            "tile": m.group(3) or m.group(4),
            "ledger_line": line,
        }
    return rows

def image_info(path: Path) -> tuple[int|None,int|None,str]:
    if Image is None:
        return None,None,""
    try:
        with Image.open(path) as im:
            return im.width, im.height, im.format or ""
    except Exception as exc:
        return None,None,f"decode-error:{type(exc).__name__}"

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--community-repo",type=Path,required=True)
    ap.add_argument("--dest",type=Path,default=Path("archive/stickers"))
    args=ap.parse_args()

    ledger_path=args.community_repo/"stickers.md"
    source_root=args.community_repo/"images"/"stickers"
    ledger=parse_ledger(ledger_path.read_text(encoding="utf-8",errors="replace"))
    if not ledger:
        raise SystemExit("no numbered sticker rows parsed from community ledger")

    originals=args.dest/"originals"
    derived=args.dest/"derived"/"community-edited"
    if originals.exists(): shutil.rmtree(originals)
    if derived.exists(): shutil.rmtree(derived)
    originals.mkdir(parents=True,exist_ok=True)
    derived.mkdir(parents=True,exist_ok=True)

    records=[]
    seen_files=set()
    for path in sorted(source_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
            continue
        m=SERIAL_RE.match(path.stem)
        if not m:
            continue
        serial=int(m.group(1))
        if serial not in ledger:
            continue
        rel=path.relative_to(source_root)
        is_edited="edited" in rel.parts
        category="derived-community-edit" if is_edited else "community-original"
        outbase=derived if is_edited else originals/ f"{serial:03d}"
        outbase.mkdir(parents=True,exist_ok=True)
        # Preserve source filename; add a stable prefix only if a collision occurs.
        dest=outbase/path.name
        if dest.exists() and digest(dest)!=digest(path):
            dest=outbase/f"community-{path.name}"
        shutil.copy2(path,dest)
        sha=digest(dest)
        if (category,sha) in seen_files:
            dest.unlink()
            continue
        seen_files.add((category,sha))
        w,h,fmt=image_info(dest)
        row=ledger[serial]
        records.append({
            "serial":f"{serial:03d}",
            "tile":row["tile"],
            "symbol":row["symbol"],
            "category":category,
            "canonical_input":"yes" if category=="community-original" else "no",
            "path":str(dest.as_posix()),
            "source_repo":"gamesbyian/INSIDE-ARG",
            "source_ref":"master",
            "source_path":str(path.relative_to(args.community_repo).as_posix()),
            "sha256":sha,
            "width":w or "",
            "height":h or "",
            "format":fmt,
            "notes":"",
        })

    represented={int(r["serial"]) for r in records if r["category"]=="community-original"}
    missing=sorted(set(ledger)-represented)

    args.dest.mkdir(parents=True,exist_ok=True)
    fields=["serial","tile","symbol","category","canonical_input","path","source_repo","source_ref","source_path","sha256","width","height","format","notes"]
    with (args.dest/"manifest.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(records)

    summary={
        "schema_version":1,
        "ledger_repo":"gamesbyian/INSIDE-ARG",
        "ledger_ref":"master",
        "ledger_serial_count":len(ledger),
        "community_original_files":sum(r["category"]=="community-original" for r in records),
        "community_edited_files":sum(r["category"]=="derived-community-edit" for r in records),
        "serials_with_original":len(represented),
        "serials_missing_original":missing,
        "rule":"Only manifest rows with canonical_input=yes are physical-photo inputs. Derived edits are reference-only.",
    }
    (args.dest/"inventory.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")

    readme=f"""# Canonical sticker image archive

This directory is the repository boundary for physical INSIDE Collector's Edition sticker imagery.

## Authority

The seed corpus is the community-maintained `gamesbyian/INSIDE-ARG` fork. Its `stickers.md` ledger determines which three-digit identifiers are established physical stickers. Files are never admitted merely because a filename happens to contain three digits.

- `originals/<serial>/`: community-accepted source photographs. These are valid independent image-analysis inputs.
- `derived/community-edited/`: historical community edits/crops/enhancements. These are useful references but are **not** independent observations.
- `manifest.csv`: canonical machine-readable inventory and provenance.
- `inventory.json`: coverage summary.

Future independently recovered photographs should be added as new manifest rows only after their physical serial association is verified. Byte-identical mirrors should add provenance, not duplicate observational weight.

Current seed coverage: **{len(represented)} / {len(ledger)} ledger serials** with at least one community original; **{sum(r["category"]=="community-original" for r in records)} original files** and **{sum(r["category"]=="derived-community-edit" for r in records)} community-derived files**.

Future analysis must read `manifest.csv`. Recursive filename guessing is prohibited.
"""
    (args.dest/"README.md").write_text(readme,encoding="utf-8")
    print(json.dumps(summary,indent=2))
    if missing:
        print("WARNING: ledger serials without root community original:",",".join(f"{x:03d}" for x in missing))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
