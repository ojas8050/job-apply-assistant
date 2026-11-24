# Apply playbook

## Browser setup
The default backend is the user's own Chrome session with a browser-automation MCP
(for example Claude in Chrome). Load every tool you need in ONE call (use the host's
tool-search facility, listing: tab context, navigate, computer/click, read_page,
get_page_text, find, form_input, file_upload, tab create/close). Use the user's existing
logged-in session. Never ask for job-board passwords.

## Per-application loop
1. **Duplicate check first** (`scripts/dedupe_check.py`): if the job is already applied,
   queued or in progress on any board, skip it. Re-check right before submitting too: a job
   can be applied to on another board during the same run.
   **Open** the apply URL in a new tab. Read the page text first; screenshot only when
   layout matters.
2. **Identify the ATS** from the URL and page chrome; load its quirks from `job-boards.md`.
3. **Upload the right resume** (default, or the tailored PDF) with `file_upload`. Wait for
   the parse to finish.
4. **Verify the autofill field by field** against `profile.md`. Parsers corrupt dates,
   split names wrong, drop the country code from phone numbers, and import stale data
   from the user's earlier applications on that site.
5. **Skills and education fields:** compare the JD's skill list with the profile and enter
   ALL the user's real skills, not just those the JD names; remove parser junk the user
   lacks; never add anything from the boundary list. Never leave Education empty.
6. **Screening questions:** answer from the profile. Authorization, sponsorship,
   relocation and notice period come from the Logistics section verbatim. Anything not
   covered: collect all such questions and ask in one batch, then save the answers.
7. **Free text / cover letter:** paste the tailored letter. For "why this company" boxes
   write 2-4 sentences grounded in the JD and the profile, no invented enthusiasm.
8. **Multi-page forms:** finish all pages, walk back and re-read before submitting.
9. **Dry run:** if this is a dry run, stop here. Write the pre-submit summary to
   `<workspace>/dry-runs/<company>-<role>.md`, log `status=dry-run`, leave without
   submitting, and go to the next job.
10. **Pre-submit gate:** print company, role, resume used, every answer given. Wait for the
   go-ahead unless this batch was pre-authorized.
11. **Submit**, then confirm it landed (confirmation page, email, or the board's
    "Applied" state). No confirmation = not logged as applied.
12. **Log** the row and close the tab.

## Fields the user must fill themselves
Government ID numbers, tax IDs, bank details, passwords, one-time codes, and any field
asking for a name "as per" an identity document you cannot read. Also declarations that
carry legal weight (relatives, conflicts of interest, criminal/credit/background-check
consents): show the text and let the user decide. Say exactly which fields are left, then
carry on with the rest.

## Known upload limits (verify, sites change)
- Some boards (e.g. Naukri) attach the resume from the user's *profile*; per-job upload
  is impossible there. Check the profile resume before a run.
- LinkedIn Easy Apply creates its file input dynamically and opens a native OS picker,
  which automation cannot reach. Only resumes already saved to the account can be picked;
  the user uploads once by hand.
- Company ATSs (Greenhouse, Lever, Ashby, Workday) expose real file inputs.
- Custom widgets (date pickers, multi-selects, SAP SuccessFactors upload buttons) may
  ignore typed text or scripted clicks. Fall back to clicking through the widget or hand
  the field to the user.
- Required dropdowns can be irrelevant to the user's field (e.g. sales-channel lists).
  Pick the nearest TRUE option, or ask. Do not guess a false one.

## Stop conditions
Stop and report on: CAPTCHA, OTP/2FA, identity or document verification, a login wall, a
timed assessment, a request for government ID or bank details, an application fee, or a
warning about automated access. Describe what is on screen and let the user take over.

## Failure handling
Log `status=failed` with the reason and continue. Never retry a submit that may have gone
through: check the applied state first. A page that looks unchanged after Submit is
UNVERIFIED, not applied: log it as `unverified` and ask the user to look.

## Tracker
`applications.csv` header:

```
date,company,title,location,source,apply_url,resume_used,status,score,notes,job_key
```

`job_key` = the output of `dedupe_check.py --key` (normalized company|title|city). Fill it for
every row so later duplicate checks are exact.

`status`: shortlisted | applied | dry-run | unverified | failed | blocked | queued | skipped | screening |
interview | offer | rejected. Use `shortlisted` for jobs shown to the user and not yet decided (for example a stretch
role). Update the status on later runs when a board or email shows movement.
