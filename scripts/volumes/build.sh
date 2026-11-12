#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GENERATE="$ROOT/scripts/volumes/generate.sh"
PYTHON_BIN="${PYTHON:-python3}"

die() { echo "error: $*" >&2; exit 1; }

generate_one() {
  local volume="$1"
  [[ -f "$ROOT/configs/volumes/${volume}.conf" ]] || die "unknown volume '$volume'"
  bash "$GENERATE" "$volume"
}

build_all() {
  local conf volume
  for conf in "$ROOT/configs/volumes"/*.conf; do
    [[ -f "$conf" ]] || continue
    volume="$(basename "$conf" .conf)"
    generate_one "$volume"
  done

  "$PYTHON_BIN" -m px --root "$ROOT" build --keep-going
  "$PYTHON_BIN" -m px --root "$ROOT" verify
  "$PYTHON_BIN" "$ROOT/scripts/verify_volumes.py" --config-dir "$ROOT/configs/volumes" --build-dir "$ROOT/build"
}

build_one() {
  local volume="$1"
  generate_one "$volume"
  "$PYTHON_BIN" -m px --root "$ROOT" build "$volume" --edition en
  "$PYTHON_BIN" "$ROOT/scripts/verify_volumes.py" \
    --config-dir "$ROOT/configs/volumes" \
    --build-dir "$ROOT/build" \
    --volume "$volume"
}

[[ $# -eq 1 ]] || die "Usage: $0 <all|vol1|vol2|vol3>"

case "$1" in
  all) build_all ;;
  vol1|vol2|vol3) build_one "$1" ;;
  *) die "unknown build target: $1" ;;
esac
