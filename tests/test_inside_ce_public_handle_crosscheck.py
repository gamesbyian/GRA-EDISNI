"""Tests for exact-only public-handle canonical sticker reconciliation."""
import importlib.util
from pathlib import Path
import unittest
import csv

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("ce_owner_handles",ROOT/"scripts/crosscheck_inside_ce_public_handles.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SAMPLE = """
- L08 - https://www.reddit.com/user/Knuckles316/ via dragonslayer875. confirmed lost.
- [338](images/stickers/338.jpg) (symb: - img: E) - During a search, I came across this [Resetera post](https://www.resetera.com/threads/a-public-arg-topic.430745/page-5), where on page 5, user juxjuxjux confirmed he bought the CE.
- L46 - [Reddit user Afaith_1](https://www.reddit.com/r/PlaydeadsInside/s/mPfxvoJOj6) contacted. lost.
- [470](images/stickers/470.jpg) (symb: / img: B) [Reddit comment from No-Program385](https://www.reddit.com/r/example/comment/a).
- U47 - [where Reddit user Shaxai confirms two copies](https://www.reddit.com/r/oddheader/comments/1wmvl0x).
- [043](images/stickers/043.jpg) (symb: / img: G) - [this Reddit comment from Leading_Highlight553](https://www.reddit.com/comments/1vdbrus/_/pf7wee4/) as buyer.
- [123](images/stickers/123.jpg) - link https://x.com/some_artist/status/111
"""
class PublicHandleTests(unittest.TestCase):
    def test_same_platform_exact_positive_reconciliation(self):
        idx=mod.canonical_index(SAMPLE)
        cases=[
            ("reddit","Knuckles316","L08"),
            ("resetera","juxjuxjux","338"),
            ("reddit","Afaith_1","L46"),
            ("reddit","Leading_Highlight553","043"),
            ("reddit","No-Program385","470"),
            ("reddit","Shaxai","U47"),
            ("twitter","some_artist","123"),
        ]
        for platform,name,expected in cases:
            relation,labels,match=mod.classify("https://example.com",platform,name,idx)
            self.assertEqual(relation,"same_platform_handle_in_canonical_needs_review",name)
            self.assertIn(expected,labels,name)
            self.assertEqual(match,name)
    def test_exactness_platform_isolation_and_no_automatic_equivalence(self):
        idx=mod.canonical_index(SAMPLE)
        for platform,author in [
            ("reddit","Leading_Highlight553x"),("reddit","Knuckles316x"),("twitter","Knuckles316"),("reddit","juxjuxjux"),
            ("resetera","Shaxai"),("reddit","Afaith"),("instagram","Afaith_1"),("reddit","")]:
            rel,labels,_=mod.classify("",platform,author,idx)
            self.assertNotEqual(rel,"same_platform_handle_in_canonical_needs_review")
            self.assertEqual(labels,[])
        result=mod.annotate([{"source_url":"https://example.net",
                                  "public_platform":"reddit","public_author":"Knuckles316"}],SAMPLE)
        self.assertEqual(result[0]["new_confirmed_stickers"],0)
        self.assertEqual(result[0]["source_evidence_status"],
                         "requires_original_post_and_canonical_reconciliation")
    def test_public_profile_url_detection(self):
        self.assertEqual(mod.user_handle("https://old.reddit.com/user/Knuckles316/"),
                         ("reddit","knuckles316"))
        self.assertEqual(mod.user_handle("https://twitter.com/Some_Artist/status/123"),
                         ("twitter","some_artist"))
        self.assertIsNone(mod.user_handle("https://reddit.com/r/PlaydeadsInside/comments/123"))
        self.assertIsNone(mod.user_handle("file:///tmp/user/Knuckles316"))
        self.assertIsNone(mod.user_handle("https://example.com/user/Knuckles316"))
        self.assertIsNone(mod.user_handle("https://x.com/intent/tweet"))
    def test_control_fixtures_separate_source_from_person_and_copies(self):
        file=ROOT/"data/reference/inside-ce-owner-source-recall-controls-2026-10-13.tsv"
        with file.open(encoding="utf-8",newline="") as f:
            rows=list(csv.DictReader(f,delimiter="\t"))
        self.assertEqual(len(rows),9)
        self.assertEqual(len({r["id"] for r in rows}),9)
        self.assertLess(len({r["source_url"] for r in rows}),len(rows),
                         "Two distinct commenters can use the same source URL")
        self.assertIn("known_lost_owner_post_different_url",
                      [r["known_source_class"] for r in rows])
        self.assertTrue(all(r["source_url"].startswith("https://") for r in rows))
        self.assertEqual(next(r for r in rows if r["id"]=="P09")["expected_canonical_entry"],"043")
if __name__=="__main__":
    unittest.main()
