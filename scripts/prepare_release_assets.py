#!/usr/bin/env python3
"""Stage volume PDFs with deterministic, collision-resistant release names."""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from pathlib import Path


def asset_name(relative_path: Path) -> str:
    parts = (*relative_path.parent.parts, relative_path.stem)
    readable = "--".join(parts)
    readable = re.sub(r"[^A-Za-z0-9._-]+", "-", readable).strip("-._")
    readable = (readable or "arliz-volume")[:140].rstrip("-._") or "arliz-volume"
    digest = hashlib.sha256(relative_path.as_posix().encode("utf-8")).hexdigest()[:12]
    return f"{readable}-{digest}.pdf"


def prepare_release_assets(source_dir: Path, destination_dir: Path) -> list[Path]:
    source_dir = source_dir.resolve()
    destination_dir = destination_dir.resolve()
    if not source_dir.is_dir():
        raise ValueError(f"PDF source directory does not exist: {source_dir}")
    try:
        destination_dir.relative_to(source_dir)
    except ValueError:
        pass
    else:
        raise ValueError("release asset destination must not be inside the source directory")

    pdfs = sorted(
        (path for path in source_dir.rglob("*") if path.is_file() and path.suffix.lower() == ".pdf"),
        key=lambda path: path.relative_to(source_dir).as_posix(),
    )
    if not pdfs:
        raise ValueError(f"No PDFs found in {source_dir}")

    destination_dir.mkdir(parents=True, exist_ok=True)
    for existing in destination_dir.glob("*.pdf"):
        existing.unlink()

    assets: list[Path] = []
    for source in pdfs:
        target = destination_dir / asset_name(source.relative_to(source_dir))
        if target.exists():
            raise ValueError(f"release asset collision: {target.name}")
        shutil.copy2(source, target)
        assets.append(target)
    return assets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("destination_dir", type=Path)
    args = parser.parse_args()
    try:
        assets = prepare_release_assets(args.source_dir, args.destination_dir)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")
    print(f"Prepared {len(assets)} release PDF asset(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
