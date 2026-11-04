"""Write the results of the 4 November 2026 verification pass (VERIFICATION_2026-11-04.csv) into REFERENCES.md and
PROBLEMS.md. Idempotent: tags and correction notes are replaced, not duplicated. python3 apply_verification.py"""
import csv
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATE = "2026-11-04"
TAG = {"verified": f"verified {DATE}", "corrected": f"verified {DATE}; details corrected, see VERIFICATION_{DATE}.csv",
       "not_found": f"not located {DATE}", "unreachable": f"unreachable {DATE}"}
MARK = f"## 0b. Verification pass of {DATE}"


def main():
    rows = {r["key"]: r for r in csv.DictReader((HERE / f"VERIFICATION_{DATE}.csv").open(encoding="utf-8"))}
    md = (HERE / "REFERENCES.md").read_text(encoding="utf-8").splitlines()
    done = Counter()
    for i, line in enumerate(md):
        m = re.match(r"^(- .*?)(?: — \*corrected \d{4}-\d{2}-\d{2}:.*?\*)? \*\*\[[^\]]*\]\*\* `([^`]+)`\s*$", line)
        if not m or m.group(2) not in rows:
            continue
        r = rows[m.group(2)]
        text = m.group(1)
        if r["status"] == "corrected":
            fix = "; ".join(x for x in (r["title_in_source"], r["year_in_source"], r["working_url"] or r["doi"]) if x)
            text += f" — *corrected {DATE}: {fix}*"
        md[i] = f"{text} **[{TAG[r['status']]}]** `{m.group(2)}`"
        done[r["status"]] += 1
    (HERE / "REFERENCES.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    missing = sorted(set(rows) - {k for k in rows if any(f"`{k}`" in l for l in md)})
    # PROBLEMS.md section
    p = (HERE / "PROBLEMS.md").read_text(encoding="utf-8")
    p = re.sub(rf"\n{re.escape(MARK)}.*?(?=\n## 1\. )", "\n", p, flags=re.S)
    counts = Counter(r["status"] for r in rows.values())
    lines = [MARK, "",
             f"The {len(rows)} entries that had been taken from project files without checking were opened one by one on {DATE} "
             f"(`VERIFICATION_{DATE}.csv`): {counts['verified']} verified as entered, {counts['corrected']} verified with corrected "
             f"details (title, author, year or URL), {counts['not_found']} not located, {counts['unreachable']} unreachable. "
             "Tags in `REFERENCES.md` were updated accordingly; `cite.py` flags the entries that could not be located.", "",
             "**Not located or unreachable:**"]
    for k, r in sorted(rows.items()):
        if r["status"] in ("not_found", "unreachable"):
            lines.append(f"- `{k}`: {r['notes']}")
    lines += ["", "**Material corrections** (full details in the CSV):"]
    for k, r in sorted(rows.items()):
        if r["status"] == "corrected":
            lines.append(f"- `{k}`: {r['title_in_source']} ({r['year_in_source']}) — {r['notes'][:220]}{'…' if len(r['notes']) > 220 else ''}")
    lines.append("")
    p = p.replace("\n## 1. ", "\n" + "\n".join(lines) + "\n## 1. ", 1)
    (HERE / "PROBLEMS.md").write_text(p, encoding="utf-8")
    print("tags updated:", dict(done), "| keys not found in REFERENCES.md:", missing)


if __name__ == "__main__":
    main()
