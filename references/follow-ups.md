# Follow-up notes (`followup` mode)

Drafts only (unless the user chose a sending level in `referrals-and-dms.md`). The user sends everything themselves otherwise. This mode never sends a message or a
connection request unless `preferences.md` explicitly says it may.

## Steps
1. Read `applications.csv`. Candidates: `status=applied`, applied 7+ days ago, no matching
   reply event in `pipeline.csv`. Rank by `score`, take the top N (default 5). Skip
   companies already followed up (check `followups/`).
2. For each, find the recruiter or hiring manager on LinkedIn through the user's
   logged-in browser (read-only). Pace yourself and stop on any warning. If nobody is
   found, say so; never guess a name.
3. Draft a note under 200 characters: who the user is, the role, one real matching result
   from `profile.md`. No invented numbers, no "passionate".
4. Save to `<workspace>/followups/<date>.md` as a table: company, role, person, profile
   link, draft, character count.
5. Present the drafts. When the user says they sent one, log event `followed-up` in
   `pipeline.csv`.
