# Referral and DM pass (optional, OFF unless the user turned it on)

Applies only if `preferences.md` > "Referrals and DMs" says the user wants it. The user
chooses the level during onboarding. Never go beyond the chosen level, and never send
anything the user has not allowed. LinkedIn is the usual channel; use the user's own
logged-in session, at human pace.

## Levels (the user picks one; default A)
- **A. Drafts only.** Find people and write messages; the user sends them.
- **B. Send DMs to 1st connections.** Send the referral DM yourself to existing 1st-degree
  connections only. Connection requests stay drafts.
- **C. Also send connection requests.** B, plus connection requests (with a short note, see
  below) to 2nd/3rd-degree people. Log each one and DM them after they accept.
Also ask separately: may recruiter-style **emails** found in hiring posts be sent (default
no, drafts only)? Their consent to send applies to the chosen scope only.

## When to run
After an application is submitted (any board or career site), or as a backfill over past
`applied` rows in `applications.csv`. Run it AFTER the board sweeps, as the last pass, so it
never delays applications. Keep the job id and link for every application in the tracker
(the notes column) so this step has them; if the id is missing, fetch the posting.

## Finding people
1. People search on the company name plus a role keyword that fits the user's field.
   Prefer 1st connections, then 2nd, then anyone relevant.
2. Screens, always applied:
   - working professionals only (skip students and people not yet working);
   - skip people at the user's current or former employers if the user said to;
   - skip anyone with an existing thread with the user, or already in the queue file;
   - skip staffing vendors that have no employees on the network.
3. Batch size: 10-25 people per sitting. Stop a batch on any LinkedIn warning.

## Tracking file
Create `<workspace>/referral-queue.csv`:
```
date,person,profile_url,company,role,job_id,job_url,status,notes
```
`status`: invited | accepted | dm_sent | replied | skipped. Never delete rows. Check this
file at the start of each pass: for people who accepted, send (or draft) the DM and update
the row.

## Referral DM
Short and human, written fresh every time. Include: the role title, the job id/number, the
job link, and that the user has already applied. One ask, nothing more. Rules:
- casual tone, no corporate template, no stock lines ("happy to share my resume"); check
  recent sent messages and never repeat wording;
- only facts from `profile.md`; never invent anything;
- never send anything beyond the referral ask.

## Connection requests (level C only)
- Note under LinkedIn's 300-character limit, mentioning the role. Add a note only when the
  job is a strong match AND the posting looks genuine (real company, recent, not an
  evergreen or ghost listing); otherwise send a plain request.
- Free accounts get few notes and a weekly invite cap: about 15 new invites per day is a
  safe ceiling, and stop when LinkedIn warns or the note option disappears.
- Daily total (DMs + invites) default target 25-30; go higher only on days with many 1st
  connections.

## LinkedIn inbox check
Whenever LinkedIn is opened for this pass, read Messaging first and answer new threads:
- read the whole thread and answer what was actually asked (job id, resume, availability,
  notice period, referral) using only profile facts;
- casual, varied wording, never a reused phrase;
- if they ask for something the user does not have (a skill, a document), say so honestly
  or ask the user first;
- skip obvious spam and InMail ads; log calls, assessments and documents to `pipeline.csv`
  and `queue.md` for the user;
- stale docked chat panels can send to the wrong person: close any open panel and verify the
  recipient before typing.
At level A, replies are drafted and shown, not sent.

## Hiring posts in the feed
While reading the feed, catch posts like "we're hiring <the user's role>":
- the JD and apply route are usually in the post, sometimes only inside an image: read
  images too;
- an apply link -> apply there (queue if it needs a login);
- an email address -> draft an email (send only if the user allowed it): subject names the
  role and "via LinkedIn post"; body short and written fresh: saw the post for <role>, who
  the user is in one line from the profile, resume attached, happy to chat. If the post
  asks for details (notice period, location, pay) answer from the profile; unknown -> ask.
- log it in `applications.csv` (`source=linkedin-post`, `status=drafted` or `emailed`) and
  add the poster to the referral queue if they should be messaged.

## Stop conditions
Stop the pass and report on: a LinkedIn warning or restriction, the invite cap, a request
for money, a move to another messaging app, or any message the user has not allowed you to
send.
