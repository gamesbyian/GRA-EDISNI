#!/usr/bin/env python3
"""Original Terminal41 marked-record/recovery page: source operation audit.

DISCOVER, not a CE erasure-code decoding. The original page uses actual labels
'Omit MARKED', '-o /MARKED', '-i /MARKED', 'err. corr.(1)' and 'DATA salvage'.
This program reports what *the preserved bytes* allow a reader to prove,
without importing any H108 sticker model or manufacturing parity checks.

Run: python scripts/audit_terminal41_marked_recovery.py
     python scripts/audit_terminal41_marked_recovery.py --output /tmp/marked.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = (
    "terminal41.link/dat/breach_contribution_reg.html"
)
SOURCE = ROOT / "archive/external/twinysam-inside-arg" / RELATIVE
MANIFEST = ROOT / "data/terminal41-source-tree.json"

HEX_ROW = re.compile(r"^([0-9A-F]{64})(.*)$")


def source_lines(content: str) -> list[str]:
    # HTML wrappers are the authored display carrier; inline terminal field
    # delimiters use [square brackets], which this conversion preserves.
    return [line.strip() for line in re.sub(r"<[^>]*>", "\n", content)
            .replace("\r\n", "\n").split("\n") if line.strip()]


def parse(content: str) -> tuple[list[dict], list[str]]:
    lines = source_lines(content)
    state = "pre_omit"
    rows = []
    for idx, text in enumerate(lines):
        if "[Omit][MARKED]" in text:
            state = "halt_echo"
        if "[Transmission reloaded]" in text:
            state = "post_reload"
        if "[Transmission commence" in text:
            state = "post_resume"
        m = HEX_ROW.fullmatch(text)
        if not m:
            continue
        digest, suffix = m.groups()
        assert suffix in ("", "[*]", "[alt]", "[alt][alt]", "[/]"), (
            idx, suffix
        )
        rows.append({
            "display_line_index_0_based": idx,
            "stage": state,
            "hex": digest,
            "suffix": suffix,
            "is_marked_star": suffix == "[*]",
            "is_alternate": "alt" in suffix,
        })
    return rows, lines


def nominal_remove_marked(rows: list[dict]) -> list[dict]:
    """Simple operation suggested by source text, NOT original server logic."""
    return [r for r in rows if not r["is_marked_star"]]


def hamming(a: str, b: str) -> int:
    assert re.fullmatch("[0-9A-F]{64}", a)
    assert re.fullmatch("[0-9A-F]{64}", b)
    return (int(a, 16) ^ int(b, 16)).bit_count()


def nearest_unique_distances(rows: list[dict]) -> dict:
    unique = sorted(set(r["hex"] for r in rows))
    assert len(unique) == 118
    nearest = {}
    for idx, a in enumerate(unique):
        nearest[a] = min(hamming(a, b) for j, b in enumerate(unique)
                         if idx != j)
    alternate = sorted(set(r["hex"] for r in rows if r["is_alternate"]))
    alt_nearest = sorted(nearest[x] for x in alternate)
    assert alt_nearest == [102, 104, 106, 106], alt_nearest
    assert min(nearest.values()) == 98
    return {
        "minimum_any_distinct_hex_record_bit_distance": min(nearest.values()),
        "minimum_distance_from_each_alt_hex_record_to_any_other": alt_nearest,
        "individual_hex_record_width_bits": 256,
        "very_local_edits_below_32_bits_found": sum(d < 32 for d in nearest.values()),
        "interpretation": (
            "There are no obviously one-bit or few-bit neighbour records among "
            "the displayed 256-bit values. This is NOT a collision/security "
            "analysis; even one-character changes in hashed originals could "
            "have avalanche distances."
        ),
    }


def audit() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["source_tree_sha"] == "4de72d7c2f21bd9eb4144fda51281c84cbcb90c4"
    entry = next(e for e in manifest["files"]
                 if e["path"] == RELATIVE)
    data = SOURCE.read_bytes()
    # Git blob fingerprint: sha1(b"blob " + ascii(byte size) + b"\0" + data).
    # The archived copy may have its own history; report *rather than assume*
    # equality to the upstream tree's frozen blob SHA.
    blob_sha = hashlib.sha1(
        b"blob " + str(len(data)).encode() + b"\0" + data
    ).hexdigest()
    text = data.decode("utf-8")
    rows, lines = parse(text)
    by_stage = {
        name: [r for r in rows if r["stage"] == name]
        for name in ("pre_omit", "halt_echo", "post_reload", "post_resume")
    }
    assert {stage:len(rs) for stage,rs in by_stage.items()} == {
        "pre_omit":68, "halt_echo":2, "post_reload":31, "post_resume":32,
    }
    unique = Counter(r["hex"] for r in rows)
    assert (len(rows),len(unique)) == (133,118)
    assert sum(n > 1 for n in unique.values()) == 12
    assert len(rows) - len(unique) == 15
    suffixes = dict(sorted(Counter(r["suffix"] for r in rows).items()))
    assert suffixes == {
        "":118,"[*]":10,"[/]":1,"[alt]":3,"[alt][alt]":1,
    }
    required_literals = [
        "[Omit][MARKED]",
        "[-o /MARKED][-o -m \"*\"]",
        "[Transmission reloaded][err. corr.(1)]",
        "[Investigate][MARKED]",
        "[-i /MARKED][-i -m \"*\"]",
        "[DATA salvage commence -s -X -X]",
    ]
    assert all(literal in text for literal in required_literals)

    pre = by_stage["pre_omit"]
    pre_marked = [r for r in pre if r["is_marked_star"]]
    pre_unmarked = nominal_remove_marked(pre)
    assert len(pre_marked) == 7 and len(pre_unmarked) == 61
    later_records = set(
        r["hex"] for r in by_stage["post_reload"] + by_stage["post_resume"]
    )
    pre_star_survivors = sorted(
        {r["hex"] for r in pre_marked} & later_records
    )
    assert pre_star_survivors == []

    # The page itself echoes one marked digest with a changed wrapper token
    # at the halt boundary. It is an actual visible tagged-record identity,
    # not a recovered parity equation.
    echo = by_stage["halt_echo"]
    assert echo[0]["hex"] == echo[1]["hex"]
    assert {r["suffix"] for r in echo} == {"[*]", "[/]"}
    assert echo[0]["hex"] == pre_marked[-1]["hex"]

    intersections = {}
    for left in by_stage:
        for right in by_stage:
            if left >= right:
                continue
            a = set(r["hex"] for r in by_stage[left])
            b = set(r["hex"] for r in by_stage[right])
            intersections[left + "__" + right] = len(a & b)
    assert intersections["post_reload__pre_omit"] == 4 or (
        intersections.get("pre_omit__post_reload") == 4
    )
    assert intersections.get("post_resume__pre_omit",
                             intersections.get("pre_omit__post_resume")) == 1

    return {
        "mode":"DISCOVER / historical source operation, not a CE ECC algorithm",
        "source_path":SOURCE.relative_to(ROOT).as_posix(),
        "source_manifest_tree_sha":manifest["source_tree_sha"],
        "manifest_recorded_git_blob_sha":entry["blob_sha"],
        "actual_archived_copy_git_blob_sha":blob_sha,
        "archived_copy_matches_manifest_git_blob":blob_sha == entry["blob_sha"],
        "source_byte_count":len(data),
        "hex_character_width":64,
        "hex_record_count":len(rows),
        "unique_hex_record_count":len(unique),
        "distinct_repeated_records":sum(n > 1 for n in unique.values()),
        "extra_occurrences_from_repetition":len(rows)-len(unique),
        "record_tag_counts":suffixes,
        "stage_census":{
            name:{
                "record_count":len(rs),
                "distinct_hex_values":len(set(r["hex"] for r in rs)),
                "star_marked_count":sum(r["is_marked_star"] for r in rs),
                "alt_label_count":sum(r["is_alternate"] for r in rs),
            }
            for name,rs in by_stage.items()
        },
        "observed_source_literals":required_literals,
        "nominal_remove_marked_operation":{
            "initial_pre_omit_records":68,
            "initial_star_marked_records":7,
            "remaining_pre_omit_records_if_starred_removed":61,
            "initial_marked_hex_values_repeated_after_reload_or_resume":
                len(pre_star_survivors),
            "halt_echo_duplicates_same_hex_different_tags":True,
        },
        "cross_section_identical_value_counts":dict(sorted(intersections.items())),
        "different_256bit_record_local_difference":nearest_unique_distances(rows),
        "limitations":[
            "The literal 'err. corr.(1)' exists in source, but NO parity matrix, syndrome, field, encoder or repair demonstration has been identified.",
            "An author's fictional 'data salvage' label does not prove a cryptographic error correction pipeline implemented on a server.",
            "The reconstruction of filtering [*] is a source-instructed nominal operation, not independently observed backend execution.",
            "Hex record equality/duplicates are not H108 stickers, and this page does not specify an H108 coordinate map.",
            "Original source chronology and an actual CE sticker receiver remain separate unknowns.",
        ],
    }


def self_test() -> None:
    sample = "<pre>\n" + "\n".join([
        "A"*64+"[*]",
        "[Omit][MARKED]",
        "A"*64+"[/]",
        "[Transmission reloaded][err. corr.(1)]",
        "B"*64,
        "[Transmission commence(+1+)]",
        "C"*64,
    ]) + "\n</pre>"
    rows,_ = parse(sample)
    assert [r["stage"] for r in rows] == [
        "pre_omit","halt_echo","post_reload","post_resume"
    ]
    assert len(nominal_remove_marked(rows)) == 3
    assert hamming("0"*64,"0"*64)==0
    assert hamming("0"*64,"F"*64)==256
    assert hamming("0"*63+"1","0"*64)==1
    print("synthetic parsing, label, filtering and bit-distance controls: pass")


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    p.add_argument("--self-test",action="store_true")
    args=p.parse_args()
    self_test()
    if args.self_test:return
    result=audit()
    output=json.dumps(result,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding="utf-8")
        print("saved",args.output)
    else:
        print(output)


if __name__=="__main__":
    main()
