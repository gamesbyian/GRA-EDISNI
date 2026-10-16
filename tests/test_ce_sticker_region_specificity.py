"""No-network specificity controls, pinned-original holdout and media-source safety."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.external_evidence.benchmark_sticker_region_stress import (
    SIZE, NEGATIVE_KINDS, PATCH_FRACTIONS, DISTANCE_CUTOFFS,
    challenge, composite, scene_background,
)
from scripts.external_evidence.benchmark_sticker_region_real_negatives import (
    PINNED_ROLES, sources_to_scan, report_negatives,
)
from scripts.external_evidence.benchmark_sticker_region_holdout import load_holdouts
from scripts.external_evidence.visual_region_probe import load_regions, scan

ROOT=Path(__file__).resolve().parents[1]


class SpecificityChallengeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.refs=load_regions(ROOT/"data/reference/inside-ce-sticker-region-pilot-rois.csv",ROOT)
        cls.holdouts=load_holdouts(ROOT/"data/reference/inside-ce-sticker-region-independent-holdout.csv",
                                 ROOT,{x["reference_id"] for x in cls.refs})

    def test_frozen_adversarial_backgrounds_do_not_contain_source_original_crops(self):
        self.assertEqual(len(NEGATIVE_KINDS),4)
        self.assertEqual(PATCH_FRACTIONS,(0.01,0.03,0.08))
        self.assertEqual(DISTANCE_CUTOFFS,(24,32,40,48,56,65))
        digests=[]
        for kind in NEGATIVE_KINDS:
            image=scene_background(kind)
            self.assertEqual(image.size,SIZE)
            digests.append(hashlib.sha256(image.tobytes()).hexdigest())
            self.assertEqual(image.tobytes(),scene_background(kind).tobytes())
        self.assertEqual(len(set(digests)),4)

    def test_smaller_sticker_is_fixed_fraction_and_has_disjoint_original_photo(self):
        case=self.holdouts[0]
        area=[]
        for idx,fraction in enumerate(PATCH_FRACTIONS):
            scene, box=composite(case,ROOT,fraction,idx)
            self.assertEqual(scene.size,SIZE)
            occupied=(box[2]-box[0])*(box[3]-box[1])/(SIZE[0]*SIZE[1])
            self.assertAlmostEqual(occupied,fraction,delta=0.004)
            area.append(occupied)
        self.assertLess(area[0],area[1])
        self.assertLess(area[1],area[2])
        self.assertFalse(any(r["reference_id"]=="sticker-"+case["serial"] for r in self.refs))
        with self.assertRaisesRegex(ValueError,"unfrozen"):
            composite(case,ROOT,0.025,0)

    def test_no_claim_of_classification_on_lookalike_negative(self):
        scene=scene_background("ticket-with-slash")
        hypotheses, stats=scan(scene,self.refs,max_windows=250,
                               max_refine_windows=0,max_suggestions=8)
        self.assertTrue(stats["not_exhaustive_when_capped"])
        self.assertTrue(all(p["new_sticker_confirmed"] is False for p in hypotheses))
        self.assertTrue(all(p["evidence_grade"]=="unvalidated-region-similarity-only"
                            for p in hypotheses))

    def test_challenge_cannot_be_silently_retuned_on_known_sources(self):
        with self.assertRaisesRegex(ValueError,"frozen"):
            challenge(self.refs,self.holdouts,ROOT,max_windows=150)
        with self.assertRaisesRegex(ValueError,"frozen"):
            challenge(self.refs,self.holdouts,ROOT,top_k=1)
        with self.assertRaisesRegex(ValueError,"expects exactly four"):
            challenge(self.refs,self.holdouts[:2],ROOT)
        with self.assertRaisesRegex(ValueError,"expects five"):
            challenge(self.refs[:4],self.holdouts,ROOT)

    def test_real_image_negative_controls_are_sha_pinned_and_fail_closed(self):
        manifest=json.loads((ROOT/"data/reference/inside-ce-visual-sources.json").read_text())
        pinned=[x for x in manifest["sources"]
                if x.get("expected_sha256") and x.get("role") in PINNED_ROLES]
        self.assertGreaterEqual(len(pinned),5)
        self.assertTrue(any(x["role"]=="positive-control-public-owner-open-ce-no-visible-sticker"
                            for x in pinned))
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            good=Image.new("RGB",(120,90),"black")
            path=root/"synthetic-original.jpg"
            good.save(path)
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            fixture={"sources":[{"id":"synthetic-original","extension":".jpg",
                                 "role":"negative-control-standalone",
                                 "expected_sha256":digest,
                                 "url":"https://example.org/provenance"}]}
            images, missing=sources_to_scan(fixture,root)
            self.assertEqual(len(images),1)
            self.assertEqual(missing,[])
            self.assertEqual(images[0]["sha256"],digest)
            report=report_negatives(fixture,root,self.refs)
            self.assertEqual(report["negative_controls_scanned"],1)
            self.assertEqual(report["new_confirmed_stickers"],0)
            self.assertTrue(all(x["scanned_negative_images"]==1
                                for x in report["operating_points"]))
            fixture["sources"][0]["expected_sha256"]="f"*64
            with self.assertRaisesRegex(ValueError,"digest mismatch"):
                sources_to_scan(fixture,root)
            fixture["sources"][0]["id"]="../escape"
            with self.assertRaisesRegex(ValueError,"source ID"):
                sources_to_scan(fixture,root)
            with self.assertRaisesRegex(ValueError,"frozen"):
                report_negatives({"sources":[]},root,self.refs,max_windows=200)

    def test_unacquired_negative_is_explicit_not_implicitly_sticker_free(self):
        manifest=json.loads((ROOT/"data/reference/inside-ce-visual-sources.json").read_text())
        with tempfile.TemporaryDirectory() as temp:
            result=report_negatives(manifest,Path(temp),self.refs)
        self.assertEqual(result["negative_controls_scanned"],0)
        self.assertGreater(result["negative_controls_expected"],0)
        self.assertEqual(len(result["unavailable_or_invalid_source_controls"]),
                         result["negative_controls_expected"])
        self.assertEqual(result["new_confirmed_stickers"],0)
        self.assertTrue(all(point["scanned_negative_images"]==0
                            for point in result["operating_points"]))


if __name__=="__main__":
    unittest.main()
