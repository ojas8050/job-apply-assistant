# Tailoring the resume to the JD

Goal: the ATS ranks the resume highly and the human reader sees their own job
description reflected in the first third of page one. The master resume is never
modified. Tailor only when the default resume does not already cover what the JD needs.

## The hard line: reframe, never invent

Allowed: reordering, rewording, re-emphasizing, choosing which TRUE bullets appear,
swapping a synonym for the JD's own term when it means the same thing, promoting a real
skill from a buried line into the headline.

Never allowed: a tool, employer, title, date, degree, certification, metric or
years-of-experience figure the master resume does not already support. If the JD asks
for something the user lacks, leave the gap and flag it in the shortlist notes. A 70%
match that survives scrutiny beats a 100% match that collapses in the interview.

Adjacent skill: do not claim it. A software JD says Cypress and the user has Selenium; a
nursing JD asks for a telemetry certification and the user has med-surg experience; an
accounting JD names NetSuite and the user has QuickBooks. Lead with the transferable
framing ("framework-agnostic UI automation", "five years of monitored-patient care",
"ERP month-end close") and let the recruiter judge.

## Method
1. Extract from the JD, in its words: required skills, nice-to-haves, tooling, domain,
   seniority, and the 3-4 responsibilities it repeats or lists first.
2. Map each requirement to evidence in `profile.md`: strong / partial / absent. The
   absent list is the honest gap list; it goes in the shortlist notes, not on the resume.
3. Rewrite the headline and summary to name the target title and the JD's top three
   requirements, using the user's real numbers. Highest-leverage edit.
4. Reorder the skills block so the JD's stack comes first, using the JD's exact
   spelling ("CI/CD" vs "CICD", "EHR" vs "electronic health record", "A/P" vs "accounts payable").
   ATS keyword matching is literal.
5. Pick and reorder bullets: the top 4-5 bullets of the current role map to the JD's top
   responsibilities. Cutting is fine, the master keeps everything.
6. Re-word bullets toward the JD's vocabulary, keeping the metric intact.
7. Keep to the master's page count (2 pages max unless the user says otherwise).

## Keyword coverage check
List the JD's required terms and confirm each appears in the tailored text at least once,
in a true context. Report it ("14/17 required terms present; missing: X, Y - genuine gaps").

## ATS-safe formatting
No tables, text boxes, columns, headers/footers, images or icons. Standard section
headings, dates as `MMM YYYY - MMM YYYY`, upload PDF unless the form asks for DOCX.

## Build
```bash
cp "<master resume>.md" "<workspace>/tailored/<company>-<role>.md"
# edit that copy, then:
<skill dir>/scripts/build_resume.sh "<workspace>/tailored/<company>-<role>.md"
```
`build_resume.sh` converts Markdown -> DOCX (pandoc) -> PDF and warns above the page
limit. Verify the built PDF (`pdftotext`) before uploading: contact line, dates and
headings must survive the round-trip. Upload the PDF, not the markdown.

## Cover letter
Only when the form has a slot (or the user's preferences say to attach one). Three short
paragraphs: why this role at this company (from the JD), two concrete proof points from
the profile, a one-line close. Name the company and role. No "I am passionate about", no
claims about products the user has not used.

## Record
Put the built PDF's filename in the `resume_used` column of `applications.csv`.
