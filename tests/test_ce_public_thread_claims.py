"""Offline single-thread buyer/retraction reconciliation with non-owner case boundaries."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from scripts.external_evidence.audit_public_ce_thread_claims import audit, classify_body


class PublicThreadClaimsTests(unittest.TestCase):
    def test_same_author_retraction_overrides_earlier_i_bought_statement(self):
        rows = [
            {"id": "fkeb0sa", "link_id": "t3_fhvflq", "created_utc": 1584109347,
             "author": "lengbleu", "body": "Just bought the damn thing.... It better be worth it!"},
            {"id": "fkkj7it", "link_id": "t3_fhvflq", "created_utc": 1584285250,
             "author": "lengbleu", "body": "I didn't buy it in the end"},
        ]
        result = audit(rows, "fhvflq")
        self.assertEqual(result["summary"]["later_purchase_retractions"], 1)
        statement = result["public_author_claim_groups"][0]
        self.assertEqual(statement["classification"], "same-thread-later-purchase-retraction-review")
        self.assertEqual(statement["observed_statement_count"], 2)
        self.assertFalse(statement["physical_copy_confirmed"])
        self.assertFalse(statement["sticker_serial_confirmed"])
        self.assertTrue(statement["statements"][0]["comment_url"].endswith("/fkeb0sa/"))

    def test_different_author_declining_does_not_retract_buyers_statement(self):
        rows = [
            {"id": "fkeb0sa", "author": "buyer", "created_utc": 10,
             "body": "I bought the CE"},
            {"id": "fkkj7it", "author": "other", "created_utc": 20,
             "body": "I didn't buy it in the end"},
        ]
        result = audit(rows, "fhvflq")
        by_author = {r["public_author"]: r for r in result["public_author_claim_groups"]}
        self.assertEqual(by_author["buyer"]["classification"], "purchase-text-only-no-receipt-confirmed")
        self.assertEqual(by_author["other"]["classification"], "purchase-declined-or-cancelled")
        self.assertEqual(result["summary"]["later_purchase_retractions"], 0)

    def test_deleted_comment_and_cross_thread_comment_excluded(self):
        rows = [
            {"id": "fkeb0sa", "author": "buyer", "link_id": "t3_fhvflq",
             "body": "Just bought the damn thing"},
            {"id": "fkkj7it", "author": "buyer", "link_id": "t3_another",
             "body": "I didn't buy it"},
            {"id": "fkkj7ig", "author": "buyer", "link_id": "t3_fhvflq",
             "body": "[removed] I didn't buy it"},
        ]
        result = audit(rows, "fhvflq")
        self.assertEqual(result["summary"]["later_purchase_retractions"], 0)
        self.assertEqual(result["public_author_claim_groups"][0]["observed_statement_count"], 1)

    def test_stated_receipt_cannot_be_promoted_to_physical_serial(self):
        r = audit([{"id": "fkdw8nu", "author": "existing-case",
                    "body": "I got mine from eBay, brand new"}], "fhvflq", truncated=True)
        self.assertEqual(r["public_author_claim_groups"][0]["classification"],
                         "receipt-text-only-not-physical-sticker")
        self.assertTrue(r["possible_partial_archived_tree"])
        self.assertFalse(r["public_author_claim_groups"][0]["physical_copy_confirmed"])

    def test_snippets_sanitize_links_and_malformed_post_ids_fail(self):
        r = audit([{"id": "fkeb0sa", "author": "reader", "created_utc": 2,
                    "body": "I purchased it https://example.org/private"}], "fhvflq")
        self.assertNotIn("example.org", r["public_author_claim_groups"][0]["statements"][0]["context_excerpt"])
        self.assertEqual(classify_body("[deleted] I bought one"), [])
        with self.assertRaises(ValueError):
            audit([], "../../secrets")

    def test_direct_cli_help_from_repo_root(self):
        script = Path(__file__).resolve().parents[1] / "scripts/external_evidence/audit_public_ce_thread_claims.py"
        process = subprocess.run([sys.executable, str(script), "--help"],
                                 capture_output=True, text=True, timeout=10)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("--post-id", process.stdout)


if __name__ == "__main__":
    unittest.main()
