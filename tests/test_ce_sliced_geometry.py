"""No-network tests for tiled paper proposals and disjoint frozen novel sources."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.external_evidence.visual_sliced_geometry import (
    overlap_over_smaller, starts, tile_plan, suggest,scan_index
)
from scripts.external_evidence.benchmark_sliced_geometry_new_sources import (
    load_novel, paper_patch, positive, background, NEGATIVES, FRACTIONS, SIZE,
)
from scripts.external_evidence.visual_region_probe import box_iou,sha256

ROOT=Path(__file__).resolve().parents[1]
HOLD=ROOT/"data/reference/inside-ce-novel-tiny-paper-crop-holdouts-20261016.csv"


class SlicedGeometryTests(unittest.TestCase):
    def test_tile_coverage_at_edges_without_cap(self):
        self.assertEqual(starts(300,300,.25),[0])
        self.assertEqual(starts(720,300,.25),[0,225,420])
        with self.assertRaises(ValueError):
            starts(720,300,.8)
        boxes,coverage=tile_plan(1440,1080,max_tiles=24)
        self.assertEqual(coverage["tiles_proposed"],coverage["tiles_evaluated"])
        self.assertTrue(any(a==0 and b==0 for a,b,_,_ in boxes))
        self.assertTrue(any(r==1440 and bot==1080 for _,_,r,bot in boxes))
        self.assertTrue(all(x1<x2 and y1<y2 for x1,y1,x2,y2 in boxes))
        self.assertEqual(boxes,tile_plan(1440,1080,max_tiles=24)[0])

    def test_bounded_tiles_sparsify_full_image_not_only_left_top(self):
        boxes,coverage=tile_plan(3000,4000,max_tiles=12)
        self.assertTrue(coverage["tiling_incomplete_at_cap"])
        self.assertEqual(len(boxes),12)
        self.assertEqual(coverage["tiles_censored_by_budget"],
                         coverage["tiles_proposed"]-12)
        self.assertTrue(any(x==0 for x,_,_,_ in boxes))
        self.assertTrue(any(y==0 for _,y,_,_ in boxes))
        self.assertTrue(any(r==3000 for _,_,r,_ in boxes))
        self.assertTrue(any(b==4000 for _,_,_,b in boxes))
        self.assertEqual(boxes,tile_plan(3000,4000,max_tiles=12)[0])
        with self.assertRaises(ValueError):
            tile_plan(3000,4000,max_tiles=0)
        with self.assertRaises(ValueError):
            tile_plan(3000,4000,max_tiles=49)

    def test_overlap_over_smaller_merges_nested_not_unrelated(self):
        self.assertEqual(overlap_over_smaller([0,0,100,100],[25,25,75,75]),1.)
        self.assertEqual(overlap_over_smaller([0,0,30,30],[300,300,330,330]),0.)
        self.assertAlmostEqual(overlap_over_smaller([0,0,60,60],[30,0,90,60]),.5)
        self.assertLess(box_iou([0,0,100,100],[25,25,75,75]),.5)

    def test_tiny_white_card_tiled_proposals_are_review_only(self):
        scene=Image.new("RGB",(960,720),(40,52,60))
        draw=ImageDraw.Draw(scene)
        paper=(830,620,888,673)
        draw.rectangle(paper,fill=(232,231,225))
        draw.line([(849,659),(875,630)],fill=(16,20,23),width=6)
        boxes,stats=suggest(scene,max_tiles=24,top_k=8)
        self.assertTrue(boxes)
        self.assertTrue(any(box_iou(p["bbox_xyxy_original_pixels"],paper)>.4
                            for p in boxes))
        self.assertTrue(all(p["new_sticker_confirmed"] is False for p in boxes))
        self.assertEqual(stats["tiles_evaluated"],len(stats["tile_locations"]))
        self.assertTrue(stats["global_pass_included"])
        self.assertTrue(stats["never_verifies_ce_sticker"])
        self.assertTrue(all(0<=p["bbox_xyxy_original_pixels"][0]<
                            p["bbox_xyxy_original_pixels"][2]<=960 for p in boxes))
        self.assertEqual((boxes,stats),suggest(scene,max_tiles=24,top_k=8))
        with self.assertRaises(ValueError):
            suggest(scene,top_k=0)

    def test_source_manifest_is_distinct_and_pixel_bounded(self):
        cases=load_novel(HOLD,ROOT)
        self.assertEqual({r["serial"] for r in cases},{"021","171"})
        self.assertEqual(len(FRACTIONS),3)
        self.assertEqual(len(NEGATIVES),4)
        self.assertEqual(SIZE,(1440,1080))
        for case in cases:
            patch=paper_patch(case,ROOT)
            self.assertGreater(min(patch.size),100)
            im,box=positive(case,ROOT,FRACTIONS[0],0)
            area=(box[2]-box[0])*(box[3]-box[1])/(SIZE[0]*SIZE[1])
            self.assertAlmostEqual(area,FRACTIONS[0],delta=.0002)
            self.assertEqual(im.size,SIZE)
        with tempfile.TemporaryDirectory() as tmp:
            tampered=Path(tmp)/"bad.csv"
            tampered.write_text(HOLD.read_text().replace("641b257b","00000000"),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"digest mismatch"):
                load_novel(tampered,ROOT)
            tampered.write_text(HOLD.read_text().replace("021,","003,",1),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"identities"):
                load_novel(tampered,ROOT)

    def test_no_network_file_acquisition_and_source_byte_binding(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            path=root/"photo.jpg"
            Image.new("RGB",(120,100),"black").save(path)
            index={"candidates":[
                {"id":"real","path":"photo.jpg","sha256":sha256(path),
                 "source_kind":"s1","source_url":"https://example.org/post"},
                {"id":"different","path":"photo.jpg","sha256":"0"*64,
                 "source_kind":"s2"}
            ]}
            report=scan_index(index,root,max_files=2,max_tiles=5,top_k=8)
            self.assertEqual(report["scanned_source_files"],1)
            self.assertEqual(report["source_failures"][0]["reason"],"sha256-mismatch")
            self.assertEqual(report["new_confirmed_stickers"],0)
            self.assertFalse(report["autonomous_sticker_detection_validated"])
            self.assertEqual(report["candidates"][0]["source_url"],"https://example.org/post")


if __name__=="__main__":
    unittest.main()
