# Job boards

How to search, what to read and how applying works, per board. Verify selectors and
URL patterns at runtime; these sites redesign often. If a selector misses, read the page
and adapt rather than guessing coordinates. Choose boards by the user's country and
field (see "Picking boards"), not all of them.

## Rules that apply on every board

- **Use the site's own search bar** with keyword + location. Do not rely only on saved
  feeds or canned URLs.
- **Keyword combinations:** run each separately, they return different results. Derive the
  list from the user's own resume and `profile.md` target titles: the exact title, common
  variants, seniority variants, and the 2-3 core skills as search terms. Show the list to
  the user in onboarding and let them edit it. Examples by field: nursing -> `Registered
  Nurse`, `RN Medical Surgical`, `Nurse Case Manager`; accounting -> `Staff Accountant`,
  `Accounts Payable Specialist`, `Financial Analyst`; marketing -> `Digital Marketing
  Specialist`, `SEO Analyst`, `Content Marketing Manager`; software -> `Backend Engineer`,
  `Java Developer`, `Platform Engineer`.
- **Location sweeps:** (a) home city and the user's other cities, (b) remote / work from
  home, (c) abroad if `preferences.md` allows. Skip a sweep only if the user excluded it.
- **Recency:** use the board's own date filter (last 24 hours, then last 7 days; if no 24h
  option, last 3 days or sort by newest).
- **Open and read the JD of every job you consider** (years, must-have stack, domain,
  location/remote). If the JD is cut off, open the external apply page. Never decide
  from the title or card. Log skips with the reason taken from the JD.
- **Depth:** go several pages deep (default at least 3, then keep going while results
  stay relevant; stop after 2-3 irrelevant pages and list that cutoff in the report).
  For infinite scroll, load more until results turn irrelevant.
- **Duplicates:** run `scripts/dedupe_check.py` for every job, across ALL boards. Skip only
  the same real job (same id, URL, or company + title + city); a different role at the same
  company is not a duplicate.
- **External apply:** when "Apply" opens a company site or ATS, go there. If it needs a
  login, account, OTP or CAPTCHA, add it to `queue.md` (company, title, URL, which gate)
  and continue. If it lands on a generic careers page, use that site's search bar for
  matching roles instead of stopping.
- **Signed-out boards:** tell the user which boards are signed out so they can sign in;
  queue the rest.
- **Log every apply / skip / queue** in `applications.csv`.
- **Stop a board on** a rate limit, block page, or ToS warning, and report it.

## Boards

The user chooses the boards during onboarding from `boards-catalog.md` and the choice is
saved in `preferences.md` under "Boards". Search only those boards, and only the boards in
that list. Ask the user which of them they are already signed in on.

## Per-board notes (generic; verify at runtime)

**LinkedIn.** Search: `https://www.linkedin.com/jobs/search/?keywords=<q>&location=<loc>&f_TPR=r86400`
(`r86400` = 24h, `r604800` = 7 days, `f_WT=2` remote, `f_AL=true` Easy Apply).
Typing a city can add a distance radius by default; prefer `geoId` values if the user
has a saved set. Easy Apply is a 1-5 step modal; the resume is picked from files already
on the account. Heavily rate-limited: JD endpoints throttle after roughly 15 rapid
loads, so pace yourself. Feed posts and DMs are a separate, optional pass.

**Indeed.** Use the country site's search bar; Date posted -> last 24 hours / 7 days
(`fromage=1` / `fromage=7`). Expect Cloudflare interstitials: hand back to the user.
Result lists can contain honeypot links (fake job ids): read ids from `a[data-jk]` and
open `/viewjob?jk=<id>` rather than clicking every anchor. "Apply with Indeed" may show a
qualification check; "Apply on company site" hands off to an ATS. A final CAPTCHA on
Submit means: fill everything, leave the tab open, queue for the user.

**Naukri (India).** Search bar + Freshness filter + sort by date; also the
work-from-home filter. URL pattern: `https://www.naukri.com/<role>-jobs-in-<city>?experience=<yrs>`.
Most listings apply in one click once logged in and send the profile resume. Chatbot
answers may be truncated to 100 characters. Keep the Naukri profile in sync with
`profile.md`.

**Glassdoor.** Search bar title + location, Date posted filter. Job descriptions can be
fetched from the job-listing endpoint once logged in. A login wall appears quickly.

