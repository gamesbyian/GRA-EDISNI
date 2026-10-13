"""Exact all-period selected-null regression for CE glyph observations."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "period_null", ROOT / "scripts" / "audit_ce_period_selection_null.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CEPeriodSelectionNullTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actual = MODULE.audit(ROOT / "data" / "observations.csv")
        cls.saved = json.loads(
            (ROOT / "data" / "ce-period-selection-null-2026-10-12.json")
            .read_text(encoding="utf-8"))

    def test_exact_saved_integer_counts(self):
        self.assertEqual(self.actual, self.saved)
        self.assertEqual(self.actual["denominator"], 37399079244620030691600)
        self.assertEqual(self.actual["union_bound_numerator"], 377822188953098255)
        self.assertEqual(self.actual["physical_observations"], 84)
        self.assertEqual((self.actual["body_entries"], self.actual["tail_entries"]),
                         (72, 12))
        self.assertEqual((self.actual["body_slashes"], self.actual["tail_slashes"]),
                         (44, 4))

    def test_all_observable_periods_and_post_selection(self):
        a = self.actual
        self.assertEqual(a["maximum_observable_period"], 595)
        self.assertEqual(a["period_range"], [1, 595])
        self.assertEqual(a["minimum_repeat_support"], 18)
        self.assertEqual((a["eligible_periods"], a["nonzero_null_periods"]),
                         (137, 27))
        self.assertAlmostEqual(a["union_bound_upper_probability"],
                               1.0102446279006965e-05, places=15)

    def test_fixed_108_is_within_union_bound(self):
        a = self.actual
        p108 = next(x for x in a["candidate_nulls"] if x["period"] == 108)
        self.assertEqual(p108["repeat_excess"], 18)
        self.assertEqual(p108["favorable_assignments"], 217839326948876160)
        self.assertAlmostEqual(p108["fixed_period_null_probability"],
                               5.824724334094749e-06, places=15)
        self.assertLess(p108["fixed_period_null_probability"],
                        a["union_bound_upper_probability"])

    def test_tiny_groupwise_oracle(self):
        MODULE.small_oracle()
        self.assertEqual(MODULE.favorable([(2, 0)], 1, 0), 0)
        self.assertEqual(MODULE.favorable([(2, 0)], 2, 0), 1)
        self.assertEqual(MODULE.favorable([(1, 1)], 1, 1), 1)
        self.assertEqual(MODULE.favorable([(1, 1)], 0, 0), 0)


if __name__ == "__main__":
    unittest.main()
