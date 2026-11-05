"""Standalone HTML of the V9.1 research note and the proposed constitution changes (no JavaScript, no external files,
opens from disk in any browser): python3 build_page.py -> V91_institutions.html"""
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parent
spec = importlib.util.spec_from_file_location("dash", U / "v67" / "dashboard" / "build_dashboard.py")
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)

CSS = """:root{--bg:#fbfaf7;--fg:#1f2328;--mut:#5b636d;--line:#d9d6cf;--acc:#2f6f5e;--th:#efece5}
@media (prefers-color-scheme:dark){:root{--bg:#16181b;--fg:#e6e3dd;--mut:#a3a9b0;--line:#3a3d42;--acc:#7cc4ad;--th:#22252a}}
body{background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;margin:0}
main{max-width:900px;margin:0 auto;padding:24px 16px 64px}h1{font-size:1.6em;line-height:1.25}h2{margin-top:2em;color:var(--acc)}
.tw{overflow-x:auto}table{border-collapse:collapse;margin:1em 0;font-size:.92em}th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
th{background:var(--th)}code{font-size:.9em}blockquote,.note{color:var(--mut)}hr{border:0;border-top:1px solid var(--line);margin:3em 0}"""


def md(path):
    text = (HERE / path).read_text()
    text = re.sub(r"(?m)^   (\s*)- ", lambda m: "    " + m.group(1) + "- ", text)  # 3-space nesting -> 4
    text = re.sub(r"(?m)^> ?", "", text)  # quoted proposal texts as plain paragraphs
    return D.md_to_html(text)


def main():
    body = md("RESEARCH_NOTE.md") + "\n<hr>\n" + md("CONSTITUTION_CONSISTENCY_CHECK.md") + "\n<hr>\n" + md("PROPOSED_CONSTITUTION_CHANGES.md")
    page = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>UNIRA V9.1 Institutions</title><style>{CSS}</style></head><body><main>{body}</main></body></html>\n")
    (HERE / "V91_institutions.html").write_text(page)
    print("wrote", HERE / "V91_institutions.html")


if __name__ == "__main__":
    main()
