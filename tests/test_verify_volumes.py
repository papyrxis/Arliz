from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from scripts.check_gix_tags import invalid_gix_tags
from scripts.verify_volumes import expected_pdf_name, read_volume_metadata, valid_pdf


def strip_config_comments(source: str) -> str:
    """Remove # comments without stripping hashes inside quoted values."""
    cleaned_lines: list[str] = []
    for line in source.splitlines():
        characters: list[str] = []
        quote: str | None = None
        escaped = False
        for character in line:
            if quote is not None:
                characters.append(character)
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == quote:
                    quote = None
            elif character in {"'", '"'}:
                quote = character
                characters.append(character)
            elif character == "#":
                break
            else:
                characters.append(character)
        cleaned_lines.append("".join(characters))
    return "\n".join(cleaned_lines)


def configured_entries(config: str, variable: str) -> list[str] | None:
    uncommented = strip_config_comments(config)
    match = re.search(
        rf"(?ms)^\s*{re.escape(variable)}\s*=\s*\((.*?)^\s*\)",
        uncommented,
    )
    if match is None:
        return None
    return [
        value
        for _, value in re.findall(r"""(["'])(.*?)\1""", match.group(1))
    ]


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

    def test_config_parser_ignores_comments_and_preserves_quoted_hashes(self) -> None:
        config = """CHAPTERS=(
  # The repository's actual chapter path is listed below.
  "volumes/vol2/vol02"
  "chapters/hash#tag"
)
"""
        self.assertEqual(
            configured_entries(config, "CHAPTERS"),
            ["volumes/vol2/vol02", "chapters/hash#tag"],
        )

    def test_all_configured_chapter_and_backmatter_sources_exist(self) -> None:
        for config_path in sorted(Path("configs/volumes").glob("*.conf")):
            config = config_path.read_text(encoding="utf-8")
            for variable in ("CHAPTERS", "BACKMATTER"):
                with self.subTest(config=config_path.name, variable=variable):
                    entries = configured_entries(config, variable)
                    self.assertIsNotNone(entries, f"{variable} missing in {config_path}")
                    assert entries is not None
                    self.assertTrue(entries, f"{variable} is empty in {config_path}")
                    for entry in entries:
                        source = Path(entry)
                        if source.suffix != ".tex":
                            source = source.with_suffix(".tex")
                        self.assertTrue(
                            source.is_file(),
                            f"{config_path.name} {variable} references missing source {source}",
                        )


if __name__ == "__main__":
    unittest.main()
