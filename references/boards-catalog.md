# Boards and the board-selection question

Used in onboarding (SKILL.md, Phase 0, step 1). The user chooses which of THESE boards the
skill will run on. Do not offer, suggest or search boards outside this list. Save the
choice in `preferences.md` under "Boards". Re-ask only if the user says "add a board" or
"drop a board" (and only add one if the user names it themselves).

## How to ask: ONE plain message, no clickable widgets

Send the message below as ordinary text, all at once. Do NOT use a multi-select tool or
checkbox symbols: multi-select tools split a long list into several pages with small arrows
that users miss, and `[ ]` boxes look clickable but are not. The user answers by typing.

Accept any of these answers: numbers ("1, 2, 4" or "1 2 4"), board names ("LinkedIn,
Indeed"), "all", or a shortcut word. After they answer, repeat back the boards you
understood by NAME and ask them to correct you if it is wrong, then move on.

Message to send (copy exactly):

```
Which job boards should I run on? Just type your answer, no clicking needed.

Type the numbers (for example: 1, 2, 4), or the names, or one of these shortcuts:
  india   = 1, 2, 3, 4, 5, 7, 9, 10, 15
  global  = 1, 2, 4, 6, 11, 12, 13, 14, 15   (outside India)
  all     = everything below

 1.  LinkedIn Jobs
 2.  Indeed
 3.  Naukri                  (India only)
 4.  Glassdoor
 5.  Hirist                  (India only)
 6.  Wellfound
 7.  Instahyre               (India only)
 8.  TopHire                 (India only; placement service, may have no job list)
 9.  Foundit                 (India only)
10.  Cutshort                (India only)
11.  Welcome to the Jungle
12.  Y Combinator Work at a Startup
13.  Himalayas
14.  Flexiple
15.  Company career sites    (Workday, Greenhouse, Lever, Ashby, iCIMS, Taleo, custom)
16.  LinkedIn feed hiring posts (read-only unless you allow emailing)

IMPORTANT: I work inside your own Chrome browser, using your own logins. For every board
you pick, please sign in to it in Chrome first. I never ask for, see or type your passwords.
A board you are signed out of is skipped until you sign in.
Also tell me which of the boards you picked you are already signed in on.
```

## After the user answers
1. Repeat the chosen boards back by name; fix if they say it is wrong.
2. Write the chosen boards into `preferences.md` under "Boards".
3. Later, after the profile is approved, check each chosen board's sign-in state yourself
   (`references/signin-check.md`) and tell the user which boards are missing a login.
4. Search only the chosen boards, in the order of the list above.
5. Do not mention or offer boards that are not on this list.
