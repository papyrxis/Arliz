from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_gix_tags import invalid_gix_tags
from scripts.verify_volumes import expected_pdf_name, read_volume_metadata, valid_pdf


class VerifyVolumesTests(unittest.TestCase):
    def test_expected_pdf_name(self) -> None:
        self.assertEqual(
            expected_pdf_name("Zero_to_Bit", 1, 2026),
            "2026_ARLIZ_Zero_to_Bit_Volume_1.pdf",
        )

    def test_reads_volume_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "vol1.conf"
            config.write_text('VOLUME_TITLE="Zero_to_Bit"\nVOLUME_NUM=1\n', encoding="utf-8")
            self.assertEqual(read_volume_metadata(config), ("Zero_to_Bit", 1))

    def test_valid_pdf_requires_header_and_eof(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pdf = Path(directory) / "valid.pdf"
            pdf.write_bytes(b"%PDF-1.7\nbody\n%%EOF\n")
            self.assertTrue(valid_pdf(pdf))
            pdf.write_bytes(b"not a pdf")
            self.assertFalse(valid_pdf(pdf))

    def test_gix_rejects_semver_shaped_legacy_tags(self) -> None:
        self.assertEqual(
            invalid_gix_tags(["v1.0.0", "v1.2.0-rc.1", "latest-pre-release", "v1.0.0-beta-Volume_I"]),
            ["v1.0.0-beta-Volume_I"],
        )


if __name__ == "__main__":
    unittest.main()
