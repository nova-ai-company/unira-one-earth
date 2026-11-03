import csv, json, os, re, sys, collections, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reg import REFS, ORDER
import refs_data, refs_lit, refs_other, refs_mdextra  # noqa

ROOT = '/Users/adammoreau/UNIRA'
OUT = os.path.join(ROOT, 'references')
CSL = json.load(open(os.path.join(HERE, 'csl.json')))
EST = json.load(open(os.path.join(HERE, 'estat.json')))
WB = json.load(open(os.path.join(HERE, 'wb.json')))
UC = {u: (c, t) for u, c, t in json.load(open(os.path.join(HERE, 'urlcheck.json')))}
TODAY = '2026-11-03'

GROUPS = [('data', 'Official statistics and datasets'), ('article', 'Peer-reviewed articles'),
          ('report', 'Reports, working papers and grey literature (IPCC, IEA, WHO, ILO, UNEP, etc.)'),
          ('book', 'Books'), ('other', 'Other: web pages, press, encyclopaedias, legal texts')]
NONBIB = {'estat', 'wbcode', 'vtok', 'ver2', 'skipbib'}


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(s or ''))).strip()


def csl_year(m):
    for k in ('published-print', 'issued'):
        dp = (m.get(k) or {}).get('date-parts')
        if dp and dp[0] and dp[0][0]:
            return str(dp[0][0])
    return None


def csl_authors(m, cap=10):
    au = m.get('author') or []
    names = []
    for a in au:
        if 'family' in a:
            names.append(a['family'] + (', ' + a['given'] if a.get('given') else ''))
        elif a.get('literal') or a.get('name'):
            names.append('{' + (a.get('literal') or a.get('name')) + '}')
    names = [n for n in names if n.strip(' ,')]
    if len(names) > cap:
        names = names[:6] + ['others']
    return ' and '.join(names)


# ---------------------------------------------------------------- finalise entries
for k in ORDER:
    e = REFS[k]
    f = e['f']
    v = e['ver']
    verified = False
    how = ''
    if v == 'doi':
        m = CSL.get(f['doi'])
        if m and 'error' not in m:
            t = strip_tags(m.get('title') if isinstance(m.get('title'), str) else (m.get('title') or [''])[0])
            if 'author' not in f:
                a = csl_authors(m)
                if a:
                    f['author'] = a
            if 'title' not in f:
                f['title'] = t
            ct = m.get('container-title')
            ct = ct[0] if isinstance(ct, list) and ct else ct
            if e['type'] == 'article':
                if ct:
                    f.setdefault('journal', strip_tags(ct))
                for src, dst in (('volume', 'volume'), ('issue', 'number')):
                    if m.get(src) and not (e['key'] == 'virtanen2013' and src == 'issue'):
                        f.setdefault(dst, str(m[src]))
                pg = m.get('page') or m.get('article-number')
                if pg and '-' in str(pg) and len(set(str(pg).split('-'))) == 1:
                    pg = str(pg).split('-')[0]
                if pg:
                    f.setdefault('pages', str(pg).replace('-', '--'))
            y = csl_year(m)
            if y and 'year' not in f:
                f['year'] = y
            verified = True
            how = 'DOI metadata (doi.org)'
            e['csl_title'] = t
        else:
            e['prob'].append('DOI ' + f['doi'] + ' could not be resolved in this task.')
    elif v == 'eurostat':
        m = EST.get(f['estat'])
        if m and m.get('name'):
            f['title'] = m['name'] + ' (' + f['estat'].replace('_', r'\_') + ')'
            f['doi'] = m['doi']
            f['note'] = f.get('note', '') + '; last data update ' + (m.get('update') or '')[:10] + ' per Eurostat metadata'
            verified, how = True, 'Eurostat SDMX dataflow metadata'
    elif v == 'wb':
        code = f.get('wbcode')
        if code and code in WB and 'name' in WB[code]:
            f['title'] = WB[code]['name'] + ' (' + code + ')'
            org = WB[code].get('org', '').split(',')[0].split(';')[0].strip()
            if org:
                f['note'] = f.get('note', '') + '; underlying source: ' + org
            verified, how = True, 'World Bank API indicator metadata'
        elif not code:
            verified, how = True, 'World Bank API source metadata'
    elif v in ('who', 'ilo'):
        verified, how = True, {'who': 'WHO xMart REF_INDICATOR metadata', 'ilo': 'ILOSTAT SDMX dataflow metadata'}[v]
    elif v == 'url':
        u = f.get('url', '')
        tok = f.get('vtok')
        c, t = UC.get(u, (None, None))
        if tok is not None and c and c.split()[0] in ('200', '206') and (tok == '' and t is not None or tok and t and tok.lower() in t.lower()):
            verified, how = True, 'landing page title checked'
            if tok == '':
                verified = False  # reachable but nothing to compare
    elif v is True:
        verified, how = True, 'publisher/catalogue record'
    if f.get('ver2'):
        verified, how = True, 'publisher/catalogue record'
    e['verified'] = verified
    e['how'] = how
    # reachability notes for unverified URLs
    if not verified and f.get('url') in UC:
        c, t = UC[f['url']]
        if c.split()[0] in ('403', '401', '404', '503', '000', 'ERR'):
            e['prob'].append('URL not reachable by the fetcher in this task (HTTP ' + c.split()[0] + ').')


