"""Synthetic offline tests for forum archive indexing and exact symbolic search."""
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("forum_local_search", ROOT / "scripts/forum_local_search.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

FIXTURES = [
    {"url": "https://forum.example/t/1", "forum": "Example", "language": "en",
     "title": "INSIDE collector edition", "text": "Playdead puzzle. Photo /043 and A10N7.",
     "captured_at": "2020-04-10", "original_post_date": "2019-02-01",
     "source_kind": "verified_thread"},
    {"url": "https://forum.example/t/2", "forum": "Example", "language": "zh",
     "text": "玩家在討論貼紙 /43 的可能用途；代碼 B02。",
     "captured_at": "2022-01-01", "original_post_date": "2016-07-06"},
    {"url": "https://other.example/post/3", "language": "ja",
     "text": "プレイデッド シール。A10N7 ではない。",
     "captured_at": "2018-05-01", "source_kind": "warc_capture"},
]

class ForumLocalSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = module.connection(Path(self.temp.name) / "search.db")
        with self.db:
            for doc in FIXTURES:
                self.assertTrue(module.add_document(self.db, doc))
    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def test_exact_leading_zeros_and_punctuation(self):
        r = module.search(self.db, "/043")
        self.assertEqual(len(r["matches"]), 1)
        self.assertEqual(r["matches"][0]["url"], "https://forum.example/t/1")
        self.assertEqual(r["matches"][0]["captured_at"], "2020-04-10")
        self.assertEqual(r["matches"][0]["original_post_date"], "2019-02-01")
        self.assertEqual(len(module.search(self.db, "/43")["matches"]), 1)
        self.assertNotEqual(module.search(self.db, "/43")["matches"][0]["url"],
                            r["matches"][0]["url"])

    def test_casefold_and_case_sensitive(self):
        self.assertEqual(module.search(self.db, "playdead")["hits_shown"], 0)
        self.assertEqual(module.search(self.db, "playdead", ignore_case=True)["hits_shown"], 1)
        self.assertEqual(module.search(self.db, "A10N7")["hits_shown"], 2)

    def test_short_nonlatin_substrings_and_wildcards(self):
        self.assertEqual(module.search(self.db, "貼紙")["hits_shown"], 1)
        self.assertEqual(module.search(self.db, "シール")["hits_shown"], 1)
        self.assertEqual(module.search(self.db, "/0")["hits_shown"], 1)
        self.assertEqual(module.search(self.db, "100%")["hits_shown"], 0)

    def test_fts_phrase_and_filters(self):
        self.assertEqual(module.search(self.db, "Playdead puzzle", mode="phrase")["hits_shown"], 1)
        self.assertEqual(module.search(self.db, "A10N7", host="other.example")["hits_shown"], 1)
        self.assertEqual(module.search(self.db, "A10N7", host="nonexistent.example")["hits_shown"], 0)

    def test_idempotency_and_provenance(self):
        with self.db:
            self.assertFalse(module.add_document(self.db, FIXTURES[0]))
            revised = dict(FIXTURES[0], captured_at="2023-01-01")
            self.assertTrue(module.add_document(self.db, revised))
        self.assertEqual(module.search(self.db, "/043")["hits_shown"], 2)

    def test_jsonl_ingest_and_repeated_runs(self):
        p = Path(self.temp.name) / "data.jsonl"
        p.write_text(json.dumps(FIXTURES[0], ensure_ascii=False) + "\n" +
                     json.dumps(dict(FIXTURES[0], url="https://forum.example/t/4"),
                                ensure_ascii=False) + "\n", encoding="utf-8")
        r = module.ingest_jsonl(self.db, p)
        self.assertEqual(r["duplicates"], 1)
        self.assertEqual(r["inserted"], 1)
        self.assertEqual(module.ingest_jsonl(self.db, p)["inserted"], 0)

    def test_html_keeps_replies_and_omits_scripts(self):
        raw = "<html><script>private = 1</script><article><p>INSIDE sticker</p>" + \
              "<div class='reply'>/043<br>貼紙</div></article></html>"
        text = module.html_to_text(raw)
        self.assertIn("/043", text)
        self.assertIn("貼紙", text)
        self.assertNotIn("private", text)

    def test_no_url_or_empty_data(self):
        with self.assertRaises(ValueError):
            module.add_document(self.db, {"url": "file:///secret", "text": "hello"})
        with self.assertRaises(ValueError):
            module.add_document(self.db, {"url": "https://x.example/", "text": ""})

    def test_limit_and_scope(self):
        self.assertTrue(module.search(self.db, "A10N7", limit=1)["truncated"])
        self.assertEqual(module.search(self.db, "A10N7", limit=1)["matches"][0]["scope"],
                         "offline_ingested_corpus_only")
        with self.assertRaises(ValueError):
            module.search(self.db, "x", limit=0)

if __name__ == "__main__":
    unittest.main()
