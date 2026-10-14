#!/usr/bin/env python3
"""Conservatively audit the publicly archived October 2026 CE auction source.

An exact account absence, a $400 bid, or a September sale observation do not
establish a new physical CE owner, an eBay item, image, sticker or serial.
"""
from __future__ import annotations
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def inspect(source: dict, ledger: str) -> dict:
    post, comment = source["thread_id"], source["comment_id"]
    if not all(re.fullmatch(r"[a-z0-9]{5,12}", s, re.I) for s in (post, comment)):
        raise ValueError("invalid original public thread/comment ID")
    link = source["original_comment_url"]
    u = urlparse(link)
    if (u.scheme != "https" or u.hostname != "www.reddit.com"
            or u.path != f"/comments/{post}/_/{comment}/"
            or u.username or u.password or u.query or u.fragment):
        raise ValueError("original public permalink mismatch")
    if not re.fullmatch(r"[0-9a-f]{64}", source["original_archive_response_sha256"]):
        raise ValueError("invalid source archive SHA256")
    handle = source["public_account"]
    if not re.fullmatch(r"[A-Za-z0-9_-]{3,32}", handle):
        raise ValueError("invalid public source pseudonym")
    created = datetime.fromtimestamp(source["published_timestamp"], timezone.utc)
    if source["published_utc"] != created.strftime("%Y-%m-%dT%H:%M:%SZ"):
        raise ValueError("timestamp and publication date conflict")
    statements = source["purchase_claim"]
    if not (statements["auction_winning_price_reported_usd"] == 400
            and statements["reported_shipping_usd"] == 0
            and statements["claimed_other_september_sale_price_usd"] == 380):
        raise ValueError("original primary-source sale quantities differ")
    if (source["canonical_reconciliation"]["not_proof_of_additional_copy"] is not True
            or source["canonical_reconciliation"]["not_known_sticker_number"] is not True
            or statements["physical_transaction_status"] !=
                "self-reported-win-not-independent-delivery-confirmation"):
        raise ValueError("public statement cannot be promoted into physical evidence")
    seen = list(re.finditer(
        r"(?<![A-Za-z0-9_-])" + re.escape(handle) + r"(?![A-Za-z0-9_-])",
        ledger, re.I))
    return {
        "source_url": link,
        "public_account": handle,
        "created_utc": source["published_utc"],
        "archived_response_sha256": source["original_archive_response_sha256"],
        "source_status": ("possible-existing-canonical-pseudonym-review" if seen
                          else "unreconciled-exact-account-public-auction-claim"),
        "known_name_occurrences": len(seen),
        "ebay_original_item_id": statements["auction_listing_id"],
        "auction_win_claim_usd": 400,
        "other_september_sale_secondhand_claim_usd": 380,
        "no_auction_media_verified": True,
        "delivery_confirmed": False,
        "new_owner_case_confirmed": False,
        "new_sticker_serial_confirmed": False,
        "caveat": "Same physical box may be resold; exact name absence is not new-owner proof.",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path,
                    default=Path("data/reference/inside-ce-oct2026-ebay-auction-public-lead.json"))
    ap.add_argument("--ledger", type=Path,
                    default=Path("archive/external/twinysam-inside-arg/stickers.md"))
    ap.add_argument("--out", type=Path,
                    default=Path("visual-evidence-work/ce-oct2026-ebay-auction-source-audit.json"))
    args = ap.parse_args()
    result = inspect(json.loads(args.manifest.read_text(encoding="utf-8")),
                     args.ledger.read_text(encoding="utf-8"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"schema_version": 1, "source": result}, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
