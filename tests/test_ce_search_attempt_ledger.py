"""Offline, deterministic CE search attempt ledger tests."""
import unittest
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
from scripts.external_evidence.audit_search_attempts import evaluate, brave_result_events

D = "a" * 64


class SearchAttemptAuditTests(unittest.TestCase):
    def setUp(self):
        self.tasks = [{"task_id":"a","index_query":"site:reddit.com INSIDE iam8bit"},
                      {"task_id":"b","index_query":"site:youtube.com INSIDE collector"},
                      {"task_id":"c","index_query":"site:forum.example INSIDE"}]

    def test_empty_planned_is_not_searched(self):
        out,pending,log = evaluate(self.tasks,[])
        self.assertEqual(out["planned_tasks"],3)
        self.assertEqual(out["real_provider_attempts"],0)
        self.assertEqual(out["tasks_with_sufficient_recorded_evidence"],0)
        self.assertEqual(len(pending),3)
        self.assertEqual(log,[])
        self.assertEqual(out["new_confirmed_stickers"],0)

    def test_blocks_and_skips_preserved_as_censored(self):
        events=[
            {"task_id":"a","attempt_id":"a1","status":"blocked","http_status":429},
            {"task_id":"b","status":"not_attempted_after_provider_block"},
            {"task_id":"c","attempt_id":"c1","status":"index_search_success",
             "response_sha256":D,"pages_exhausted":False,"result_count":10}
        ]
        out,pending,log=evaluate(self.tasks,events)
        self.assertEqual(out["real_provider_attempts"],2)
        self.assertEqual(out["blocked_or_error_events"],1)
        self.assertEqual(out["tasks_marked_not_attempted_after_provider_block"],1)
        self.assertEqual(out["tasks_with_sufficient_recorded_evidence"],0)
        self.assertEqual(len(pending),3)
        self.assertEqual(next(x for x in pending if x["task_id"]=="a")["retry_policy"],
                         "manual-review-before-retrying")
        self.assertEqual(next(x for x in pending if x["task_id"]=="c")["retry_policy"],
                         "pagination-requires-review")
        self.assertEqual(len(log),3)

    def test_valid_complete_and_unique_retries(self):
        events=[
            {"task_id":"a","attempt_id":"r1","status":"provider_timeout"},
            {"task_id":"a","attempt_id":"r2","status":"index_search_success",
             "response_sha256":D,"pages_exhausted":True},
            {"task_id":"b","attempt_id":"b1","status":"original_source_retrieved",
             "response_sha256":D}
        ]
        out,pending,_=evaluate(self.tasks,events)
        self.assertEqual(out["real_provider_attempts"],3)
        self.assertEqual(out["tasks_with_sufficient_recorded_evidence"],2)
        self.assertEqual([x["task_id"] for x in pending],["c"])
        self.assertEqual(out["new_confirmed_stickers"],0)
        self.assertEqual(out["task_manifest_sha256"],
                         evaluate(self.tasks,events)[0]["task_manifest_sha256"])

    def test_invalid_or_misleading_claims_rejected(self):
        cases=[
            ([{"task_id":"a","status":"index_search_success","attempt_id":"x"}],"SHA256"),
            ([{"task_id":"a","status":"index_search_success","attempt_id":"x",
               "response_sha256":D,"pages_exhausted":False},
              {"task_id":"a","status":"blocked","attempt_id":"x"}],"duplicate"),
            ([{"task_id":"a","status":"http_error","attempt_id":"x",
               "no_evidence_exists":True}],"absence"),
            ([{"task_id":"a","status":"pagination_incomplete","attempt_id":"x",
               "pages_exhausted":True}],"exhausted"),
            ([{"task_id":"not-in-manifest","status":"blocked","attempt_id":"x"}],"not in"),
            ([{"task_id":"a","status":"new-owner-verified","attempt_id":"x"}],"unknown"),
            ([{"task_id":"a","status":"blocked"}],"attempt_id"),
        ]
        for events,expected in cases:
            with self.subTest(events=events), self.assertRaisesRegex(ValueError,expected):
                evaluate(self.tasks,events)

    def test_actual_brave_metadata_is_only_index_recall_not_original_source(self):
        rows=[
            {"task_id":"a","task_index":0,"status":"index_search_success",
             "matches":[{"url":"https://www.reddit.com/r/PlaydeadsInside/comments/eers0x"}],
             "possibly_truncated":False},
            {"task_id":"b","task_index":1,"status":"http_error","http_status":429},
            {"task_id":"c","task_index":2,"status":"not_attempted"},
        ]
        events=brave_result_events(rows,"gha-123")
        self.assertEqual(len(events),2)
        self.assertEqual(events[0]["attempt_id"],"gha-123-0")
        self.assertEqual(events[0]["response_digest_scope"],"normalized_result_matches_not_raw_http")
        self.assertFalse(events[0]["original_source_body_retrieved"])
        out,pending,_=evaluate(self.tasks,events)
        self.assertEqual(out["real_provider_attempts"],2)
        self.assertEqual(out["tasks_with_sufficient_recorded_evidence"],0)
        self.assertEqual(len(pending),3)
        self.assertEqual(out["new_confirmed_stickers"],0)
        with self.assertRaisesRegex(ValueError,"run_id"):
            brave_result_events(rows,"bad id")
        with self.assertRaisesRegex(ValueError,"matches"):
            brave_result_events([{"task_id":"a","task_index":0,
                                 "status":"index_search_success"}],"r1")

    def test_exact_manifest_bytes_and_brave_run_binding(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            manifest=root/"plan.jsonl"
            raw="".join(json.dumps(row)+"\n" for row in self.tasks)
            manifest.write_text(raw,encoding="utf-8")
            digest=hashlib.sha256(raw.encode("utf-8")).hexdigest()
            from scripts.external_evidence.audit_search_attempts import main
            with patch.object(sys,"argv",["audit_search_attempts.py","--tasks",str(manifest),
                                          "--out",str(root/"report")]):
                main()
            result=json.loads((root/"report/run-summary.json").read_text())
            self.assertEqual(result["task_manifest_sha256"],digest)
            self.assertEqual(result["task_manifest_digest_scope"],"exact_input_bytes")
            self.assertEqual(result["real_provider_attempts"],0)
            sample=[{"task_id":"a","task_index":0,"status":"index_search_success",
                     "matches":[],"manifest_sha256":digest}]
            self.assertEqual(len(brave_result_events(sample,"run-1",digest)),1)
            with self.assertRaisesRegex(ValueError,"frozen exact-byte"):
                brave_result_events(sample,"run-1","f"*64)

    def test_task_manifest_duplicates_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            evaluate(self.tasks+[self.tasks[0]],[])


if __name__=="__main__":
    unittest.main()
