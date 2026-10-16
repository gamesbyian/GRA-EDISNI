"""Offline calibrated *feasibility* tests for candidate ROI matching.

Synthetic positives paste crops of documented original physical sticker photos.
They test resizing/placement, not independently photographed stickers. Negative
controls probe false-positive review ranks; no result proves sticker identity.
"""
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.external_evidence.visual_region_probe import (
    FRACTIONS, box_iou, diverse_candidates, fingerprint, load_regions, proxy_image, run, scan, select_windows, sha256
)


REPO=Path(__file__).resolve().parents[1]
MANIFEST=REPO/"data/reference/inside-ce-sticker-region-pilot-rois.csv"


def actual_template(serial):
    import csv
    with MANIFEST.open(encoding="utf-8",newline="") as f:
        row=next(r for r in csv.DictReader(f) if r["serial"]==serial)
    path=REPO/row["source_path"]
    with Image.open(path) as original:
        image=original.convert("RGB")
        box=[round(float(row[k])*dim) for k,dim in zip(
             ("left","top","right","bottom"),
             (image.width,image.height,image.width,image.height))]
        return image.crop(tuple(box))


def scene_with_patch(serial, *, angle=0, scale=(108,108), xy=(403,279)):
    scene=Image.new("RGB",(720,540),(65,74,82))
    draw=ImageDraw.Draw(scene)
    draw.rectangle((25,25,190,85), fill=(170,152,134))
    draw.ellipse((250,35,365,160),fill=(98,30,35))
    draw.rectangle((510,85,670,170), fill=(208,206,200))
    patch=actual_template(serial).rotate(angle,expand=True).resize(scale,Image.Resampling.LANCZOS)
    scene.paste(patch,xy)
    return scene, list((*xy,xy[0]+patch.width,xy[1]+patch.height))


class RegionPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.refs=load_regions(MANIFEST,REPO)

    def test_source_original_sha_and_explicit_crops(self):
        self.assertEqual(len(self.refs),20)
        self.assertEqual(set(r["reference_id"] for r in self.refs),
                         {"sticker-003","sticker-037","sticker-038",
                          "sticker-065","sticker-125"})
        self.assertEqual(set(x["reference_rotation_degrees"] for x in self.refs),
                         {0,90,180,270})
        self.assertTrue(all(r["reference_source_sha256"] and
                            len(r["reference_source_sha256"])==64 for r in self.refs))

    def test_multiscale_windows_cover_corner_and_late_spatial_regions(self):
        regions,cov=select_windows(720,540,1200)
        self.assertGreater(cov["proposed_windows"],cov["scored_windows"])
        self.assertEqual(cov["scored_windows"],1200)
        self.assertEqual(cov["proposed_windows"]-cov["scored_windows"],
                         cov["windows_omitted_at_cap"])
        self.assertTrue(cov["not_exhaustive_when_capped"])
        self.assertGreaterEqual(cov["strata_sampled"],12)
        self.assertTrue(any(x[0]>350 and x[1]>250 for x in regions))
        self.assertTrue(any(x[0]<100 and x[1]<100 for x in regions))
        self.assertEqual((regions,cov),select_windows(720,540,1200))
        with self.assertRaises(ValueError):
            select_windows(720,540,0)

    def test_actual_original_sticker_patch_within_collector_scene(self):
        scene,realbox=scene_with_patch("037")
        results,cov=scan(scene,self.refs,max_windows=2200,max_suggestions=12)
        self.assertGreaterEqual(cov["scored_windows"],1000)
        self.assertEqual(cov["suggestions_shown"],len(results))
        self.assertTrue(all(r["new_sticker_confirmed"] is False for r in results))
        self.assertTrue(any(box_iou(x["bbox_xyxy_original_pixels"],realbox) >= .40
                            for x in results[:12]),
                        f"actual original sticker patch region missed: {results[:3]}")

    def test_rotated_photo_is_review_only(self):
        scene,realbox=scene_with_patch("003",angle=90)
        results,cov=scan(scene,self.refs,max_windows=2200,max_suggestions=15)
        self.assertTrue(results)
        self.assertTrue(any(box_iou(x["bbox_xyxy_original_pixels"],realbox) >= .30
                            for x in results),
                        "rotation produced no useful candidate region")
        self.assertEqual({x["evidence_grade"] for x in results},
                         {"unvalidated-region-similarity-only"})

    def test_negative_and_coverage_without_false_identity(self):
        scene=Image.new("RGB",(720,540),(125,126,127))
        draw=ImageDraw.Draw(scene)
        draw.rectangle((400,280,510,390),fill="white")
        draw.rectangle((425,330,490,338),fill="black")
        hits,coverage=scan(scene,self.refs,max_windows=300,max_suggestions=6)
        self.assertTrue(coverage["not_exhaustive_when_capped"])
        self.assertLessEqual(len(hits),6)
        # Even if a visually similar decoy ranks highly, never a numbered discovery.
        self.assertTrue(all(h["new_sticker_confirmed"] is False for h in hits))

    def test_roi_batch_budget_reaches_later_source_groups(self):
        sources = [{"id":f"first-{i}","source_kind":"A","path":f"{i}.jpg"}
                   for i in range(12)]
        sources += [{"id":"late1","source_kind":"Z","path":"x.jpg"},
                    {"id":"late2","source_kind":"Z","path":"y.jpg"}]
        chosen=diverse_candidates(sources,3)
        self.assertEqual([x["id"] for x in chosen],["first-0","late1","first-1"])
        self.assertEqual(len({x["source_kind"] for x in chosen}),2)
        self.assertEqual(chosen,diverse_candidates(sources,3))
        with self.assertRaises(ValueError):
            diverse_candidates(sources,0)

    def test_digest_is_provenance_gate_and_cap_visible(self):
        scene,box=scene_with_patch("037")
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            path=root/"accepted.jpg"
            scene.save(path)
            rows={"candidates":[
              {"id":"c1","path":"accepted.jpg","sha256":sha256(path),
               "source_kind":"public-test","source_url":"https://example.org/p"},
              {"id":"c2","path":"../outside.jpg","sha256":"0"*64},
              {"id":"c3","path":"accepted.jpg","sha256":"0"*64}]}
            result=run(rows,self.refs,root,max_files=2,max_windows=250)
            self.assertEqual(result["candidate_files_selected"],2)
            self.assertEqual(result["candidate_files_not_scanned_by_cap"],1)
            self.assertEqual(result["candidate_files_scanned"],1)
            self.assertEqual(result["errors"][0]["failure"],"unavailable_or_unsafe_image")
            result2=run({"candidates":[rows["candidates"][2]]},
                        self.refs,root,max_files=1,max_windows=250)
            self.assertEqual(result2["errors"][0]["failure"],"source_digest_mismatch")
            self.assertEqual(result2["new_confirmed_stickers"],0)

    def test_pixel_and_origin_guard(self):
        with self.assertRaises(ValueError):
            proxy_image(Image.new("RGB",(400,300)),long_side=0).load()
        self.assertGreater((fingerprint(actual_template("037"))[0]),0)
        self.assertEqual(box_iou([0,0,100,100],[100,100,200,200]),0.0)


if __name__=="__main__":
    unittest.main()
