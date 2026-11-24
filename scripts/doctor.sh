#!/usr/bin/env bash
# Setup check for job-apply-assistant.
#
#   doctor.sh [workspace]        (default workspace: ~/job-hunt, or the path in ~/job-hunt/workspace.txt)
#
# Prints OK / MISSING / OPTIONAL per item and exits 1 if something REQUIRED is missing.
# It cannot see the browser tool from the shell: after this passes, ask Claude to list your
# open Chrome tabs; if it cannot, install/connect the Chrome automation tool first.
set -u

WS="${1:-}"
if [[ -z "$WS" ]]; then
  if [[ -f "$HOME/job-hunt/workspace.txt" ]]; then WS="$(cat "$HOME/job-hunt/workspace.txt")"; else WS="$HOME/job-hunt"; fi
fi
FAIL=0
ok()   { printf '  OK        %s\n' "$1"; }
miss() { printf '  MISSING   %s\n' "$1"; FAIL=1; }
opt()  { printf '  OPTIONAL  %s\n' "$1"; }

echo "job-apply-assistant setup check (workspace: $WS)"
echo "Required"
if command -v python3 >/dev/null; then
  if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)'; then
    ok "python3 $(python3 -c 'import platform;print(platform.python_version())') (needs 3.9+)"
  else
    miss "python3 is older than 3.9 (duplicate checker needs 3.9+)"
  fi
else
  miss "python3 not found"
fi

if [[ -d "$WS" ]]; then ok "workspace folder exists"; else opt "workspace folder not created yet (the first run creates it)"; fi

if [[ -f "$WS/profile.md" ]]; then
  ok "profile.md present"
  RES="$(grep -iE '^- *Master resume path:' "$WS/profile.md" | head -1 | sed -E 's/^[^:]*:[[:space:]]*//')"
  RES="${RES/#\~/$HOME}"
  if [[ -z "$RES" ]]; then miss "profile.md has no 'Master resume path'"
  elif [[ -f "$RES" ]]; then
    ok "resume file found: $RES"
    SZ=$(wc -c <"$RES"); (( SZ > 2000000 )) && echo "  WARN      resume is over 2 MB; LinkedIn rejects files that large"
    case "$RES" in *.pdf|*.PDF) ;; *) echo "  WARN      resume is not a PDF; most forms prefer PDF";; esac
  else miss "resume path in profile.md does not exist: $RES"; fi
else
  opt "profile.md not created yet (onboarding creates it)"
fi
[[ -f "$WS/preferences.md" ]] && ok "preferences.md present" || opt "preferences.md not created yet (onboarding creates it)"

if [[ -f "$WS/applications.csv" ]]; then
  HDR="$(head -1 "$WS/applications.csv")"
  case "$HDR" in
    date,company,title,location,source,apply_url,resume_used,status,score,notes*) ok "applications.csv header looks right";;
    *) miss "applications.csv header is wrong: $HDR";;
  esac
fi

echo "Optional (only for the features noted)"
command -v pandoc >/dev/null && ok "pandoc (tailored resumes)" || opt "pandoc not found: tailored resume PDFs will not build"
if [[ "$(uname)" == "Darwin" && -d "/Applications/Microsoft Word.app" ]]; then ok "Microsoft Word (PDF export)"
elif command -v soffice >/dev/null; then ok "LibreOffice (PDF export)"
else opt "no Word/LibreOffice found: tailored resumes stay .docx until you export a PDF"; fi
[[ -n "${APIFY_TOKEN:-}" ]] && ok "APIFY_TOKEN set (bulk search)" || opt "no APIFY_TOKEN: the skill searches through your browser instead"

echo
if (( FAIL )); then echo "Result: fix the MISSING items above, then run again."; exit 1; fi
echo "Result: shell checks passed. Last check: ask Claude to list your open Chrome tabs. If it cannot, install/connect the Chrome automation tool."