# ---------------------------------------------------------------- scanning helpers
def rx(p):
    return re.compile(p)


for k in ORDER:
    REFS[k]['_pats'] = [rx(p) for p in REFS[k]['pats']]
    REFS[k]['_md'] = [rx(p) for p in REFS[k]['md']]

MAP = []  # (key, where, claim, evidence_class)
UNMATCHED = []

EVID_CSV = ['v62/audit/hours_productivity_evidence.csv', 'v62/audit/source_verification.csv', 'v65/thresholds/thresholds.csv',
            'v66/construction/evidence.csv', 'v66/ecology/evidence.csv', 'v66/evidence_health/evidence.csv',
            'v68/verification/verification.csv', 'v69/evidence/evidence.csv', 'v70/evidence/evidence.csv',
            'v71/evidence/evidence.csv', 'v72/evidence/evidence.csv', 'v76/peace_force/evidence.csv',
            'v76/migration/evidence.csv', 'source_tree/v53/evidence_registry.csv', 'source_tree/v60/evidence.csv']
MANIFESTS = sorted(os.path.relpath(os.path.join(d, 'raw_manifest.csv'), ROOT)
                   for d, _, fs in os.walk(ROOT) if 'raw_manifest.csv' in fs and 'repro_work' not in d and '/v' in d and os.path.relpath(d, ROOT).split('/')[0] in
                   {'v%d' % i for i in range(62, 78)})


def short(s, n=150):
    s = re.sub(r'\s+', ' ', s or '').strip()
    return s if len(s) <= n else s[:n - 1] + '…'


def match_text(text):
    hits = []
    for k in ORDER:
        for p in REFS[k]['_pats']:
            if p.search(text):
                hits.append(k)
                break
    return hits


for path in EVID_CSV:
    rows = list(csv.DictReader(open(os.path.join(ROOT, path), encoding='utf-8')))
    for i, r in enumerate(rows, 2):
        cit = r.get('citation') or ''
        url = r.get('url') or r.get('url_or_doi') or r.get('source_url') or ''
        text = cit + ' | ' + url
        claim = r.get('finding') or r.get('quantity') or r.get('indicator') or r.get('item') or r.get('estimate_as_stated') or ''
        if path.endswith('verification.csv') and r.get('item'):
            claim = 'item ' + r['item'] + ': ' + (r.get('notes') or r.get('source_value') or '')
        if path.endswith('hours_productivity_evidence.csv'):
            claim = r.get('estimate_as_stated', '')
        val = r.get('value') or r.get('value_as_stated') or r.get('claimed_value') or r.get('recorded_value') or ''
        unit = r.get('unit', '')
        if val and val not in claim:
            claim = claim + ' = ' + val + (' ' + unit if unit else '')
        ec = r.get('evidence_class') or ''
        vf = r.get('verified_in_fetched_text') or r.get('status') or ''
        evc = ec or (('verified_in_fetched_text: ' + vf) if 'verified_in_fetched_text' in r else ('status: ' + vf if vf else ''))
        rid = r.get('id') or ''
        where = '%s (row %d%s)' % (path, i, ', id ' + rid if rid else '')
        hits = match_text(text)
        if not hits:
            UNMATCHED.append((where, short(text, 120), short(claim, 100)))
        for k in hits:
            MAP.append((k, where, short(claim), short(evc, 60)))

