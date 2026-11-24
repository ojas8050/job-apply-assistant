# Weekly review (`review` mode)

Read-only analysis; writes one report to `<workspace>/reviews/<YYYY-MM-DD>.md`. Default
window: last 7 days (the user may ask for 30 days or all-time).

## Compute from `applications.csv` and `pipeline.csv`
1. Applications, replies, interviews, rejections - by source board and by resume variant
   (`resume_used`, normalising filename spellings).
2. Which resume variant and board get the most replies. Say plainly when the sample is too
   small to conclude (do not over-read 1-2 replies).
3. Patterns in skipped / failed / blocked / unverified rows from `notes`: recurring
   ruling-out reasons, account walls, throttles, unanswered screening questions.
4. Stale applications (10+ days, no reply) -> suggest `followup`.
5. Questions still marked `UNKNOWN - ASK USER` in `profile.md`.
6. **Three changes for next week** (searches, resume or profile), each tied to a number
   from steps 1-3.

Spot-check: pick 3 submitted applications and re-read exactly what the employer received
(resume + answers) to confirm nothing was misstated.
