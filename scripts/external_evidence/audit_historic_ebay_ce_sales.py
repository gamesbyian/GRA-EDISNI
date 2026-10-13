#!/usr/bin/env python3
"""Audit third-party historical sale IDs against canonical community sticker ledger.

Conservative: an exact eBay ID absent from stickers.md is a source lead, never
evidence of a new owner, new object, readable seal or missing ledger evidence.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ID_PATTERN = re.compile(r"(?<!\d)\d{12}(?!\d)")


def audit(rows: list[dict], ledger: str) -> dict:
    seen = set()
    output = []
    for entry in rows:
        item_id = entry["item_id"]
        if not re.fullmatch(r"\d{12}", item_id) or item_id in seen:
            raise ValueError(f"invalid/duplicate eBay item ID: {item_id}")
        seen.add(item_id)
        if entry["ebay_url"] != f"https://www.ebay.com/itm/{item_id}":
            raise ValueError(f"eBay source URL mismatch: {item_id}")
        canonical_exact_id = item_id in set(ID_PATTERN.findall(ledger))
        status = ("known-ledger-exact-item-id" if canonical_exact_id
                  else "excluded-other-game" if entry["initial_reconciliation"] == "wrong-game"
                  else "unreconciled-item-id-only")
        if entry["initial_reconciliation"] == "canonical-known" and not canonical_exact_id:
            raise ValueError(f"claimed-known item not in ledger: {item_id}")
        if entry["initial_reconciliation"] == "unreconciled-by-canonical-exact-item-id" and canonical_exact_id:
            raise ValueError(f"previously unknown item now in canonical ledger: {item_id}")
        output.append({
            "item_id": item_id, "original_listing_url": entry["ebay_url"],
            "third_party_date": entry["sale_date"],
            "third_party_title": entry["title"],
            "third_party_condition": entry["condition"],
            "status": status, "case_ref_if_known": entry.get("canonical_case"),
            "evidence_limit": "secondary historic sale metadata; original images not recovered",
        })
    groups = {}
    for item in output:
        groups.setdefault(item["status"], []).append(item)
    return {"schema_version": 1, "total_indexed": len(output),
            "known_source_urls": groups.get("known-ledger-exact-item-id", []),
            "unreconciled_source_urls": groups.get("unreconciled-item-id-only", []),
            "excluded_other_game": groups.get("excluded-other-game", []),
            "method": "exact original eBay item-ID presence within snapshot canonical stickers.md only"}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=Path("data/reference/inside-ce-public-historic-ebay-sale-index.json"))
    p.add_argument("--ledger", type=Path, default=Path("archive/external/twinysam-inside-arg/stickers.md"))
    p.add_argument("--output", type=Path, default=Path("visual-evidence-work/historical-ebay-sale-source-audit.json"))
    args = p.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    report = audit(manifest["sale_records"], args.ledger.read_text(encoding="utf-8"))
    report["index_source"] = manifest["source_page"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: len(report[k]) for k in
        ("known_source_urls", "unreconciled_source_urls", "excluded_other_game")}))


if __name__ == "__main__":
    main()
