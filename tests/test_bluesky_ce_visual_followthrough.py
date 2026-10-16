"""Exact offline negative/positive controls for bounded native Bluesky followthrough."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import tempfile
import unittest
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/"scripts"))
spec=importlib.util.spec_from_file_location("source_follow",ROOT/"scripts/probe_bluesky_ce_visual_followthrough.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class FrozenSourceFollowthrough(unittest.TestCase):
    def test_offline_defaults_no_requests(self):
        with tempfile.TemporaryDirectory() as d:
            r=m.probe(output=Path(d), live=False,
                image_getter=lambda _:self.fail("image HTTP attempted"),
                query_fetcher=lambda *_:self.fail("search HTTP attempted"))
            self.assertEqual(r["requests_sent"],0)
            self.assertEqual(r["state"],"planned_unexecuted")
            self.assertEqual(len(r["planned"]["source_images"]),3)
            self.assertEqual({x["key"] for x in r["planned"]["queries"]},
                             set(m.RETRY + m.PAGINATE))
            self.assertEqual(r["new_confirmed_stickers"],0)

    def test_bound_exact_three_images_two_retries_two_second_pages(self):
        queries=[]
        def fetch(endpoint,params):
            queries.append(dict(params))
            if "cursor" in params:
                return {"posts": [],"cursor": "still_more"}
            if params["query"] in {t["query"] for t in m.manifest()["queries"][-2:]}:
                return {"posts":[],"cursor":"page2"}
            return {"posts":[]}
        calls=[]
        def photo(url):
            calls.append(url)
            return b"\\xff\\xd8\\xff" + b"imagebytes","image/jpeg",".jpg"
        # Literal JPEG magic, not a real JPEG: test covers access control and storage.
        def jpeg(url):
            calls.append(url)
            return bytes.fromhex("ffd8ff") + b"imagebytes","image/jpeg",".jpg"
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            r=m.probe(live=True,output=root,image_getter=jpeg,
                       query_fetcher=fetch,sleep_fn=lambda *_:None)
            self.assertEqual(len(calls),3)
            self.assertEqual(r["media_retrieval_count"],3)
            self.assertEqual(r["requests_sent"],6)
            self.assertEqual(r["successful_search_requests"],6)
            self.assertEqual(len(queries),6)
            self.assertEqual(sum("cursor" in x for x in queries),2)
            self.assertEqual(len(list(root.glob("*.jpg"))),3)
            self.assertFalse(r["original_media_interpreted_in_automated_run"])
            self.assertTrue(all(x["sticker_verified"] is False for x in r["image_records"]))

    def test_rate_limit_blocks_remaining_queries_not_image_records(self):
        attempts=[]
        def blocked(endpoint,params):
            attempts.append(params)
            raise urllib.error.HTTPError("https://api.bsky.app",429,"rate limit",{},None)
        with tempfile.TemporaryDirectory() as d:
            r=m.probe(live=True,output=Path(d),query_fetcher=blocked,
                image_getter=lambda _:(_ for _ in ()).throw(ValueError("HTTP forbidden")),
                sleep_fn=lambda *_:None)
            self.assertEqual(len(attempts),1)
            self.assertEqual(r["requests_sent"],1)
            self.assertEqual(r["stop_reason"],"provider_access_stop_429")
            self.assertTrue(all(x["status"]=="acquisition_error" for x in r["image_records"]))
            self.assertEqual(len([x for x in r["query_records"]
                                  if x["status"]=="not_attempted_after_provider_block"]),3)
            self.assertEqual(r["new_confirmed_stickers"],0)

    def test_failed_first_cursor_page_does_not_invent_followup(self):
        def empty(endpoint, params):
            return {"posts":[]}
        with tempfile.TemporaryDirectory() as d:
            r=m.probe(live=True,output=Path(d),query_fetcher=empty,
                image_getter=lambda _:(_ for _ in ()).throw(ValueError("offline")),
                sleep_fn=lambda *_:None)
            self.assertEqual(r["requests_sent"],4)
            self.assertEqual(sum(x["status"]=="no_cursor_to_follow"
                                 for x in r["query_records"]),2)
            self.assertEqual(r["successful_search_requests"],4)
            self.assertEqual(r["media_retrieval_count"],0)


if __name__ == "__main__":
    unittest.main()
