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
    def test_serial_not_auto_confirmed(self):
        got=mod.triage([{"url":"https://example.org/img","title":"Sticker /043"}],[])
        self.assertEqual(got[0]["new_confirmed_stickers"],0)
        self.assertIn("numeric_candidate_not_serial_proof",got[0]["reason_codes"])
if __name__=="__main__":unittest.main()
