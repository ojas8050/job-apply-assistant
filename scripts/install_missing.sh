#!/usr/bin/env bash
# Install what the skill needs and the machine lacks, from the OS package manager only.
#
#   install_missing.sh plan                         show what is missing and exactly what would run
#   install_missing.sh install <item...> [--dry-run]   install the named items (python3 pandoc libreoffice)
#
# Rules this script follows:
#   - It never runs anything without being asked: `plan` changes nothing; `install` needs the
#     item names, and the skill only calls it after the user said yes.
#   - Package managers only (brew, apt-get, dnf). Never `curl | bash`, never an unknown URL.
#   - It never installs Homebrew itself and never types a sudo password. Commands that need
#     sudo are printed for the user to run in their own terminal.
#   - --dry-run prints the commands and runs nothing.
set -u

MODE="${1:-plan}"; shift 2>/dev/null || true
DRY=0; ITEMS=()
for a in "$@"; do if [[ "$a" == "--dry-run" ]]; then DRY=1; else ITEMS+=("$a"); fi; done

PM=""
for c in brew apt-get dnf; do command -v "$c" >/dev/null 2>&1 && { PM="$c"; break; }; done

have() {
  case "$1" in
    python3)
      command -v python3 >/dev/null 2>&1 && python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)' ;;
    pandoc)
      command -v pandoc >/dev/null 2>&1 ;;
    libreoffice)
      command -v soffice >/dev/null 2>&1 || [[ -d /Applications/LibreOffice.app ]] || [[ -d "/Applications/Microsoft Word.app" ]] ;;
    *) return 1 ;;
  esac
}

cmd_for() {
  case "$PM:$1" in
    brew:python3)         echo "brew install python" ;;
    brew:pandoc)          echo "brew install pandoc" ;;
    brew:libreoffice)     echo "brew install --cask libreoffice" ;;
    apt-get:python3)      echo "sudo apt-get install -y python3" ;;
    apt-get:pandoc)       echo "sudo apt-get install -y pandoc" ;;
    apt-get:libreoffice)  echo "sudo apt-get install -y libreoffice-writer" ;;
    dnf:python3)          echo "sudo dnf install -y python3" ;;
    dnf:pandoc)           echo "sudo dnf install -y pandoc" ;;
    dnf:libreoffice)      echo "sudo dnf install -y libreoffice-writer" ;;
    *)                    echo "" ;;
  esac
}

role()  { [[ "$1" == "python3" ]] && echo "required" || echo "optional"; }
why()   {
  case "$1" in
    python3)     echo "runs the duplicate checker and the resume helper" ;;
    pandoc)      echo "only for tailored resumes (Markdown to DOCX/PDF); a small download" ;;
    libreoffice) echo "only to turn tailored resumes into PDF if you have no Word; a LARGE download" ;;
  esac
}

manual_note() {
  cat <<'NOTE'

Things this script cannot or will not do for you:
  - Install the Chrome automation extension for Claude. Chrome asks for your click to add any
    extension; the skill will open the right page and tell you what to click.
  - Connect Gmail / Google Calendar. You grant that access yourself (only for `inbox` mode).
  - Install Homebrew. If you are on macOS without it, run the official installer from
    https://brew.sh yourself, then run this again.
  - Enter your password. Commands that start with `sudo` are printed for you to run.
NOTE
}

case "$MODE" in
  plan)
    echo "Package manager found: ${PM:-none}"
    printf '\n%-12s %-9s %-10s %s\n' ITEM STATUS NEEDED "WHAT IT IS FOR"
    for it in python3 pandoc libreoffice; do
      if have "$it"; then st="installed"; else st="MISSING"; fi
      printf '%-12s %-9s %-10s %s\n' "$it" "$st" "$(role "$it")" "$(why "$it")"
    done
    echo
    echo "Would run (only if you say yes):"
    any=0
    for it in python3 pandoc libreoffice; do
      if ! have "$it"; then
        c="$(cmd_for "$it")"
        if [[ -n "$c" ]]; then echo "  $it: $c"; else echo "  $it: no supported package manager found; install it by hand"; fi
        any=1
      fi
    done
    (( any )) || echo "  (nothing: everything is installed)"
    manual_note
    ;;
  install)
    (( ${#ITEMS[@]} )) || { echo "usage: install_missing.sh install <python3|pandoc|libreoffice>... [--dry-run]" >&2; exit 2; }
    FAIL=0
    for it in "${ITEMS[@]}"; do
      case "$it" in python3|pandoc|libreoffice) ;; *) echo "unknown item: $it (allowed: python3 pandoc libreoffice)" >&2; FAIL=1; continue;; esac
      if have "$it"; then echo "[$it] already installed, skipping"; continue; fi
      c="$(cmd_for "$it")"
      if [[ -z "$c" ]]; then echo "[$it] no supported package manager; please install it manually"; FAIL=1; continue; fi
      if [[ "$c" == sudo* && "$(id -u)" != "0" ]]; then
        echo "[$it] needs your password. Run this yourself in a terminal, then tell me when it's done:"
        echo "      $c"
        FAIL=1; continue
      fi
      echo "[$it] $c"
      if (( DRY )); then echo "[$it] dry run: not executed"; continue; fi
      if eval "$c"; then
        if have "$it"; then echo "[$it] installed and verified"; else echo "[$it] command finished but the tool is not on PATH yet; open a new terminal and run doctor.sh"; FAIL=1; fi
      else
        echo "[$it] install FAILED; see the output above"; FAIL=1
      fi
    done
    exit $FAIL
    ;;
  *)
    echo "usage: install_missing.sh plan | install <item...> [--dry-run]" >&2; exit 2 ;;
esac
