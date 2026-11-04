"""Build v77/review/REVIEW_INDEX.html from the four Markdown files. Plain HTML + inline CSS, no JS."""
import html
import re
import sys
from pathlib import Path

D = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
DOCS = [("brief", "REVIEW_BRIEF.md", "Review brief"),
        ("questions", "REVIEW_QUESTIONS.md", "Review questions by field"),
        ("reviewers", "REVIEWERS.md", "Reviewers needed"),
        ("form", "FEEDBACK_FORM.md", "Feedback form"),
        ("audit", "SELF_AUDIT_2026-11-04.md", "Self-audit (4 Nov 2026)")]


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", t)
    return t


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md, prefix):
    lines = md.split("\n")
    out, i, n = [], 0, len(lines)
    para = []
    hid = 0

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < n:
        ln = lines[i]
        s = ln.strip()
        if not s:
            flush(); i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            flush()
            lvl = len(m.group(1)) + 1  # doc h1 -> h2
            hid += 1
            out.append(f'<h{lvl} id="{prefix}-{hid}">{inline(m.group(2))}</h{lvl}>')
            i += 1; continue
        if s == "---":
            flush(); out.append("<hr>"); i += 1; continue
        if s.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            flush()
            head = cells(s)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i])); i += 1
            t = ['<div class="tw"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t)); continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", ln):
            flush()
            # collect list block (including indented continuation lines)
            block = []
            while i < n and (re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]) or (lines[i].startswith("   ") and lines[i].strip())
                             or (not lines[i].strip() and i + 1 < n and re.match(r"^\s+([-*]|\d+\.)?\s*\S", lines[i + 1]) and lines[i + 1].startswith(" "))):
                block.append(lines[i]); i += 1
            out.append(render_list(block)); continue
        para.append(s); i += 1
    flush()
    return "\n".join(out)


def render_list(block):
    """Nested list rendering by indentation."""
    html_out, stack = [], []  # stack of (indent, tag)
    open_li = []
    lines = [l for l in block if l.strip()]
    j = 0
    while j < len(lines):
        ln = lines[j]
        if ln.strip().startswith("|") and not re.match(r"^\s*([-*]|\d+\.)\s+", ln):
            tbl = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                tbl.append(lines[j].strip()); j += 1
            head = cells(tbl[0]); rows = [cells(r) for r in tbl[2:]]
            t = '<div class="tw"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            html_out.append(t + "</tbody></table></div>")
            continue
        j += 1
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", ln)
        if m:
            ind = len(m.group(1).replace("\t", "    "))
            tag = "ol" if m.group(2)[0].isdigit() else "ul"
            while stack and ind < stack[-1][0]:
                html_out.append("</li></" + stack.pop()[1] + ">")
            if not stack or ind > stack[-1][0]:
                start = ""
                if tag == "ol" and m.group(2) != "1.":
                    start = f' start="{m.group(2)[:-1]}"'
                html_out.append(f"<{tag}{start}>")
                stack.append((ind, tag))
            else:
                html_out.append("</li>")
            html_out.append("<li>" + inline(m.group(3)))
        else:  # continuation paragraph inside current item
            html_out.append("<br>" + inline(ln.strip()))
    while stack:
        html_out.append("</li></" + stack.pop()[1] + ">")
    return "".join(html_out)


CSS = """
body{margin:0;background:#fbfbf8;color:#1d1d1b;font-family:Georgia,"Times New Roman",serif;font-size:17px;line-height:1.55}
.wrap{max-width:860px;margin:0 auto;padding:24px 16px 64px}
header{border-bottom:2px solid #1d1d1b;margin-bottom:24px;padding-bottom:12px}
h1{font-size:1.7em;margin:0 0 6px}
h2{font-size:1.45em;margin:48px 0 10px;border-top:1px solid #c9c9c2;padding-top:20px}
h3{font-size:1.15em;margin:28px 0 8px}
h4,h5{font-size:1em;margin:20px 0 6px}
.lead{color:#4a4a45;margin:0}
nav ol{padding-left:22px}
nav li{margin:4px 0}
a{color:#1f4e8c}
code{font-family:Menlo,Consolas,monospace;font-size:0.86em;background:#efefe8;padding:1px 3px;word-wrap:break-word}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:12px 0}
table{border-collapse:collapse;font-size:0.9em;width:100%}
th,td{border:1px solid #c9c9c2;padding:5px 7px;vertical-align:top;text-align:left}
th{background:#ececE4}
li{margin:3px 0}
.doc{margin-top:8px}
.src{font-size:0.85em;color:#4a4a45}
.top{font-size:0.85em}
footer{margin-top:48px;font-size:0.85em;color:#4a4a45;border-top:1px solid #c9c9c2;padding-top:12px}
@media (prefers-color-scheme: dark){
 body{background:#1a1a19;color:#e6e6e0}
 header{border-color:#e6e6e0}
 h2,footer{border-color:#444}
 th,td{border-color:#444}
 th{background:#2a2a28}
 code{background:#2a2a28}
 a{color:#8ab4f0}
 .lead,.src,footer{color:#b0b0a8}
}
@media print{.top,nav{display:none}h2{page-break-before:always}}
"""


def main():
    parts, nav = [], []
    for key, fn, title in DOCS:
        md = (D / fn).read_text(encoding="utf-8")
        body = convert(md, key)
        nav.append(f'<li><a href="#{key}">{html.escape(title)}</a> &middot; <a href="{fn}">{fn}</a></li>')
        parts.append(f'<section class="doc" id="{key}"><p class="src">Source file: <a href="{fn}">{fn}</a> &middot; '
                     f'<a class="top" href="#top">back to contents</a></p>{body}</section>')
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UNIRA Review Package</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap" id="top">
<header>
<h1>UNIRA research V6.2&ndash;V7.6: external review package</h1>
<p class="lead">For independent expert reviewers. 3 November 2026. No reviewer has been contacted yet. This page reproduces the four Markdown documents in this folder, which are authoritative.</p>
</header>
<nav><h2 style="border:0;margin-top:0;padding-top:0">Contents</h2><ol>{''.join(nav)}</ol>
<p class="src">Main research files: <code>v67/WORKING_PAPER_02.md</code> (the paper), <code>v75/constitution/UNIRA_CONSTITUTION_DRAFT.md</code>, <code>v62/audit/AUDIT_FINDINGS.md</code>, and <code>RESEARCH_NOTE.md</code> in v62&ndash;v71.</p></nav>
{''.join(parts)}
<footer>Static HTML. It uses no scripts and no external resources. Generated from the Markdown files in <code>v77/review/</code>.</footer>
</div>
</body>
</html>
"""
    (D / "REVIEW_INDEX.html").write_text(page, encoding="utf-8")


main()
