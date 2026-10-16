#!/usr/bin/env python3
"""Audit public CE transfer-claim sources against canonical source ledger.

A URL/author absent from the community's written ledger is an *unreconciled
public text lead*, NEVER proof of a new owner, sticker or physical CE.
Specifically distinguishes removal of the numbered game-wrapper component.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ID_RE = re.compile(r"[a-z0-9]{5,12}", flags=re.I)
NAME_RE = re.compile(r"[A-Za-z0-9_-]{3,32}")
EXPECTED_STATUSES = {
    "known_canonical_lost_L46",
    "speculative_original_game_component_separated",
    "physical_sticker_not_observed_in_this_source",
}


def canonical_name_matches(name: str, ledger: str) -> list[str]:
    if not NAME_RE.fullmatch(name):
        raise ValueError("Public Reddit handle has invalid characters")
    pattern = re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(name) +
                         r"(?![A-Za-z0-9_-])", flags=re.I)
    return [ledger[max(0, m.start()-100):min(len(ledger),m.end()+140)]
            for m in list(pattern.finditer(ledger))[:8]]


def validate(leads: list[dict], ledger: str) -> dict:
    seen = set()
    review = []
    for lead in leads:
        lid = lead["lead_id"]
        pid, cid = lead["post_id"], lead["comment_id"]
        if not ID_RE.fullmatch(pid) or not ID_RE.fullmatch(cid):
            raise ValueError("Invalid public post/comment ID")
        original = lead["original_comment_url"]
        url = urlparse(original)
        if (url.scheme != "https" or url.hostname != "www.reddit.com"
                or not re.fullmatch(
                    rf"/r/[A-Za-z0-9_]+/comments/{re.escape(pid)}/comment/{re.escape(cid)}/?",
                    url.path, re.I
                ) or url.username or url.password or url.query or url.fragment):
            raise ValueError("Original public comment permalink mismatch")
        if lid in seen:
            raise ValueError("Duplicate historical lead ID")
        seen.add(lid)
        name = lead["account_as_published"]
        known = canonical_name_matches(name, ledger)
        stamp = lead.get("archive_created_utc")
        if not isinstance(stamp, int) or not 1_500_000_000 < stamp < 2_000_000_000:
            raise ValueError("Missing or invalid archived source timestamp")
        published_iso = datetime.fromtimestamp(stamp, timezone.utc).isoformat(
            timespec="seconds").replace("+00:00","Z")
        sha = lead.get("archived_thread_response_sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", sha):
            raise ValueError("Missing exact public archive response SHA-256")
        if (lead.get("canonical_status") != "known_lost_L46"
                or lead.get("canonical_exact_pseudonym_in_stickers_md") is not True
                or lead.get("canonical_sticker_loss_confirmation_date") != "2026-09-22"):
            raise ValueError("Current canonical L46 reconciliation must be preserved")
        if set(lead.get("statuses", [])) != EXPECTED_STATUSES:
            raise ValueError("Unexpected or promoted lead statuses")
        if lead.get("sticker_number_observed") is not False or lead.get("physical_copy_newly_proven") is not False:
            raise ValueError("Public purchase text may not certify a sticker or a new physical copy")
        review.append({
            "lead_id": lid, "public_source_url": original,
            "public_source_author": name, "source_published_utc": published_iso,
            "known_canonical_pseudonym_occurrences": len(known),
            "canonical_pseudonym_evidence": known,
            "source_status": "known-canonical-lost-L46-historical-source-only",
            "historical_snapshot_contains_public_handle": bool(known),
            "seller_or_game_wrapper_custody": "unverified",
            "source_photo_available": bool(lead.get("original_media_retrieved", False)),
            "sticker_number_confirmed": False,
            "new_physical_owner_case_confirmed": False,
            "caveat": "Current canonical L46 explicitly names this Reddit user and confirms sticker lost. The archived ledger snapshot can be older; a zero snapshot match is NOT novelty.",
        })
    return {
        "schema_version": 1,
        "source_count": len(review),
        "candidate_count_not_canonical_exact_pseudonym": sum(
            r["known_canonical_pseudonym_occurrences"] == 0 for r in review),
        "new_stickers_confirmed": 0,
        "new_physical_copies_confirmed": 0,
        "current_unreconciled_owner_leads": 0,
        "records": review,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path,
                   default=Path("data/reference/inside-ce-2026-disc-retained-acquisition-leads.json"))
    p.add_argument("--canonical-ledger", type=Path,
                   default=Path("archive/external/twinysam-inside-arg/stickers.md"))
    p.add_argument("--output", type=Path,
                   default=Path("visual-evidence-work/public-ce-split-sale-review.json"))
    args = p.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    report = validate(data["leads"], args.canonical_ledger.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n",
                           encoding="utf-8")
    print(json.dumps({"source_count": report["source_count"],
                      "unreconciled_pseudonyms":
                          report["candidate_count_not_canonical_exact_pseudonym"],
                      "new_stickers_confirmed": report["new_stickers_confirmed"]}))


if __name__ == "__main__":
    main()
