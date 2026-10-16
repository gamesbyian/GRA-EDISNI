"""October 2026 public auction lead cannot be mistaken for verified original sticker."""
from __future__ import annotations
import json
import unittest
from pathlib import Path
from scripts.external_evidence.audit_public_ce_october_auction import inspect


class October2026OwnerLeadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.source = json.loads((
            root/"data/reference/inside-ce-oct2026-ebay-auction-public-lead.json"
        ).read_text(encoding="utf-8"))
        cls.ledger = (
            root/"archive/external/twinysam-inside-arg/stickers.md"
        ).read_text(encoding="utf-8")

    def test_source_now_reconciled_with_known_043_despite_stale_archive(self):
        out = inspect(self.source, self.ledger)
        self.assertEqual(out["source_status"],
                         "closed-known-canonical-043-buyer-source")
        self.assertEqual(out["known_name_occurrences"], 0)
        self.assertEqual(out["created_utc"], "2026-10-11T10:52:15Z")
        self.assertEqual(out["auction_win_claim_usd"], 400)
        self.assertEqual(out["other_september_sale_secondhand_claim_usd"], 380)
        self.assertFalse(out["new_owner_case_confirmed"])
        self.assertFalse(out["new_sticker_serial_confirmed"])

    def test_complete_original_comment_has_no_original_ebay_item_or_media_link(self):
        full = self.source["complete_public_original_review"]
        self.assertEqual(full["comment_character_count"], 4603)
        self.assertEqual(len(full["comment_text_sha256"]), 64)
        self.assertEqual(full["outbound_urls_in_comment"], 0)
        self.assertEqual(full["candidate_ebay_item_numbers_in_comment"], 0)
        self.assertFalse(full["seller_photo_link_recovered"])
        methods = self.source["public_marketplace_photo_recovery"]
        self.assertFalse(methods["exact_eBay_sale_listing_id_recovered"])
        self.assertFalse(methods["seller_original_image_recovered"])

    def test_known_alias_in_ledger_changes_review_class_not_serial(self):
        out = inspect(self.source, self.ledger + "\n- U99 Leading_Highlight553")
        self.assertEqual(out["known_name_occurrences"], 1)
        self.assertEqual(out["source_status"], "closed-known-canonical-043-buyer-source")
        self.assertTrue(out["snapshot_name_match_only_not_novelty"])
        self.assertFalse(out["new_sticker_serial_confirmed"])

    def test_host_post_and_timestamp_invariants(self):
        with self.assertRaisesRegex(ValueError, "permalink"):
            inspect({**self.source,
                     "original_comment_url":
                     "https://www.reddit.com.evil.example/comments/1vdbrus/_/pf7wee4/"}, self.ledger)
        with self.assertRaisesRegex(ValueError, "publication date"):
            inspect({**self.source, "published_timestamp": 1700000000}, self.ledger)
        with self.assertRaisesRegex(ValueError, "SHA256"):
            inspect({**self.source, "original_archive_response_sha256": "nonexistent"}, self.ledger)

    def test_sale_claim_not_promoted_to_physical_evidence(self):
        claim = {**self.source["purchase_claim"], "physical_transaction_status": "verified"}
        with self.assertRaisesRegex(ValueError, "physical evidence"):
            inspect({**self.source, "purchase_claim": claim}, self.ledger)


if __name__ == "__main__":
    unittest.main()
