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

    def test_actual_source_context_separates_five_arg_posts_and_owner(self):
        samples = [
            ("Do I still need Inside Collector’s edition jelly statue?",
             "possible_owner_claim"),
            ("Wow, there's some kind of ARG around Playdead's game, Inside. "
             "The game's Collector's Edition had cipher symbols on stickers",
             "arg_discussion"),
            ("If you have the Collector's Edition of Inside and haven't "
             "thrown away the sticker that sealed the package, help the community",
             "arg_discussion"),
            ("ATTENTION ANYONE WITH A COLLECTOR'S EDITION OF PLAYDEAD'S INSIDE! "
             "HELP SOLVE THE ARG!", "arg_discussion"),
            ("theres this ARG going on with playdead’s Inside where pieces of "
             "a code were written on packaging for collectors edition",
             "arg_discussion"),
            ("A football podcast called Inside The Huddle", "unrelated_or_unresolved"),
            ("Inside the huddle: CFL preview today", "unrelated_or_unresolved"),
            ("I bought the Ecco the Dolphin Collector's Edition",
             "unrelated_or_unresolved"),
            ("House of 1000 Doors: Evil Inside Collector's Edition",
             "unrelated_or_unresolved"),
            ("House of 1000 Doors: Evil Inside Collector's Edition code giveaway",
             "unrelated_or_unresolved"),
            ("Finally got my Blue Prince merch package today and it's missing "
             "the pin and desk mat. Instead I found two random children's "
             "picture books inside. I didn't order them, and iam8bit doesn't "
             "even sell them.", "unrelated_or_unresolved"),
            ("@iam8bit.com sent us a mystery package. What was inside? 👀",
             "unrelated_or_unresolved"),
            ("I received a numbered sticker on my INSIDE Collector's Edition "
             "from iam8bit!", "possible_owner_claim"),
            ("I got my iam8bit Huddle from the game INSIDE delivered today",
             "possible_owner_claim"),
            ("", "unrelated_or_unresolved"),
        ]
        for body, expected in samples:
            with self.subTest(body=body):
                self.assertEqual(triage.classify_ce_context(body), expected)

    def test_real_publisher_anniversary_recovered_without_owner_promotion(self):
        official_body = ("Happy 10th Birthday to INSIDE! We're thinking a lot about "
                         "the extremely normal collector's edition we made. "
                         "https://youtu.be/gqlQaHgRaHg")
        self.assertEqual(
            triage.classify_ce_context(official_body, "iam8bit.com"),
            "publisher_domain_handle_reference")
        self.assertEqual(
            triage.classify_ce_context(official_body, "anonymous.bsky.social"),
            "unrelated_or_unresolved")
        self.assertEqual(
            triage.classify_ce_context(
                "@iam8bit.com sent us a mystery package. What was inside?",
                "iam8bit.com"), "unrelated_or_unresolved")
        publisher = dict(POST, uri="at://did:plc:4nwd4d33o3hw6b5b3syxokii/app.bsky.feed.post/3mphksb3pku2h",
                         handle="iam8bit.com", text_excerpt=official_body, target=False)
        false_parcel = dict(POST,
            uri="at://did:plc:unrelated/app.bsky.feed.post/xyzabc",
            handle="sixoneindie.com", target=False,
            text_excerpt="@iam8bit.com sent us a mystery package. What was inside?")
        report = {"state": "executed_bounded", "results": [
            {"kind": "blind_discovery", "status": "ok", "key": "frozen",
             "version": "v2", "posts": [publisher, false_parcel, POST]}]}
        hits, summary = triage.build_queue(report)
        self.assertEqual(len(hits), 2)
        self.assertEqual(hits[0]["uri"], URI)
        self.assertEqual(hits[1]["context_class"], "publisher_domain_handle_reference")
        self.assertFalse(hits[1]["owner_verified"])
        self.assertFalse(hits[1]["sticker_verified"])
        self.assertEqual(summary["excluded_from_review_queue"], 1)

    def test_topic_gating_removes_false_positives_without_losing_raw_count(self):
        football = dict(POST, uri="at://did:plc:sport/app.bsky.feed.post/abc123",
                        handle="sports.bsky.social", target=False,
                        text_excerpt="Inside The Huddle - Indigenous football news")
        unrelated = dict(POST, uri="at://did:plc:other/app.bsky.feed.post/def456",
                         handle="other.bsky.social", target=False,
                         text_excerpt="I bought a collector edition of something inside a box")
        report = {"state": "executed_bounded", "results": [
            {"kind": "blind_discovery", "status": "ok", "version": "v1",
             "key": "inside_huddle", "posts": [football, unrelated, POST]}]}
        hits, summary = triage.build_queue(report)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["uri"], URI)
        self.assertEqual(summary["unique_public_post_uris"], 3)
        self.assertEqual(summary["relevant_review_candidates"], 1)
        self.assertEqual(summary["excluded_from_review_queue"], 2)
        self.assertTrue(summary["original_unfiltered_api_results_retained"])

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
