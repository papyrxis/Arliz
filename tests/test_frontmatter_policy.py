from __future__ import annotations

import unittest
from pathlib import Path


class OptionalVolumeFrontmatterTests(unittest.TestCase):
    def test_volume_specific_frontmatter_is_optional(self) -> None:
        template = Path("main.tex").read_text(encoding="utf-8")
        for section in ("cover", "acknowledgments", "preface", "introduction"):
            with self.subTest(section=section):
                self.assertIn(
                    f"\\InputOptionalVolumeFrontmatter{{@FRONTMATTER_DIR@/{section}}}",
                    template,
                )

    def test_shared_frontmatter_remains_required(self) -> None:
        template = Path("main.tex").read_text(encoding="utf-8")
        for section in ("title", "copyright", "about_author"):
            with self.subTest(section=section):
                self.assertIn(f"\\input{{@MAIN_FRONTMATTER@/{section}}}", template)


if __name__ == "__main__":
    unittest.main()
