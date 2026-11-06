#!/usr/bin/env bash
set -euo pipefail
die() { echo "error: $*" >&2; exit 1; }

if [[ $# -ne 1 ]]; then
  echo "Usage: $(basename "$0") <vol1|vol2|vol3|...>" >&2
  exit 1
fi

VOL="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONF="$ROOT/configs/volumes/${VOL}.conf"
TEMPLATE="$ROOT/main.tex"

[[ -f "$CONF" ]]     || die "no config for volume '$VOL' (expected $CONF)"
[[ -f "$TEMPLATE" ]] || die "template not found ($TEMPLATE)"

source <(tr -d '\r' < "$CONF")

: "${FRONTMATTER_DIR:?FRONTMATTER_DIR not set in $CONF}"
: "${CHAPTERS:?CHAPTERS not set in $CONF}"
: "${BACKMATTER:?BACKMATTER not set in $CONF}"
: "${PDF_TITLE:?PDF_TITLE not set in $CONF}"
: "${PDF_TITLE_FRONT:?PDF_TITLE_FRONT not set in $CONF}"
: "${PDF_COVER_TITLE:?PDF_COVER_TITLE not set in $CONF}"
: "${PDF_SUBJECT:?PDF_SUBJECT not set in $CONF}"
: "${PDF_KEYWORDS:?PDF_KEYWORDS not set in $CONF}"
: "${MAIN_FRONTMATTER:?MAIN_FRONTMATTER not set in $CONF}"
: "${VOLUME_NUM:?VOLUME_NUM not set in $CONF}"
: "${VOLUME_TITLE:?VOLUME_TITLE not set in $CONF}"
: "${VOLUME_DISPLAY_TITLE:?VOLUME_DISPLAY_TITLE not set in $CONF}"

# Fail before LaTeX starts when a configured source path is misspelled.
require_tex_source() {
  local entry="$1"
  local label="$2"
  local relative="$entry"
  [[ "$relative" == *.tex ]] || relative="${relative}.tex"
  [[ -f "$ROOT/$relative" ]] || die "$label source not found: $relative (configured in $CONF)"
}

for source in "${CHAPTERS[@]}"; do
  require_tex_source "$source" "chapter"
done
for source in "${BACKMATTER[@]}"; do
  require_tex_source "$source" "back matter"
done
for source in title copyright about_author; do
  require_tex_source "$MAIN_FRONTMATTER/$source" "shared front matter"
done

YEAR="$(date -u '+%Y')"
OUT_BASENAME="${YEAR}_ARLIZ_${VOLUME_TITLE}_Volume_${VOLUME_NUM}"

OUTPUT="$ROOT/${OUT_BASENAME}.tex"

CHAPTERS_BLOCK=""
for c in "${CHAPTERS[@]}"; do
  CHAPTERS_BLOCK+="\\input{${c}}"$'\n'
done

BACKMATTER_BLOCK=""
for b in "${BACKMATTER[@]}"; do
  BACKMATTER_BLOCK+="\\input{${b}}"$'\n'
done

escape_sed() {
  printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/[\/&]/\\&/g'
}

T_PDF_TITLE="$(escape_sed "$PDF_TITLE")"
T_PDF_TITLE_FRONT="$(escape_sed "$PDF_TITLE_FRONT")"
T_PDF_COVER_TITLE="$(escape_sed "$PDF_COVER_TITLE")"
T_PDF_SUBJECT="$(escape_sed "$PDF_SUBJECT")"
T_PDF_KEYWORDS="$(escape_sed "$PDF_KEYWORDS")"
T_FRONTMATTER_DIR="$(escape_sed "$FRONTMATTER_DIR")"
T_MAIN_FRONTMATTER="$(escape_sed "$MAIN_FRONTMATTER")"
T_VOLUME_DISPLAY_TITLE="$(escape_sed "$VOLUME_DISPLAY_TITLE")"
T_VOLUME_NUM="$(escape_sed "$VOLUME_NUM")"

{
  while IFS='' read -r line || [[ -n "$line" ]]; do
    case "$line" in
      *'@CHAPTERS@'*)
        printf '%s' "$CHAPTERS_BLOCK"
        ;;
      *'@BACKMATTER@'*)
        printf '%s' "$BACKMATTER_BLOCK"
        ;;
      *)
        printf '%s\n' "$line" \
          | sed \
              -e "s/@PDF_TITLE@/${T_PDF_TITLE}/g" \
              -e "s/@PDF_TITLE_FRONT@/${T_PDF_TITLE_FRONT}/g" \
              -e "s/@PDF_COVER_TITLE@/${T_PDF_COVER_TITLE}/g" \
              -e "s/@PDF_SUBJECT@/${T_PDF_SUBJECT}/g" \
              -e "s/@PDF_KEYWORDS@/${T_PDF_KEYWORDS}/g" \
              -e "s/@FRONTMATTER_DIR@/${T_FRONTMATTER_DIR}/g" \
              -e "s/@MAIN_FRONTMATTER@/${T_MAIN_FRONTMATTER}/g" \
              -e "s/@VOLUME_DISPLAY_TITLE@/${T_VOLUME_DISPLAY_TITLE}/g" \
              -e "s/@VOLUME_NUM@/${T_VOLUME_NUM}/g"
        ;;
    esac
  done < "$TEMPLATE"
} > "$OUTPUT"

echo "generated ${OUTPUT#$ROOT/}"
