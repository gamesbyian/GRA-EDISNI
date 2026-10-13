"""Offline verified Imgur public gallery -> comment-permalink provenance tests."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.external_evidence.index_public_imgur_gallery import gallery_metadata
from scripts.external_evidence.visual_index import candidates


class GalleryProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.directory = self.root / "gallery-demoGallery"
        nested = self.directory / "imgur" / "demo"
        nested.mkdir(parents=True)
        self.image = nested / "imgur_demoGallery_001_example.jpg"
        im = Image.new("RGB", (320, 240), "white")
        d = ImageDraw.Draw(im)
        d.rectangle((10, 20, 140, 220), fill="black")
        im.save(self.image)
        (nested / (self.image.name + ".json")).write_text(json.dumps({
            "url": "https://i.imgur.com/example.jpg", "date": "2020-01-27",
            "id": "example",
        }))
        self.gallery = {
            "id": "demoGallery",
            "url": "https://imgur.com/gallery/demoGallery",
            "source_page_url": "https://www.reddit.com/comments/e9bteo/_/ffptzb1/",
            "evidence_role": "synthetic-historical-gallery",
        }

    def test_original_media_and_reddit_comment_are_both_preserved(self):
        manifest = gallery_metadata(self.directory, self.gallery)
        self.assertEqual(manifest["image_count"], 1)
        self.assertEqual(manifest["errors"], [])
        self.assertEqual(manifest["image_urls"][self.image.name],
                         "https://i.imgur.com/example.jpg")
        self.assertEqual(manifest["source_pages"][self.image.name],
                         self.gallery["source_page_url"])
        self.assertEqual(manifest["sha256"][self.image.relative_to(self.directory).as_posix()],
                         hashlib.sha256(self.image.read_bytes()).hexdigest())
        (self.directory / "acquisition.json").write_text(json.dumps(manifest) + "\n")
        records, errors = candidates(self.root, max_files=10)
        self.assertEqual(len(records), 1)
        self.assertFalse(errors)
        self.assertEqual(records[0]["source_url"], self.gallery["source_page_url"])
        self.assertEqual(records[0]["image_url"], "https://i.imgur.com/example.jpg")

    def test_imgur_a_album_link_accepted_without_changing_exact_source(self):
        self.gallery["url"] = "https://imgur.com/a/demoGallery"
        record = gallery_metadata(self.directory, self.gallery)
        self.assertEqual(record["gallery_url"], self.gallery["url"])
        self.assertEqual(record["image_count"], 1)
        self.assertEqual(record["source_pages"][self.image.name],
                         self.gallery["source_page_url"])

    def test_bad_metadata_does_not_bless_bytes(self):
        self.image.with_suffix(".jpg.json").write_text(json.dumps({
            "url": "http://127.0.0.1/example.jpg"}))
        report = gallery_metadata(self.directory, self.gallery)
        self.assertEqual(report["image_count"], 0)
        self.assertEqual(report["retrieval_status"], "no-verified-images")
        self.assertEqual(len(report["errors"]), 1)

    def test_invalid_gallery_or_comment_url_fails(self):
        bad = dict(self.gallery, url="https://imgur.com/gallery/other")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            gallery_metadata(self.directory, bad)
        bad = dict(self.gallery, source_page_url="http://localhost/private")
        with self.assertRaisesRegex(ValueError, "not approved"):
            gallery_metadata(self.directory, bad)


if __name__ == "__main__":
    unittest.main()
