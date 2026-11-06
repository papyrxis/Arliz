#!/usr/bin/env python3
"""Verify that every configured Arliz volume produced a complete PDF."""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def read_volume_metadata(config_path: Path) -> tuple[str, int]:
    text = config_path.read_text(encoding="utf-8")
    title = re.search(r'^\s*VOLUME_TITLE\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    number = re.search(r'^\s*VOLUME_NUM\s*=\s*(\d+)\s*$', text, re.MULTILINE)
    if not title or not number:
        raise ValueError(f"{config_path}: VOLUME_TITLE and VOLUME_NUM are required")
    return title.group(1), int(number.group(1))


def expected_pdf_name(title: str, number: int, year: int) -> str:
    return f"{year}_ARLIZ_{title}_Volume_{number}.pdf"


def valid_pdf(path: Path) -> bool:
    try:
        size = path.stat().st_size
        if size < 16:
            return False
        with path.open("rb") as stream:
            header = stream.read(8)
            stream.seek(max(0, size - 2048))
            tail = stream.read()
        return header.startswith(b"%PDF-") and b"%%EOF" in tail
    except OSError:
        return False


def verify_volumes(config_dir: Path, build_dir: Path, year: int | None = None) -> list[Path]:
    year = year or datetime.now(timezone.utc).year
    configs = sorted(config_dir.glob("*.conf"))
    if not configs:
        raise ValueError(f"No volume configurations found in {config_dir}")

    outputs: list[Path] = []
    for config in configs:
        title, number = read_volume_metadata(config)
        pdf = build_dir / expected_pdf_name(title, number, year)
        if not valid_pdf(pdf):
            raise ValueError(f"{config.name}: missing or incomplete PDF: {pdf}")
        outputs.append(pdf)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=Path("configs/volumes"))
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--year", type=int, default=None)
    args = parser.parse_args()
    try:
        outputs = verify_volumes(args.config_dir, args.build_dir, args.year)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for output in outputs:
        print(f"OK  {output} ({output.stat().st_size:,} bytes)")
    print(f"Verified {len(outputs)} Arliz volume PDF(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
