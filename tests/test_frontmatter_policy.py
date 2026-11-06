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

    def test_volume_intro_environment_matches_the_project_definition(self) -> None:
        environment = Path("configs/env.tex").read_text(encoding="utf-8")
        self.assertIn(r"\newenvironment{volumeintro}", environment)
        for source in (
            "volumes/vol1/vol1.tex",
            "volumes/vol2/vol02.tex",
            "volumes/vol3/vol3.tex",
        ):
            content = Path(source).read_text(encoding="utf-8")
            with self.subTest(source=source):
                self.assertIn(r"\begin{volumeintro}", content)
                self.assertIn(r"\end{volumeintro}", content)
                self.assertNotIn("volumesintro", content)

    def test_ci_uses_pinned_python_build_dependencies(self) -> None:
        lock = Path(".ci/locks/python-requirements.lock").read_text(encoding="utf-8")
        workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")
        self.assertIn("PyYAML==6.0.3", lock)
        self.assertIn("pip install -r .ci/locks/python-requirements.lock -e workspace", workflow)
        self.assertIn("python-cache-dependency-path: .ci/locks/python-requirements.lock", workflow)

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
