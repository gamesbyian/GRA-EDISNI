"""Offline tests: CE index-hit dedup, comment provenance, false-positive controls."""
import importlib.util
import json
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ce_index_triage", ROOT / "scripts/triage_inside_ce_index_results.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def hit(url, title="INSIDE collector's edition", description="CE owners"):
    return {"url": url, "title": title, "description": description}

def result(task_id, matches, **kw):
    return {"task_id": task_id, "community": "r/GameSale", "term": "INSIDE CE",
            "status": "index_search_success", "language_hint": "en",
            "manifest_sha256": "abcd"*16, "matches": matches, **kw}

class TriageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
    def tearDown(self):
        self.tmp.cleanup()

    def test_reddit_comment_identity_and_thread_context(self):
        urls = [
            "https://old.reddit.com/r/GameSale/comments/i0vgml/my_listing/pida/?utm_source=foo",
            "https://www.reddit.com/r/GameSale/comments/i0vgml/my_listing/pidb/?context=3",
            "https://reddit.com/r/GameSale/comments/i0vgml/my_listing/pida/",
            "https://www.reddit.com/r/GameSale/comments/i0vgml/comment/pida",
        ]
        keys = [mod.normalize_url(x) for x in urls]
        self.assertEqual(keys[0], keys[2])
        self.assertEqual(keys[0], keys[3])
        self.assertNotEqual(keys[0][2], keys[1][2])
        self.assertEqual({x[1] for x in keys}, {"reddit:i0vgml"})
        self.assertEqual(keys[0][2], "reddit-comment:pida")

    def test_source_permalink_without_comment_cannot_prove_comment(self):
        u, thread, evidence = mod.normalize_url(
            "https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/now_shipping_finally/"
        )
        self.assertEqual(thread, "reddit:e9bteo")
        self.assertEqual(evidence, "reddit-thread:e9bteo")
        self.assertEqual(u, "https://www.reddit.com/comments/e9bteo")
        u2, thread2, evidence2 = mod.normalize_url(
            "https://www.reddit.com/r/PlaydeadsInside/s/FooBAr123"
        )
        self.assertFalse(thread2)
        self.assertTrue(evidence2.startswith("reddit-short:"))

    def test_youtube_comment_and_ebay_item(self):
        a = mod.normalize_url("https://youtu.be/abc123?t=11")
        b = mod.normalize_url("https://www.youtube.com/watch?v=abc123&utm_source=a")
        self.assertEqual(a, b)
        comment = mod.normalize_url("https://youtube.com/watch?v=abc123&lc=Ugw123")
        self.assertNotEqual(comment[2], a[2])
        self.assertEqual(comment[1], a[1])
        ebay = mod.normalize_url("https://www.ebay.com/itm/Inside-Collectors-Edition/123456789012?hash=aaa")
        ebay2 = mod.normalize_url("https://www.ebay.com/itm/123456789012")
        self.assertEqual(ebay, ebay2)

    def test_tracking_removed_but_meaningful_parameters_preserved(self):
        u, _, _ = mod.normalize_url(
            "https://example.org/thread/55?utm_source=abc&page=2&fbclid=X")
        self.assertEqual(u, "https://example.org/thread/55?page=2")
        self.assertNotEqual(u, mod.normalize_url("https://example.org/thread/55?page=1")[0])

    def test_canonical_ledger_exact_versus_thread_overlap(self):
        raw = [
            result("t1", [
                hit("https://reddit.com/r/GameSale/comments/i0vgml/title/comment/abc"),
                hit("https://www.iam8bit.com/products/inside-ps4-physical-game",
                    "INSIDE PS4 Physical Game", "Limited Edition of 2000, $29.99"),
            ]),
            result("t2", [
                hit("https://old.reddit.com/r/GameSale/comments/i0vgml/title/comment/xyz"),
                hit("https://www.reddit.com/r/GameSale/comments/i0vgml/title/comment/abc?context=3"),
            ]),
            {"task_id": "oops", "status": "http_error", "matches": [
                hit("https://unretrieved.example/sticker/043")
            ]},
        ]
        p = self.root / "result.jsonl"
        p.write_text("".join(json.dumps(x) + "\n" for x in raw))
        findings, stat = mod.read_index_hits([p])
        self.assertEqual(stat["successful_queries"], 2)
        self.assertEqual(stat["failed_queries"], 1)
        self.assertEqual(stat["raw_search_hits"], 4)
        self.assertEqual(len(findings), 3)
        ledger = [{"source_url": "https://www.reddit.com/r/GameSale/comments/i0vgml"}]
        results = mod.classify(findings, ledger)
        self.assertEqual(len(results), 3)
        self.assertEqual(sum(x["prior_ledger_relation"] ==
                             "same_thread_only_no_independent_owner_proof"
                             for x in results), 2)
        self.assertEqual(sum("possible_standalone_ps4_false_positive" in x["review_warning"]
                             for x in results), 1)
        self.assertEqual(max(x["index_hit_occurrences"] for x in results), 2)
        self.assertTrue(all(x["new_confirmed_stickers"] == 0 for x in results))
        self.assertTrue(all(x["review_status"] == "unreviewed_source_content"
                            for x in results))
        self.assertTrue(all(x["source_relation"] == "index_candidate_url_only"
                            for x in results))

    def test_exact_ledger_link_and_no_auto_confirmation(self):
        source = "https://www.reddit.com/r/GameSale/comments/i0vgml"
        u, t, e = mod.normalize_url(source)
        found = {u: {"canonical_url": u, "thread_key": t, "evidence_key": e,
                     "first_title": "INSIDE CE sticker 329 owner got mine",
                     "first_description": "My CE has sticker 329.",
                     "index_hit_occurrences": 1, "tasks": {"task1"},
                     "languages": {"en"}, "manifests": set()}}
        results = mod.classify(found, [{"source_url": source}])
        self.assertEqual(results[0]["prior_ledger_relation"], "exact_ledger_url")
        self.assertEqual(results[0]["new_confirmed_stickers"], 0)

    def test_spreadsheet_formula_and_missing_provider_fields(self):
        self.assertEqual(mod.spreadsheet_safe("=HYPERLINK(\"x\")"),
                         "'=HYPERLINK(\"x\")")
        self.assertEqual(mod.spreadsheet_safe(" +IMPORTXML(...)"),
                         "' +IMPORTXML(...)")
        self.assertEqual(mod.spreadsheet_safe("ordinary item"), "ordinary item")
        path = self.root / "malformed.jsonl"
        path.write_text(json.dumps({
            "task_id": "one", "status": "index_search_success",
            "matches": [{"url": "https://forum.example/t/1",
                         "title": None, "description": None}]
        }))
        found, _ = mod.read_index_hits([path])
        self.assertEqual(next(iter(found.values()))["first_title"], "")
        path.write_text(json.dumps({"task_id": "one",
                                    "status": "index_search_success",
                                    "matches": {"url": "https://forum.example"}}))
        with self.assertRaises(ValueError):
            mod.read_index_hits([path])

    def test_community_canonical_exact_source_vs_thread_context(self):
        markdown = """- [Known owner](https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/comment/falotig/)
- [Known channel](https://www.youtube.com/watch?v=ZqYhhptmhmo&lc=UgwABC123)
- [Other](https://www.example.net/some/thing)"""
        urls, topics = mod.canonical_refs(markdown)
        self.assertGreaterEqual(len(urls), 3)
        self.assertIn("reddit:e9bteo", topics)
        known, thread, evidence = mod.normalize_url(
            "https://old.reddit.com/r/PlaydeadsInside/comments/e9bteo/comment/falotig/")
        other, _, other_evidence = mod.normalize_url(
            "https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/now_shipping/comment/OTHER9")
        self.assertIn(known, urls)
        self.assertNotIn(other, urls)
        pool = {
            known: {"thread_key": thread, "evidence_key": evidence,
                    "first_title": "Known photo", "first_description": "",
                    "index_hit_occurrences": 1, "tasks": {"x"}, "languages": {"en"}},
            other: {"thread_key": thread, "evidence_key": other_evidence,
                    "first_title": "Different reply", "first_description": "",
                    "index_hit_occurrences": 1, "tasks": {"y"}, "languages": {"en"}},
        }
        classified = mod.classify(pool, [], urls, topics)
        relations = {x["canonical_url"]: x["canonical_relation"] for x in classified}
        self.assertEqual(relations[known], "canonical_exact_source_url")
        self.assertEqual(relations[other], "canonical_thread_context_only")
        self.assertTrue(all(x["new_confirmed_stickers"] == 0 for x in classified))

    def test_input_security_and_duplicate_task_detection(self):
        self.assertRaises(ValueError, mod.normalize_url, "file:///private/owner.jpg")
        p = self.root / "invalid.jsonl"
        p.write_text(json.dumps({"task_id": "x", "status": "index_search_success",
                                 "matches": [hit("file:///private/owner.jpg")]}) + "\n")
        findings, stats = mod.read_index_hits([p])
        self.assertEqual(stats["malformed_hits"], 1)
        self.assertEqual(len(findings), 0)
        p.write_text(json.dumps({"status": "index_search_success",
                                 "matches": [hit("https://example.org/")]}))
        with self.assertRaises(ValueError):
            mod.read_index_hits([p])

if __name__ == "__main__":
    unittest.main()
