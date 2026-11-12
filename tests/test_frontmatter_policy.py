from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml


PACKAGE_IMPORT = re.compile(
    r"\\(?:usepackage|RequirePackage)\s*(?:\[[^\]]*\]\s*)?\{([^}]+)\}"
)


def strip_tex_comments(source: str) -> str:
    """Remove TeX comments while preserving escaped percent signs."""
    cleaned_lines: list[str] = []
    for line in source.splitlines():
        characters: list[str] = []
        preceding_backslashes = 0
        for character in line:
            if character == "%" and preceding_backslashes % 2 == 0:
                break
            characters.append(character)
            if character == "\\":
                preceding_backslashes += 1
            else:
                preceding_backslashes = 0
        cleaned_lines.append("".join(characters))
    return "\n".join(cleaned_lines)


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

    def test_ci_installs_the_pinned_workspace_wheel_without_a_submodule(self) -> None:
        lock = Path(".ci/locks/python-requirements.lock").read_text(encoding="utf-8")
        workflow = Path(".github/workflows/build.yml").read_text(encoding="utf-8")
        self.assertIn("PyYAML==6.0.3", lock)
        self.assertIn("papyrxis_workspace-0.5.1-py3-none-any.whl", lock)
        self.assertIn("python -m pip install -r .ci/locks/python-requirements.lock", workflow)
        self.assertNotIn("-e workspace", workflow)
        self.assertNotIn("submodules: recursive", workflow)
        self.assertFalse(Path(".gitmodules").exists())

    def test_workspace_schema_declares_three_independent_book_documents(self) -> None:
        config = yaml.safe_load(Path("workspace.yml").read_text(encoding="utf-8"))
        self.assertEqual(config["schema_version"], 2)
        self.assertEqual(config["project"]["type"], "collection")
        self.assertEqual(set(config["documents"]), {"vol1", "vol2", "vol3"})
        for document_id, document in config["documents"].items():
            with self.subTest(document=document_id):
                self.assertEqual(document["type"], "book")
                self.assertEqual(set(document["editions"]), {"en"})
                self.assertEqual(
                    document["editions"]["en"]["source"],
                    f".generated/{document_id}/main.tex",
                )

    def test_font_stack_uses_only_the_shared_toolchain(self) -> None:
        fonts = Path("configs/fonts.tex").read_text(encoding="utf-8")
        active_source = strip_tex_comments(fonts)
        packages = {
            package.strip()
            for imported in PACKAGE_IMPORT.findall(active_source)
            for package in imported.split(",")
        }

        for optional_package in ("mathdesign", "beramono", "charter"):
            with self.subTest(package=optional_package):
                self.assertNotIn(optional_package, packages)

        for required_package in ("mathpazo", "helvet", "babel", "microtype"):
            with self.subTest(package=required_package):
                self.assertIn(required_package, packages)

    def test_font_policy_ignores_comments_not_active_package_imports(self) -> None:
        source = r"""
% The old mathdesign and Charter packages must stay disabled.
% \usepackage{charter}
\usepackage{mathpazo}
\usepackage[english]{babel}
"""
        packages = {
            package.strip()
            for imported in PACKAGE_IMPORT.findall(strip_tex_comments(source))
            for package in imported.split(",")
        }
        self.assertEqual(packages, {"mathpazo", "babel"})


if __name__ == "__main__":
    unittest.main()
