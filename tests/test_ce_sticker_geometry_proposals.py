"""No-network OpenCV geometry proposal tests with explicit false-positive semantics."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import cv2
from PIL import Image,ImageDraw

from scripts.external_evidence.visual_geometry_proposals import propose,scan_index
from scripts.external_evidence.visual_region_probe import box_iou,sha256
from scripts.external_evidence.benchmark_sticker_region_stress import scene_background


class GeometryProposalTests(unittest.TestCase):
    def test_white_small_paper_without_claiming_a_sticker(self):
        scene=Image.new("RGB",(720,540),(48,55,62))
        d=ImageDraw.Draw(scene)
        target=[440,280,502,342]
        d.rectangle(target,fill=(231,226,218))
        d.polygon([(464,321),(471,321),(492,300),(484,300)],fill=(17,18,18))
        d.text((466,333),"039",fill=(24,25,26))
        proposals,stats=propose(scene)
        self.assertTrue(proposals,"expected generic white-paper box candidate")
        self.assertTrue(any(box_iou(x["bbox_xyxy_original_pixels"],target)>=.50
                            for x in proposals))
        self.assertEqual(stats["method"],"opencv-otsu-fixed-sweep-external-contours")
        self.assertGreater(stats["all_contours_considered"],0)
        self.assertTrue(all(x["new_sticker_confirmed"] is False for x in proposals))
        self.assertTrue(all(x["candidate_type"]=="bright-rectangle-unverified" for x in proposals))
        self.assertTrue(stats["negative_specificity_not_established"])

    def test_deceptive_sticker_free_scene_is_not_claimed_clean(self):
        image=scene_background("ticket-with-slash")
        proposals,stats=propose(image,max_proposals=8)
        self.assertTrue(all(x["new_sticker_confirmed"] is False for x in proposals))
        self.assertLessEqual(len(proposals),8)
        self.assertGreater(len(stats["thresholds_attempted"]),0)

    def test_blank_scene_no_auto_claim(self):
        im=Image.new("RGB",(400,300),(85,85,85))
        proposals,counts=propose(im,max_proposals=8)
        self.assertEqual(proposals,[])
        self.assertEqual(counts["retained_after_dedup_and_budget"],0)
        with self.assertRaises(ValueError):
            propose(im,max_proposals=0)
        with self.assertRaises(ValueError):
            propose(im,max_proposals=201)

    def test_acquisition_digest_and_safe_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            p=root/"known.jpg"
            Image.new("RGB",(300,300),"white").save(p)
            manifest={"candidates":[
                {"id":"good","path":"known.jpg","sha256":sha256(p),
                 "source_kind":"sourceA","source_url":"https://example.org/photo"},
                {"id":"unsafe","path":"../outside.jpg","sha256":"0"*64,
                 "source_kind":"sourceB"},
                {"id":"mismatch","path":"known.jpg","sha256":"f"*64,
                 "source_kind":"sourceC"}]}
            report=scan_index(manifest,root,max_files=3,max_proposals=8)
            self.assertEqual(report["source_images_examined"],1)
            self.assertEqual(len(report["source_images_failed"]),2)
            self.assertEqual(report["new_confirmed_stickers"],0)
            self.assertTrue(all(x["new_sticker_confirmed"] is False
                                for x in report["candidates"]))


if __name__=="__main__":
    unittest.main()
