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

    def test_font_stack_uses_only_the_shared_toolchain(self) -> None:
        fonts = Path("configs/fonts.tex").read_text(encoding="utf-8")
        for optional_package in ("mathdesign", "beramono", "charter"):
            with self.subTest(package=optional_package):
                self.assertNotIn(optional_package, fonts)
        for required_package in ("mathpazo", "helvet", "babel", "microtype"):
            with self.subTest(package=required_package):
                self.assertIn(f"\\usepackage", fonts)
                self.assertIn(required_package, fonts)


if __name__ == "__main__":
    unittest.main()
