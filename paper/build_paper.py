"""Insert per-section source lines and the reference list into Paper V1 from the project bibliography, then build a
standalone HTML page (no JavaScript, no external files; opens in any browser) and, on macOS, a .docx.
The paper's sections reuse the sections of Working Paper 02 whose citations are mapped in references/CITATION_MAP.csv
(MAP below), so every reference in the paper is one whose verification status is recorded in references/.
python3 build_paper.py"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parent
sys.path.insert(0, str(U / "references"))
sys.path.insert(0, str(U / "v67" / "dashboard"))
from check_bib import parse_bib  # noqa: E402
from cite import labels, md_lines, ref_list, strip_generated, uses  # noqa: E402
from build_dashboard import CSS, md_to_html  # noqa: E402

PAPER = HERE / "UNIRA_PAPER_V1.md"
MAP = {"2": ["2"], "3": ["3"], "4": ["5"], "5": ["6"], "6": ["7"], "7": ["4", "8", "9"], "9": ["2"], "10": ["12"], "11": ["13"]}


def main():
    entries = parse_bib((U / "references" / "REFERENCES.bib").read_text(encoding="utf-8"))
    lab, lines = labels(entries), md_lines()
    wp = {k[1:]: v for k, v in uses("v67/WORKING_PAPER_02.md").items() if re.fullmatch(r"§\d+", k)}
    s = strip_generated(PAPER.read_text(encoding="utf-8")).rstrip() + "\n"
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^## (\d+)\.", s, flags=re.M)]
    nxt = [m.start() for m in re.finditer(r"^## ", s, flags=re.M)]
    inserts, allkeys = [], set()
    for pos, num in heads:
        keys = set().union(*(wp.get(w, set()) for w in MAP.get(num, [])))
        keys = {k for k in keys if k in lab and k in lines}
        if keys:
            allkeys |= keys
            end = next((p for p in nxt if p > pos), len(s))
            cites = "; ".join(sorted({lab[k] for k in keys}, key=str.lower))
            inserts.append((end, f"<!-- refs:begin sources §{num} -->\n\n*Sources for this section:* {cites}.\n\n<!-- refs:end -->\n\n"))
    for end, block in sorted(inserts, reverse=True):
        s = s[:end].rstrip() + "\n\n" + block + s[end:]
    n_unverified = sum(1 for k in allkeys if not lines[k][1])
    block = ["<!-- refs:begin reference list -->", "## References", "",
             f"Author–year list of the {len(allkeys)} sources cited in sections 2–11 (generated from `references/REFERENCES.bib`). "
             f"{len(allkeys) - n_unverified} were verified against DOI metadata, a publisher or catalogue record or the landing page; "
             f"{n_unverified} are marked *not independently verified*. A second verification pass on 4 November 2026 is recorded in "
             "`references/VERIFICATION_2026-11-04.csv`. Sources of the preliminary section 8 are listed row by row, with their "
             "verification status, in `v87/livingstandard/basket.json` and the `evidence.csv` files of `v88/`, `v90/` and `v91/`.", ""]
    block += ref_list(allkeys, lab, lines) + ["", "<!-- refs:end -->"]
    s = s.rstrip() + "\n\n" + "\n".join(block) + "\n"
    PAPER.write_text(s, encoding="utf-8")
    body = md_to_html(s)
    page = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>UNIRA Paper V1</title><style>{CSS} .wrap{{max-width:820px}} p,li{{line-height:1.65}}</style></head>"
            f"<body><div class='wrap'>{body}</div></body></html>\n")
    (HERE / "UNIRA_PAPER_V1.html").write_text(page, encoding="utf-8")
    if shutil.which("textutil"):
        subprocess.run(["textutil", "-convert", "docx", "-output", str(HERE / "UNIRA_Paper_V1.docx"), str(HERE / "UNIRA_PAPER_V1.html")],
                       capture_output=True)
    print(f"paper: {len(allkeys)} references ({n_unverified} not independently verified), {len(inserts)} source lines")


if __name__ == "__main__":
    main()
