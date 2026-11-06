#!/usr/bin/env python3
"""Fail safely when a SemVer-shaped tag cannot be read by gix."""
from __future__ import annotations

import re
import subprocess
import sys

_GIX_SEMVER = re.compile(
    r"^v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
_SEMVER_SHAPED = re.compile(r"^v?[0-9]+\.[0-9]+\.[0-9]+")


def invalid_gix_tags(tags: list[str]) -> list[str]:
    return [
        tag for tag in tags
        if _SEMVER_SHAPED.match(tag) and not _GIX_SEMVER.fullmatch(tag)
    ]


def main() -> int:
    result = subprocess.run(
        ["git", "tag", "--list"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip() or "error: could not list Git tags", file=sys.stderr)
        return result.returncode or 1

    invalid = invalid_gix_tags(result.stdout.splitlines())
    if invalid:
        print("error: gix cannot safely calculate a version while these SemVer-shaped tags are present:", file=sys.stderr)
        for tag in invalid:
            print(f"  - {tag}", file=sys.stderr)
        print("Keep historical tags unchanged; create an explicitly reviewed, gix-compatible replacement tag before bumping.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
