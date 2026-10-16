"""Strict source/disjointness/evidence invariant tests for independent CE ROI holdouts."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.external_evidence.benchmark_sticker_region_holdout import (
    evaluate_holdouts,load_holdouts
)
from scripts.external_evidence.visual_region_probe import load_regions

REPO=Path(__file__).resolve().parents[1]
REF=REPO/"data/reference/inside-ce-sticker-region-pilot-rois.csv"
HOLD=REPO/"data/reference/inside-ce-sticker-region-independent-holdout.csv"


class IndependentRegionHoldoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.references=load_regions(REF,REPO)
        cls.ids={r["reference_id"] for r in cls.references}

    def test_pinned_real_photo_holdout_is_disjoint(self):
        cases=load_holdouts(HOLD,REPO,self.ids)
        self.assertEqual({x["serial"] for x in cases},
                         {"039","047","063","118"})
        self.assertEqual({x["serial"] for x in cases}&
                         {x.removeprefix("sticker-") for x in self.ids},set())
        self.assertTrue(all(x["source_sha256"] and
                            len(x["source_sha256"])==64 for x in cases))

    def test_actual_source_region_scoring_is_not_owner_or_serial_recognition(self):
        cases=load_holdouts(HOLD,REPO,self.ids)
        # Record measured true outcomes rather than assuming our present
        # descriptor generalizes. Do not relax the threshold after failures.
        report=evaluate_holdouts(cases,self.references,REPO,
                                 max_windows=1600,max_refine_windows=1200,top_k=8)
        summary=report["summary"]
        self.assertEqual(summary["holdout_photographs"],4)
        self.assertEqual(summary["reference_unique_photographs"],5)
        self.assertFalse(summary["false_positive_rate_measured"])
        self.assertTrue(summary["reference_vs_holdout_serial_disjoint"])
        self.assertEqual(summary["new_confirmed_stickers"],0)
        self.assertLessEqual(summary["detected_at_iou_060"],
                             summary["detected_at_iou_040"])
        self.assertLessEqual(summary["detected_at_iou_040"],
                             summary["detected_at_iou_025"])
        self.assertLessEqual(summary["detected_at_iou_025"],4)
        for record in report["cases"]:
            self.assertFalse(record["new_sticker_confirmed"])
            self.assertGreaterEqual(record["best_topk_box_iou"],0)
            self.assertLessEqual(record["best_topk_box_iou"],1)
            self.assertEqual(len(record["ground_truth_xyxy_original_pixels"]),4)
            self.assertTrue(record["reference_templates_disjoint"])
            self.assertTrue(all(p["new_sticker_confirmed"] is False
                                for p in record["suggestions"]))

    def test_reference_leak_and_sha_tamper_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            src=HOLD.read_text(encoding="utf-8")
            swapped=Path(temp)/"bad.csv"
            swapped.write_text(src.replace("039,","003,",1),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"also in"):
                load_holdouts(swapped,REPO,self.ids)
            swapped.write_text(src.replace("d00931f4","00000000"),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"digest mismatch"):
                load_holdouts(swapped,REPO,self.ids)


if __name__=="__main__":
    unittest.main()
