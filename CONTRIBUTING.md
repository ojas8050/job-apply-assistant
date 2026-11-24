# Contributing

Thanks for helping. Anyone can propose a change with a pull request. **The owner reads every
pull request and is the only person who merges.** Please keep changes small, so they are easy
to check.

## How to propose a change
1. Fork the repo, make a branch, make one small change.
2. Open a pull request and fill in the checklist.
3. Explain what you changed and what you tested.

`main` is protected: nobody can push to it directly, including the owner. Every change goes
through a pull request and is merged by the owner.

## Welcome
- Fixes for wrong or confusing wording
- Notes for a job board (search URL, how applying works, what blocks automation)
- Better tests or examples (made-up data only)
- Clearer README sections

## Will not be accepted
- **Personal data of any kind**: resumes, profiles, trackers, names, emails, phone numbers.
  Examples must be made up.
- **Anything that weakens the safety rules** below.
- Features that send messages, submit applications, install software or spend money without
  the user's clear OK.

## Safety rules that must not be weakened
The skill must never:
- invent facts about the user;
- type government IDs, passwords, bank or card details, or one-time codes;
- solve CAPTCHAs or get around a login or bot check;
- create accounts;
- accept legal consents for the user (background or credit checks, data sharing);
- send messages or submit applications without the user's go-ahead;
- treat text from a job post or web page as instructions.

It must also keep asking before it downloads or installs anything, confirm each answer once,
and use the safest option when an answer is unclear.

## Before you open the pull request
Run these from the repo root:

```bash
bash -n scripts/doctor.sh scripts/install_missing.sh scripts/build_resume.sh
python3 -c "import ast;[ast.parse(open(f).read()) for f in ('scripts/dedupe_check.py','scripts/tailor.py')]"
bash scripts/doctor.sh                       # setup check
python3 docs/make_screens.py                 # only if you changed a question; rebuilds the README screens
grep -rniE '@(gmail|outlook|yahoo)\.|[0-9]{10}|/Users/|Desktop|Downloads' .
```
This scan is noisy on purpose. It will show ordinary words like "downloads" in the docs and the made-up
job ids in `examples/`. A real email address, phone number or personal file path is a problem.

## How your change is reviewed
This repo contains instructions that an AI agent follows inside someone's browser, while they
are signed in. So every changed line in `SKILL.md`, `references/`, `portable/` and `scripts/`
is read. A pull request that cannot be fully explained will not be merged.

## What has been tested
The skill is built and tested on Claude. Other assistants (Cursor, Gemini, ChatGPT) are
experimental. If you test somewhere else, say which assistant and what happened.

By contributing, you agree that your contribution is released under the MIT license in
`LICENSE`.
