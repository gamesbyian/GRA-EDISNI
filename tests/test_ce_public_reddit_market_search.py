"""Offline synthetic controls for public archived cross-community CE image discovery."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from scripts.external_evidence.search_public_reddit_ce_media import (
    clean_item, curated_case_map, known_status, media_urls, relevant, relevant_excerpt, scan, search_url
)


class ArchivedMarketSearchTests(unittest.TestCase):
    def test_shop_vague_inside_word_is_filtered(self):
        self.assertFalse(relevant({"title": "Inside the Limited Collectors Studio"}))
        self.assertTrue(relevant({"title": "INSIDE Collector's Edition iam8bit new photos"}))
        self.assertTrue(relevant({"body": "Received the Playdead Huddle model today"}))

    def test_exact_photo_gallery_and_relative_media_sources(self):
        post = {"id": "i0vgml", "title": "[US] Inside Collector's Edition sale",
                "selftext": "Selling my copy. Photo: https://i.imgur.com/abc123.jpg "
                            "and https://imgur.com/gallery/XYZ123",
                "url": "https://www.reddit.com/r/GameSale/comments/i0vgml/",
                "created_utc": 1596153600, "subreddit": "GameSale"}
        row = clean_item(post, "post")
        self.assertEqual(row["post_id"], "i0vgml")
        self.assertIn("https://i.imgur.com/abc123.jpg", row["direct_image_urls"])
        self.assertIn("https://imgur.com/gallery/XYZ123", row["gallery_urls"])
        self.assertGreaterEqual(row["score"], 10)
        self.assertEqual(row["source_page_url"], "https://www.reddit.com/comments/i0vgml/")
        self.assertEqual(known_status(row, {"reddit": {"i0vgml"}, "imgur": set()}),
                         "post-id-present-in-known-ledger")
        self.assertEqual(known_status(row, {"reddit": set(), "imgur": set()}),
                         "unreconciled-by-exact-url")

    def test_curated_known_case_by_exact_post_id_only(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "curated.json"
            file.write_text(json.dumps({"sources": [
                {"reddit_post_id": "iuutfq", "case_ref": "U32"},
                {"reddit_post_id": "izs23a", "case_ref": "U32"},
                {"ebay_item_id": "257753799919", "case_ref": "/047"}
            ]}))
            c = curated_case_map(file)
            self.assertEqual(c, {"iuutfq": "U32", "izs23a": "U32"})
            partial = {"post_id": "iuutfq", "direct_image_urls": [], "gallery_urls": []}
            self.assertEqual(known_status(partial, {"reddit": set(), "imgur": set(),
                                                      "case_by_post_id": c}),
                             "existing-curated-case-U32")
            partial["post_id"] = "i0vgml"
            self.assertEqual(known_status(partial, {"reddit": set(), "imgur": set(),
                                                      "case_by_post_id": c}),
                             "unreconciled-by-exact-url")
            file.write_text(json.dumps({"sources": [
                {"reddit_post_id": "iuutfq", "case_ref": "invalid-new-owner"}]}))
            with self.assertRaisesRegex(ValueError, "case"):
                curated_case_map(file)

    def test_ce_phrase_deep_in_inventory_retained_in_short_excerpt(self):
        old_inventory = "One game for sale. " * 150
        post = {"id": "i0vgml", "title": "Games, collectibles, swag for sale",
                "selftext": old_inventory + "INSIDE Collector's Edition from iam8bit; includes Huddle."}
        row = clean_item(post, "post")
        self.assertIsNotNone(row)
        self.assertGreater(row["excerpt_body_offset"], 1500)
        self.assertIn("Collector", row["context_excerpt"])
        self.assertIn("iam8bit", row["context_excerpt"])
        self.assertLessEqual(len(row["context_excerpt"]), 320)
        self.assertNotIn("One game for sale. One game for sale. One game for sale.", row["context_excerpt"])

    def test_context_sample_redacts_external_urls(self):
        post = {"title": "Sale", "selftext": "Hello " + "filler " * 70 +
                "iam8bit CE sticker https://i.imgur.com/example.jpg and a numbered seal"}
        excerpt, start = relevant_excerpt(post)
        self.assertGreater(start, 55)
        self.assertIn("[public URL]", excerpt)
        self.assertNotIn("https://", excerpt)

    def test_comment_media_and_archived_deleted_not_counted(self):
        row = clean_item({"id":"f12345", "link_id":"t3_e9bteo",
                          "subreddit":"PlaydeadsInside",
                          "body":"My iam8bit sticker photo https://i.redd.it/photo.jpg"},
                         "comment")
        self.assertEqual(row["source_page_url"],
                         "https://www.reddit.com/comments/e9bteo/_/f12345/")
        self.assertEqual(len(row["direct_image_urls"]), 1)
        self.assertIsNone(clean_item({"id":"f12346", "link_id":"t3_e9bteo",
                             "body":"[removed] iam8bit photo https://i.redd.it/file.jpg"},
                             "comment"))
        self.assertIsNone(clean_item({"id":"f12347", "link_id":"t3_e9bteo",
                             "body":"just a game no CE information"}, "comment"))

    def test_preview_and_embedded_src_cannot_be_arbitrary_hosts(self):
        item = {"url":"https://i.redd.it/public.jpg",
                "preview":{"images":[{"source":{"url":"https://preview.redd.it/a.jpg?width=100&amp;format=jpg"}}]},
                "media_metadata":{"x":{"s":{"u":"http://i.redd.it/unsecured.jpg"}}},
                "selftext":"https://example.com/other.jpg https://imgur.com/a/AlbumCode"}
        direct, galleries=media_urls(item)
        self.assertEqual(len(direct),2)
        self.assertEqual(len(galleries),1)
        self.assertIn("https://preview.redd.it/a.jpg?width=100&format=jpg",direct)

    def test_archive_filters_are_bounded_and_typed(self):
        entry={"id":"q","kind":"post","subreddit":"GameSale","term":"inside collector"}
        parsed=urlparse(search_url(entry,30))
        self.assertEqual(parsed.hostname,"arctic-shift.photon-reddit.com")
        self.assertEqual(parse_qs(parsed.query)["query"], ["inside collector"])
        with self.assertRaises(ValueError):
            search_url({**entry, "subreddit":"GameSale&author=someone"},30)

    def test_duplicate_cross_query_records_and_failure_are_explicit(self):
        queries=[{"id":"q1","kind":"post","subreddit":"GameSale","term":"iam8bit"},
                 {"id":"q2","kind":"post","subreddit":"gamecollecting","term":"real doll"},
                 {"id":"q3","kind":"comment","subreddit":"gamecollecting","term":"realdoll"}]
        post={"id":"i0vgml","title":"Selling my iam8bit Playdead inside collector",
              "url":"https://i.redd.it/salephoto.jpg","created_utc":1596153600}
        def get(url):
            if "comments/search" in url: raise OSError("temporary API outage")
            return {"data":[post]}, "abc"*21+"a"
        records,audit,failures,photos,galleries=scan(queries,
                    {"reddit":set(),"imgur":set()},requester=get,per_query=10)
        self.assertEqual(len(records),1)
        self.assertEqual(records[0]["matched_search_ids"], ["q1","q2"])
        self.assertEqual(len(photos),1)
        self.assertEqual(len(galleries),0)
        self.assertEqual(len(failures),1)
        self.assertEqual(audit[2]["status"],"unavailable")
        self.assertEqual(photos[0]["source_page_url"], records[0]["source_page_url"])


if __name__ == "__main__":
    unittest.main()
