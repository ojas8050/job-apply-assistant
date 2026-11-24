#!/usr/bin/env bash
# Build a tailored resume: Markdown -> DOCX -> PDF.
#
#   build_resume.sh <tailored.md> [out_basename]
#
# Environment (all optional):
#   MASTER_DOCX  a .docx whose styles pandoc should copy, so the tailored file looks like
#                the user's master resume. Without it pandoc's default styling is used.
#   MAX_PAGES    page budget before a warning is printed (default 2).
#
# PDF renderer, first one found wins: Microsoft Word (macOS), LibreOffice (soffice),
# then pandoc's own PDF engine. Outputs land next to the input .md.
set -euo pipefail

SRC="${1:?usage: build_resume.sh <tailored.md> [out_basename]}"
[[ -f "$SRC" ]] || { echo "no such file: $SRC" >&2; exit 1; }
command -v pandoc >/dev/null || { echo "pandoc is required (https://pandoc.org)" >&2; exit 1; }

DIR="$(cd "$(dirname "$SRC")" && pwd)"
BASE="${2:-$(basename "${SRC%.md}")}"
DOCX="$DIR/$BASE.docx"
PDF="$DIR/$BASE.pdf"

REF=()
if [[ -n "${MASTER_DOCX:-}" && -f "$MASTER_DOCX" ]]; then
  REF=(--reference-doc="$MASTER_DOCX")
else
  echo "note: no MASTER_DOCX set, using pandoc default styling" >&2
fi

pandoc "$SRC" "${REF[@]}" -o "$DOCX"
echo "docx: $DOCX"

if [[ "$(uname)" == "Darwin" && -d "/Applications/Microsoft Word.app" ]]; then
  osascript <<OSA >/dev/null
with timeout of 300 seconds
    tell application "Microsoft Word"
        set wasRunning to running
        open POSIX file "$DOCX"
        set d to active document
        save as d file name POSIX file "$PDF" file format format PDF
        close document 1 saving no
        if not wasRunning then quit
    end tell
end timeout
OSA
elif command -v soffice >/dev/null; then
  soffice --headless --convert-to pdf --outdir "$DIR" "$DOCX" >/dev/null 2>&1
  [[ "$DIR/$BASE.pdf" == "$PDF" ]] || mv "$DIR/$BASE.pdf" "$PDF"
else
  pandoc "$SRC" -o "$PDF" 2>/dev/null || {
    echo "No PDF renderer found. Install LibreOffice or a LaTeX engine, or open $DOCX and export a PDF." >&2
    exit 1
  }
fi

[[ -f "$PDF" ]] || { echo "PDF render failed" >&2; exit 1; }
PAGES=$(python3 - "$PDF" <<'PY' 2>/dev/null || echo '?'
import re, sys
d = open(sys.argv[1], 'rb').read()
print(len(re.findall(rb'/Type\s*/Page[^s]', d)) or '?')
PY
)
echo "pdf:  $PDF  ($PAGES pages)"

MAX_PAGES="${MAX_PAGES:-2}"
if [[ "$PAGES" =~ ^[0-9]+$ ]] && (( PAGES > MAX_PAGES )); then
  echo "WARN: $PAGES pages exceeds the $MAX_PAGES-page target - trim bullets in $SRC and rebuild." >&2
fi
