# Sign-in check (the skill does this itself, before searching)

Run this once the profile is approved and before the first search, and again whenever the
user says "signed in". The skill never relies on the user's word alone: it opens each chosen
board in the user's own Chrome and looks.

## What to do
1. For each board the user chose (`preferences.md` > Boards), open its home or jobs page in a
   new tab and read the page (page text first, screenshot only if unclear).
2. Decide one of three states:
   - **Signed in**: an account signal is visible (avatar, the user's name, "My account",
     "Profile", a jobs feed that only signed-in users get).
   - **Signed out**: a "Sign in / Log in / Register" button, a login wall, an auth redirect,
     or an empty list that the board only fills for members.
   - **Can't tell**: a Cloudflare or "verify you are human" check, a blank page, or a layout
     you do not recognise. Treat it as not confirmed and say so.
3. Never type credentials, never click "Continue with Google/Apple/LinkedIn" on the user's
   behalf, and never solve a verification check. Signing in is the user's step.
4. Do not stop at the first signed-out board: check all of them, then report once.

## Signals to look for (verify at runtime, sites change)
| Board | Where to look | Signed in looks like | Signed out looks like |
|---|---|---|---|
| LinkedIn Jobs, LinkedIn feed posts | linkedin.com/feed | "Me" menu, "Start a post" | redirect to a login or auth-wall page |
| Indeed | your country's Indeed home page | account icon or email at top right | "Sign in" link |
| Naukri | naukri.com | your name / "View profile" | "Login" and "Register" buttons |
| Glassdoor | glassdoor.com | your avatar or profile menu | "Sign in" or a sign-up wall |
| Hirist | hirist.tech | profile menu | "Login" |
| Wellfound | wellfound.com/jobs | your avatar | "Log in" |
| Instahyre | instahyre.com | opportunities feed | redirect to login |
| TopHire | tophire.co | account menu | "Login" |
| Foundit | foundit.in | your name | "Login" / "Register" |
| Cutshort | cutshort.io/jobs | job list shows | blank list or login prompt |
| Welcome to the Jungle | welcometothejungle.com | your avatar | "Sign in" |
| Y Combinator Work at a Startup | workatastartup.com | your name / "Applied" markers | "Log in" |
| Himalayas | himalayas.app | your avatar | "Sign in" |
| Flexiple | flexiple.com | account area | "Login" |
| Company career sites | no login needed to browse | n/a | employer accounts are handled at apply time and queued |

## The message to the user (copy this shape)
Send ONE message after checking all boards:

```
I checked your boards in Chrome.

Signed in:      LinkedIn Jobs, Indeed
Not signed in:  Glassdoor, Wellfound, Himalayas
Couldn't tell:  Cutshort (a verification check appeared)

Please open each "not signed in" board in Chrome, sign in yourself, and then tell me
"signed in". I'll check them again. I never see or type your password.
Other options: say "skip Glassdoor" to drop a board, or "start without them" and I'll begin
with the boards that are signed in.
```
If every board is signed in, say so in one line and start the search. If none are signed in,
do not start; ask the user to sign in first.

## After the user replies
- **"signed in":** re-check ONLY the boards that were missing and report again with the same
  message shape. After three rounds for the same board, ask whether to drop it.
- **"skip X":** remove X from `preferences.md` > Boards and mention it in the final report.
- **"start without them":** start on the signed-in boards. Keep the missing ones listed in
  `queue.md` and remind the user at the next checkpoint and in the final report.
- **No reply:** do not start boards that are not signed in. Wait.

## During the run
If a board signs the user out mid-run (login wall, "session expired"), stop that board, add it
to `queue.md` with what happened, continue with the other boards, and include it in the next
message to the user. Never retry in a loop.
