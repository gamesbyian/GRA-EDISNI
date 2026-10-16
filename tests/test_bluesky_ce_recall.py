"""Deterministic, fully offline tests for the public Bluesky known-positive audit."""
import importlib.util
import unittest
import urllib.error
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/audit_bluesky_ce_recall.py"
spec = importlib.util.spec_from_file_location("bluesky_recall", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class BlueskyRecallTests(unittest.TestCase):
    def test_frozen_plan_and_blindness(self):
        tasks = m.plan()
        self.assertEqual(len(tasks), 17)
        for t in tasks[1:]:
            self.assertNotIn("tomcaswell", t["query"].lower())
            self.assertNotIn(m.GOLD_RKEY, t["query"])
            self.assertNotIn(m.GOLD_DID, t["query"])
        self.assertTrue(all(t["params"].get("allTime") == "true"
                            for t in tasks[1:] if t["version"] == "v2"))

    def test_offline_default_never_networks(self):
        report = m.run(fetch_fn=lambda *x: self.fail("network attempted"))
        self.assertEqual(report["state"], "planned_unexecuted")
        self.assertEqual(report["requests_sent"], 0)

    def test_positive_independent_source_and_two_blind_hits(self):
        def fake(endpoint, params):
            post = {"uri": m.GOLD_URI,
                    "author": {"handle": "tomcaswell.games"},
                    "record": {"text": "inside collector's edition",
                               "createdAt": "2026-08-16T10:00:00Z"}}
            if endpoint.endswith("getPostThread"):
                return {"thread": {"post": post}}
            query = params.get("q", params.get("query"))
            return {"posts": [post] if query == "inside collector's edition" else [],
                    "hitsTotal": 1, "cursor": "next"}
        result = m.run(execute=True, max_requests=4, fetch_fn=fake,
                       sleep_fn=lambda _: None)
        self.assertTrue(result["direct_post_retrievable"])
        self.assertEqual(len(result["blind_hits"]), 2)
        self.assertEqual(result["requests_sent"], 4)
        self.assertEqual(result["tasks_unattempted"], 13)

    def test_fail_closed_on_rate_limit(self):
        def blocked(endpoint, params):
            raise urllib.error.HTTPError("https://public.api.bsky.app",
                                         429, "Rate limit", {}, None)
        report = m.run(execute=True, fetch_fn=blocked)
        self.assertEqual(report["requests_sent"], 1)
        self.assertEqual(report["stop_reason"], "provider_access_stop_429")
        self.assertIsNone(report["direct_post_retrievable"])

    def test_direct_control_failure_does_not_erase_search(self):
        calls = []
        def missing_direct(endpoint, params):
            calls.append(endpoint)
            if endpoint.endswith("getPostThread"):
                raise urllib.error.HTTPError("https://public.api.bsky.app",
                                             404, "gone", {}, None)
            return {"posts": []}
        report = m.run(execute=True, fetch_fn=missing_direct, max_requests=3,
                       sleep_fn=lambda _: None)
        self.assertEqual(report["requests_sent"], 3)
        self.assertIsNone(report["direct_post_retrievable"])

    def test_v2_403_does_not_suppress_distinct_v1(self):
        seen = []
        def endpoint_acl(endpoint, params):
            seen.append(endpoint)
            if endpoint.endswith("getPostThread"):
                return {"thread": {"post": {
                    "uri": m.GOLD_URI, "author": {"handle": "tomcaswell.games"},
                    "record": {"text": "inside collector's edition"}}}}
            if endpoint.endswith("searchPostsV2"):
                raise urllib.error.HTTPError("https://public.api.bsky.app",
                                            403, "Forbidden", {}, None)
            return {"posts": []}
        report = m.run(execute=True, max_requests=17,
                       fetch_fn=endpoint_acl, sleep_fn=lambda _: None)
        self.assertEqual(report["requests_sent"], 10)
        self.assertEqual(report["blocked_versions"], ["v2"])
        self.assertEqual(report["tasks_skipped_endpoint_block"], 7)
        self.assertTrue(report["direct_post_retrievable"])
        self.assertEqual(sum(x.endswith("searchPostsV2") for x in seen), 1)
        self.assertEqual(sum(x.endswith("searchPosts") for x in seen), 8)

    def test_matching_exact_at_uri_not_post_id_only(self):
        fake = {"uri": "at://did:plc:other/app.bsky.feed.post/3mta6ecjbvk2i",
                "author": {}, "record": {"text": "same ID different identity"}}
        output = m.summarize(1, m.plan()[1], {"posts": [fake]})
        self.assertFalse(output["gold_found"])

    def test_request_limits(self):
        for n in (-1, 0, 18, 1000):
            with self.assertRaises(ValueError):
                m.run(max_requests=n)
        with self.assertRaises(ValueError):
            m.run(delay=0.2)
        with self.assertRaises(ValueError):
            m.fetch("not-an-approved-endpoint", {})

if __name__ == "__main__":
    unittest.main()
