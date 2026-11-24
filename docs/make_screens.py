#!/usr/bin/env python3
"""Build the screen images in docs/screens/ from the skill's own files.

The question screens (boards, referrals, sign-in report, board profiles, dry-run record) copy
their text word for word from the files the skill reads, so the pictures cannot drift from what
users see. Messages the assistant words itself (setup, onboarding) are typical examples and are
marked as such in the README.

usage: python3 docs/make_screens.py        (run from the repo root; rewrites docs/screens/*.svg)
"""
import os, re, sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs', 'screens')
os.makedirs(OUT, exist_ok=True)

FONT = "SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
FS, CW, LH = 14, 8.45, 22          # font size, char width, line height
W, PAD = 900, 28
COLS = 95                          # wrap width in characters (conservative)
COL = {'t': '#E2E8F0', 'b': '#FFFFFF', 'c': '#FBBF24', 'g': '#4ADE80', 'r': '#F87171',
       'a': '#FBBF24', 'm': '#94A3B8', 'k': '#38BDF8'}


def read(path):
    return open(os.path.join(ROOT, path), encoding='utf-8').read()


def fence_after(path, marker):
    """First ``` block after the line containing marker."""
    text = read(path)
    i = text.index(marker)
    m = re.search(r'```[a-z]*\n(.*?)\n```', text[i:], re.S)
    return m.group(1).split('\n')


TOK = re.compile(r'(\*\*.+?\*\*|`.+?`|\{[gram]\|.+?\})')


def spans(text):
    out = []
    for part in TOK.split(text):
        if not part:
            continue
        if part.startswith('**'):
            out.append((part[2:-2], 'b'))
        elif part.startswith('`'):
            out.append((part[1:-1], 'c'))
        elif part.startswith('{'):
            out.append((part[3:-1], part[1]))
        else:
            out.append((part, 't'))
    return out


def wrap_spans(sp, indent, cols):
    """Wrap a list of (text, cls) into lines of (indent, [(text, cls)])."""
    words = []
    for t, c in sp:
        for w in re.findall(r'\s+|\S+', t):
            words.append((w, c))
    lines, cur, n = [], [], indent
    for w, c in words:
        if w.isspace():
            if cur:
                cur.append((' ', c)); n += 1
            continue
        if n + len(w) > cols and cur:
            while cur and cur[-1][0] == ' ':
                cur.pop()
            lines.append(cur); cur, n = [], indent
        cur.append((w, c)); n += len(w)
    while cur and cur[-1][0] == ' ':
        cur.pop()
    if cur:
        lines.append(cur)
    return lines


