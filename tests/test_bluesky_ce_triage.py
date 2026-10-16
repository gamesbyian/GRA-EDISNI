"""Offline, source-first regression tests for public Bluesky CE lead triage."""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location(
    "bluesky_triage", ROOT / "scripts/triage_bluesky_ce_recall.py")
triage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triage)

URI = "at://did:plc:msovagwqdq3ew2rrikvpqp7c/app.bsky.feed.post/3mta6ecjbvk2i"
POST = {
    "uri": URI, "handle": "tomcaswell.games",
    "created_at": "2026-08-16T21:53:12.962Z",
    "text_excerpt": "Do I still need Inside Collector’s edition jelly statue?",
    "target": True,
}

class PublicBlueskyTriageTests(unittest.TestCase):
    def test_dedup_firsthand_question_stays_unverified(self):
        report = {
            "state": "executed_bounded", "api_host": "primary",
            "fetched_at_utc": "2026-10-16T10:00:00Z",
            "results": [
                {"kind": "direct_control", "status": "ok", "post": POST},
                {"kind": "blind_discovery", "status": "ok", "key": "exact",
                 "version": "v1", "posts": [POST], "returned": 1},
                {"kind": "blind_discovery", "status": "ok", "key": "broader",
                 "version": "v2", "posts": [POST], "returned": 1},
                {"kind": "blind_discovery", "status": "error",
                 "version": "v1", "key": "blocked", "http_status": 403},
            ],
        }
        hits, summary = triage.build_queue(report)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["url"],
                         "https://bsky.app/profile/tomcaswell.games/post/3mta6ecjbvk2i")
        self.assertEqual(hits[0]["lead_score"], 4)
        self.assertEqual(len(hits[0]["search_matches"]), 2)
        self.assertEqual(hits[0]["new_confirmed_stickers"], 0)
        self.assertFalse(hits[0]["owner_verified"])
        self.assertFalse(hits[0]["sticker_verified"])
        self.assertEqual(summary["failed_queries"], 1)
        self.assertEqual(summary["unique_public_post_uris"], 1)
        self.assertTrue(summary["known_positive_found"])
        self.assertEqual(summary["new_confirmed_stickers"], 0)

    def test_reject_unexecuted_and_invalid_public_locator(self):
        with self.assertRaises(ValueError):
            triage.build_queue({"state": "planned_unexecuted", "results": []})
        bad = dict(POST, handle="../../bad")
        report = {"state": "executed_bounded", "results": [
            {"kind": "blind_discovery", "status": "ok", "posts": [bad]}]}
        hits, summary = triage.build_queue(report)
        self.assertEqual(hits, [])
        self.assertEqual(summary["unique_public_post_uris"], 0)
        with self.assertRaises(ValueError):
            triage.build_queue(report, max_candidates=0)

    def test_source_ids_never_merged_by_similar_text(self):
        other = dict(POST, uri="at://did:plc:different/app.bsky.feed.post/abc123",
                     target=False)
        report = {"state": "executed_bounded", "results": [
            {"kind": "blind_discovery", "status": "ok",
             "key": "topic", "version": "v1", "posts": [POST, other]}]}
        hits, summary = triage.build_queue(report)
        self.assertEqual(len(hits), 2)
        self.assertEqual(summary["unique_public_post_uris"], 2)
        self.assertTrue(all(p["new_confirmed_stickers"] == 0 for p in hits))

if __name__ == "__main__":
    unittest.main()
