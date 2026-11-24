# job-apply-assistant

A Claude Code skill that finds jobs that fit your resume, fills the applications in your own
logged-in browser, and keeps a tracker. It ships with no personal data: your profile,
preferences, resume and tracker live in a workspace folder on your computer (default
`~/job-hunt/`), created by an onboarding chat the first time you use it.

You stay in control. By default it shows you a summary before it submits anything, never
types government IDs, passwords or codes, and never sends messages for you.

---

## 1. What you need

**Required**
| What | Why |
|---|---|
| **Claude Code** (desktop app or CLI) | Runs the skill |
| **A browser-automation tool for Claude** that drives your own Chrome, for example the **Claude in Chrome** extension (install it from Anthropic's current instructions) | Lets Claude search boards and fill forms in the browser where you are already signed in |
| **Google Chrome**, signed in to the job boards you want to use | The skill uses your existing logins and never asks for passwords |
| **Your resume as a PDF** | Uploaded to forms and read to build your profile |
| **Python 3.9 or newer** (`python3 --version`) | Runs the duplicate checker and resume helper |

**Optional (install only what you need)**
| What | When you need it |
|---|---|
| **pandoc** (https://pandoc.org) + **LibreOffice** (https://www.libreoffice.org) or Microsoft Word | Only for tailored resumes (`tailor` mode): Markdown -> DOCX -> PDF |
| **Gmail and Google Calendar connectors** for Claude | Only for `inbox` mode (recruiter email -> draft replies and interview slots) |
| **An Apify account + `APIFY_TOKEN`** (https://apify.com) | Only if you want bulk search without the browser |
| **A LinkedIn account** | Only for the LinkedIn board and the referral/DM pass |

## 2. Files and information to have ready

Have these before you start so onboarding takes about five minutes:
1. **Resume (PDF)**, the version you want sent by default. Keep it under 2 MB (LinkedIn's
   limit). A `.md` or `.docx` copy is only needed if you want per-job tailoring.
2. **Cover letter (PDF)**, optional. If you give one, say whether to attach it everywhere
   there is an upload slot.
3. **Certificates or transcripts**, optional. Some company forms ask for them.
4. **Links**: LinkedIn, GitHub, portfolio (or "none").
5. **Answers a resume does not contain:** work authorization for each country you would
   work in, notice period, current and expected pay (and whether to disclose current pay),
   relocation, preferred cities, remote or on-site, earliest start date.
6. **A list of skills you do NOT have.** This keeps the skill from putting you in roles you
   cannot do and from claiming a skill on a form.
7. **Which boards you use and are signed in on** (the skill asks).

## 3. Install

1. Copy this folder to `~/.claude/skills/job-apply-assistant/` (personal use) or to
   `<your project>/.claude/skills/job-apply-assistant/`.
2. Install the Chrome automation tool for Claude and sign in to your job boards in Chrome.
3. Optional tools: `pandoc` and LibreOffice (or Word) for tailored resumes.
4. Start a **new** Claude Code session so it loads the skill.
5. Say "run the doctor" (or run `scripts/doctor.sh`) to check Python, pandoc, your resume path
   and the optional tools. Then ask Claude to list your open Chrome tabs; if it cannot, the
   Chrome automation tool is not connected yet.

## 4. First run: what happens

Say something like **"find me jobs"** or **"run the job-apply-assistant skill"**. The skill asks, in order:

1. **Which job boards to use**: one message with a numbered list of 16 (LinkedIn Jobs,
   Indeed, Naukri, Glassdoor, Hirist, Wellfound, Instahyre, TopHire, Foundit, Cutshort,
   Welcome to the Jungle, Y Combinator Work at a Startup, Himalayas, Flexiple, company career
   sites, LinkedIn feed hiring posts). You just **type** your answer: numbers ("1, 2, 4"),
   names, `all`, or a shortcut (`india` or `global`). It repeats your choice back so you can
   correct it, and asks which boards you are already signed in on. It tells you up front: **sign in to every
   board you pick, in your own Chrome, before the search starts.** The skill never asks for or
   types your passwords, and it skips any board you are signed out of.
2. **Referral and DM pass?** No (default), A drafts only, B send DMs to your 1st connections,
   C also send connection requests. Plus whether recruiter emails may be sent or are drafts.
3. **Your resume** (and cover letter). It reads the resume and builds `profile.md`.
4. **The things a resume lacks** (authorization, notice period, pay, relocation, cities).
5. **Skills you do not have.**
6. **Run rules:** experience range, apply without asking or confirm each time, how deep to
   search, abroad and remote, optional consent boxes.
7. **Dry run first?** (recommended): fills forms but never submits, so you see exactly what
   would be sent.
8. **Keyword check:** it shows the job titles and search terms it derived from your resume
   (and the gaps it noticed) so you can edit them.
9. **Confirm the profile.** Nothing runs until you approve it.
10. **Sign-in check, done by the skill itself.** After you approve the profile, it opens each
    chosen board in your Chrome and looks. It then tells you in one message which boards are
    signed in, which are not, and which it couldn't tell. Sign in to the missing ones yourself,
    then say "signed in" and it re-checks only those. It never searches a board that is signed
    out, and never sees or types your password.
11. **Board profiles.** For every board you're signed in on, it asks whether to **R**eview your
    profile there (it tells you what to fix, changes nothing), **U**pdate it (it shows the exact
    changes first and edits only after you approve), or **N** leave it alone. Employers often
    read the board profile, not just your resume. It uses only facts from your resume, never
    adds skills you said you don't have, and asks separately before touching visibility or
    privacy settings.

Everything is saved in the workspace, so the next run skips onboarding.

## 5. Every run: what it does

1. **Search** each chosen board: search bar, several keyword combinations, last 24 hours then
   last 7 days, home city plus remote (and abroad if you allowed it). It **opens and reads
   the job description of every job**, never judging from the title alone.
2. **Duplicate check across boards** (`scripts/dedupe_check.py`): the same job on LinkedIn,
   Indeed and Naukri is applied to once. It matches job ids, URLs, and company + title + city.
3. **Score** each job 0-100 and show a shortlist with the main reason to apply and the main
   risk. You can drop rows.
4. **Tailor** the resume only when a job needs a skill you really have that your resume
   buries. It reframes true bullets and never invents anything.
5. **Apply:** it fills the form from your profile, checks every autofilled field, answers
   screening questions (and asks you once for any it does not know, then remembers), shows a
   summary, and submits after your OK (unless you pre-approved a batch).
6. **Log** every job in `applications.csv`: applied, skipped (with the reason from the JD),
   failed, queued, or unverified.
7. **Report:** counts, what is waiting on you, searches that stopped early and why.

## 6. What you will have to do yourself

The skill stops and hands over (listing each item in `queue.md`) for:
- government IDs, tax numbers, bank details, passwords and one-time codes
- CAPTCHAs, human-verification checks, logins and timed assessments
- legal declarations and consents (background, credit, criminal checks)
- anything it cannot do in a custom form widget (for example some date pickers or upload
  buttons); it tells you exactly which field is left

## 7. Commands you can use

| Say | What happens |
|---|---|
| "find me jobs" / "apply to jobs" | Full run (search, shortlist, apply) |
| `dry-run` | Full flow, but it never presses Submit; it saves what it would send. Recommended for your first run |
| `doctor` | Checks your setup and tells you what is missing |
| `profile-update <board>` | Review or update your profile on one signed-in board (never applies to jobs) |
| `search <role> in <city>` | Search and score only, no applying |
| `status` | Funnel summary from your tracker, flags stale applications |
| `tailor <job url>` | Build a tailored resume for one posting |
| `inbox` | Recruiter email -> draft replies and calendar proposals (drafts only) |
| `prep <company>` / `mock <company>` / `debrief <company>` | Interview brief, mock interview, post-call notes |
| `followup` | Draft follow-up notes for applications older than 7 days |
| `review` | Weekly analysis and three changes for next week |

## 8. Files it creates in your workspace

```
~/job-hunt/
  profile.md          who you are (facts only, never guessed)
  preferences.md      the run rules you chose
  applications.csv    one row per job: date, company, title, location, source, URL, resume used,
                      status, score, notes, job_key
  queue.md            things waiting on you (logins, codes, unknown answers)
  referral-queue.csv  only if you enabled the referral/DM pass
  postings/  tailored/  dry-runs/  interviews/  followups/  reviews/  pipeline.csv
```
These hold personal data. Keep them out of public repos and never paste them into other tools.

## 8b. Examples and scheduling

- `examples/` has made-up sample files (a profile, preferences, a tracker with a duplicate and
  an unverified row, a shortlist, a waiting-on-you queue, and a dry-run record) so you can
  see what you will get before you start.
- `references/scheduling.md` explains how to run a daily 24-hour search (search or dry-run
  only) and what cannot run unattended.

## 9. Troubleshooting

| Symptom | What to do |
|---|---|
| "Board is signed out" | Sign in in Chrome, say "signed in", it continues |
| Cloudflare or "verify you are human" page | Complete it yourself; the skill never bypasses it |
| LinkedIn stops loading jobs | It throttles after about 15 rapid loads; wait and let the skill pace itself |
| Status says `unverified` | The page showed no confirmation after Submit; check the board's "Applied" list and tell the skill the result |
| A form field would not take typed text | Custom widget; the skill tells you which field to fill by hand |
| Resume upload not possible on a board | Some boards (Naukri, LinkedIn Easy Apply) only use the resume saved to your account; update it there once |
| `doctor` reports MISSING | Fix the listed item, run it again |
| Tailored PDF will not build | Install `pandoc` and LibreOffice (or Word), or open the generated `.docx` and export a PDF |

## 10. Safety, privacy and terms

It will not invent facts, type government IDs, passwords or bank details, solve CAPTCHAs,
create accounts, accept background/credit-check consents, or send messages without your
go-ahead. Some job sites forbid automation in their terms of use; you use this on your own
accounts at your own risk, and a site may limit or suspend an account for automated use.
Your resume and answers are sent to the employers and boards you apply to; the skill sends
nothing anywhere else.

## 11. Publishing checklist (maintainers)

Before publishing, confirm nothing personal is in the folder:
```bash
grep -rniE '@(gmail|outlook|yahoo)\.|[0-9]{10}|/Users/|Desktop|Downloads' .
```
Expected: only the example paths in this README. Never add `profile.md`, `preferences.md`,
`applications.csv`, `queue.md`, resumes or cover letters (see `.gitignore`).

Ways to publish:
- **GitHub repo:** put this folder at the repo root (or under `skills/job-apply-assistant/`), add
  a `LICENSE` of your choice, push. Users copy the folder into `~/.claude/skills/`.
- **Claude Code plugin:** wrap it with a `.claude-plugin/plugin.json` and a
  `skills/job-apply-assistant/` directory, then list it in a plugin marketplace repo.
- **Zip:** `zip -r job-apply-assistant.zip job-apply-assistant -x '*.DS_Store'`.

If this will be shared outside your company or organization, check whether your employer
needs to sign off on it first.

## 12. Layout

```
SKILL.md                         entry point: rules, onboarding, phases, modes
references/boards-catalog        the 16 boards, asked in one plain message
references/job-boards            search method, per-board notes, ATS quirks, speed tricks
references/preferences-template  run rules the user chooses at onboarding
references/profile-template      candidate profile shape (includes "skills I do NOT have")
references/apply-playbook        per-application loop, human-only fields, stop conditions
references/match-rubric          scoring and dealbreakers
references/tailoring             reframe-never-invent resume tailoring
references/referrals-and-dms     optional referral / DM pass, off by default
references/board-profile-update  optional review/update of your profile on each signed-in board
references/signin-check          the skill checks each board's login itself and reports what's missing
references/{follow-ups,inbox-to-calendar,interview-prep,weekly-review,apify,scheduling}
scripts/doctor.sh                setup check (Python, pandoc, resume path, optional tools)
scripts/dedupe_check.py          cross-board duplicate check
scripts/build_resume.sh          markdown -> docx -> pdf (pandoc; Word or LibreOffice)
scripts/tailor.py                reorder/reword a base resume, then build
examples/                        made-up sample files
```
