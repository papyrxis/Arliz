#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS_DIR="$ROOT/scripts/volumes"
GENERATE="$SCRIPTS_DIR/generate.sh"
BUILD_DIR="$ROOT/build"

die()  { echo "error: $*" >&2; exit 1; }
info() { echo "==> $*"; }

usage() {
  echo "Usage: $(basename "$0") <vol1|vol2|vol3|all>" >&2
  exit 1
}

build_one() {
  local vol="$1"
  local conf="$ROOT/configs/volumes/${vol}.conf"

  [[ -f "$conf" ]] || die "unknown volume '$vol' (no $conf)"

  source <(tr -d '\r' < "$conf")

  : "${VOLUME_NUM:?VOLUME_NUM not set in $conf}"
  : "${VOLUME_TITLE:?VOLUME_TITLE not set in $conf}"

  local year
  year="$(date -u '+%Y')"
  local out_basename="${year}_ARLIZ_${VOLUME_TITLE}_Volume_${VOLUME_NUM}"

  info "[$vol] generate ${out_basename}.tex"
  bash "$GENERATE" "$vol"

  info "[$vol] compile (latexmk → pdflatex, 2 passes + biber)"
  mkdir -p "$BUILD_DIR/$vol"

  (
    cd "$ROOT"
    latexmk \
      -pdf \
      -pdflatex="pdflatex -file-line-error -interaction=nonstopmode %O %S" \
      -use-make \
      -recorder \
      -output-directory="$BUILD_DIR/$vol" \
      "${out_basename}.tex"
  )

  local src="$BUILD_DIR/$vol/${out_basename}.pdf"
  local dst="$BUILD_DIR/${out_basename}.pdf"
  [[ -f "$src" ]] || die "latexmk finished but $src not found"
  cp "$src" "$dst"

  info "[$vol] done → build/${out_basename}.pdf"
}

[[ $# -eq 1 ]] || usage

case "$1" in
  all)
    for conf in "$ROOT/configs/volumes"/*.conf; do
      build_one "$(basename "$conf" .conf)"
    done
    ;;
  vol*)
    build_one "$1"
    ;;
  *)
    usage
    ;;
esac