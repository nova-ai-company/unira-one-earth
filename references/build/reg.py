import re
REFS = {}
ORDER = []


def R(key, group=None, bibtype=None, ver=None, pats=(), md=(), prob=None, extend=False, **f):
    """Register a reference.
    ver: 'doi' (verify/fill from doi.org CSL), 'eurostat', 'wb', 'who', 'ilo' (live API metadata),
         'url' (verified if landing page title contains vtok), 'false' (project files only), True (manually verified)
    pats: regexes matched against CSV citation+url text; md: regexes matched against markdown lines.
    prob: list of problem strings for PROBLEMS.md
    """
    if extend:
        e = REFS[key]
        e['pats'] += list(pats)
        e['md'] += list(md)
        if prob:
            e['prob'] += list(prob) if isinstance(prob, (list, tuple)) else [prob]
        for k, v in f.items():
            e['f'][k] = v
        return e
    assert key not in REFS, key
    assert re.fullmatch(r'[a-z0-9_]+', key), key
    e = dict(key=key, group=group, type=bibtype, ver=ver, pats=list(pats), md=list(md),
             prob=(list(prob) if isinstance(prob, (list, tuple)) else ([prob] if prob else [])), f=dict(f))
    REFS[key] = e
    ORDER.append(key)
    return e
