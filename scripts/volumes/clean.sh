#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG_DIR="$ROOT/configs/volumes"

die() { echo "error: $*" >&2; exit 1; }

clean_one() {
  local vol="$1"
  local conf="$CONFIG_DIR/$vol.conf"
  [[ -f "$conf" ]] || die "unknown volume '$vol' (no $conf)"

  # These configuration files are maintained in this repository.
  source <(tr -d '\r' < "$conf")
  : "${VOLUME_NUM:?VOLUME_NUM not set in $conf}"
  : "${VOLUME_TITLE:?VOLUME_TITLE not set in $conf}"

  local basename
  basename="$(date -u '+%Y')_ARLIZ_${VOLUME_TITLE}_Volume_${VOLUME_NUM}"
  rm -f "$ROOT/$basename.tex" "$ROOT/build/$basename.pdf"
  rm -rf "$ROOT/build/$vol"
  echo "cleaned $vol"
}

case "${1:-all}" in
  all)
    for conf in "$CONFIG_DIR"/*.conf; do
      [[ -f "$conf" ]] || continue
      clean_one "$(basename "$conf" .conf)"
    done
    # Remove generated files from earlier calendar years as well.
    find "$ROOT" -maxdepth 1 -type f -name '*_ARLIZ_*_Volume_*.tex' -delete
    rm -rf "$ROOT/build"
    ;;
  vol*)
    [[ $# -eq 1 ]] || die "usage: $0 [all|vol1|vol2|vol3]"
    clean_one "$1"
    ;;
  *)
    die "usage: $0 [all|vol1|vol2|vol3]"
    ;;
esac
