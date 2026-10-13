"""Public archived CE search rate limiting and exact-post-ID probe offline tests."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from scripts.external_evidence.search_public_reddit_ce_media import (
    ArchiveHTTPFailure, scan
)
from scripts.external_evidence.lookup_public_ce_resale_posts import probe


class ArchiveReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.q = [{"id": f"q{i}", "kind": "post", "subreddit": "GameSale", "term": "realdoll"}
                  for i in range(1, 7)]
        self.empty_known = {"reddit": set(), "imgur": set()}

    def test_stops_immediately_at_rate_limit_and_reports_remaining_unattempted(self):
        counter = {"calls": 0}
        def requester(url):
            counter["calls"] += 1
            if counter["calls"] == 2:
                raise ArchiveHTTPFailure(429, "Too many requests", "3600")
            return {"data": []}, "a"*64
        found, audit, failures, pics, galleries = scan(
            self.q, self.empty_known, requester=requester)
        self.assertEqual(counter["calls"], 2)
        self.assertEqual(len(failures), 1)
        self.assertEqual(audit[1]["http_status"], 429)
        self.assertEqual(audit[1]["retry_after"], "3600")
        self.assertEqual([x["status"] for x in audit[2:]], ["not-attempted"]*4)
        self.assertEqual((found,pics,galleries), ([],[],[]))

    def test_stops_after_three_consecutive_invalid_keyword_rejections(self):
        counter = {"calls": 0}
        def requester(url):
            counter["calls"] += 1
            raise ArchiveHTTPFailure(422, "bad keyword query")
        _, audit, failures, _, _ = scan(self.q, self.empty_known, requester=requester)
        self.assertEqual(counter["calls"],3)
        self.assertEqual(len(failures),3)
        self.assertEqual(audit[-1]["status"],"not-attempted")
        self.assertIn("Three consecutive",audit[-1]["reason"])

    def test_success_resets_consecutive_422_counter(self):
        counter = {"calls": 0}
        def requester(url):
            counter["calls"] += 1
            if counter["calls"] in (1,3,5):
                raise ArchiveHTTPFailure(422,"unsupported search")
            return {"data": []},"b"*64
        _, audit, failures, _, _ = scan(self.q, self.empty_known, requester=requester)
        self.assertEqual(counter["calls"],6)
        self.assertEqual(sum(x["status"]=="ok" for x in audit),3)
        self.assertEqual(len(failures),3)

    def test_exact_id_control_batch_and_duplicate_role(self):
        source = [
            {"id":"i0vgml", "source_page_url":"https://www.reddit.com/comments/i0vgml/",
             "source_role":"unreconciled-2020-resale-lead"},
            {"id":"k4wyvu", "source_page_url":"https://www.reddit.com/comments/k4wyvu/",
             "source_role":"known-unknown-sticker-U32"},
        ]
        def requester(url):
            self.assertIn("ids=i0vgml,k4wyvu",url)
            return {"data":[{
                "id":"i0vgml", "title":"INSIDE Collector's Edition sale",
                "selftext":"iam8bit Playdead Huddle; https://i.redd.it/box.jpg",
                "url":"https://www.reddit.com/comments/i0vgml/",
            }]}, "c"*64
        result = probe(source,self.empty_known,requester=requester)
        self.assertEqual(result["status"],"ok")
        self.assertEqual(result["records"][0]["direct_image_urls"],["https://i.redd.it/box.jpg"])
        self.assertEqual(result["records"][0]["source_role"],source[0]["source_role"])
        self.assertEqual(result["records"][1]["status"],"not-found-in-archive")

    def test_exact_id_batch_unavailable_does_not_invent_absence(self):
        src = [{"id":"i0vgml","source_page_url":"https://reddit.com/comments/i0vgml/",
                "source_role":"known-unresolved"}]
        report = probe(src,self.empty_known,requester=lambda _: (_ for _ in ()).throw(OSError("offline")))
        self.assertEqual(report["status"],"archive-unavailable")
        self.assertEqual(report["records"][0]["status"],"not-attempted-service-error")

    def test_direct_script_import_works_from_repo_root(self):
        root=Path(__file__).resolve().parents[1]
        script=root/"scripts/external_evidence/lookup_public_ce_resale_posts.py"
        proc=subprocess.run([sys.executable,str(script),"--help"],
                            capture_output=True,text=True,timeout=10)
        self.assertEqual(proc.returncode,0,proc.stderr)


if __name__ == "__main__":
    unittest.main()
