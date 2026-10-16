"""Offline tests for exact, cumulative GHA web-index campaign cursors."""
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "forum_index_resume", ROOT / "scripts/run_global_forum_index_search.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def fixture():
    return [
        {"task_id": f"id-{i}", "community": "論壇" if i % 2 else "A forum",
         "term": f"シール {i}", "index_query": f"site:example.org INSIDE {i}",
         "language": "ja" if i % 2 else "en",
         "state": "planned_unexecuted"}
        for i in range(5)
    ]

class IndexResumeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.tasks = fixture()
    def tearDown(self):
        self.temp.cleanup()

    def test_manifest_digest_and_stable_unicode(self):
        path = self.root / "tasks.jsonl"
        path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in self.tasks),
                        encoding="utf-8")
        got, digest = mod.load_manifest(path)
        self.assertEqual(got, self.tasks)
        self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())
        path.write_text(path.read_text(encoding="utf-8").replace("シール", "貼紙"),
                        encoding="utf-8")
        self.assertNotEqual(mod.load_manifest(path)[1], digest)

    def test_two_consecutive_offsets_without_duplicates(self):
        invoked = []
        def search(q, key, count, language):
            invoked.append(q)
            return [{"url": "https://example.org/1", "title": "test", "description": ""}]
        first = mod.run_campaign(self.tasks, manifest_sha256="a"*64, key="fake-test",
                                 output=self.root / "first.jsonl", start_index=0,
                                 max_queries=2, search_fn=search, sleep_fn=lambda s: None)
        self.assertEqual(first["next_index"], 2)
        self.assertEqual(first["start_index"], 0)
        second = mod.run_campaign(self.tasks, manifest_sha256="a"*64, key="fake-test",
                                  output=self.root / "second.jsonl", start_index=2,
                                  max_queries=3, search_fn=search, sleep_fn=lambda s: None)
        self.assertTrue(second["complete"])
        self.assertEqual(second["next_index"], 5)
        self.assertEqual(len(set(invoked)), 5)
        actual = [json.loads(x) for p in (self.root / "first.jsonl",
                 self.root / "second.jsonl") for x in p.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([x["task_index"] for x in actual], list(range(5)))
        self.assertTrue(all(x["coverage"] == "partial_external_index_no_negative_evidence"
                            for x in actual))

    def test_index_full_page_is_censored_not_completeness_proof(self):
        two = self.tasks[:1]
        def api(query, key, count, language):
            return [{"url": "https://example.org/a"},
                    {"url": "https://example.org/b"}]
        result = mod.run_campaign(
            two, manifest_sha256="a" * 64, key="dummy",
            output=self.root / "capped.jsonl", start_index=0,
            max_queries=1, max_results=2,
            search_fn=api, sleep_fn=lambda _: None)
        item = json.loads((self.root / "capped.jsonl").read_text().strip())
        self.assertTrue(item["possibly_truncated"])
        self.assertEqual(item["index_pages_requested"], 1)
        self.assertEqual(item["index_page_limit"], 2)
        self.assertFalse(item["original_source_body_retrieved"])
        self.assertTrue(result["complete"])  # tasks done, *not* source corpus exhaustive

    def test_rate_limit_halts_at_failed_index(self):
        called = []
        def search(q, key, count, language):
            called.append(q)
            if " 1" in q:
                raise urllib.error.HTTPError(q, 429, "Throttled", {}, None)
            return []
        result = mod.run_campaign(self.tasks, manifest_sha256="b"*64, key="fake-test",
                                  output=self.root / "blocked.jsonl", start_index=0,
                                  max_queries=5, search_fn=search, sleep_fn=lambda s: None)
        self.assertEqual(result["next_index"], 1)
        self.assertEqual(result["index_queries_attempted"], 2)
        self.assertEqual(result["failures"], 1)
        self.assertIn("429", result["stopped"])
        self.assertFalse(result["complete"])
        rows = [json.loads(x) for x in (self.root / "blocked.jsonl").read_text().splitlines()]
        self.assertEqual(rows[-1]["task_index"], 1)
        self.assertEqual(rows[-1]["http_status"], 429)

    def test_failed_network_requests_preserve_resume_position(self):
        def break_network(q, key, count, language):
            raise urllib.error.URLError("simulated")
        r = mod.run_campaign(self.tasks, manifest_sha256="c"*64, key="fake-test",
                             output=self.root / "failed.jsonl", start_index=3,
                             max_queries=2, search_fn=break_network, sleep_fn=lambda s: None)
        self.assertEqual(r["next_index"], 3)
        self.assertEqual(r["failures"], 1)

    def test_invalid_input_and_completed_empty_batch(self):
        for kwargs in ({"start_index": -1}, {"start_index": 6},
                       {"max_queries": 0}, {"max_queries": 1001},
                       {"max_results": 0}, {"delay_seconds": 0},
                       {"key": ""}):
            props = dict(manifest_sha256="f"*64, key="test",
                         output=self.root / "invalid.jsonl",
                         start_index=0, max_queries=1,
                         search_fn=lambda *args: [], sleep_fn=lambda s: None)
            props.update(kwargs)
            with self.assertRaises(ValueError):
                mod.run_campaign(self.tasks, **props)
        ok = mod.run_campaign(self.tasks, manifest_sha256="f"*64, key="test",
                              output=self.root / "done.jsonl", start_index=5,
                              max_queries=2, search_fn=lambda *args: [],
                              sleep_fn=lambda s: None)
        self.assertTrue(ok["complete"])
        self.assertEqual(ok["index_queries_attempted"], 0)

    def test_manifest_rejects_nonplanned_or_duplicate_tasks(self):
        path = self.root / "invalid.jsonl"
        for rows in ([dict(self.tasks[0], state="index_search_success")],
                     [self.tasks[0], self.tasks[0]]):
            path.write_text("".join(json.dumps(x) + "\n" for x in rows))
            with self.assertRaises(ValueError):
                mod.load_manifest(path)

if __name__ == "__main__":
    unittest.main()
