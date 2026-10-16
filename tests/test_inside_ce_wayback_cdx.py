"""Synthetic tests for Wayback CDX metadata probes, with no network traffic."""
from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import unittest
import urllib.error
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "probe_inside_ce_wayback_cdx", ROOT / "scripts/probe_inside_ce_wayback_cdx.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class Response(io.BytesIO):
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()


class WaybackProbeTests(unittest.TestCase):
    def test_control_rows_have_real_urls_and_limits(self):
        rows = probe.load_rows(probe.CONTROLS, "controls")
        self.assertEqual(len(rows), 16)
        tasks = probe.generate(rows, per_window_limit=5, max_sources=4)
        self.assertEqual(len(tasks), 8)
        self.assertEqual({x["status"] for x in tasks}, {"planned_unexecuted"})
        for task in tasks:
            url = urlsplit(task["cdx_url"])
            self.assertEqual(url.hostname, "web.archive.org")
            values = parse_qs(url.query)
            self.assertEqual(values["limit"], ["5"])
            self.assertEqual(values["output"], ["json"])
            self.assertIn(task["window"], ("2016-2020", "2021-2026"))

    def test_sample_capture_not_post_proof(self):
        sample = [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
            ["20191225080100", "https://example.org/thread/9", "200",
             "text/html", "ABC123"],
        ]
        body = json.dumps(sample).encode("utf-8")
        tasks = probe.generate(
            [{"label": "test", "url": "https://example.org/thread/9",
              "evidence": "external", "window": "2019"}],
            per_window_limit=10, max_sources=1)
        observed = []
        def transport(req, timeout):
            self.assertEqual(timeout, 25)
            self.assertEqual(urlsplit(req.full_url).hostname, "web.archive.org")
            observed.append(req.full_url)
            return Response(body)
        # Only one simulated request to avoid delay.
        results = probe.run(tasks[:1], delay_seconds=2, transport=transport)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["sampled_captures"], 1)
        self.assertEqual(results[0]["status"], "metadata_sample_received")
        self.assertIn("metadata_sample_not_historical_fulltext", results[0]["coverage"])
        self.assertNotIn("original_post_date", results[0]["captures"][0])
        self.assertEqual(len(observed), 1)

    def test_bad_headers_and_short_queries(self):
        with self.assertRaises(ValueError):
            probe.parse_cdx(b'{"error":"not index"}')
        with self.assertRaises(ValueError):
            probe.parse_cdx(b'[["timestamp"],["2019"]]')
        with self.assertRaises(ValueError):
            probe.generate([], max_sources=51, per_window_limit=12)
        with self.assertRaises(ValueError):
            probe.generate([], max_sources=1, per_window_limit=101)
        with self.assertRaises(ValueError):
            probe.run([], delay_seconds=0)

    def test_domain_scoping_and_reddit_policy(self):
        rows = [
            {"label": "blocked", "url": "https://www.reddit.com/r/any",
             "access": "reddit_platform_rights_and_removed_content_policy",
             "evidence": "public"},
            {"label": "allowed", "url": "https://forum.example/threads/",
             "evidence": "public"}
        ]
        tasks = probe.generate(rows, max_sources=2, per_window_limit=2)
        self.assertEqual(len(tasks), 2)
        self.assertTrue(all(x["label"] == "allowed" for x in tasks))

    def test_all_unattempted_followers_are_preserved_and_never_fetched(self):
        tasks = probe.generate(
            [{"label": "a", "url": "https://forum.example/one", "evidence": "x"},
             {"label": "b", "url": "https://forum.example/two", "evidence": "x"}],
            max_sources=2, per_window_limit=1)
        called = []
        def forbidden(req, timeout):
            called.append(req.full_url)
            raise urllib.error.HTTPError(req.full_url, 403, "blocked", {}, None)
        results = probe.run(tasks, delay_seconds=2, transport=forbidden)
        self.assertEqual(len(called), 1)
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0]["status"], "http_error")
        self.assertEqual([x["status"] for x in results[1:]],
                         ["not_attempted_after_provider_block"] * 3)
        self.assertEqual([x["source_url"] for x in results],
                         [x["source_url"] for x in tasks])
        stats = probe.summarize_run(results, executed=True)
        self.assertEqual(stats["attempted_requests"], 1)
        self.assertEqual(stats["not_attempted_after_provider_block"], 3)
        self.assertEqual(stats["sources_selected"], 2)
        self.assertEqual(stats["tasks_written"], 4)
        self.assertEqual(stats["provider_or_parse_failures"], 1)


    def test_error_handling_no_retry_or_bypass(self):
        tasks = probe.generate(
            [{"label": "x", "url": "https://forum.example/",
              "evidence": "unverified"}],
            max_sources=1, per_window_limit=1)
        def deny(req, timeout):
            raise urllib.error.HTTPError(req.full_url, 429, "rate-limited", {}, None)
        got = probe.run(tasks, delay_seconds=2, transport=deny)
        self.assertEqual(len(got), len(tasks))
        self.assertEqual(got[0]["status"], "http_error")
        self.assertEqual(got[0]["http_status"], 429)
        self.assertEqual(got[1]["status"], "not_attempted_after_provider_block")
        self.assertIn("429", got[1]["reason"])


if __name__ == "__main__":
    unittest.main()
