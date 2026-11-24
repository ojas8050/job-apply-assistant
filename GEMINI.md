# Instructions for AI coding agents (experimental)

This repository is a job-application skill. It is written and tested for **Claude Code**
(`SKILL.md` is the entry point). Other agents can follow the same files, but this is untested.

- **First decide your mode** (`SKILL.md`, "Step 0"). If you can control the user's own browser,
  use agent mode. If not, use chat mode (`portable/ASSISTANT-PROMPT.md`) and never mix the two.
- Read `SKILL.md`, then the files in `references/` as it directs.
- Wherever the docs name Claude's browser tool ("Claude in Chrome"), use your own browser
  automation tool that controls the user's own signed-in browser.
- The scripts in `scripts/` are plain Python and bash and work anywhere.
- Keep every rule in `SKILL.md` "Non-negotiables": never invent facts, never type government IDs
  or passwords, hand back at CAPTCHAs and logins, ask before downloading or installing anything,
  and show a summary before submitting (or run in dry-run mode).
- If you have no browser tool, do not pretend. Use `portable/ASSISTANT-PROMPT.md` (chat mode).
- Confirm each answer once, and if an answer is unclear use the safest option and ask again with
  numbers; "yes" or "okay" never means "send".
