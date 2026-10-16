"""Controlled search discovery pilot tests, strictly offline."""
import importlib.util
import sys
import unittest
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("ce_discovery",
    ROOT / "scripts/discover_bluesky_inside_ce.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class DiscoveryTests(unittest.TestCase):
    def test_frozen_manifest_blind_queries(self):
        tasks = m.discovery_plan()
        self.assertEqual(len(tasks), 16)
        for task in tasks:
            self.assertEqual(task["params"]["allTime"], "true")
            self.assertEqual(task["params"]["since"], m.START)
            self.assertEqual(task["params"]["until"], m.END)
            self.assertNotIn("tomcaswell", task["query"])
            self.assertNotIn("3mta6ecjbvk2i", task["query"])
            self.assertEqual(task["endpoint"], "app.bsky.feed.searchPostsV2")
            self.assertTrue(task["query"])

    def test_network_opt_in_and_source_specific_returns(self):
        offline = m.execute(fetch_fn=lambda *a: self.fail("unexpected GET"))
        self.assertEqual(offline["requests_sent"], 0)
        self.assertEqual(offline["state"], "planned_unexecuted")
        calls = []
        def fake(endpoint, params):
            calls.append(params["query"])
            return {"posts": []}
        online = m.execute(live=True, request_cap=3,
                           fetch_fn=fake, sleep_fn=lambda _: None)
        self.assertEqual(online["requests_sent"], 3)
        self.assertEqual(online["tasks_unattempted"], 13)
        self.assertEqual(len(calls), 3)

    def test_stop_on_forbidden_and_rate_limit(self):
        for code in (401, 402, 403, 429):
            def denied(endpoint, params):
                raise urllib.error.HTTPError("https://api.bsky.app",code,
                    "No",{},None)
            report = m.execute(live=True, fetch_fn=denied)
            self.assertEqual(report["requests_sent"], 1)
            self.assertEqual(report["stop_reason"],f"provider_access_stop_{code}")

    def test_response_does_not_promote_owner_claim(self):
        def fake(endpoint, params):
            return {"posts":[{"uri":"at://did:plc:a/app.bsky.feed.post/x",
                "author":{"handle":"a.bsky.social"},
                "record":{"text":"My Inside Collector's Edition!"}}]}
        report=m.execute(live=True,request_cap=1,fetch_fn=fake,
                         sleep_fn=lambda _:None)
        self.assertEqual(report["results"][0]["posts"][0]["target"],False)
        self.assertEqual(report["results"][0]["status"],"ok")

    def test_caps(self):
        for cap in (0,17):
            with self.assertRaises(ValueError): m.execute(request_cap=cap)
        with self.assertRaises(ValueError): m.execute(delay=0.1)

if __name__=="__main__":
    unittest.main()
