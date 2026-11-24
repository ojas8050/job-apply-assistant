#!/usr/bin/env python3
"""Cross-board duplicate check against the tracker.

The same job often appears on several boards under different titles and URLs. Run this
BEFORE applying (and while searching) so one real job is applied to once.

usage:
  dedupe_check.py <applications.csv> --company "Acme Pvt Ltd" --title "Sr. QA Engineer (Remote)" \
                  [--location "Bengaluru, India"] [--url <apply_url>] [--jobid <id>]
  dedupe_check.py --key --company ... --title ... [--location ...]     # just print the job_key

exit code 0 = NEW (safe to apply), 1 = DUPLICATE (prints the matching row and why),
2 = usage error.

Matching, strongest first:
  1. same canonical job id (LinkedIn /jobs/view/<id>, Indeed jk=<id>, Glassdoor jl=<id>,
     Naukri ...-<digits>, Wellfound /jobs/<id>-, Greenhouse/Lever/Ashby uuids, or --jobid)
  2. same apply URL with tracking parameters removed
  3. same job_key  = normalized company | normalized title | normalized city
  4. same (or abbreviated) company + same city + near-identical title, abbreviation-aware
     ("RN Med Surg" = "Registered Nurse, Medical Surgical"; "Hosp." = "Hospital")
Only rows whose status shows the job was really acted on count as duplicates:
applied, unverified, queued, screening, interview, offer, rejected, emailed, drafted.
Rows marked skipped/failed/blocked do NOT block a later attempt.
"""
import argparse
import csv
import re
import sys
from difflib import SequenceMatcher
from urllib.parse import urlparse, parse_qs

COUNTS = {'applied', 'unverified', 'queued', 'queued-login', 'queued-needs-user',
          'screening', 'interview', 'offer', 'rejected', 'emailed', 'drafted',
          'in-progress', 'already-applied'}

LEGAL = r'\b(pvt|private|ltd|limited|inc|incorporated|llc|llp|corp|corporation|gmbh|plc|co|company|' \
        r'technologies|technology|technologies|tech|solutions|software|systems|services|group|' \
        r'india|global|labs|digital)\b'
TITLE_SYN = [
    (r'\bsr\b\.?', 'senior'), (r'\bjr\b\.?', 'junior'), (r'\bquality assurance\b', 'qa'),
    (r'\bsoftware development engineer in test\b', 'sdet'),
    (r'\bsoftware engineer in test\b', 'sdet'), (r'\btest automation engineer\b', 'automation qa engineer'),
    (r'\bqa automation engineer\b', 'automation qa engineer'), (r'\bsoftware test engineer\b', 'qa engineer'),
    (r'\bengineer i\b', 'engineer'), (r'\b(i|1)\b$', ''),
    (r'\bmed[ -]?surg\b', 'medical surgical'), (r'\bmgr\b', 'manager'), (r'\bdev\b', 'developer'),
]
CITY_SYN = {'bangalore': 'bengaluru', 'bombay': 'mumbai', 'gurgaon': 'gurugram', 'new delhi': 'delhi',
            'madras': 'chennai', 'calcutta': 'kolkata', 'poona': 'pune'}


