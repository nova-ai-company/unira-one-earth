"""Insert author-year source lines and a reference list into the working paper and the book.
Sources come from CITATION_MAP.csv (which section uses which reference) and REFERENCES.bib/.md.
Idempotent: generated blocks sit between <!-- refs:begin ... --> / <!-- refs:end --> markers and are
replaced on every run.
python3 cite.py"""
import csv
import re
from collections import defaultdict
from pathlib import Path

from check_bib import parse_bib

HERE = Path(__file__).resolve().parent
U = HERE.parent
PAPER = U / "v67" / "WORKING_PAPER_02.md"
BOOK_BIB = U / "v73" / "book" / "BIBLIOGRAPHY.md"
WEAK = ("wiki_", "connexion_", "swissinfo_", "notesfrompoland")  # encyclopaedia/press: to be replaced


def surname(a):
    a = a.strip()
    if a.startswith("{") and a.endswith("}"):
        return a[1:-1]
    return a.split(",")[0].strip() if "," in a else a.split()[-1]


def suffix(i):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return letters[i] if i < 26 else letters[i // 26 - 1] + letters[i % 26]


def labels(entries):
    raw = {}
    for _, key, f, _ in entries:
        auth = [x for x in re.split(r"\s+and\s+", f.get("author", "").strip()) if x]
        if not auth:
            who = f.get("institution") or f.get("publisher") or f.get("journal") or f.get("howpublished") or "Anon."
        elif len(auth) == 1:
            who = surname(auth[0])
        elif len(auth) == 2:
            who = f"{surname(auth[0])} & {surname(auth[1])}"
        else:
            who = f"{surname(auth[0])} et al."
        who = who.replace("{", "").replace("}", "")
        code = re.search(r"\(([A-Za-z0-9\\_.\-]*_[A-Za-z0-9\\_.\-]*)\)\s*$", f.get("title", ""))
        if code and f.get("author", "").startswith("{"):  # an institution's dataset: name it by its code
            who = f"{who} {code.group(1).replace(chr(92), '')},"
        raw[key] = (who, f.get("year", "n.d."))
    # disambiguate identical author-year pairs with a, b, c (in key order)
    groups = defaultdict(list)
    for k, v in raw.items():
        groups[v].append(k)
    out = {}
    for (who, yr), keys in groups.items():
        for i, k in enumerate(sorted(keys)):
            out[k] = f"{who} {yr}{suffix(i) if len(keys) > 1 else ''}"
    return out


def md_lines():
    """key -> formatted reference line from REFERENCES.md, without the verification tag and key."""
    out = {}
    for line in (HERE / "REFERENCES.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"- (.*) \*\*\[(verified[^\]]*|from project files|not located[^\]]*|unreachable[^\]]*)\]\*\* `([^`]+)`\s*$", line)
        if m:
            out[m.group(3)] = (m.group(1).strip(), m.group(2).startswith("verified"), m.group(2))
    return out


def uses(prefix):
    m = defaultdict(set)
    for r in csv.DictReader((HERE / "CITATION_MAP.csv").open(encoding="utf-8")):
        if r["where_used"].startswith(prefix):
            m[r["where_used"][len(prefix):].strip()].add(r["ref_key"])
    return m


def ref_list(keys, lab, lines):
    out = []
    for k in sorted(keys, key=lambda k: lines[k][0].lower()):
        text, ok, tag = lines[k]
        flags = []
        if not ok:
            flags.append("could not be located on 4 November 2026" if tag.startswith(("not located", "unreachable")) else "not independently verified")
        if k.startswith(WEAK):
            flags.append("secondary source, to be replaced by a primary one")
        out.append(f"- {text}" + (f" *[{'; '.join(flags)}]*" if flags else ""))
    return out


def strip_generated(s):
    return re.sub(r"\n*<!-- refs:begin[^>]*-->.*?<!-- refs:end -->\n*", "\n\n", s, flags=re.S)


def cite_paper(lab, lines):
    s = strip_generated(PAPER.read_text(encoding="utf-8")).rstrip() + "\n"
    m = uses("v67/WORKING_PAPER_02.md")
    sections = {k[1:]: v for k, v in m.items() if re.fullmatch(r"§\d+", k)}
    # a sources line at the end of each numbered section (just before the next '## ' heading)
    heads = [(mm.start(), mm.group(1)) for mm in re.finditer(r"^## (\d+)\.", s, flags=re.M)]
    nxt = [mm.start() for mm in re.finditer(r"^## ", s, flags=re.M)]
    inserts = []
    for pos, num in heads:
        if num in sections:
            end = next((p for p in nxt if p > pos), len(s))
            cites = "; ".join(sorted({lab[k] for k in sections[num]}, key=str.lower))
            inserts.append((end, f"<!-- refs:begin sources §{num} -->\n\n*Sources for this section:* {cites}.\n\n<!-- refs:end -->\n\n"))
    for end, block in sorted(inserts, reverse=True):
        s = s[:end].rstrip() + "\n\n" + block + s[end:]
    allkeys = set().union(*m.values())
    block = ["<!-- refs:begin reference list -->", "## References", "",
             "Author–year list of every source used in this paper (generated from `references/REFERENCES.bib`; "
             "the full bibliography of the project, with DOIs and verification notes, is in `references/`).", ""]
    block += ref_list(allkeys, lab, lines) + ["", "<!-- refs:end -->"]
    s = s.rstrip() + "\n\n" + "\n".join(block) + "\n"
    PAPER.write_text(s, encoding="utf-8")
    return len(allkeys), len(inserts)


def book_bibliography(lab, lines):
    m = uses("v73/book/")
    allkeys = set().union(*m.values())
    text = ["# Bibliography", "",
            "*Every source cited in the chapters and their notes, in author–year order. Generated from the project bibliography "
            "(`references/REFERENCES.bib`), where each entry records how it was checked.*", ""]
    text += ref_list(allkeys, lab, lines)
    BOOK_BIB.write_text("\n".join(text) + "\n", encoding="utf-8")
    return len(allkeys)


def main():
    entries = parse_bib((HERE / "REFERENCES.bib").read_text(encoding="utf-8"))
    lab, lines = labels(entries), md_lines()
    missing = [k for k in lab if k not in lines]
    if missing:
        raise SystemExit(f"keys without a formatted line in REFERENCES.md: {missing[:5]}")
    n, secs = cite_paper(lab, lines)
    nb = book_bibliography(lab, lines)
    print(f"paper: {n} references, source lines in {secs} sections; book bibliography: {nb} references")


if __name__ == "__main__":
    main()
