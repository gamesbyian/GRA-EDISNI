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

    def test_gold_locator_scope_and_known_answer_leak(self):
        tasks = gold.plan(self.records)
        by = {(x["control_id"], x["gold_search_variant"]): x for x in tasks}
        for variant in ("a", "b"):
            self.assertEqual(by[("G05", variant)]["site_scope"], "ebay.com")
            self.assertEqual(by[("G05", variant)]["gold_target_locator_quality"],
                             "short_redirect_requires_original_listing")
            self.assertEqual(by[("G10", variant)]["gold_target_locator_quality"],
                             "profile_not_original_image_post")
            self.assertNotIn("328", by[("G08", variant)]["index_query"])
        self.assertEqual(by[("G07", "a")]["site_scope"], "twitter.com")
        self.assertEqual(by[("G07", "b")]["site_scope"], "x.com")

    def test_x_com_is_same_exact_post_not_a_new_owner(self):
        case = next(x for x in self.records if x["control_id"] == "G07")
        report, summary = gold.evaluate([case], [
            {"control_id": "G07", "status": "index_search_success",
             "matches": [{"url":
                "https://x.com/KaydHendricks/status/1205585260207050753"}]}
        ])
        self.assertEqual(report[0]["outcome"], "exact_source_found")
        self.assertEqual(report[0]["exact_source_matches"], 1)
        self.assertEqual(summary["controls_with_indexed_exact_source"], 1)

    def test_shortlink_and_account_profile_cannot_pass_original_photo_recall(self):
        cases = [x for x in self.records if x["control_id"] in ("G05", "G10")]
        report, summary = gold.evaluate(cases, [
            {"control_id": x["control_id"], "status": "index_search_success",
             "matches": [{"url": x["target_url"]}]}
            for x in cases
        ])
        by = {x["control_id"]: x for x in report}
        self.assertEqual(by["G05"]["outcome"], "original_locator_unscorable")
        self.assertEqual(by["G10"]["outcome"], "original_locator_unscorable")
        self.assertFalse(by["G05"]["original_source_recall_scoreable"])
        self.assertFalse(by["G10"]["original_source_recall_scoreable"])
        self.assertEqual(summary["controls_with_unscoreable_original_locator"], 2)
        self.assertEqual(summary["controls_with_indexed_exact_source"], 0)

    def test_pure_offline_plan_is_accepted_as_zero_execution(self):
        report, summary = gold.evaluate(self.records, gold.plan(self.records))
        self.assertEqual(summary["queries_attempted"], 0)
        self.assertEqual(summary["queries_explicitly_unattempted"], 24)
        self.assertEqual(summary["controls_without_executed_search"], 12)
        self.assertEqual(summary["controls_with_unscoreable_original_locator"], 2)
        self.assertEqual(summary["controls_with_indexed_exact_source"], 0)
        self.assertTrue(all(x["source_recall_assertion"] == "no_claim_of_historical_absence"
                            for x in report))

    def test_skipped_task_is_not_attempted_or_provider_failure(self):
        case = next(x for x in self.records if x["control_id"] == "G06")
        tasks = gold.plan([case])
        report, summary = gold.evaluate([case], [
            {"task_id": t["task_id"], "status": "not_attempted", "matches": []}
            for t in tasks
        ])
        self.assertEqual(report[0]["outcome"], "not_executed")
        self.assertEqual(report[0]["provider_queries_attempted"], 0)
        self.assertEqual(report[0]["provider_queries_explicitly_unattempted"], 2)
        self.assertEqual(summary["queries_explicitly_unattempted"], 2)
        self.assertEqual(summary["queries_attempted"], 0)

    def test_successful_empty_one_page_is_partial_not_exhaustive_failure(self):
        case = next(x for x in self.records if x["control_id"] == "G06")
        report, summary = gold.evaluate([case], [{
            "control_id": "G06", "status": "index_search_success", "matches": []}])
        self.assertEqual(report[0]["outcome"], "partial_index_inconclusive")
        self.assertEqual(report[0]["provider_queries_without_result_record"], 1)
        self.assertEqual(summary["queries_succeeded"], 1)
        self.assertEqual(summary["queries_not_represented_in_results"], 1)
        self.assertEqual(report[0]["source_recall_assertion"], "no_claim_of_historical_absence")

    def test_duplicate_or_conflicting_task_results_are_invalid(self):
        case = next(x for x in self.records if x["control_id"] == "G06")
        task = gold.plan([case])[0]
        duplicated = {"task_id": task["task_id"],
                      "control_id": "G06", "status": "index_search_success", "matches": []}
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            gold.evaluate([case], [duplicated, duplicated])
        with self.assertRaisesRegex(ValueError, "does not belong"):
            gold.evaluate(self.records, [dict(duplicated, control_id="G07")])
        with self.assertRaisesRegex(ValueError, "Unrecognized gold"):
            gold.evaluate([case], [{"control_id": "G06", "status": "something_unknown"}])

    def test_mixed_cyrillic_latin_source_query_rejected(self):
        case = next(x for x in self.records if x["control_id"] == "G10")
        self.assertEqual(gold.mixed_latin_cyrillic_words(
            "INSIDE Playdead коллекционное издание хaдл распаковка"), ["хaдл"])
        self.assertEqual(gold.mixed_latin_cyrillic_words(
            "INSIDE Playdead коллекционное издание хаддл распаковка"), [])
        with self.assertRaisesRegex(ValueError, "Mixed Latin-Cyrillic"):
            gold.plan([dict(case, source_discovery_query_a="INSIDE хaдл")])
        self.assertEqual(len(gold.plan([case])), 2)

    def test_future_known_serial_leak_rejected_but_years_allowed(self):
        case = next(x for x in self.records if x["control_id"] == "G08")
        deliberately_leaked = dict(case, source_discovery_query_b=
                                  "Playdead owner sticker 328 reddit")
        with self.assertRaisesRegex(ValueError, "serial leaked"):
            gold.plan([deliberately_leaked])
        historical_year = dict(case, source_discovery_query_b=
                               "INSIDE CE unboxing 2019")
        self.assertEqual(len(gold.plan([historical_year])), 2)

    def test_bad_controls_and_unknown_result(self):
        with self.assertRaises(FileNotFoundError):
            gold.load_gold(Path("/this/file/should/not/exist.tsv"))
        cases = [self.records[0]]
        with self.assertRaises(ValueError):
            gold.evaluate(cases, [{"control_id": "NOT_REAL", "status": "index_search_success"}])

if __name__ == "__main__":
    unittest.main()
