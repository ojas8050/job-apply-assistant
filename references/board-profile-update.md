# Job-board profile review and update (asked after sign-in, per board)

Many employers read the user's profile on a board, not only the resume (Naukri, LinkedIn,
Wellfound and Instahyre in particular). Once a board is confirmed signed in
(`signin-check.md`), ask the user whether they want that board's profile reviewed or updated.
Never change a profile without being asked and without showing the exact change first.

## The question (send ONE message covering all boards that are signed in)

```
You're signed in on: LinkedIn Jobs, Indeed, Glassdoor.

Many employers read your profile on each board, not just your resume. Do you want me to
review or improve your profile on any of them? For each board, answer:

  R = Review only. I tell you what to fix and change nothing.
  U = Update it. I show you the exact changes first; after you approve, I make them.
  N = Leave it alone.

Reply like:  "LinkedIn U, Indeed R, rest N"   or   "all R"   or   "all N".
A few things only you can change (photo, verification codes, email or phone).
```
Boards that sign in later (after the user fixes a missing login) get the same question when
they are re-checked. Save the answers in `preferences.md` under "Board profile updates".

## Review (both R and U start here, read-only)
1. Open the board's profile page and read every section.
2. Compare it with `profile.md` and the master resume. List, per board:
   - **Missing or empty sections** (summary, skills, experience, education, certifications).
   - **Outdated facts** (job title, employer, dates, notice period, expected pay, location).
   - **Resume file:** is the attached resume the current one? (Boards like Naukri send this
     file with every application.)
   - **Headline and summary:** names the target title and the 2-3 strongest real skills,
     with the user's real numbers.
   - **Skills:** real skills from the profile that are not listed; skills listed that the
     user does not have (remove) and anything on the boundary list (never add).
   - **Search settings the board uses to match you:** preferred locations, job type, notice
     period, salary expectation fields.
   - **Typos and inconsistencies** between this board and the resume.
3. Present a before -> after list, ordered by impact. Each item: field, current text, proposed
   text, and why. Mark each item `fact from your profile` so the user can see nothing is
   invented.

## Update (U only, after the user approves)
- Wait for "apply these" (or the user's edits). Apply only approved items.
- Edit one field at a time, save, then re-read the page to verify it stuck. Report anything
  that failed to save.
- Where a widget will not take scripted input (date pickers, custom uploads), tell the user
  which field is left for them.
- Log what changed in `<workspace>/board-profiles.md`: date, board, field, old -> new.

## Rules
- **Facts only.** Every word comes from `profile.md` or the resume. Never invent a title,
  metric, skill, certification or employer.
- **Boundary list is final.** Never add a skill, license or certification the user said they
  do not have, and remove such entries if the board already lists them (after telling the
  user).
- **Never touch** passwords, security or two-factor settings, email or phone, payment, account
  deletion, or anything involving identity documents.
- **Ask separately before changing visibility or privacy**: "open to work" visibility,
  who can see the profile, recruiter-contact settings, job alerts and notification settings.
  These affect who sees the user, so each needs its own yes.
- **Do not mass-change.** If the board offers a bulk "update everything from resume" or
  "auto-fill profile from resume" button, review the result before accepting it: parsers
  corrupt dates and titles.
- Keep a short pause between edits and stop if the board shows a warning or rate limit.
- A profile update is not an application: never apply to any job during this step.

## Per-board notes (generic; verify at runtime)
- **LinkedIn:** headline, About, Experience, Skills, Education, Featured, custom profile URL,
  uploaded resumes list. Leave visibility settings alone unless asked.
- **Naukri:** resume headline, key skills, profile summary, employment, education, and the
  attached resume file. Naukri sends this profile with every one-click apply.
- **Indeed:** resume and contact preferences, job preferences. Keep to what is in the profile.
- **Glassdoor:** profile and resume upload; it asks for little, so review quickly.
- **Wellfound, Instahyre, Cutshort, Foundit, Hirist, TopHire:** headline, skills, experience,
  preferences (role, location, salary, notice period), and the resume file.
- **Welcome to the Jungle, Y Combinator Work at a Startup, Himalayas, Flexiple:** the profile
  fields they use for matching (roles, seniority, skills, location, work authorization). Do not
  change anything the user said not to change on a board they already finished setting up.
- **Company career sites and LinkedIn feed posts:** no profile to review.