for path in MANIFESTS:
    rows = list(csv.DictReader(open(os.path.join(ROOT, path), encoding='utf-8')))
    for i, r in enumerate(rows, 2):
        ds = r.get('dataset') or r.get('source') or ''
        text = ds + ' | ' + r.get('url', '') + ' | ' + r.get('file', '')
        hits = match_text(text)
        where = '%s (row %d, %s)' % (path, i, r.get('file', ''))
        if not hits:
            UNMATCHED.append((where, short(text, 120), ''))
        for k in hits:
            MAP.append((k, where, short('raw data file ' + r.get('file', '') + ' retrieved ' + r.get('retrieved_at_utc', '')[:10] + ' (sha256 ' + r.get('sha256', '')[:12] + '…)'), 'VERIFIED_OFFICIAL (frozen raw file)'))

# take-up rates: aggregate by source_dataset x evidence_class
tk = collections.Counter()
for r in csv.DictReader(open(os.path.join(ROOT, 'v63/flows/outputs/takeup_rates.csv'))):
    tk[(r['source_dataset'], r['evidence_class'])] += 1
for (ds, ec), n in sorted(tk.items()):
    codes = set(re.findall(r'(lfsi_long_[a-z0-9]+|lfsi_sla_a|ilc_lvhl30)', ds.replace('|e01', '|lfsi_long_e01')))
    for c in sorted(codes):
        k = 'eurostat_' + c.replace('_', '')
        if k in REFS:
            MAP.append((k, 'v63/flows/outputs/takeup_rates.csv', 'take-up rates by pool (%d rows, source %s)' % (n, ds), ec))

# ---------------------------------------------------------------- markdown scanning
MD = [l.strip() for l in open(os.path.join(HERE, 'mdfiles.txt')) if l.strip()]
MD += ['v66/ecology/ecology.md', 'v66/construction/construction.md', 'v72/TRANSITION_RULES.md', 'v63/DESIGN_CLARIFICATIONS_2026-11-03.md']
MD = [m for m in MD if os.path.exists(os.path.join(ROOT, m))]


def section_label(path, heading_stack, line, state):
    return state.get('sec', '')


def md_sections(path):
    lines = open(os.path.join(ROOT, path), encoding='utf-8').read().split('\n')
    sec = ''
    out = []
    in_notes = False
    for ln in lines:
        h = re.match(r'^(#{1,4})\s+(.*)', ln)
        if path.endswith('WORKING_PAPER_02.md'):
            if h:
                t = h.group(2)
                mm = re.match(r'(\d+)\.\s', t)
                if mm:
                    sec = '§' + mm.group(1)
                elif t.startswith('Appendix — UNIRA Constitution'):
                    sec = 'Appendix A (safeguard articles)'
                elif t.startswith('Appendix — UNIRA transition'):
                    sec = 'Appendix B (transition rules)'
                elif t.startswith('Article'):
                    sec = 'Appendix A, ' + t.split('—')[0].strip()
                elif t.startswith('Sources and reproducibility'):
                    sec = 'Sources and reproducibility table'
                elif t.startswith('Distribution inside'):
                    sec = 'Appendix B (distribution, V7.4)'
                elif h.group(1) == '#':
                    sec = 'Abstract'
            tm = re.match(r'\*\*(T\d)\.', ln)
            if tm and sec.startswith('Appendix B'):
                sec = 'Appendix B, ' + tm.group(1)
        elif '/book/CHAPTER_' in path:
            ch = int(re.search(r'CHAPTER_(\d+)', path).group(1))
            if h and 'Notes on sources' in h.group(2):
                in_notes = True
            sec = 'Ch. %d%s' % (ch, ', Notes on sources' if in_notes else ', text')
        elif path.endswith('UNIRA_CONSTITUTION_DRAFT.md'):
            am = re.match(r'\*\*Article (\w+)', ln)
            if am:
                sec = 'Art. ' + am.group(1)
            elif re.match(r'\*\*(T-\d)', ln):
                sec = re.match(r'\*\*(T-\d)', ln).group(1)
            elif h:
                sec = h.group(2).split('—')[0].strip()
        else:
            if h:
                t = re.sub(r'[*`]', '', h.group(2)).strip()
                mm = re.match(r'(Part [A-Z]|§?\d+[a-z]?\.?|[A-Z]\.)\s', t)
                sec = (t[:60])
        out.append((sec, ln))
    return out


seen = set()
for path in MD:
    for sec, ln in md_sections(path):
        plain = ln.strip()
        if not plain:
            continue
        for k in ORDER:
            for p in REFS[k]['_md']:
                mm = p.search(plain)
                if mm:
                    key = (k, path, sec)
                    if key not in seen:
                        seen.add(key)
                        a = max(0, mm.start() - 70)
                        snippet = re.sub(r'[*`|]+', ' ', plain[a:mm.end() + 80]).strip()
                        MAP.append((k, path + (' ' + sec if sec else ''), short(snippet, 160), ''))
                    break

