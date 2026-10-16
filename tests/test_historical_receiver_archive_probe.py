import importlib.util
from pathlib import Path
import unittest

FILE = Path(__file__).resolve().parents[1] / "scripts/probe_historical_printer_receiver_archives.py"
spec = importlib.util.spec_from_file_location("archival", FILE)
archival = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archival)

class ArchiveReceiverTests(unittest.TestCase):
    def test_source_safety_and_plan(self):
        archival.self_test()
        jobs = archival.planned()
        self.assertEqual(len(jobs), 12)
        self.assertEqual(len(set(j["url"] for j in jobs)), 12)
        self.assertEqual({j["label"] for j in jobs}, {"PDJS2018", "T41HOP2019"})

    def test_cdx_metadata(self):
        raw = b'[["timestamp","original","statuscode","digest"],["20180604000000","http://www.playdead.com/js/dist.js","200","DIGEST"]]'
        rows = archival.extract_captures({"provider":"wayback_cdx"}, raw)
        self.assertEqual(rows[0]["digest"], "DIGEST")

    def test_alternate_provider_schema(self):
        raw = b'{"response_items":[{"linkToArchive":"http://arquivo.pt/wayback/20180604000000/foo"}]}'
        rows = archival.extract_captures({"provider":"arquivo_history"}, raw)
        self.assertEqual(len(rows), 1)
        self.assertTrue(archival.detect_replay(rows[0])[0].startswith("https://arquivo.pt/"))

    def test_no_origins(self):
        for domain in ("playdead.com", "terminal41.link", "user.example"):
            with self.assertRaises(ValueError):
                archival.assert_archive_url("https://" + domain + "/")

if __name__ == "__main__":
    unittest.main()
