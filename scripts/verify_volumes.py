#!/usr/bin/env python3
"""Verify Arliz's configured volume PDFs against the Workspace v2 manifest."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def read_volume_metadata(config_path: Path) -> tuple[str, int]:
    text = config_path.read_text(encoding="utf-8")
    title = re.search(r'^\s*VOLUME_TITLE\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    number = re.search(r'^\s*VOLUME_NUM\s*=\s*(\d+)\s*$', text, re.MULTILINE)
    if not title or not number:
        raise ValueError(f"{config_path}: VOLUME_TITLE and VOLUME_NUM are required")
    return title.group(1), int(number.group(1))


def expected_pdf_name(title: str, number: int) -> str:
    return f"ARLIZ_{title}_Volume_{number}.pdf"


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


def verify_volumes(config_dir: Path, build_dir: Path, volume: str | None = None) -> list[Path]:
    configs = sorted(config_dir.glob("*.conf"))
    if volume is not None:
        configs = [path for path in configs if path.stem == volume]
        if not configs:
            raise ValueError(f"unknown volume {volume!r} in {config_dir}")

    manifest_path = build_dir / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"Workspace build manifest not found: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read Workspace manifest {manifest_path}: {exc}") from exc

    if manifest.get("schema_version") != 2:
        raise ValueError("Workspace manifest must use schema_version 2")
    results = manifest.get("results")
    if not isinstance(results, list):
        raise ValueError("Workspace manifest results must be a list")

    records: dict[tuple[str, str], dict] = {}
    for record in results:
        if not isinstance(record, dict):
            raise ValueError("Workspace manifest contains a malformed result")
        key = (record.get("document_id"), record.get("edition"))
        if key in records:
            raise ValueError(f"duplicate Workspace manifest result: {key[0]}/{key[1]}")
        records[key] = record

    project_root = build_dir.resolve().parent
    outputs: list[Path] = []
    for config in configs:
        document_id = config.stem
        title, number = read_volume_metadata(config)
        output = build_dir / document_id / "en" / expected_pdf_name(title, number)
        output_relative = output.resolve().relative_to(project_root).as_posix()
        record = records.get((document_id, "en"))
        if record is None:
            raise ValueError(f"{document_id}/en: missing from Workspace build manifest")
        if record.get("status") != "success":
            raise ValueError(f"{document_id}/en: Workspace build status is {record.get('status')!r}")
        if record.get("output") != output_relative:
            raise ValueError(
                f"{document_id}/en: expected manifest output {output_relative}, "
                f"found {record.get('output')!r}"
            )
        if not valid_pdf(output):
            raise ValueError(f"{document_id}/en: missing or incomplete PDF: {output}")
        outputs.append(output)

    if not outputs:
        raise ValueError(f"No volume configurations found in {config_dir}")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=Path("configs/volumes"))
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--volume", choices=("vol1", "vol2", "vol3"))
    args = parser.parse_args()
    try:
        outputs = verify_volumes(args.config_dir, args.build_dir, args.volume)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for output in outputs:
        print(f"OK  {output} ({output.stat().st_size:,} bytes)")
    print(f"Verified {len(outputs)} Arliz volume PDF(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