# ---------------------------------------------------------------- outputs
os.makedirs(OUT, exist_ok=True)
used = collections.Counter(k for k, *_ in MAP)


def bibval(v):
    v = str(v)
    v = v.replace('&', r'\&').replace(r'\\&', r'\&').replace('%', r'\%').replace(r'\\%', r'\%').replace('#', r'\#').replace('_', r'\_').replace(r'\\_', r'\_')
    return v


def bib_entry(e):
    f = e['f']
    t = e['type']
    fields = []
    order = ['author', 'editor', 'title', 'booktitle', 'journal', 'volume', 'number', 'pages', 'edition', 'type', 'institution', 'organization',
             'publisher', 'address', 'howpublished', 'year', 'doi', 'url', 'urldate', 'note']
    note = f.get('note', '').strip('; ')
    ann = ('Verified in this task: ' + e['how']) if e['verified'] else 'From project files (not independently verified in this task)'
    for name in order:
        if name == 'note':
            val = (note + '. ' if note else '') + ann
        else:
            val = f.get(name)
        if not val:
            continue
        if name in ('url', 'doi'):
            fields.append('  %s = {%s}' % (name, val))
        elif name in ('author', 'editor'):
            fields.append('  %s = {%s}' % (name, val.replace('&', r'\&').replace(r'\\&', r'\&')))
        else:
            fields.append('  %s = {%s}' % (name, bibval(val)))
    if t == 'techreport' and 'institution' not in f:
        fields.insert(2, '  institution = {%s}' % bibval(f.get('publisher') or strip_braces(f.get('author', '')) or 'n.a.'))
    return '@%s{%s,\n%s\n}\n' % (t, e['key'], ',\n'.join(fields))


def strip_braces(s):
    return s.replace('{', '').replace('}', '')


def apa_authors(a):
    if not a:
        return ''
    parts = [p.strip() for p in a.split(' and ')]
    out = []
    etal = False
    for p in parts:
        if p == 'others':
            etal = True
            continue
        if p.startswith('{'):
            out.append(strip_braces(p))
            continue
        if ',' in p:
            fam, giv = [x.strip() for x in p.split(',', 1)]
            if giv and giv != '?':
                ini = ' '.join(w[0] + '.' for w in re.split(r'[\s]+', giv.replace('.', ' ').strip()) if w)
                ini = re.sub(r'(\w)\.-', r'\1.-', ini)
                out.append('%s, %s' % (fam, ini))
            else:
                out.append(fam)
        else:
            out.append(p)
    if etal:
        s = (', '.join(out) + ', et al.') if len(out) > 1 or ',' in out[0] else out[0] + ' et al.'
    elif len(out) == 1:
        s = out[0]
    elif len(out) == 2:
        s = out[0] + ', & ' + out[1] if ',' in out[0] else out[0] + ' & ' + out[1]
    else:
        s = ', '.join(out[:-1]) + ', & ' + out[-1]
    return s


def md_entry(e):
    f = e['f']
    au = apa_authors(f.get('author') or f.get('editor')) or strip_braces(f.get('howpublished', '')) or 'Anon.'
    yr = f.get('year') or 'n.d.'
    title = strip_braces(f.get('title', '[untitled]')).replace('\\&', '&').replace('\\_', '_').replace('--', '–')
    t = e['type']
    s = '%s (%s). ' % (au, yr)
    if t == 'article':
        s += '%s. *%s*' % (title.rstrip('.'), f.get('journal', ''))
        if f.get('volume'):
            s += ', *%s*' % f['volume']
            if f.get('number'):
                s += '(%s)' % f['number']
        if f.get('pages'):
            s += ', %s' % f['pages'].replace('--', '–')
        s += '.'
    elif t == 'incollection':
        s += '%s. In *%s*' % (title, strip_braces(f.get('booktitle', '')))
        if f.get('pages'):
            s += ' (pp. %s)' % f['pages'].replace('--', '–')
        s += '. %s.' % f.get('publisher', '')
    elif t == 'book':
        s += '*%s*. %s%s.' % (title, (f['address'] + ': ') if f.get('address') else '', f.get('publisher', ''))
    elif t == 'techreport':
        s += '*%s*' % title
        extra = ' '.join(x for x in [f.get('type', ''), f.get('number', '')] if x)
        if extra:
            s += ' (%s)' % extra
        inst = strip_braces(f.get('institution', ''))
        s += '. ' + (inst + '.' if inst and inst not in au else '')
    else:
        s += '*%s*' % title
        if f.get('howpublished'):
            s += ' [%s]' % strip_braces(f['howpublished']).replace('\\_', '_')
        if e['group'] == 'data':
            s += ' [Data set]'
        s += '.'
    if f.get('doi'):
        s += ' https://doi.org/%s' % f['doi']
    if f.get('url') and (not f.get('doi') or e['group'] in ('data', 'other') or t in ('techreport', 'misc')):
        s += ' %s' % f['url']
    if f.get('urldate') and (e['group'] in ('data', 'other') or t == 'misc' or not f.get('doi')):
        s += ' (accessed %s)' % f['urldate']
    s += ' **[%s]** `%s`' % ('verified' if e['verified'] else 'from project files', e['key'])
    return s.replace('  ', ' ')


