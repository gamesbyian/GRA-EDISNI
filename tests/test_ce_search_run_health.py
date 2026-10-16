"""Evidence-accounting gold controls for all major CE public search surfaces."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "search_health", ROOT / "scripts/audit_ce_search_run_health.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class PublicSearchHealthTests(unittest.TestCase):
    def test_planned_is_not_executed(self):
        result = m.health("brave_index", [
            {"task_id": "x", "status": "planned_unexecuted", "matches": []}])
        self.assertEqual(result["counts"]["not_attempted"], 1)
        self.assertEqual(result["counts"].get("valid_provider_responses", 0), 0)
        self.assertIn("some_tasks_never_attempted", result["flags"])
        self.assertEqual(result["new_confirmed_stickers"], 0)

    def test_truncated_success_not_complete_recall(self):
        result = m.health("bluesky", {
            "state": "executed_bounded",
            "results": [
                {"kind": "direct_control", "status": "ok"},
                {"kind": "blind_discovery", "status": "ok",
                 "posts": [{"uri": "at://x"}], "cursor_available": True},
                {"kind": "blind_discovery", "status": "error", "http_status": 403},
                {"kind": "blind_discovery", "status": "skipped_after_endpoint_access_failure"}
            ]})
        self.assertEqual(result["counts"]["source_direct_controls"], 1)
        self.assertEqual(result["counts"]["valid_provider_responses"], 1)
        self.assertEqual(result["counts"]["provider_failures"], 1)
        self.assertEqual(result["counts"]["not_attempted"], 1)
        self.assertEqual(result["counts"]["potentially_truncated_query_pages"], 1)
        self.assertIn("first_page_does_not_establish_recall", result["flags"])

    def test_web_index_empty_success_not_historical_absence(self):
        result = m.health("brave_index", [
            {"status": "index_search_success", "matches": []},
            {"status": "request_error", "matches": []}])
        self.assertEqual(result["counts"]["valid_provider_responses"], 1)
        self.assertEqual(result["counts"]["provider_failures"], 1)
        self.assertEqual(result["new_confirmed_stickers"], 0)

    def test_cdx_rate_limit_preserves_unattempted_slots(self):
        result = m.health("wayback_cdx", [
            {"status": "http_error", "http_status": 429},
            {"status": "not_attempted_after_provider_block"}])
        self.assertEqual(result["row_count"], 2)
        self.assertEqual(result["counts"]["not_attempted"], 1)

    def test_reddit_candidate_cap_is_recorded(self):
        result = m.health("reddit_archive", [
            {"status": "ok", "returned": 10, "page_limit": 10,
             "possibly_truncated": True, "new_candidates_omitted_at_cap": 4},
            {"status": "not-attempted"}])
        self.assertEqual(result["counts"]["qualified_candidates_dropped_by_cap"], 4)
        self.assertIn("qualified_candidates_dropped", result["flags"])

    def test_acquisition_outcome_vs_process(self):
        result = m.health("public_harvest", {"sources": [
            {"classification": "ok", "files": [{"size": 100, "path": "x.bin"}]},
            {"classification": "ok", "files": []},
            {"classification": "webpage-fetch-failed", "files": []}]})
        self.assertEqual(result["counts"]["source_payload_acquired"], 1)
        self.assertEqual(result["counts"]["success_without_payload"], 1)
        self.assertEqual(result["counts"]["not_acquired"], 1)
        self.assertIn("zero_payload_despite_success_classification", result["flags"])

    def test_html_source_skips_do_not_become_zero_image_proof(self):
        x = m.health("html_images", {
            "source_coverage": {
                "source_metadata_files": 2, "html_pages_seen": 3,
                "readable_html_pages": 0, "oversized_html_pages": 3},
            "image_mentions": []})
        self.assertIn("source_pages_not_inspected", x["flags"])
        self.assertIn("no_html_body_scanned", x["flags"])

    def test_json_object_jsonl_and_empty_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "sample"
            file.write_text('{"status":"ok"}\n{"status":"error"}\n')
            self.assertEqual(len(m.load_input(file)), 2)
            file.write_text(json.dumps({"results": [{"status": "ok"}]}))
            self.assertEqual(len(m.load_input(file)["results"]), 1)
            file.write_text("")
            with self.assertRaises(ValueError):
                m.load_input(file)
        with self.assertRaises(ValueError):
            m.health("bad", {})
        with self.assertRaises(ValueError):
            m.health("brave_index", {"results": []})

if __name__ == "__main__":
    unittest.main()
