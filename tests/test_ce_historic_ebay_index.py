"""Secondary eBay public-sale lead reconciliation, no network."""
import json
import unittest
from pathlib import Path

from scripts.external_evidence.audit_historic_ebay_ce_sales import audit


class HistoricEbayAuditTests(unittest.TestCase):
    def test_complete_seed_reconciles_to_seven_unlisted_sources(self):
        root = Path(__file__).resolve().parents[1]
        rows = json.loads((root/"data/reference/inside-ce-public-historic-ebay-sale-index.json").read_text())["sale_records"]
        ledger = (root/"archive/external/twinysam-inside-arg/stickers.md").read_text()
        result = audit(rows, ledger)
        self.assertEqual(result["total_indexed"], 14)
        self.assertEqual(len(result["known_source_urls"]), 6)
        self.assertEqual(len(result["unreconciled_source_urls"]), 7)
        self.assertEqual(len(result["excluded_other_game"]), 1)
        ids = {r["item_id"] for r in result["unreconciled_source_urls"]}
        self.assertIn("389713956842", ids)
        self.assertNotIn("297682348686", ids)
        self.assertNotIn("196542141679", ids)

    def test_known_id_cannot_be_misclassified_unknown(self):
        row = {"item_id": "297682348686", "ebay_url": "https://www.ebay.com/itm/297682348686",
               "sale_date": "2025-10-14", "title": "Inside CE", "condition": "cib",
               "initial_reconciliation": "unreconciled-by-canonical-exact-item-id"}
        with self.assertRaisesRegex(ValueError, "now in canonical"):
            audit([row], "known 297682348686")

    def test_bad_and_duplicate_listing_ids_rejected(self):
        row = {"item_id": "123456789012", "ebay_url": "https://www.ebay.com/itm/123456789012",
               "sale_date": "2026-01-01", "title": "sample", "condition": "new",
               "initial_reconciliation": "unreconciled-by-canonical-exact-item-id"}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit([row,row], "")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            audit([{**row, "ebay_url": "https://example.com/itm/123456789012"}], "")


if __name__ == "__main__":
    unittest.main()
