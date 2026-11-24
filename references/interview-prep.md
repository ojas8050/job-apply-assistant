# Interview prep, mock and debrief (`prep`, `mock`, `debrief`)

Files go to `<workspace>/interviews/<company>-<role>/` (`brief.md`, `mock-<date>.md`,
`debrief-<date>.md`). Truth only: every claim about the user comes from `profile.md`;
unsupported topics are marked as gaps, never papered over.

## `prep <company> [role] [date]` - one-page brief
Inputs: the saved JD in `postings/` (or ask for a paste), the tailored resume if any,
`profile.md`. Produce:
1. Company in 5 lines: what they sell, to whom, recent news (web search; cite sources, say
   so if thin).
2. Why the user fits: 3 points, each tied to a real result in the profile.
3. A 60-second intro for this role.
4. 8 likely questions with answer outlines from real experience. For skills on the user's
   boundary list, draft an honest "I haven't used X, the closest is Y" answer.
5. Notice period and expected pay answers from the Logistics section.
6. 4 sharp questions to ask them.
Also check the resume that was sent: the user must be ready to defend every line on it.

## `mock <company> [technical|hr]`
One question at a time; wait for the answer. After each: score /10, what was missing, a
stronger version using only real experience. After 6 questions name the 3 weakest areas.
Save transcript and scores to `mock-<date>.md`. Tailor technical questions to the user's
field (from `profile.md`).

## `debrief <company>`
The user pastes call notes. Produce: a short thank-you email draft (draft only), the
tracker update (event `interview-done`, next step, date in `pipeline.csv`), and 2 answers
to strengthen next time. Save to `debrief-<date>.md`.
