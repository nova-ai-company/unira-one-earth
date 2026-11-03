import json, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
st = json.load(open(os.path.join(HERE, 'refs_state.json')))
um = json.load(open(os.path.join(HERE, 'unmatched.json')))['unmatched']

CROSS = [
 ('Uganda school-grant leakage: 80% vs 87%', ['reinikka2004', 'reinikka2004power'],
  'v69/evidence/evidence.csv rows 15-16 give "80 -> <20 %" captured before/after the newspaper campaign and "13 % received" in 1991-95 (i.e. 87% not received). WORKING_PAPER_02 §9 and Appendix A Art. 13, and constitution Art. 33, say "87% -> under 20%", mixing the two statistics. Use one statistic consistently (e.g. "schools received 13% of grants in 1991-95; capture fell from about 80% to under 20% after publication").'),
 ('Official development assistance: 0.33% vs 0.26% of GNI', ['oecd2026oda'],
  'v68/verification item 8 marks the earlier "~0.33% of donor GNI" as CONTRADICTED (2025 preliminary: USD 174.3 bn = 0.26%; 0.34% in 2024). Book Ch. 12/13 use 0.26%. Check that no text still uses 0.33%.'),
 ('Brazil audits: "8-13%" and "Ferraz & Finan" vs evidence 7.9% / 12.7% and Avis, Ferraz & Finan (2018)', ['avis2018'],
  'WORKING_PAPER_02 Appendix A Art. 14 and constitution Art. 36 say audits cut corruption by "8-13%" citing "Ferraz & Finan"; v69 evidence row 36 gives 7.9% (12.7% with multiple audits) from Avis, Ferraz & Finan (2018, JPE), read via a J-PAL summary. Cite avis2018 and state 7.9-12.7%.'),
 ('World home building: 3.4 bn m2 is a NET stock increase', ['globalabc2026gsr'],
  'v68 item 6: +3.4 bn m2 (2024) is the net residential stock increase (GSR 2025-2026), not gross construction. WORKING_PAPER_02 §13 condition 6 still calls it "today\'s world rate" of home building, and §7 gives "3.3-4.7 bn m2 a year today" as construction capacity. Reword as net stock increase.'),
 ('UN peacekeeping peak: 106,595 vs about 108,000', ['unpk2015factsheet', 'pew2016peacekeeping'],
  'UN Fact Sheet (31 March 2015) gives 106,595 uniformed personnel; Pew (2016) gives about 108,000 "by April 2015". Constitution Art. 5 uses 106,595 as "peak"; the peak month is not established.'),
 ('Poland convergence "51% -> 81%" combines two sources and years', ['paih_poland80', 'notesfrompoland2026'],
  'WORKING_PAPER_02 §11: 51% (2004, trade.gov.pl) and 81% (2025, Notes from Poland citing Eurostat; the same source gives 44% for 1995). Cite Eurostat GDP per capita in PPS directly for both years.'),
 ('Military spending label: "SIPRI 2025" vs SIPRI Fact Sheet April 2026', ['sipri2026milex'],
  'Constitution Art. 5 cites "SIPRI 2025" for the 2.5% of world output; the source is the April 2026 fact sheet on 2025 data. Use sipri2026milex consistently.'),
 ('Renewable additions 2025: 669 GW (solar+wind) vs 692 GW (all renewables)', ['irena2026rcs'],
  'v66/ecology row E10 gives 692 GW of renewable capacity added; WORKING_PAPER_02 §6 and v68 item 5 use 669 GW (510 solar + 159 wind). Both are from IRENA RCS 2026; make sure each use names the right scope.'),
 ('Consumer food waste 19% and supply-chain loss 13%: different primary sources', ['unep2024fwi', 'fao_sdg1231'],
  'v65/thresholds rows 5-6 attribute both to UNEP Food Waste Index 2024 ("FAO estimate as cited in UNEP"), marked unverified; v68 verified 19% (UNEP 2024 via UN News) and 13.3% (FAO SDG 12.3.1a, 2023). Cite fao_sdg1231 for the loss figure.'),
 ('Decent-living energy range of Rao, Min & Mastrucci (2019): 12-24 vs 11-24 GJ', ['rao2019'],
  'v65/thresholds row 11 gives "12-24 (or 11-24)" from a secondary citation; primary article not read.'),
 ('van Baal et al. (2008): life-expectancy differences 5 and 8 vs 5 and 7 years', ['vanbaal2008', 'plosmed2008commentary'],
  'v66/evidence_health row 41: the editors\' summary says 5 and 8 years, the companion commentary 5 and 7.'),
 ('Constitution Art. 25 note: 20 vs 21 regions to block', [],
  'Book Ch. 5 and 14 note that the constitution says 20 regions can block, while v75/outputs/voting.json (double_majority_55_65_sqrt) gives 21. Not a citation problem, but the figure differs between documents.'),
 ('Employment-rate benchmark: "Iceland 85%" vs IS 85.8 (2025)', ['eurostat_lfsiempa'],
  'WORKING_PAPER_02 §3 rounds to 85%; v68 item 10 gives IS 85.8, MT 83.6, NL 83.4 (2025). Earlier text omitted Malta.'),
 ('World population 2050: 9.66 bn (UN WPP 2024 medium) vs "9.7 bn"', ['unwpp2024'],
  'v66/ecology row P01 marks 9.66 bn as not re-fetched ("caller: ~9.7"); the paper and book use 9.7 bn. Confirm from the WPP 2024 file in v66/data/raw.'),
 ('Paris vacant dwellings: 136,957 (RP2022) superseded by 139,075 (RP2023)', ['insee2025log2022', 'insee2026dc_paris'],
  'v62/audit/source_verification row 10.'),
 ('France GDP 2023: first (provisional) vintage', ['insee2024compta'],
  'EUR 2,822.5 bn is the May 2024 first estimate; later vintages not checked (v62/audit).'),
 ('Statistics Bureau of Japan bulletin date', ['statjapan2024hls'],
  'URL/project say 30 October 2024; page title says "News Bulletin September 30, 2024".'),
]

