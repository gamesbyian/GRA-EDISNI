"""Offline controls for opt-in public historical Reddit media metadata."""
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.external_evidence.recover_reddit_image_links import (
    endpoints, scan, unpack, visible_image_urls
)


class HistoricalMediaTests(unittest.TestCase):
    def test_module_can_execute_directly_from_repository_root(self):
        script = Path(__file__).resolve().parents[1] / "scripts/external_evidence/recover_reddit_image_links.py"
        proc = subprocess.run([sys.executable, str(script), "--help"],
                              check=False, capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("--manifest", proc.stdout)

    def test_known_post_media_fields_only(self):
        item = {
            "id": "eers0x", "url": "https://i.redd.it/outer-photo.jpg",
            "preview": {"images": [{"source": {"url": "https://preview.redd.it/crop.png?width=1080&amp;format=png"}}]},
            "media_metadata": {"a": {"s": {"u": "https://i.imgur.com/album-image.jpg"}}},
            "author": "Do-not-leak-owner-profiles",
            "thumbnail": "https://reddit.com/avatar.png",
        }
        urls = visible_image_urls(item)
        self.assertEqual(len(urls), 3)
        self.assertIn("https://preview.redd.it/crop.png?width=1080&format=png", urls)
        self.assertFalse(any("avatar" in x or "Do-not" in x for x in urls))

    def test_archive_record_id_matched(self):
        payload = {"data": [{"id": "another", "url": "https://i.redd.it/wrong.jpg"},
                            {"id": "eers0x", "url": "https://i.redd.it/right.jpg"}]}
        self.assertEqual(unpack(payload, "eers0x")["url"], "https://i.redd.it/right.jpg")
        self.assertIsNone(unpack(payload, "e9bteo"))
        with self.assertRaises(ValueError):
            endpoints("bad/identifier")

    def test_fallback_is_recorded_without_invented_physical_observation(self):
        sources = [{"id": "known-2019", "url": "https://www.reddit.com/r/PlaydeadsInside/comments/eers0x/"}]
        def requester(url):
            if "arctic-shift" in url:
                raise OSError("temporary 504")
            return {"data": [{"id": "eers0x", "url": "https://i.redd.it/posted-image.jpg"}]}, "a"*64
        reports, leads = scan(sources, requester)
        self.assertEqual(reports[0]["provider"], "pullpush")
        self.assertEqual(reports[0]["status"], "archived-metadata-available")
        self.assertEqual(reports[0]["archive_attempts"][0]["status"], "failed")
        self.assertEqual(leads[0]["review_status"], "archive-url-unfetched")
        self.assertEqual(leads[0]["source_page_url"], sources[0]["url"])
        self.assertNotIn("serial", leads[0])

    def test_both_providers_missing_is_explicit_failure(self):
        sources = [{"id": "missing", "url": "https://reddit.com/r/p/comments/e9bteo/"}]
        reports, leads = scan(sources, lambda url: ({"data": []}, "f"*64))
        self.assertEqual(reports[0]["status"], "unavailable")
        self.assertEqual(len(reports[0]["archive_attempts"]), 2)
        self.assertEqual(leads, [])


if __name__ == "__main__":
    unittest.main()