def sortkey(k):
    f = REFS[k]['f']
    return (strip_braces(f.get('author') or f.get('title', '')).lower(), f.get('year', ''))


keys = [k for k in ORDER]
with open(os.path.join(OUT, 'REFERENCES.bib'), 'w', encoding='utf-8') as fh:
    fh.write('% UNIRA research project -- consolidated bibliography (V6.2-V7.7 sources)\n')
    fh.write('%% Generated %s. One entry per distinct source. Field "note" states whether the entry was verified in this task.\n' % TODAY)
    fh.write('% Groups: see REFERENCES.md. Usage map: CITATION_MAP.csv. Open issues: PROBLEMS.md.\n\n')
    for g, gname in GROUPS:
        fh.write('%% ===================== %s =====================\n\n' % gname)
        for k in sorted([k for k in keys if REFS[k]['group'] == g], key=sortkey):
            fh.write(bib_entry(REFS[k]) + '\n')

cnt = collections.Counter(REFS[k]['group'] for k in keys)
ver = collections.Counter(REFS[k]['group'] for k in keys if REFS[k]['verified'])
with open(os.path.join(OUT, 'REFERENCES.md'), 'w', encoding='utf-8') as fh:
    fh.write('# UNIRA — References\n\n')
    fh.write('Consolidated bibliography for the UNIRA research (V6.2–V7.7): working paper, book, constitution draft and evidence files. '
             'Author–year format (APA-like). Each entry ends with **[verified]** if its bibliographic details were confirmed in this task '
             '(DOI metadata via doi.org, Eurostat/World Bank/WHO/ILO metadata APIs, publisher or catalogue record, or the landing-page title), '
             'otherwise **[from project files]**, followed by its BibTeX key.\n\n')
    fh.write('Generated %s. BibTeX: `REFERENCES.bib`. Where each source is used: `CITATION_MAP.csv`. Known issues: `PROBLEMS.md`. Check: `python3 references/check_bib.py`.\n\n' % TODAY)
    fh.write('| Group | Entries | Verified |\n| --- | --- | --- |\n')
    for g, gname in GROUPS:
        fh.write('| %s | %d | %d |\n' % (gname, cnt[g], ver[g]))
    fh.write('| **Total** | **%d** | **%d** |\n\n' % (sum(cnt.values()), sum(ver.values())))
    fh.write('Access dates: datasets use the retrieval timestamps in the `raw_manifest.csv` files; web sources use the project fetch date (all evidence reviews are dated 2026-11-03).\n\n')
    for g, gname in GROUPS:
        fh.write('## %s\n\n' % gname)
        for k in sorted([k for k in keys if REFS[k]['group'] == g], key=sortkey):
            fh.write('- ' + md_entry(REFS[k]) + '\n')
        fh.write('\n')

MAP.sort(key=lambda r: (r[0], r[1]))
with open(os.path.join(OUT, 'CITATION_MAP.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['ref_key', 'where_used', 'claim_or_figure', 'evidence_class'])
    for r in MAP:
        w.writerow(r)

json.dump({'unmatched': UNMATCHED}, open(os.path.join(HERE, 'unmatched.json'), 'w'), indent=1)
json.dump({k: {'group': REFS[k]['group'], 'verified': REFS[k]['verified'], 'prob': REFS[k]['prob'], 'f': REFS[k]['f'], 'uses': used[k]} for k in keys},
          open(os.path.join(HERE, 'refs_state.json'), 'w'), indent=1, ensure_ascii=False)
print('entries', len(keys), dict(cnt), 'verified', dict(ver), 'map rows', len(MAP), 'unmatched', len(UNMATCHED))
unused = [k for k in keys if used[k] == 0]
print('UNUSED:', unused)
for u in UNMATCHED:
    print('UNMATCHED', u)