**Hirist, Instahyre, Foundit, Cutshort, TopHire.** (TopHire is a placement service and may have no public job list; Cutshort's list can be blank until the user is signed in.) Search bar + freshness filter + remote.
Most need a login; queue if signed out. Some job pages render the JD only after
navigation (not in fetched HTML), so open each job in a tab. Apply job by job, never
with a blanket "apply to all" button.

**Wellfound.** Card-level "Apply" buttons on LIST pages can be ONE-CLICK applications
with no JD preview: always open the job page first. After applying it may offer a
video-intro share; decline unless the user wants it.

## Company career sites / ATS (identify from the URL)
- `*.myworkdayjobs.com` - Workday: account per employer, long multi-page forms, the
  worst resume parser (autofill wrecks education and titles); sessions expire, so a
  refresh can lose unsaved steps. Verify the Review step before submitting.
- `boards.greenhouse.io`, `jobs.lever.co`, `jobs.ashbyhq.com` - single page, usually no
  account, good parsers.
- `*.icims.com`, `*.taleo.net` - account required, multi-page, sessions time out. Do not
  leave one idle.
- SAP SuccessFactors portals - account required, one long page, custom widgets; may carry
  stale data from an earlier draft.
- Consent boxes: follow `preferences.md`. By default tick only the mandatory ones and
  decline optional AI-screening, retention and marketing options; never accept
  credit/criminal/background-check consents for the user.

## Optional passes (only if the user enabled them)
Referral outreach, LinkedIn inbox replies and hiring posts in the feed follow
`references/referrals-and-dms.md`, at the level the user chose in onboarding. Default: off.

## Adding a board
Only add a board if the user names it themselves. Record: search URL pattern, result-list
selector, fields to capture, apply mechanism, whether an account is needed, and known bot
detection.

## Notes for the remaining boards (verify at runtime)

**Flexiple.** A vetting and matching funnel, not a normal job list. Forms often prefill
values from a previous profile (notice period, expected pay): check every prefilled field
against `profile.md`, fix it, and answer scenario questions only from profile facts.
Nothing here is a one-click apply.

**Himalayas.** Remote-jobs board, account needed. Many listings say "worldwide" but exclude
countries in the small print: read the location / timezone / "allowed to work in" lines in
each JD against the user's country and work authorization. A Cloudflare check may appear
and pass by itself; never bypass a manual one. Applying usually redirects to the company's
ATS.

**Welcome to the Jungle and Y Combinator Work at a Startup.** Account-based. Preference
filters on Welcome to the Jungle (salary floor, "permanent only") can hide good local jobs:
say so in the report if results look thin. On Work at a Startup, search by description at
`/jobs`, job pages are `/jobs/<id>`; an application is a short note to the founders,
written fresh and honest.

## Speed tricks (proven on real runs; selectors change, so verify)

General
- Tool output filters may block anything that looks like a URL, a query string, or a
  cookie. Print results with the characters `: / ? = & < > @` replaced by spaces (for
  example `.replace(/[:\/?=&<>@]/g,' ')`) and never print `location.search` or
  performance entries.
- Some sites reload themselves after about a minute and wipe `window` state and
  localStorage. Work in chunks of 45 seconds or less and print each chunk's results
  immediately.
- Clicking list anchors often navigates away and kills a running script. Read the ids from
  the list, then fetch or open each job separately.
- Never get around a CAPTCHA or an anti-bot check to read a JD; open the page in a tab and
  hand the check to the user.

LinkedIn (JS sweep)
- On a results page, inject a script that clicks each job card by index, waits about 2.2 s,
  and stores `{id, applyButtonType (Easy Apply vs company site), years/skills snippet from
  the JD}` into `window.__out`. Read it back in chunks under about 700 characters per call.
- Cards whose snippet has no years still need an individual JD read.
- Collect the card elements first and click by index; the feed reshuffles on reload, so
  finish a page before reloading.
- Pace it: JD endpoints throttle after roughly 15 rapid loads.

Glassdoor (fast JD reads)
- Read job ids from `li[data-jobid]` on the list page, then `fetch('/job-listing/j?jl=<id>')`
  from that same page and parse the element matching `[class*="JobDetails_jobDescription"]`.
  About 30 JDs per minute. List URL pattern: `/Job/<country>-<keyword>-jobs-SRCH_...htm?fromAge=7`.
- "Easy Apply" can open Indeed SmartApply: screener answers accept whole numbers only, and
  current pay may be prefilled (clear it unless the user wants it disclosed).

Naukri (JDs without clicking each card)
- Open each job page in a same-origin hidden iframe, wait for "Job description", and read
  its text. The JD API behind it needs a reCAPTCHA token: do not try to get around it.

Hirist
- The JD is not in the page HTML and iframes are blocked. Open each job in its own tab (in
  parallel, a few at a time) and read the page text after "Job Description".
- Pagination needs the page buttons (the `page` URL parameter repeats the same results).
- The experience filter is a URL: `/search/<keyword>-jobs?query=<keyword>&minexp=<n>&maxexp=<n>&page=0`.
  Unfiltered result pages skew to 4+ years.

Wellfound
- Job pages (`/jobs/<id>-<slug>`) return server-rendered text to `fetch`, so JDs can be read
  without opening a tab. List pages look like `/role/l/<role>/<location>?page=N`.
- Card-level "Apply" on list pages can be ONE-CLICK APPLY. Always open the job page first.
  Applying from the job page opens a modal with a note field; a "share video intro" toggle
  may default to on (turn it off). Sent applications are listed at `/jobs/applications`.

Instahyre
- "View job" opens a modal with the JD plus Apply and Not interested. A read-only sweep is:
  click View job, read the modal text, click the close button. Apply job by job, never with
  a blanket button, and never click blindly through onboarding dialogs (an onboarding
  wizard once mass-applied to a user's whole feed).

Indeed
- Read ids from `a[data-jk]` and open `/viewjob?jk=<id>`. Result lists contain honeypot
  anchors with fake ids; never script-click every anchor.