class Screen:
    def __init__(self, title):
        self.title, self.rows = title, []      # rows: dict(kind, indent, spans)

    def gap(self):
        self.rows.append({'kind': 'gap'})

    def say(self, text, indent=0):
        """Assistant paragraph; each source line wrapped, hanging indent for list items."""
        for src in text.split('\n'):
            lead = len(src) - len(src.lstrip())
            body = src.strip()
            hang = lead + (2 if re.match(r'(- |\d+\. )', body) else 0)
            first = True
            for ln in wrap_spans(spans(body), lead, COLS):
                self.rows.append({'kind': 'say', 'indent': lead if first else hang, 'spans': ln})
                first = False

    def pre(self, lines, rule=None):
        """Verbatim lines (exact text); only wrapped if longer than the screen."""
        for src in lines:
            if not src.strip():
                self.gap(); continue
            lead = len(src) - len(src.lstrip())
            cls = rule(src) if rule else 't'
            first = True
            for ln in wrap_spans([(src.strip(), cls)], lead, COLS):
                self.rows.append({'kind': 'say', 'indent': lead if first else lead + 2, 'spans': ln})
                first = False

    def user(self, text):
        first = True
        for ln in wrap_spans([(text, 'b')], 2, COLS):
            self.rows.append({'kind': 'user', 'indent': 0, 'spans': ln, 'first': first})
            first = False

    def svg(self):
        top = 56
        h = top + sum(LH if r['kind'] != 'gap' else LH // 2 for r in self.rows) + 36
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
             f'role="img" aria-label="{escape(self.title)}">',
             f'<title>{escape(self.title)}</title>',
             f'<rect width="{W}" height="{h}" rx="14" fill="#0F172A"/>',
             f'<rect width="{W}" height="40" rx="14" fill="#1E293B"/><rect y="26" width="{W}" height="14" fill="#1E293B"/>',
             '<circle cx="26" cy="20" r="6" fill="#F87171"/><circle cx="46" cy="20" r="6" fill="#FBBF24"/>'
             '<circle cx="66" cy="20" r="6" fill="#34D399"/>',
             f'<text x="{W/2}" y="25" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#94A3B8">'
             f'{escape(self.title)}</text>']
        y = top
        for r in self.rows:
            if r['kind'] == 'gap':
                y += LH // 2; continue
            x = PAD + r['indent'] * CW
            if r['kind'] == 'user':
                o.append(f'<rect x="{PAD-10}" y="{y-16}" width="{W-2*PAD+20}" height="{LH+2}" rx="6" fill="#1E293B"/>'
                         f'<rect x="{PAD-10}" y="{y-16}" width="4" height="{LH+2}" rx="2" fill="#38BDF8"/>')
                lead = f'<tspan fill="{COL["k"]}" font-weight="700">&gt; </tspan>' if r.get('first') else '<tspan>  </tspan>'
                body = ''.join(f'<tspan fill="{COL["b"]}">{escape(t)}</tspan>' for t, c in r['spans'])
                o.append(f'<text x="{PAD}" y="{y}" font-family="{FONT}" font-size="{FS}" xml:space="preserve">{lead}{body}</text>')
            else:
                ts = ''.join(f'<tspan fill="{COL[c]}"{" font-weight=\"700\"" if c=="b" else ""}>{escape(t)}</tspan>'
                             for t, c in r['spans'])
                o.append(f'<text x="{x:.1f}" y="{y}" font-family="{FONT}" font-size="{FS}" xml:space="preserve">{ts}</text>')
            y += LH
        o.append('</svg>')
        return '\n'.join(o)

    def save(self, name):
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
            f.write(self.svg())
        return os.path.join(OUT, name)


T = 'Claude Code  |  job-apply-assistant'

# ---- source text copied verbatim from the skill's own files ----
BOARDS = fence_after('references/boards-catalog.md', 'Message to send')
REFERRAL = fence_after('references/referrals-and-dms.md', 'The question to ask')
SIGNIN = fence_after('references/signin-check.md', 'The message to the user')
PROFILE_Q = fence_after('references/board-profile-update.md', 'The question')
DRYRUN = read('examples/dry-run.example.md').strip().split('\n')


def color_rule(src):
    s = src.strip()
    if s.startswith('IMPORTANT'): return 'a'
    if s.startswith('Signed in:'): return 'g'
    if s.startswith('Not signed in:'): return 'r'
    if s.startswith("Couldn't tell:"): return 'a'
    if re.match(r'^\d+\.\s', s) or re.match(r'^(india|global|all)\s+=', s): return 'k'
    if re.match(r'^\d\s{2}', s): return 'k'
    if re.match(r'^[RUN] = ', s): return 'k'
    return 't'


made = []

# 1. setup (typical wording)
s = Screen(T + '  |  1 of 8: setup'); s.user('find me jobs'); s.gap()
s.say("{m|I can control your Chrome, so I am using agent mode.}"); s.gap()
s.say("**Before we start, I checked your computer.**")
s.say("  {g|OK}      Python 3.13 (required)")
s.say("  {r|MISSING}  pandoc (optional): only for tailored resumes")
s.say("  {r|MISSING}  PDF export (optional): LibreOffice or Word; a large download"); s.gap()
s.say("I can install these for you from your system package manager only:")
s.say("  `brew install pandoc`"); s.say("  `brew install --cask libreoffice`"); s.gap()
s.say('OK to install? Say "yes to all", name the items, or "skip". Skipping only turns off tailored-resume PDFs.'); s.gap()
s.user('Yes to pandoc. Skip the rest.'); s.gap()
s.say("Installing pandoc from Homebrew. {g|Installed and verified.} I skipped LibreOffice, so tailored resumes stay as .docx files.")
made.append(s.save('01-setup.svg'))