cats = collections.OrderedDict([
  ('Possible errors and mismatches (title, authors, pages, edition, dates)', re.compile(r'differ|mismatch|Title in|Author order|Pages:|Edition|now redirects|Date mismatch|attributes|DOI record title|Title differs', re.I)),
  ('Incomplete references (missing author, year, title or venue)', re.compile(r'Incomplete|not recorded|initials only|no title|No URL|without a (legal )?reference|without full|without authors', re.I)),
  ('Values or sources not verified (secondary sources, snippets, press, tertiary)', re.compile(r'snippet|unverified|secondary|only via|via a|press|Wikipedia|blog|Opinion|Coaching|not read|second-hand|myth|Only the press|read only|not opened', re.I)),
  ('Access problems (blocked pages, mirrors, dead links)', re.compile(r'HTTP|blocked|403|404|mirror|Cloudflare|JS shell|paywall|DNS', re.I)),
])

lines = []
A = lines.append
total = len(st)
nver = sum(1 for v in st.values() if v['verified'])
withprob = {k: v for k, v in st.items() if v['prob']}
A('# UNIRA references — problems to resolve before publication\n')
A('Generated 2026-11-03 together with `REFERENCES.bib`, `REFERENCES.md` and `CITATION_MAP.csv`. '
  '%d entries in total; %d verified in this task, %d taken from project files only. %d entries carry at least one problem below.\n' % (total, nver, total - nver, len(withprob)))
A('Nothing here was "fixed" by inventing details: where a field could not be confirmed it was left out of the `.bib` entry and listed here.\n')
A('## 1. Figures cited differently in different places\n')
for i, (t, keys, d) in enumerate(CROSS, 1):
    A('%d. **%s**%s. %s' % (i, t, (' (' + ', '.join('`%s`' % k for k in keys) + ')') if keys else '', d))
A('')
assigned = collections.defaultdict(list)
for k, v in sorted(withprob.items()):
    for p in v['prob']:
        for c, rx in cats.items():
            if rx.search(p):
                assigned[c].append((k, p))
                break
        else:
            assigned['Other notes'].append((k, p))
n = 2
for c in list(cats.keys()) + ['Other notes']:
    if not assigned[c]:
        continue
    A('## %d. %s\n' % (n, c)); n += 1
    for k, p in assigned[c]:
        A('- `%s` — %s' % (k, p))
    A('')
# missing core fields
miss = []
for k, v in st.items():
    f = v['f']
    m = [x for x in ('author', 'year', 'title') if not f.get(x) and not (x == 'author' and f.get('howpublished'))]
    if m:
        miss.append((k, m))
A('## %d. Entries with missing core fields (author / year / title)\n' % n); n += 1
A('These are valid BibTeX `@misc` entries but would print as "n.d." or without author in a reference list.\n')
for k, m in sorted(miss):
    A('- `%s`: no %s' % (k, ', '.join(m)))
A('')
A('## %d. Evidence rows with no citable source\n' % n); n += 1
A('Rows in the evidence tables whose citation/URL fields are empty, an assumption, a derived value or "not found". They are not in `CITATION_MAP.csv`.\n')
for where, text, claim in um:
    A('- %s — citation field: "%s" — %s' % (where, text.strip(' |') or '(empty)', claim))
A('')
A('## %d. Entries not verified in this task\n' % n); n += 1
A('Bibliographic details below come only from the project files (citation text, URL, manifest). Most are web pages, press items, mirrors or grey literature whose landing pages could not be matched automatically.\n')
nv = sorted(k for k, v in st.items() if not v['verified'])
A(', '.join('`%s`' % k for k in nv))
A('')
open(os.path.join(OUT, 'PROBLEMS.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('problems written', len(withprob), 'missing', len(miss))
