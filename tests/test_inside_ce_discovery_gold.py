"""Offline gold-control evaluation: strict exact source and honest unknowns."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ce_gold", ROOT / "scripts/benchmark_inside_ce_discovery.py")
gold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gold)

class GoldBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = gold.load_gold(gold.DEFAULT)

    def test_twelve_community_confirmed_controls(self):
        self.assertEqual(len(self.records), 12)
        self.assertEqual(len({x["surface"] for x in self.records}), 8)
        self.assertTrue(any(x["canonical_sticker_record"] == "317" for x in self.records))
        self.assertTrue(any(x["canonical_sticker_record"] == "L40" for x in self.records))

    def test_url_not_leaked_and_24_offline_queries(self):
        tasks = gold.plan(self.records)
        self.assertEqual(len(tasks), 24)
        self.assertEqual({x["state"] for x in tasks}, {"planned_unexecuted"})
        self.assertEqual(len({x["task_id"] for x in tasks}), 24)
        for task in tasks:
            self.assertNotIn("https://", task["index_query"])
            self.assertNotIn("http://", task["index_query"])
            self.assertEqual(task["index_query"].count("site:"), 1)
        self.assertEqual(tasks[0]["control_id"], "G01")
        self.assertEqual(tasks[12]["control_id"], "G01")

    def test_strict_original_and_topic_only(self):
        cases = [x for x in self.records if x["control_id"] in ("G09", "G11")]
        result = [{
            "control_id": "G09", "status": "index_search_success",
            "matches": [{"url": cases[0]["target_url"]}]
        }, {
            "control_id": "G11", "status": "index_search_success",
            "matches": [{"url": "https://www.reddit.com/r/oddheader/comments/1wmvl0x/" }]
        }]
        report, s = gold.evaluate(cases, result)
        by_id = {x["control_id"]: x for x in report}
        self.assertEqual(by_id["G09"]["outcome"], "exact_source_found")
        self.assertEqual(by_id["G11"]["outcome"], "related_topic_only")
        self.assertEqual(s["controls_with_indexed_exact_source"], 1)

    def test_failure_does_not_count_as_negative_evidence(self):
        cases = [self.records[0], self.records[1]]
        report, stat = gold.evaluate(cases, [{
            "control_id": "G01", "status": "request_error", "matches": []
        }])
        self.assertEqual(report[0]["outcome"], "search_failed_or_unavailable")
        self.assertEqual(report[1]["outcome"], "not_executed")
        self.assertEqual(stat["controls_without_executed_search"], 1)
        self.assertTrue(all(x["source_recall_assertion"] == "no_claim_of_historical_absence"
                            for x in report))

    def test_no_gold_url_or_account_in_shipped_search_plan(self):
        plans = gold.plan(self.records)
        for task in plans:
            control = next(x for x in self.records if x["control_id"] == task["control_id"])
            self.assertNotIn(control["target_url"].lower(), task["index_query"].lower())
            path = control["target_url"].split("?", 1)[0].rstrip("/").rsplit("/", 1)[-1]
            if len(path) >= 12:
                self.assertNotIn(path.lower(), task["index_query"].lower())

    def test_bad_controls_and_unknown_result(self):
        with self.assertRaises(ValueError):
            gold.load_gold(Path("/this/file/should/not/exist.tsv"))
        cases = [self.records[0]]
        with self.assertRaises(ValueError):
            gold.evaluate(cases, [{"control_id": "NOT_REAL", "status": "index_search_success"}])

if __name__ == "__main__":
    unittest.main()