def norm_company(s):
    s = re.sub(r'[^a-z0-9& ]+', ' ', (s or '').lower())
    s = re.sub(LEGAL, ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def norm_title(s):
    s = (s or '').lower()
    s = re.sub(r'\([^)]*\)|\[[^\]]*\]', ' ', s)          # drop (Remote), [Hybrid]
    s = re.sub(r'\b(remote|hybrid|on-?site|full[- ]time|contract|permanent|urgent|hiring)\b', ' ', s)
    s = re.sub(r'[^a-z0-9+#/ ]+', ' ', s)
    for pat, rep in TITLE_SYN:
        s = re.sub(pat, rep, s)
    return re.sub(r'\s+', ' ', s).strip()


def norm_city(s):
    s = re.sub(r'[^a-z ,]+', ' ', (s or '').lower())
    first = s.split(',')[0].strip()
    first = re.sub(r'\b(urban|rural|metropolitan|area|region|district|division)\b', '', first).strip()
    first = re.sub(r'\s+', ' ', first)
    return CITY_SYN.get(first, first)


def _tokens(s):
    return [t for t in re.split(r'[^a-z0-9+#]+', s.lower()) if t]


def _tok_match(a, b):
    """Tokens match if equal, or one is an abbreviation (prefix, 3+ chars) of the other."""
    if a == b:
        return True
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    return len(short) >= 3 and long_.startswith(short)


def _expand_initialisms(tx, ty):
    """Replace a short token (2-4 letters) in tx with the adjacent tokens of ty whose initials
    spell it, e.g. 'rn' -> 'registered nurse'."""
    out, i = [], 0
    while i < len(tx):
        t, done = tx[i], False
        if 2 <= len(t) <= 4:
            for j in range(len(ty) - len(t) + 1):
                if all(ty[j + k][0] == t[k] for k in range(len(t))) and ty[j:j + len(t)] != [t]:
                    out.extend(ty[j:j + len(t)])
                    done = True
                    break
        if not done:
            out.append(t)
        i += 1
    return out


SENIORITY = {'senior', 'junior', 'lead', 'principal', 'staff', 'associate', 'manager', 'director',
             'intern', 'head', 'chief', 'vp', 'ii', 'iii', 'iv', 'graduate', 'trainee', 'entry'}


def seniority_differs(x, y):
    return {t for t in _tokens(x) if t in SENIORITY} != {t for t in _tokens(y) if t in SENIORITY}


def token_sim(x, y):
    """Share of tokens that line up between two normalized strings (abbreviation-aware)."""
    tx, ty = _tokens(x), _tokens(y)
    if not tx or not ty:
        return 0.0
    tx, ty = _expand_initialisms(tx, ty), _expand_initialisms(ty, tx)
    used, hits = set(), 0
    for a in tx:
        for i, b in enumerate(ty):
            if i not in used and _tok_match(a, b):
                used.add(i)
                hits += 1
                break
    return hits / max(len(tx), len(ty))


def similar(x, y, threshold=0.85):
    return SequenceMatcher(None, x, y).ratio() >= threshold or token_sim(x, y) >= threshold


def title_similar(x, y, threshold=0.85):
    # a different seniority level is a different job (Senior X is not X)
    return not seniority_differs(x, y) and similar(x, y, threshold)


def job_key(company, title, location):
    return f'{norm_company(company)}|{norm_title(title)}|{norm_city(location)}'


def job_id(url):
    if not url:
        return ''
    u = urlparse(url)
    q = parse_qs(u.query)
    for k in ('jk', 'jl', 'currentJobId', 'jobId', 'job_id', 'gh_jid', 'id'):
        if k in q and q[k]:
            return q[k][0].lower()
    m = re.search(r'/jobs/view/(\d+)', u.path) or re.search(r'/jobs/(\d+)', u.path) \
        or re.search(r'-(\d{8,})(?:\?|$|/)', u.path + '/') \
        or re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', u.path)
    return m.group(1).lower() if m else ''


def canon_url(url):
    if not url:
        return ''
    u = urlparse(url)
    return f'{u.netloc.lower().removeprefix("www.")}{u.path.rstrip("/").lower()}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tracker', nargs='?')
    ap.add_argument('--company', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--location', default='')
    ap.add_argument('--url', default='')
    ap.add_argument('--jobid', default='')
    ap.add_argument('--key', action='store_true', help='only print the job_key')
    a = ap.parse_args()

    key = job_key(a.company, a.title, a.location)
    if a.key:
        print(key)
        return 0
    if not a.tracker:
        ap.error('tracker csv path required')

    my_id = (a.jobid or job_id(a.url)).lower()
    my_url = canon_url(a.url)
    my_co, my_ti, my_city = norm_company(a.company), norm_title(a.title), norm_city(a.location)

    try:
        rows = list(csv.DictReader(open(a.tracker, newline='', encoding='utf-8')))
    except FileNotFoundError:
        print('NEW (no tracker yet)')
        return 0

    for n, r in enumerate(rows, start=2):
        if (r.get('status') or '').strip().lower() not in COUNTS:
            continue
        why = ''
        if my_id and my_id == job_id(r.get('apply_url', '')):
            why = f'same job id {my_id}'
        elif my_url and my_url == canon_url(r.get('apply_url', '')):
            why = 'same apply URL'
        else:
            rk = r.get('job_key') or job_key(r.get('company'), r.get('title'), r.get('location'))
            if rk == key:
                why = 'same company + title + city'
            else:
                rc, rt, rcity = norm_company(r.get('company')), norm_title(r.get('title')), norm_city(r.get('location'))
                same_city = (not my_city or not rcity or my_city == rcity)
                same_co = bool(rc) and (rc == my_co or similar(rc, my_co, 0.85))
                if same_co and same_city and title_similar(rt, my_ti, 0.85):
                    why = 'same company + city, near-identical title'
        if why:
            print(f"DUPLICATE of row {n} ({r.get('source','?')}, {r.get('date','?')}, status={r.get('status')}): "
                  f"{r.get('company')} - {r.get('title')}  [{why}]")
            return 1
    print('NEW')
    return 0


if __name__ == '__main__':
    sys.exit(main())
