"""Public split-sale original comment evidence is a lead, not physical proof."""
import json
import unittest
from pathlib import Path

from scripts.external_evidence.audit_public_ce_split_sale_leads import (
    canonical_name_matches, validate
)


class PublicCESplitSaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.sample = json.loads((
            root / "data/reference/inside-ce-2026-disc-retained-acquisition-leads.json"
        ).read_text(encoding="utf-8"))["leads"][0]
        cls.original_ledger = (
            root / "archive/external/twinysam-inside-arg/stickers.md"
        ).read_text(encoding="utf-8")

    def test_archived_source_stays_known_lost_L46_no_serial(self):
        report = validate([self.sample], self.original_ledger)
        self.assertEqual(report["source_count"], 1)
        self.assertEqual(report["candidate_count_not_canonical_exact_pseudonym"], 1)
        self.assertEqual(report["new_physical_copies_confirmed"], 0)
        self.assertEqual(report["current_unreconciled_owner_leads"], 0)
        self.assertEqual(report["new_stickers_confirmed"], 0)
        row = report["records"][0]
        self.assertEqual(row["source_published_utc"], "2026-03-08T05:32:21Z")
        self.assertEqual(row["seller_or_game_wrapper_custody"], "unverified")
        self.assertEqual(row["source_status"],
                         "known-canonical-lost-L46-historical-source-only")

    def test_existing_alias_in_ledger_forces_manual_reconciliation(self):
        seeded = self.original_ledger + "\n- L999 - user Afaith_1 already known"
        report = validate([self.sample], seeded)
        self.assertEqual(report["candidate_count_not_canonical_exact_pseudonym"], 0)
        self.assertEqual(report["records"][0]["source_status"],
                         "known-canonical-lost-L46-historical-source-only")
        self.assertEqual(report["new_stickers_confirmed"], 0)
        self.assertTrue(report["records"][0]["historical_snapshot_contains_public_handle"])

    def test_substring_match_does_not_count_as_existing_case(self):
        fake = "user NotAfaith_1Other something unrelated"
        self.assertEqual(canonical_name_matches("Afaith_1", fake), [])
        self.assertEqual(len(canonical_name_matches("Afaith_1", "Afaith_1")), 1)

    def test_invalid_spoofed_url_and_duplicate_leads_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "permalink"):
            validate([{**self.sample, "original_comment_url":
                       "https://www.reddit.com.evil.example/r/PlaydeadsInside/"
                       "comments/1l5x8rb/comment/o99qxpo/"}], "")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate([self.sample, self.sample], "")

    def test_source_timestamp_hash_and_observation_constraints(self):
        with self.assertRaisesRegex(ValueError, "SHA"):
            validate([{**self.sample, "archived_thread_response_sha256": "not-a-digest"}], "")
        with self.assertRaisesRegex(ValueError, "certify"):
            validate([{**self.sample, "sticker_number_observed": True}], "")
        with self.assertRaisesRegex(ValueError, "statuses"):
            validate([{**self.sample, "statuses": ["new-owner-proven"]}], "")


if __name__ == "__main__":
    unittest.main()
