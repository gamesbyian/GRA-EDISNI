"""Cross-pipeline failure accounting regressions (offline, no HTTP)."""
from __future__ import annotations
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

harvest = load_module("ce_harvest_health", "scripts/external_evidence/harvest_public.py")
images = load_module("ce_image_extraction_health", "scripts/external_evidence/discover_html_images.py")

class CrossPipelineFailureAccounting(unittest.TestCase):
    def test_acquisition_success_means_payload_not_zero_exit(self):
        good = {"source_id": "ok", "kind": "youtube", "classification": "ok",
                "files": [{"path": "ok/film.info.json", "size": 700}]}
        failure = {"source_id": "blocked", "kind": "webpage",
                   "classification": "webpage-fetch-failed",
                   "exit_code": 1, "files": []}
        empty = {"source_id": "empty", "kind": "youtube",
                 "classification": "ok", "exit_code": 0, "files": []}
        health = harvest.acquisition_health([good, failure, empty])
        self.assertEqual(health["selected_sources"], 3)
        self.assertEqual(health["acquired_payload_sources"], 1)
        self.assertEqual(health["not_acquired_sources"], 1)
        self.assertEqual(health["success_without_payload"], 1)
        self.assertFalse(health["all_selected_acquired_payload"])
        self.assertTrue(harvest.acquisition_health([good])["all_selected_acquired_payload"])
        self.assertFalse(harvest.acquisition_health([])["all_selected_acquired_payload"])

    def test_metadata_file_is_not_an_acquired_source(self):
        no_payload = {"source_id": "empty", "kind": "youtube",
                      "classification": "ok",
                      "files": [{"path": "empty/acquisition.json", "size": 900}]}
        health = harvest.acquisition_health([no_payload])
        self.assertEqual(health["success_without_payload"], 1)

    def test_html_extractor_reports_skipped_sources_and_pages(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sources = root / "acquired"
            valid = sources / "valid"
            valid.mkdir(parents=True)
            (valid / "acquisition.json").write_text(
                json.dumps({"source_id": "valid",
                            "url": "https://example.org/article"}))
            (valid / "page.html").write_text(
                '<html><img src="/p.jpg" alt="INSIDE CE"></html>')
            (valid / "too-big.html").write_text("X" * 100)
            invalid = sources / "invalid"
            invalid.mkdir()
            (invalid / "acquisition.json").write_text("invalid-json")
            missing = sources / "missing"
            missing.mkdir()
            (missing / "acquisition.json").write_text(json.dumps({"source_id": "missing"}))
            output = root / "candidate-images.json"
            with patch.object(sys, "argv", [
                    "discover_html_images.py", "--acquired", str(sources),
                    "--output", str(output), "--max-html-bytes", "70"]):
                images.main()
            result = json.loads(output.read_text())
            coverage = result["source_coverage"]
            self.assertEqual(coverage["source_metadata_files"], 3)
            self.assertEqual(coverage["invalid_metadata_files"], 1)
            self.assertEqual(coverage["metadata_without_public_url"], 1)
            self.assertEqual(coverage["html_pages_seen"], 2)
            self.assertEqual(coverage["oversized_html_pages"], 1)
            self.assertEqual(coverage["readable_html_pages"], 1)
            self.assertEqual(len(result["image_mentions"]), 1)
            self.assertEqual(result["unscanned_or_skipped_html"], 3)
            self.assertEqual(result["image_mentions"][0]["source_page_url"],
                             "https://example.org/article")

if __name__ == "__main__":
    unittest.main()
