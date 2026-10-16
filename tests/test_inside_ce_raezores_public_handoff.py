"""Regression gate: original-source leads cannot be republished after canonical closure.

Read-only, exact public-handle, source-status check. A matching handle is
evidence for *manual case reconciliation*, never proof of a distinct CE or
private identity; these two explicit community entries already reconcile the
original source accounts to their known cases.
"""
import csv
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location(
    "owner_source_reconcile",ROOT/"scripts/crosscheck_inside_ce_public_handles.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class OutboundLeadHandoffTests(unittest.TestCase):
    def test_both_original_leads_closed_in_status_registers(self):
        a=json.loads((ROOT/"data/reference/inside-ce-oct2026-ebay-auction-public-lead.json").read_text(encoding="utf-8"))
        b=json.loads((ROOT/"data/reference/inside-ce-2026-disc-retained-acquisition-leads.json").read_text(encoding="utf-8"))["leads"][0]
        self.assertEqual(a["public_account"],"Leading_Highlight553")
        self.assertEqual(a["status"],"closed-known-canonical-043-buyer-source-provenance-only")
        self.assertTrue(a["canonical_reconciliation"]["exact_public_handle_in_stickers_md"])
        self.assertEqual(a["canonical_reconciliation"]["confirmed_community_entry"],"043")
        self.assertFalse(a["canonical_reconciliation"]["not_known_sticker_number"])
        self.assertEqual(b["account_as_published"],"Afaith_1")
        self.assertTrue(b["canonical_exact_pseudonym_in_stickers_md"])
        self.assertEqual(b["canonical_status"],"known_lost_L46")
        self.assertEqual(b["canonical_sticker_loss_confirmation_date"],"2026-09-22")
        self.assertNotIn("unreconciled-public-acquisition-claim",b["statuses"])
        self.assertFalse(b["sticker_number_observed"])
        self.assertFalse(b["physical_copy_newly_proven"])

    def test_no_live_2026_leads_in_outgoing_packet_and_no_retracted_h04(self):
        p=(ROOT/"docs/reference/inside-ce-raezores-public-lead-handoff-2026-10-13.md").read_text(encoding="utf-8")
        self.assertIn("Current outbound lead count: zero",p)
        self.assertIn("Leading_Highlight553",p)
        self.assertIn("Afaith_1",p)
        self.assertIn("L46",p)
        self.assertIn("/043",p)
        self.assertIn("retracted",p.casefold())
        with (ROOT/"data/reference/inside-ce-raezore-handoff-candidates-2026-10-13.tsv").open(
            encoding="utf-8",newline="") as f:
            cases={r["lead_id"]:r for r in csv.DictReader(f,delimiter="\t")}
        self.assertIn("retracted",cases["H04"]["claim_type"])
        self.assertEqual(cases["H04"]["priority"],"P3")
        self.assertIn("U32",cases["H02"]["canonical_crosscheck"])

    def test_canonical_community_entries_still_reconcile_both_accounts(self):
        # CI checks out current community master. Synthetic control remains a
        # genuine offline test in environments without that optional checkout.
        synthetic=(
            "- [043](images/stickers/043.webp) (symb: / img: G) - "
            "Raezores found [this Reddit comment from Leading_Highlight553]"
            "(https://www.reddit.com/comments/1vdbrus/_/pf7wee4/) "
            "as latcholia buyer.\n"
            "- L46 - [Reddit user Afaith_1](https://www.reddit.com/r/...) "
            "confirmed that the sticker was lost.\n"
        )
        for markdown in [synthetic]+(
            [(ROOT/"canonical-inside-arg/stickers.md").read_text(encoding="utf-8")]
            if (ROOT/"canonical-inside-arg/stickers.md").is_file() else []):
            idx=mod.canonical_index(markdown)
            self.assertIn("043",idx[("reddit","leading_highlight553")])
            self.assertIn("L46",idx[("reddit","afaith_1")])
            self.assertEqual(
                mod.classify("https://www.reddit.com/comments/1vdbrus/_/pf7wee4/",
                             "reddit","Leading_Highlight553",idx)[0],
                "same_platform_handle_in_canonical_needs_review")
            self.assertEqual(
                mod.classify("https://www.reddit.com/r/PlaydeadsInside/comments/1l5x8rb/comment/o99qxpo/",
                             "reddit","Afaith_1",idx)[0],
                "same_platform_handle_in_canonical_needs_review")

if __name__=="__main__":
    unittest.main()
