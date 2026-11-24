# Running the skill on a schedule (optional)

Goal: every morning, search the last 24 hours on the user's boards and get a short summary,
without having to remember. Applying stays attended unless the user pre-authorized a batch.

## What can and cannot run unattended
- **Safe to schedule:** `search` mode (no applying) plus a summary of new matches, `status`,
  and the weekly `review`.
- **Needs the user present, or an explicit pre-authorization:** applying, anything that
  needs a login, a CAPTCHA, a code, or a government ID.
- **Needs the machine ready:** Chrome open and signed in to the boards, the Chrome
  automation tool connected, and the computer awake. A schedule on a sleeping laptop does
  nothing.

## Options (pick what your Claude setup offers; verify each before relying on it)
1. **A scheduled-task feature in your Claude app or Claude Code** (for example a `schedule`
   skill or scheduled tasks, if you have them). Create a daily task with a prompt like:
   `Run job-apply-assistant in search mode on my chosen boards for the last 24 hours. Do not
   apply. Save new matches to my workspace and give me the shortlist table.`
2. **Your operating system's scheduler** (cron or launchd on macOS/Linux, Task Scheduler on
   Windows) running Claude Code in non-interactive mode with the same prompt, for example
   `claude -p "<prompt>"`. Check your installed version's flags with `claude --help`.
3. **A manual routine:** open Claude each morning and say "search the last 24 hours".

## Rules for scheduled runs
- Use `search` mode or `dry-run` mode only, never an unattended submit.
- Respect each board's pacing and the daily caps in `preferences.md`.
- If anything blocks the run (signed out, CAPTCHA), write it to `queue.md` and stop that
  board; do not retry in a loop.
- End with a short summary: new matches since the last run, duplicates skipped, items
  waiting on the user.
