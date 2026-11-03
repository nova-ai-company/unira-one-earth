#!/usr/bin/env python3
"""Consistency check for the UNIRA bibliography (standard library only).

Checks:
  1. REFERENCES.bib parses; every entry has a key; keys are unique.
  2. Required fields per entry type are present and non-empty.
  3. Every ref_key in CITATION_MAP.csv exists in REFERENCES.bib.
  4. Every .bib key appears in REFERENCES.md (and vice versa), and is used at least once in CITATION_MAP.csv (warning only).
  5. DOIs look like DOIs; urldate looks like YYYY-MM-DD.

Usage: python3 references/check_bib.py   (exit code 0 = pass)
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(HERE, 'REFERENCES.bib')
MAP = os.path.join(HERE, 'CITATION_MAP.csv')
MD = os.path.join(HERE, 'REFERENCES.md')

# Required fields: each item is a field name or a tuple of alternatives (any one suffices).
REQUIRED = {
    'article': ['author', 'title', 'journal', 'year'],
    'book': [('author', 'editor'), 'title', 'publisher', 'year'],
    'incollection': ['author', 'title', 'booktitle', 'publisher', 'year'],
    'techreport': ['author', 'title', 'institution'],
    'misc': ['title', ('author', 'howpublished'), ('year', 'urldate', 'note')],
}


def parse_bib(text):
    """Minimal BibTeX parser: returns list of (type, key, {field: value}, line)."""
    entries = []
    i, n = 0, len(text)
    while True:
        m = re.compile(r'@(\w+)\s*\{', re.S).search(text, i)
        if not m:
            break
        etype = m.group(1).lower()
        line = text.count('\n', 0, m.start()) + 1
        j = m.end()
        depth = 1
        k = j
        while k < n and depth:
            if text[k] == '{' and text[k - 1] != '\\':
                depth += 1
            elif text[k] == '}' and text[k - 1] != '\\':
                depth -= 1
            k += 1
        if depth:
            raise ValueError('unbalanced braces in entry starting at line %d' % line)
        body = text[j:k - 1]
        key, _, rest = body.partition(',')
        fields = {}
        p = 0
        while p < len(rest):
            fm = re.compile(r'\s*([A-Za-z_]+)\s*=\s*', re.S).match(rest, p)
            if not fm:
                if rest[p:].strip(' ,\n\t'):
                    raise ValueError('cannot parse fields of %s (line %d) near: %r' % (key.strip(), line, rest[p:p + 40]))
                break
            name = fm.group(1).lower()
            q = fm.end()
            if rest[q] == '{':
                d, r = 1, q + 1
                while r < len(rest) and d:
                    if rest[r] == '{' and rest[r - 1] != '\\':
                        d += 1
                    elif rest[r] == '}' and rest[r - 1] != '\\':
                        d -= 1
                    r += 1
                val = rest[q + 1:r - 1]
            elif rest[q] == '"':
                r = rest.index('"', q + 1) + 1
                val = rest[q + 1:r - 1]
            else:
                vm = re.compile(r'[^,\s]+').match(rest, q)
                r = vm.end()
                val = vm.group(0)
            if name in fields:
                raise ValueError('duplicate field %s in %s (line %d)' % (name, key.strip(), line))
            fields[name] = val.strip()
            p = r
            cm = re.compile(r'\s*,?').match(rest, p)
            p = cm.end()
        entries.append((etype, key.strip(), fields, line))
        i = k
    return entries


def main():
    errors, warnings = [], []
    entries = parse_bib(open(BIB, encoding='utf-8').read())
    keys = {}
    for etype, key, fields, line in entries:
        if not key:
            errors.append('line %d: entry without key' % line)
            continue
        if key in keys:
            errors.append('duplicate key %s (lines %d and %d)' % (key, keys[key], line))
        keys[key] = line
        if not re.fullmatch(r'[a-z0-9_]+', key):
            warnings.append('key %s is not lower-case alphanumeric/underscore' % key)
        req = REQUIRED.get(etype)
        if req is None:
            errors.append('%s: unsupported entry type @%s' % (key, etype))
            continue
        for r in req:
            alts = r if isinstance(r, tuple) else (r,)
            if not any(fields.get(a, '').strip('{} ') for a in alts):
                errors.append('%s (@%s, line %d): missing required field %s' % (key, etype, line, ' or '.join(alts)))
        if 'doi' in fields and not re.fullmatch(r'10\.\d{4,9}/\S+', fields['doi']):
            errors.append('%s: malformed doi %r' % (key, fields['doi']))
        if 'urldate' in fields and not re.fullmatch(r'\d{4}-\d{2}-\d{2}', fields['urldate']):
            errors.append('%s: urldate not YYYY-MM-DD: %r' % (key, fields['urldate']))
        if 'year' in fields and not re.fullmatch(r'\d{4}', fields['year']):
            errors.append('%s: year not 4 digits: %r' % (key, fields['year']))

    used = {}
    with open(MAP, encoding='utf-8', newline='') as fh:
        rd = csv.DictReader(fh)
        expected = ['ref_key', 'where_used', 'claim_or_figure', 'evidence_class']
        if rd.fieldnames != expected:
            errors.append('CITATION_MAP.csv header %r != %r' % (rd.fieldnames, expected))
        for n, row in enumerate(rd, 2):
            k = row['ref_key']
            used[k] = used.get(k, 0) + 1
            if k not in keys:
                errors.append('CITATION_MAP.csv row %d: key %s not in REFERENCES.bib' % (n, k))
            if not row['where_used'].strip():
                errors.append('CITATION_MAP.csv row %d: empty where_used' % n)
    for k in keys:
        if k not in used:
            warnings.append('%s is never used in CITATION_MAP.csv' % k)

    if os.path.exists(MD):
        mdkeys = set(re.findall(r'\*\*\[(?:verified|from project files)\]\*\* `([a-z0-9_]+)`', open(MD, encoding='utf-8').read()))
        for k in keys:
            if k not in mdkeys:
                errors.append('%s missing from REFERENCES.md' % k)
        for k in mdkeys - set(keys):
            errors.append('REFERENCES.md lists %s, which is not in REFERENCES.bib' % k)

    types = {}
    for etype, *_ in entries:
        types[etype] = types.get(etype, 0) + 1
    print('REFERENCES.bib: %d entries %s' % (len(entries), dict(sorted(types.items()))))
    print('CITATION_MAP.csv: %d rows, %d distinct keys' % (sum(used.values()), len(used)))
    for w in warnings:
        print('WARNING:', w)
    for e in errors:
        print('ERROR:', e)
    print('RESULT:', 'PASS' if not errors else 'FAIL (%d errors)' % len(errors))
    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