# 2. boards (exact)
s = Screen(T + '  |  2 of 8: pick your job boards'); s.pre(BOARDS, color_rule); s.gap(); s.user('global'); s.gap()
s.say("I will run on LinkedIn Jobs, Indeed, Glassdoor, Wellfound, Welcome to the Jungle, Y Combinator, Himalayas, Flexiple and company career sites.")
made.append(s.save('02-boards.svg'))

# 3. referrals (exact)
s = Screen(T + '  |  3 of 8: referrals, in plain English'); s.pre(REFERRAL, color_rule); s.gap(); s.user('2 and 1'); s.gap()
s.say("Got it. I will write the referral messages and the recruiter emails, and you send them yourself. You can change this any time.")
made.append(s.save('03-referrals.svg'))

# 4. unclear answer (typical)
s = Screen(T + '  |  4 of 8: when an answer is unclear'); s.say("{m|Same referral question as the last screen. This user gives unclear answers:}"); s.gap()
s.user('both i want A and B'); s.gap()
s.say('**"Both" does not tell me which number you want, so I am not going to guess the riskier one.** For now I will write the messages and you send them yourself. Sending messages for you needs a clear number.')
s.say('{m|Pick one: referrals 1, 2, 3 or 4. Emails 1 or 2. Not sure? Type "2 and 1".}'); s.gap()
s.user('okay'); s.gap()
s.say('**"Okay" never counts as permission to send.** I am keeping the safe settings: I write, you send. You can change it any time by typing for example "referrals 3".')
made.append(s.save('04-unclear-answer.svg'))

# 5. onboarding (typical)
s = Screen(T + '  |  5 of 8: about you'); s.say("**Where is your resume (PDF)?** And your cover letter, if you have one."); s.user('~/Documents/jane_resume.pdf. No cover letter.'); s.gap()
s.say("Thanks, I have read it. A few things a resume does not have. Answer in one message:")
for t in ["1. Total years of professional experience, in whole years", "2. Work authorization for each country", "3. Notice period",
          "4. Current pay (may I disclose it?) and expected pay", "5. Open to relocate, and where? Preferred cities?",
          "6. Remote, hybrid or on-site?", "7. Earliest start date", '8. Equal-opportunity answers, or "prefer not to say"']:
    s.say("  " + t)
s.gap(); s.user('4 years. US citizen. 14 days. $38/hour only if a form requires it; expect $42-48. Austin or Dallas. Prefer not to say.'); s.gap()
s.say("**What do you not have?** List skills, licenses, certifications or experience you do not have, so I never claim them and I flag roles that need them."); s.user('No ICU experience, no pediatric certification, no travel nursing.')
made.append(s.save('05-about-you.svg'))

# 6. sign-in check (exact)
s = Screen(T + '  |  6 of 8: sign-in check, done by the skill'); s.pre(SIGNIN, color_rule); s.gap(); s.user('Signed in'); s.gap()
s.say("**Checked again.** {g|Signed in:} LinkedIn Jobs, Indeed, Glassdoor, Wellfound, Himalayas, Welcome to the Jungle. All your boards are signed in.")
made.append(s.save('06-signin-check.svg'))

# 7. board profile question (exact)
s = Screen(T + '  |  7 of 8: review or update your board profiles'); s.pre(PROFILE_Q, color_rule); s.gap(); s.user('LinkedIn U, Indeed R, rest N')
made.append(s.save('07-board-profiles.svg'))

# 8. dry-run record (exact, from the example file)
s = Screen(T + '  |  8 of 8: what a dry run saves instead of submitting')
s.pre([l for l in DRYRUN], lambda src: 'b' if src.startswith('# ') else ('g' if 'Not submitted' in src else 't'))
made.append(s.save('08-dry-run-record.svg'))

print('wrote', len(made), 'screens to', OUT)
