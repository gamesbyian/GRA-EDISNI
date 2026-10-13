"""Offline invariants for the global gaming-forum campaign planner."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "scripts/plan_global_forum_searches.py"
spec = importlib.util.spec_from_file_location("forum_search_plan", FILE)
planner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(planner)


class TestGlobalForumSearchPlan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = planner.load_tsv(planner.DIRECTORY)
        cls.routes = planner.load_tsv(planner.ROUTES)

    def test_exact_inventory_coverage(self):
        self.assertEqual(len(self.directory), 483)
        self.assertEqual(len(self.routes), 483)
        planner.check_routes(self.directory, self.routes)

    def test_multiple_arbitrary_queries_and_escaping(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / "tasks.jsonl"
            terms = ['INSIDE \"collector edition\"', "內幕 貼紙", "привет код"]
            stats = planner.generate(self.directory, self.routes, terms, "literal",
                                     1500, output, {"V", "C", "H"})
            self.assertEqual(stats["task_count"], 483 * len(terms))
            results = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual(len(results), len({r["task_id"] for r in results}))
            self.assertTrue(all(r["state"] == "planned_unexecuted" for r in results))
            self.assertTrue(all(r["results"] == [] for r in results))
            self.assertTrue(any(r["term"] == "內幕 貼紙" for r in results))
            self.assertTrue(all(r["index_query"].startswith("site:") for r in results))

    def test_constrained_query_cap(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                planner.generate(self.directory, self.routes, ["INSIDE"], "literal",
                                 482, Path(d) / "tasks.jsonl", {"V", "C", "H"})

    def test_scope_separation(self):
        row = next(x for x in self.routes if x["community"] == "r/PlaydeadsInside")
        self.assertEqual(row["index_query_scope"], "site:reddit.com/r/PlaydeadsInside")
        self.assertEqual(row["primary_method"], "reddit_oauth_search")
        native = planner.conditional_native_link(row, "sticker /043")
        self.assertIn("restrict_sr=1", native)
        self.assertIn("sticker+%2F043", native)

    def test_unverified_host_not_claimed_as_verified(self):
        row = next(x for x in self.routes if x["community"] == "ResetEra Gaming")
        self.assertEqual(row["classification_basis"], "unconfirmed_engine_hint")
        self.assertEqual(row["gha_mode"], "browser_after_probe")

    def test_source_inventory_is_immutable(self):
        for x in self.directory:
            self.assertIn(x["evidence_status"], {"V", "C", "H"})


if __name__ == "__main__":
    unittest.main()
