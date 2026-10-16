"""Offline recovery tests for public CE lead ranking."""
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("lead_rank",ROOT/"scripts/rank_inside_ce_public_leads.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class LeadTests(unittest.TestCase):
    def test_english_and_native_owner_scoring(self):
        for text in ["I bought the iam8bit INSIDE CE", "INSIDEを買いました シール", "comprei INSIDE iam8bit", "我買了 INSIDE 限定版"]:
            points,reasons=mod.score({"title":text})
            self.assertGreaterEqual(points,4,text)
            self.assertTrue(reasons)
    def test_caswell_exact_public_text_is_a_review_lead_not_sticker_proof(self):
        post = "Do I still need Inside Collector’s edition jelly statue?"
        score, reasons = mod.score({"text": post})
        self.assertGreaterEqual(score, 4)
        self.assertIn("possible_owner_disposal_question_not_confirmed", reasons)
        self.assertIn("specific_inside_ce_title", reasons)
        self.assertNotIn("first_person_en", reasons)
        got = mod.triage([{
            "url": "https://bsky.app/profile/tomcaswell.games/post/3mta6ecjbvk2i",
            "text": post,
        }], [])
        self.assertEqual(got[0]["new_confirmed_stickers"], 0)
        self.assertEqual(got[0]["status"], "unverified_public_lead")
        not_ce = mod.score({"text": "Do I still need this ordinary kitchen statue?"})
        self.assertNotIn("specific_inside_ce_title", not_ce[1])

    def test_exact_url_dedup_and_known(self):
        source="https://www.example.com/post/12?utm_source=x"
        got=mod.triage([{"url":source,"text":"I bought the INSIDE iam8bit CE"},
                        {"url":"http://example.com/post/12","title":"unboxing Huddle"},
                        {"url":"file:///private","text":"my address"}],["https://example.com/post/12"])
        self.assertEqual(len(got),1)
        self.assertEqual(got[0]["source_records"],2)
        self.assertTrue(got[0]["canonical_url_match"])
        self.assertEqual(got[0]["new_confirmed_stickers"],0)
    def test_real_index_envelopes_failures_and_jsonl(self):
        records=[{"task_id":"x","status":"index_search_success",
                  "matches":[{"url":"https://forum.example/t","title":"INSIDE iam8bit",
                              "description":"I received my Huddle"}]},
                 {"task_id":"y","status":"http_error",
                  "matches":[{"url":"https://never.example","title":"My CE"}]}]
        got=mod.triage(records,[])
        self.assertEqual(len(got),1)
        self.assertEqual(got[0]["url"],"https://forum.example/t")
        with tempfile.TemporaryDirectory() as temp:
            inp=Path(temp)/"in.jsonl"
            inp.write_text("".join(json.dumps(x)+"\n" for x in records),encoding="utf-8")
            parsed=[json.loads(x) for x in inp.read_text().splitlines()]
            self.assertEqual(mod.triage(parsed,[]),got)
    def test_reddit_original_post_variants_without_comment_conflation(self):
        original = "https://www.reddit.com/r/gamecollecting/comments/eaktdt/"
        variants = [
            "https://old.reddit.com/r/gamecollecting/comments/eaktdt/arrived/?utm_source=share",
            "http://reddit.com/comments/eaktdt",
            original,
        ]
        normalized = {mod.normalize_url(v) for v in variants}
        self.assertEqual(normalized, {"https://reddit.com/comments/eaktdt"})
        comment = mod.normalize_url(
            "https://reddit.com/r/gamecollecting/comments/eaktdt/arrived/xyz123")
        self.assertEqual(comment, "https://reddit.com/comments/eaktdt/comment/xyz123")
        self.assertNotIn(comment, normalized)

    def test_existing_case_crosswalk_suppresses_old_owner_lead_not_new_reply(self):
        path = ROOT / "data/reference/inside-ce-curated-public-source-crosswalk-2026-10-14.tsv"
        known = mod.load_known_source_crosswalk(path)
        self.assertEqual(len(known), 3)
        original = "https://old.reddit.com/r/gamecollecting/comments/eaktdt/my_inside_ce/"
        other_comment = original + "abcxyz"
        rows = [
            {"url":original, "title":"My INSIDE CE finally came in"},
            {"url":other_comment, "title":"I have this too"},
            {"url":"https://reddit.com/r/GameSale/comments/i0vgml/my_listing/",
             "title":"Selling my INSIDE CE"},
        ]
        results=mod.triage(rows, [], known)
        by_url={x["url"]:x for x in results}
        self.assertEqual(by_url["https://reddit.com/comments/eaktdt"]["crosswalk_record"],"L08")
        self.assertEqual(by_url["https://reddit.com/comments/i0vgml"]["crosswalk_record"],"U32")
        self.assertEqual(by_url["https://reddit.com/comments/eaktdt/comment/abcxyz"]["crosswalk_record"],"")
        self.assertEqual(by_url["https://reddit.com/comments/eaktdt"]["status"],"existing_case_context_review")
        self.assertTrue(all(x["new_confirmed_stickers"]==0 for x in results))

    def test_crosswalk_rejects_duplicate_and_missing_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"cases.tsv"
            header="source_url\\tcanonical_record\\tsource_relation\\tevidence_note\\treview_status\\n"
            row="https://reddit.com/comments/eaktdt\\tL08\\tprior\\tpublic\\tunverified\\n"
            path.write_text(header+row+row, encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.load_known_source_crosswalk(path)
            path.write_text(header+row.replace("L08",""),encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.load_known_source_crosswalk(path)

    def test_serial_not_auto_confirmed(self):
        got=mod.triage([{"url":"https://example.org/img","title":"Sticker /043"}],[])
        self.assertEqual(got[0]["new_confirmed_stickers"],0)
        self.assertIn("numeric_candidate_not_serial_proof",got[0]["reason_codes"])
if __name__=="__main__":unittest.main()
