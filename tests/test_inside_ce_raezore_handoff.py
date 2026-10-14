"""Handoff must not re-promote documented canonical owners as new CE leads."""
import csv
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HANDOFF=ROOT/"data/reference/inside-ce-raezore-handoff-candidates-2026-10-13.tsv"
LEDGER=ROOT/"data/reference/inside-ce-owner-search-ledger-2026-10-12.tsv"

class RaezoreHandoffTests(unittest.TestCase):
    def test_handoff_completeness_and_owner_novelty_guard(self):
        with HANDOFF.open(encoding="utf-8",newline="") as f:
            rows=list(csv.DictReader(f,delimiter="\t"))
        self.assertEqual(len(rows),6)
        self.assertEqual(len({x["lead_id"] for x in rows}),6)
        for x in rows:
            self.assertTrue(x["source_url"].startswith("https://"))
            self.assertTrue(x["evidence_limit"])
            self.assertTrue(x["canonical_crosscheck"])
            self.assertTrue(x["next_passive_verification"])
        cases={x["lead_id"]:x for x in rows}
        self.assertEqual(cases["H02"]["priority"],"P3")
        self.assertIn("U32",cases["H02"]["canonical_crosscheck"])
        self.assertIn("known_U32",cases["H02"]["claim_type"])
        self.assertEqual(cases["H01"]["claim_type"],"firsthand_purchase_claim")
        self.assertNotIn("confirmed_new", " ".join(x["claim_type"] for x in rows))
    def test_no_stale_unreconciled_gamesale_source(self):
        with LEDGER.open(encoding="utf-8",newline="") as f:
            rows=list(csv.DictReader(f,delimiter="\t"))
        labels={x["id"]:x for x in rows}
        for code in ("R04","R21"):
            self.assertIn("U32",labels[code]["canonical_relation"])
            self.assertIn("not_new",labels[code]["evidence_class"])
            self.assertEqual(labels[code]["new_confirmed_stickers"],"0")
        self.assertIn("U32",labels["R05"]["canonical_relation"])
if __name__=="__main__":
    unittest.main()
