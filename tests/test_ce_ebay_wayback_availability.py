"""Archive.org availability-only probes, no external networking in tests."""
import unittest
from scripts.external_evidence.probe_ce_ebay_wayback import inspect, snapshot_metadata


class ArchivedSaleCaptureTests(unittest.TestCase):
    def setUp(self):
        self.row = {"item_id":"389713956842","ebay_url":"https://www.ebay.com/itm/389713956842",
                    "sale_date":"2026-03-09","initial_reconciliation":"unreconciled-by-canonical-exact-item-id"}

    def test_archived_pointer_is_not_evidence_of_media(self):
        result=snapshot_metadata(self.row,{"archived_snapshots":{"closest":{
            "available":True,"status":"200","timestamp":"20260310001201",
            "url":"https://web.archive.org/web/20260310001201/https://www.ebay.com/itm/389713956842"}}})
        self.assertEqual(result["status"],"snapshot-advertised-not-fetched")
        self.assertEqual(result["capture_timestamp"],"20260310001201")
        self.assertIn("not reviewed",result["evidence_grade"])

    def test_missing_snapshot_is_explicit(self):
        self.assertEqual(snapshot_metadata(self.row,{"archived_snapshots":{}})["status"],
                         "no-snapshot-advertised")

    def test_external_unsafe_snapshot_does_not_get_promoted(self):
        with self.assertRaisesRegex(ValueError, "non-Wayback"):
            snapshot_metadata(self.row,{"archived_snapshots":{"closest":{
                "available": True, "url": "https://attacker.example/file.jpg"}}})

    def test_only_explicit_unreconciled_sources_allowed(self):
        with self.assertRaisesRegex(ValueError,"Only unresolved"):
            inspect([{**self.row, "initial_reconciliation":"canonical-known"}],
                    requester=lambda x: ({"archived_snapshots":{}}, "0"*64))

    def test_custom_responses_preserve_exact_item_id(self):
        records=[self.row,{**self.row,"item_id":"294530200626",
                                "ebay_url":"https://www.ebay.com/itm/294530200626"}]
        results=inspect(records,requester=lambda entry: ({"archived_snapshots":{}},
                                                           entry["item_id"]*5))
        self.assertEqual([r["item_id"] for r in results],
                         ["389713956842", "294530200626"])
        self.assertTrue(all(x["status"]=="no-snapshot-advertised" for x in results))


if __name__ == "__main__":
    unittest.main()
