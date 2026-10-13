"""Standard-library barcode intake regression checks; no network/scanner needed."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from inspect_arg_barcodes import inspect, parse_gs1_ai, verify_gtin, gtin_check_digit, normalise_scanner_format
from conjecture_lab_code128_widths import selftest, frame_preserving_shuffle, source_stream


class TestBarcodeIntake(unittest.TestCase):
    def test_gtin(self):
        self.assertEqual(gtin_check_digit("400638133393"), "1")
        self.assertEqual(verify_gtin("4006381333931")["status"], "valid_check_digit")
        self.assertEqual(verify_gtin("4006381333932")["status"], "invalid_check_digit")
        self.assertEqual(verify_gtin("CUSA-05297")["status"], "invalid_format")
        self.assertEqual(verify_gtin(" 4006381333931")["status"], "invalid_format")

    def test_gs1_scanner_id_and_variable_fields(self):
        x = inspect("]C1010400638133393121A37", "CODE-128")
        self.assertEqual(x["gs1"]["status"], "parsed_supported_subsets_only")
        self.assertEqual([f["ai"] for f in x["gs1"]["fields"]], ["01", "21"])
        self.assertEqual(x["gs1"]["fields"][0]["gtin_validation"]["status"], "valid_check_digit")
        y = parse_gs1_ai("10BATCH\x1d0104006381333931")
        self.assertEqual([f["ai"] for f in y["fields"]], ["10", "01"])
        self.assertEqual(parse_gs1_ai("0104")["status"], "malformed")
        self.assertEqual(parse_gs1_ai("9912")["status"], "unsupported_ai")

    def test_scanner_formats(self):
        self.assertEqual(normalise_scanner_format("BarcodeFormat.EAN13"), "EAN-13")
        self.assertEqual(normalise_scanner_format("BarcodeFormat.Code128"), "CODE-128")

    def test_do_not_infer_format(self):
        self.assertIsNone(inspect("0104006381333931")["gs1"])
        self.assertIsNone(inspect("4006381333931")["gtin"])
        self.assertIsNotNone(inspect("4006381333931", "EAN-13")["gtin"])

    def test_code128_table(self):
        selftest()


if __name__ == "__main__":
    unittest.main()