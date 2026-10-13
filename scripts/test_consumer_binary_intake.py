#!/usr/bin/env python3
"""All fixture bytes synthetic; proves metadata classification, not decompilation."""
import hashlib
from pathlib import Path
import struct
import tempfile
import unittest
from consumer_binary_intake import identify, inspect


def fake_pe(managed: bool) -> bytes:
    b = bytearray(1024)
    b[:2] = b"MZ"
    struct.pack_into("<I", b, 0x3c, 0x80)
    b[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<H", b, 0x80+0x18, 0x10b)
    if managed:
        struct.pack_into("<II", b, 0x80+0x18+96+14*8, 0x2000, 0x48)
    return bytes(b)


class TestIntake(unittest.TestCase):
    def test_signatures(self):
        self.assertEqual(identify(fake_pe(True)), "pe-cli-managed")
        self.assertEqual(identify(fake_pe(False)), "pe-native-or-unmarked")
        self.assertEqual(identify(b"MZ"), "truncated-pe")
        self.assertEqual(identify(b"UnityFS\0\0"), "unityfs-asset")
        self.assertEqual(identify(b"\x7fELF\x02"), "elf-native")

    def test_intake_and_symlinks(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/"INSIDE_Data"/"Managed").mkdir(parents=True)
            (root/"INSIDE_Data"/"Managed"/"Assembly-CSharp.dll").write_bytes(fake_pe(True))
            (root/"INSIDE.exe").write_bytes(fake_pe(False))
            (root/"GameAssembly.dll").write_bytes(fake_pe(False))
            (root/"global-metadata.dat").write_bytes(b"\xaf\x1b\xb1\xfa"+b"X"*8)
            (root/"Other.bin").write_bytes(b"ignored")
            try:
                (root/"symlink").symlink_to(root, target_is_directory=True)
            except OSError:
                pass
            report = inspect(root)
            self.assertEqual(len(report["files"]), 4)
            self.assertEqual(report["route"], "managed-gameplay-present; ILSpy is first-pass tool")
            self.assertFalse(report["consumer_validated"])
            m = next(f for f in report["files"] if f["role"]=="gameplay-managed-candidate")
            self.assertEqual(m["sha256"], hashlib.sha256(fake_pe(True)).hexdigest())
            self.assertEqual(m["relative_path"], "INSIDE_Data/Managed/Assembly-CSharp.dll")

    def test_fail_closed_without_gameplay(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(inspect(Path(d))["route"].startswith("no verified"))
            (Path(d)/"GameAssembly.dll").write_bytes(fake_pe(False))
            self.assertTrue(inspect(Path(d))["route"].startswith("no verified"))


if __name__ == "__main__":
    unittest.main()
