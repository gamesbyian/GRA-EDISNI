"""Bounded public Reddit archived comment media retrieval: synthetic regressions."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from scripts.external_evidence.recover_reddit_comment_images import (
    arctic_tree_url, collect_comment_links, iter_comments, scan
)


class CommentPhotoArchiveTests(unittest.TestCase):
    def test_nested_comments_and_more_are_incomplete(self):
        tree = {"kind": "Listing", "data": {"children": [
            {"kind": "t1", "data": {
                "id": "gabc12", "body": "This is my INSIDE CE sticker https://i.redd.it/abc123.jpg",
                "link_id": "t3_e9bteo", "created_utc": 1576412000,
                "replies": {"kind": "Listing", "data": {"children": [
                    {"kind": "t1", "data": {"id": "gabc13", "body": "Here's another angle: https://imgur.com/a/123",
                                         "link_id": "t3_e9bteo"}},
                    {"kind": "more", "data": {"children": ["gabc14"]}}
                ]}}
            }}
        ]}}
        comments, partial = iter_comments(tree, max_nodes=30)
        self.assertEqual(len(comments), 2)
        self.assertTrue(partial)
        pics, galleries = collect_comment_links("e9bteo",
            {"id": "thread", "url": "https://reddit.com/comments/e9bteo/"}, comments)
        self.assertEqual(len(pics), 1)
        self.assertEqual(len(galleries), 1)
        self.assertEqual(pics[0]["source_page_url"], "https://www.reddit.com/comments/e9bteo/_/gabc12/")
        self.assertEqual(pics[0]["created_utc"], 1576412000)

    def test_no_unapproved_or_deleted_links(self):
        rows = [
            {"id": "gabc01", "link_id": "t3_e9bteo", "body": "[deleted] https://i.redd.it/deleted.jpg"},
            {"id": "gabc02", "link_id": "t3_other", "body": "https://i.redd.it/wrong.jpg"},
            {"id": "gabc03", "link_id": "t3_e9bteo", "body": "http://i.redd.it/unsecured.jpg"},
            {"id": "gabc04", "link_id": "t3_e9bteo", "body": "https://example.com/unrelated"},
            {"id": "gabc05", "link_id": "t3_e9bteo", "body": "serial photo https://preview.redd.it/img.jpg?width=500&amp;format=webp"}
        ]
        media, manual = collect_comment_links("e9bteo",
               {"id": "k", "url": "https://reddit.com/comments/e9bteo/"}, rows)
        self.assertEqual(len(media), 1)
        self.assertEqual(len(manual), 0)
        self.assertIn("width=500&format=webp", media[0]["image_url"])
        self.assertEqual(media[0]["keyword_hints"], ["sticker-or-CE-context"])

    def test_provider_failure_and_fallback_does_not_claim_complete_history(self):
        def fake(url):
            if "/api/comments/tree?" in url:
                raise OSError("temporary unavailable")
            return {"data": [{"id": "gabc16", "link_id": "t3_e9bteo",
                              "body": "photos at https://ibb.co/example"}]}, "e"*64
        reports, media, galleries = scan([
            {"id": "post", "url": "https://www.reddit.com/r/PlaydeadsInside/comments/e9bteo/"}],
            requester=fake, max_comments=100)
        self.assertEqual(reports[0]["provider"], "pullpush-comments-search-first-page")
        self.assertTrue(reports[0]["possible_partial_tree"])
        self.assertEqual(len(media), 0)
        self.assertEqual(len(galleries), 1)
        self.assertEqual(galleries[0]["classification"], "gallery-or-login-needed-manual-review")

    def test_cli_direct_invocation_and_host_confinement(self):
        self.assertIn("link_id=t3_e9bteo", arctic_tree_url("e9bteo", 50))
        with self.assertRaises(ValueError):
            arctic_tree_url("../../private", 50)
        script = Path(__file__).resolve().parents[1] / "scripts/external_evidence/recover_reddit_comment_images.py"
        proc = subprocess.run([sys.executable, str(script), "--help"],
                              check=False, text=True, capture_output=True, timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("--max-comments", proc.stdout)


if __name__ == "__main__":
    unittest.main()
