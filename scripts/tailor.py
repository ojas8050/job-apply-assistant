#!/usr/bin/env python3
"""Make a per-job tailored resume (markdown) from a base markdown resume, then build the PDF.

usage:
  tailor.py --base <resume.md> --out <out.md> --headline "<text>" --summary "<text>" \
            [--first "bullet start 1|bullet start 2"] [--skills "Skill line start A|B"]

It REFRAMES only: headline, summary, skills-block ORDER and first-job bullet ORDER.
It never adds facts. The base resume must use these markdown conventions:
  - a headline line directly under the contact block (first line that follows the
    first blank line after line 1-3), replaced by --headline
  - a '## PROFESSIONAL SUMMARY' heading followed by a blank line and the summary paragraph
  - a '## TECHNICAL SKILLS' section of '- ' lines, ended by '## PROFESSIONAL EXPERIENCE'
  - bullets ('- ') under '## PROFESSIONAL EXPERIENCE', ended by the next '## ' heading
Adjust the heading names with --h-summary/--h-skills/--h-exp if the resume differs.
"""
import argparse
import os
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--base', required=True)
p.add_argument('--out', required=True)
p.add_argument('--headline')
p.add_argument('--summary')
p.add_argument('--first', help='pipe-separated starts of bullets to move first')
p.add_argument('--skills', help='pipe-separated starts of skill lines to move first')
p.add_argument('--h-summary', default='## PROFESSIONAL SUMMARY')
p.add_argument('--h-skills', default='## TECHNICAL SKILLS')
p.add_argument('--h-exp', default='## PROFESSIONAL EXPERIENCE')
p.add_argument('--no-build', action='store_true')
a = p.parse_args()

lines = open(a.base, encoding='utf-8').read().split('\n')


def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    sys.exit(f'heading not found in base resume: {prefix!r}')


if a.summary:
    si = find(a.h_summary)
    lines[si + 2] = a.summary

if a.headline:
    first_blank = next(i for i, l in enumerate(lines) if not l.strip())
    hi = next(i for i in range(first_blank, len(lines)) if lines[i].strip())
    lines[hi] = a.headline

if a.skills:
    s, e = find(a.h_skills), find(a.h_exp)
    block = [l for l in lines[s + 1:e] if l.startswith('- ')]
    new = []
    for key in a.skills.split('|'):
        m = next((b for b in block if b.startswith('- ' + key)), None)
        if m is None:
            sys.exit(f'no skills line starts with {key!r}')
        new.append(m)
    new += [b for b in block if b not in new]
    lines[s + 1:e] = [''] + new + ['']

if a.first:
    ex = find(a.h_exp)
    end = next((i for i in range(ex + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
    idxs = [i for i in range(ex, end) if lines[i].startswith('- ')]
    lo, hi = idxs[0], idxs[-1]
    bul = lines[lo:hi + 1]
    chosen = []
    for key in a.first.split('|'):
        j = next((k for k, x in enumerate(bul) if x.startswith('- ' + key)), None)
        if j is None:
            sys.exit(f'no bullet starts with {key!r}')
        chosen.append(j)
    rest = [k for k in range(len(bul)) if k not in chosen]
    lines[lo:hi + 1] = [bul[k] for k in chosen + rest]

os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, 'w', encoding='utf-8').write('\n'.join(lines))
print('wrote', a.out)

if not a.no_build:
    build = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_resume.sh')
    r = subprocess.run([build, a.out], capture_output=True, text=True)
    print((r.stdout.strip().splitlines() or [r.stderr[-300:]])[-1])
