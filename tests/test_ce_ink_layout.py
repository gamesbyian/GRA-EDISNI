"""Offline OCR-free image-region print-layout descriptor QA."""
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image,ImageDraw

from scripts.external_evidence.visual_ink_layout import (
    ink_layout,validate_geometry,annotate)
from scripts.external_evidence.visual_region_probe import sha256
from scripts.external_evidence.benchmark_ink_layout_exploration import (
    MANIFESTS,SIMULATED_NEGATIVES,WIDE_NEGATIVES,source_cases)

ROOT=Path(__file__).resolve().parents[1]


class InkLayoutTests(unittest.TestCase):
    def test_three_zones_distinguish_blank_from_printed_but_never_verify(self):
        paper=Image.new("RGB",(192,192),(229,230,226))
        blank=ink_layout(paper)
        self.assertEqual(blank["dark_pixel_fractions_by_zone"]["center_mark"],0.)
        self.assertEqual(blank["dark_pixel_fractions_by_zone"]["bottom_print"],0.)
        self.assertEqual(blank["new_sticker_confirmed"],False)
        d=ImageDraw.Draw(paper)
        d.rectangle([55,80,142,91],fill=(21,21,23))
        d.text((78,164),"123",fill=(15,16,17))
        layout=ink_layout(paper)
        self.assertGreater(layout["dark_pixel_fractions_by_zone"]["center_mark"],.001)
        self.assertGreater(layout["dark_pixel_fractions_by_zone"]["bottom_print"],.001)
        self.assertGreater(layout["center_component_stats"]["largest_component_pixels"],5)
        self.assertEqual(layout["serial_read"],None)
        self.assertFalse(layout["new_sticker_confirmed"])
        self.assertEqual(layout,ink_layout(paper))
        with self.assertRaisesRegex(ValueError,"undersized"):
            ink_layout(Image.new("RGB",(8,8),"white"))

    def test_region_bounds_refuse_source_escape_and_verified_claim(self):
        good={"bbox_xyxy_original_pixels":[10,20,110,105],
              "new_sticker_confirmed":False}
        self.assertEqual(validate_geometry(good,160,160),(10,20,110,105))
        for box in ([10,20,999,999],[10,20,4,40],["10",20,110,105],[10,20,21,25]):
            with self.subTest(box=box),self.assertRaises(ValueError):
                validate_geometry({**good,"bbox_xyxy_original_pixels":box},160,160)
        with self.assertRaisesRegex(ValueError,"unverified"):
            validate_geometry({**good,"new_sticker_confirmed":True},160,160)

    def test_only_pinned_local_sources_are_annotated(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            source=root/"owned-photo.jpg"
            Image.new("RGB",(230,180),(240,235,230)).save(source)
            index={"candidates":[{"id":"a","path":"owned-photo.jpg","sha256":sha256(source),
                                  "source_url":"https://example.org/owner/post"}]}
            proposed={"new_confirmed_stickers":0,"candidates":[{"candidate_id":"a","new_sticker_confirmed":False,"proposals":[{
                      "bbox_xyxy_original_pixels":[20,30,140,140],
                      "new_sticker_confirmed":False}]}]}
            result=annotate(index,proposed,root)
            self.assertEqual(result["source_files_scanned"],1)
            self.assertEqual(result["new_confirmed_stickers"],0)
            self.assertFalse(result["auto_sticker_detector_validated"])
            self.assertEqual(result["candidates"][0]["source_sha256"],sha256(source))
            self.assertEqual(result["candidates"][0]["proposals"][0]["ink_layout"]["serial_read"],None)
            tampered=dict(index)
            tampered["candidates"]=[{**index["candidates"][0],"sha256":"0"*64}]
            censored=annotate(tampered,proposed,root)
            self.assertEqual(censored["source_files_scanned"],0)
            self.assertEqual(censored["source_errors"][0]["reason"],"source-sha256-mismatch")
            with self.assertRaises(ValueError):
                annotate(index,proposed,root,max_files=0)

    def test_structural_previous_source_annotations_are_eleven_disjoint(self):
        self.assertEqual(len(MANIFESTS),3)
        self.assertEqual(len(SIMULATED_NEGATIVES),4)
        self.assertEqual(len(WIDE_NEGATIVES),4)
        known=set()
        import csv
        for path in MANIFESTS:
            with (ROOT/path).open(encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    self.assertNotIn(row["serial"],known)
                    known.add(row["serial"])
                    self.assertEqual(len(row["source_sha256"]),64)
        self.assertEqual(len(known),11)


if __name__=="__main__":
    unittest.main()
