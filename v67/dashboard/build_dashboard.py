"""Build a self-contained UNIRA dashboard (index.html) from model outputs.

Plain HTML + CSS + inline SVG: no JavaScript, no external files, so it opens in any
browser (including older Safari) straight from disk:  python3 build_dashboard.py
Then: open index.html   (or double-click it). Also writes WORKING_PAPER_02.docx via macOS textutil.
"""
import csv
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]


# ---------- tiny markdown -> HTML (headings, paragraphs, lists, tables, bold, code, links) ----------
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md_to_html(md):
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip() or re.fullmatch(r"\s*<!--.*-->\s*", ln):  # blank line or hidden marker
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            lvl = len(m.group(1))
            text = m.group(2)
            anchor = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            out.append(f'<h{lvl} id="{anchor}">{inline(text)}</h{lvl}>')
            i += 1
            continue
        if ln.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]
            out.append("<div class='tw'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) +
                       "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                                                        for r in body) + "</tbody></table></div>")
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s", ln):
            items, kind = [], "ol" if re.match(r"^\s*\d+\.", ln) else "ul"
            while i < len(lines) and (re.match(r"^\s*([-*]|\d+\.)\s", lines[i]) or lines[i].startswith("    ")):
                cur = lines[i]
                depth = (len(cur) - len(cur.lstrip())) // 4
                text = re.sub(r"^\s*([-*]|\d+\.)\s+", "", cur)
                items.append((depth, text))
                i += 1
            html_list, open_depth = [f"<{kind}>"], 0
            for depth, text in items:
                while depth > open_depth:
                    html_list.append("<ul>")
                    open_depth += 1
                while depth < open_depth:
                    html_list.append("</ul>")
                    open_depth -= 1
                html_list.append(f"<li>{inline(text)}</li>")
            html_list += ["</ul>"] * open_depth + [f"</{kind}>"]
            out.append("".join(html_list))
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\s*\||\s*([-*]|\d+\.)\s)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


# ---------- inline SVG charts ----------
def bar_chart(title, sub, rows, ref=1.0, ref_label="1.0 = need met", maxv=None):
    x0, w, y0, rh = 250, 430, 70, 28
    maxv = maxv or max(v for _, v in rows) * 1.1
    sx = lambda v: x0 + v / maxv * w
    h = y0 + len(rows) * rh + 20
    parts = [f'<svg viewBox="0 0 760 {h}" role="img" aria-label="{html.escape(title)}">',
             f'<text x="20" y="26" class="t">{html.escape(title)}</text>',
             f'<text x="20" y="46" class="s">{html.escape(sub)}</text>']
    for i, (label, v) in enumerate(rows):
        y = y0 + i * rh
        cls = "acc" if v < ref else "mut"
        parts.append(f'<text x="{x0-10}" y="{y+15}" text-anchor="end" class="l">{html.escape(label)}</text>')
        parts.append(f'<rect x="{x0}" y="{y+3}" width="{sx(v)-x0:.1f}" height="16" class="{cls}"><title>{html.escape(label)}: {v:.2f}</title></rect>')
        parts.append(f'<text x="{sx(v)+6:.1f}" y="{y+15}" class="l">{v:.2f}x</text>')
    parts.append(f'<line x1="{sx(ref):.1f}" x2="{sx(ref):.1f}" y1="{y0-4}" y2="{h-16}" class="ref"/>')
    parts.append(f'<text x="{sx(ref)+4:.1f}" y="{y0-8}" class="s">{ref_label}</text></svg>')
    return "".join(parts)


def line_chart(title, sub, series, xlab, ymax, ylab_fmt="{:.0f}", target=None, target_label=""):
    """series: list of (name, [(x, y), ...], css_class)."""
    x0, x1, y0, y1 = 60, 610, 60, 300
    xs = [x for _, pts, _ in series for x, _ in pts]
    xmin, xmax = min(xs), max(xs)
    sx = lambda x: x0 + (x - xmin) / (xmax - xmin) * (x1 - x0)
    sy = lambda y: y1 - y / ymax * (y1 - y0)
    p = [f'<svg viewBox="0 0 760 340" role="img" aria-label="{html.escape(title)}">',
         f'<text x="20" y="26" class="t">{html.escape(title)}</text>', f'<text x="20" y="46" class="s">{html.escape(sub)}</text>']
    for k in range(5):
        yv = ymax * k / 4
        p.append(f'<line x1="{x0}" x2="{x1}" y1="{sy(yv):.1f}" y2="{sy(yv):.1f}" class="grid"/>')
        p.append(f'<text x="{x0-8}" y="{sy(yv)+4:.1f}" text-anchor="end" class="s">{ylab_fmt.format(yv)}</text>')
    for k in range(0, int(xmax - xmin) + 1, max(1, int((xmax - xmin) // 6))):
        p.append(f'<text x="{sx(xmin+k):.1f}" y="{y1+18}" text-anchor="middle" class="s">{int(xmin+k)}</text>')
    p.append(f'<text x="{(x0+x1)/2}" y="{y1+36}" text-anchor="middle" class="s">{html.escape(xlab)}</text>')
    if target is not None:
        p.append(f'<line x1="{x0}" x2="{x1}" y1="{sy(target):.1f}" y2="{sy(target):.1f}" class="ref"/>')
        p.append(f'<text x="{x1+6}" y="{sy(target)+4:.1f}" class="s">{html.escape(target_label)}</text>')
    for name, pts, cls in series:
        d = " ".join(f"{'M' if j == 0 else 'L'}{sx(x):.1f},{sy(min(y, ymax)):.1f}" for j, (x, y) in enumerate(pts))
        p.append(f'<path d="{d}" class="ln {cls}"><title>{html.escape(name)}</title></path>')
        lx, ly = pts[-1]
        p.append(f'<text x="{sx(lx)+6:.1f}" y="{sy(min(ly, ymax))+4:.1f}" class="l {cls}t">{html.escape(name)}</text>')
    p.append("</svg>")
    return "".join(p)


CSS = """
:root{--bg:#ffffff;--fg:#1b1b1f;--mut:#5f6168;--card:#f6f6f4;--line:#e3e3df;--acc:#2f6fd6;--grey:#b9b9b1;--g2:#3a9b5d;--g3:#c2762b}
@media (prefers-color-scheme: dark){:root{--bg:#17181b;--fg:#ececf0;--mut:#a3a5ad;--card:#222327;--line:#33343a;--acc:#6ea2f5;--grey:#62646b;--g2:#5cc184;--g3:#e09a52}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:24px 16px 64px}
header h1{font-size:28px;line-height:1.2;margin:8px 0 4px}header p{color:var(--mut);margin:0 0 16px}
nav{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 24px}nav a{padding:6px 12px;border:1px solid var(--line);border-radius:999px;color:var(--fg);text-decoration:none;font-size:14px}
.tiles{display:-webkit-box;display:flex;flex-wrap:wrap;margin:0 -6px}.tile{-webkit-box-flex:1;flex:1 1 200px;margin:6px;background:var(--card);border-radius:12px;padding:14px 16px}
.tile b{display:block;font-size:26px;line-height:1.1}.tile span{color:var(--mut);font-size:13px}
.card{background:var(--card);border-radius:12px;padding:12px;margin:16px 0}
svg{width:100%;height:auto;display:block}svg text{fill:var(--fg);font-size:12px}svg .t{font-size:15px;font-weight:600}svg .s{fill:var(--mut);font-size:11.5px}
svg .l{font-size:12px}.acc{fill:var(--acc)}.mut{fill:var(--grey)}.ref{stroke:var(--mut);stroke-dasharray:4 4;stroke-width:1}
.grid{stroke:var(--line);stroke-width:1}.ln{fill:none;stroke-width:2.2}.ln.c1{stroke:var(--acc)}.ln.c2{stroke:var(--g2)}.ln.c3{stroke:var(--g3)}.ln.c4{stroke:var(--grey)}
.c1t{fill:var(--acc)}.c2t{fill:var(--g2)}.c3t{fill:var(--g3)}.c4t{fill:var(--mut)}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{font-weight:600}
h2{margin-top:40px;border-top:1px solid var(--line);padding-top:24px}code{font-size:13px;background:var(--card);padding:1px 4px;border-radius:4px}a{color:var(--acc)}
.note{color:var(--mut);font-size:13px}
"""


def main():
    v65 = json.loads((U / "v65" / "outputs" / "world_sufficiency.json").read_text())["domains"]
    suf = [("Food, decent, today waste", v65["food|decent|consumer_waste_status_quo"]["sufficiency_ratio"]),
           ("Food, decent, half waste", v65["food|decent|consumer_waste_unira"]["sufficiency_ratio"]),
           ("Food, comfortable, today waste", v65["food|comfortable|consumer_waste_status_quo"]["sufficiency_ratio"]),
           ("Food, comfortable, half waste", v65["food|comfortable|consumer_waste_unira"]["sufficiency_ratio"]),
           ("Energy, decent 15 GJ", v65["energy|decent"]["sufficiency_ratio"]),
           ("Energy, comfortable 40 GJ", v65["energy|comfortable"]["sufficiency_ratio"]),
           ("Energy, EU level 82 GJ", v65["energy|eu_today"]["sufficiency_ratio"]),
           ("Health workers, WHO 44.5", v65["health|decent"]["sufficiency_ratio"]),
           ("Health workers, EU 131", v65["health|comfortable"]["sufficiency_ratio"])]
    charts = [bar_chart("Food and energy suffice for everyone; health workers and EU-level energy do not",
                        "World supply divided by world need, latest year, 8.14 bn people", suf, maxv=3.5)]
    tr = json.loads((U / "v67" / "outputs" / "transition.json").read_text())["results"]
    tl = tr["central"]["timeline"]
    charts.append(line_chart("Share of world population at the comfortable level, central case",
                             "Energy 40 GJ, health workers 131 per 10,000, housing 27 m2 per person", [
        ("Energy", [(r["year"], 100 * r["energy_share_pop_at_target"]) for r in tl], "c1"),
        ("Health", [(r["year"], 100 * r["health_share_pop_at_target"]) for r in tl], "c2"),
        ("Housing", [(r["year"], 100 * r["housing_share_pop_at_target"]) for r in tl], "c3")],
        "years from start", 100, "{:.0f}%"))
    hrows = list(csv.DictReader((U / "v66" / "outputs" / "health_plan_annual.csv").open()))
    pick = [("central|1_status_quo_training", "Training as today", "c4"),
            ("central|2_expand_training_7pct_15y", "+7%/yr training", "c3"),
            ("central|5_ambitious_10pct_50pct_prevention_high", "Ambitious", "c1")]
    charts.append(line_chart("Health workers per 10,000 people, world", "Central training capacity; dashed line = EU level 131",
                             [(lab, [(int(r["year"]), float(r["per_10k"])) for r in hrows if r["scenario"] == sc and int(r["year"]) <= 50], c)
                              for sc, lab, c in pick], "years from start", 160, target=131, target_label="131"))
    lrows = list(csv.DictReader((U / "v64" / "outputs" / "lifecycle.csv").open()))
    def avg(cap):
        out = []
        for y in range(0, 61, 2):
            sel = [float(r["deposits_months_of_consumption"]) for r in lrows if r["money_cap"] == cap and r["productivity_growth"] in ("0.0", "0") and r["year"] == str(y)]
            if sel:
                out.append((y, sum(sel) / len(sel)))
        return out
    charts.append(line_chart("Unspent money stabilises only with the cap",
                             "Household deposits in months of regional consumption, 60-year simulation",
                             [("No cap", avg("False"), "c4"), ("Cap + credit", avg("cap_low_credit"), "c1")],
                             "years", 160))
    cmp = json.loads((U / "v68" / "outputs" / "comparison.json").read_text())
    def grouped(title, sub, cats, series):
        x0, y0, bw, gap = 230, 70, 16, 14
        rows_h = len(cats) * (len(series) * bw + gap)
        h = y0 + rows_h + 40
        p = [f'<svg viewBox="0 0 760 {h}" role="img" aria-label="{html.escape(title)}">',
             f'<text x="20" y="26" class="t">{html.escape(title)}</text>', f'<text x="20" y="46" class="s">{html.escape(sub)}</text>']
        sx = lambda v: x0 + (max(v, -30) + 30) / 130 * 470
        zero = sx(0)
        y = y0
        for ci, cat in enumerate(cats):
            p.append(f'<text x="{x0-10}" y="{y + len(series)*bw/2 + 4}" text-anchor="end" class="l">{html.escape(cat)}</text>')
            for name, vals, cls in series:
                v = vals[ci] * 100
                x, w = (sx(v), zero - sx(v)) if v < 0 else (zero, sx(v) - zero)
                p.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w, 1):.1f}" height="{bw-3}" class="{cls}"><title>{html.escape(name)}: {v:.0f}%</title></rect>')
                p.append(f'<text x="{(sx(v)+4 if v >= 0 else sx(v)-4):.1f}" y="{y+bw-5}" text-anchor="{"start" if v >= 0 else "end"}" class="s">{name} {v:.0f}%</text>')
                y += bw
            y += gap
        p.append(f'<line x1="{zero:.1f}" x2="{zero:.1f}" y1="{y0-4}" y2="{y}" class="ref"/>')
        p.append("</svg>")
        return "".join(p)
    B, B2, C = cmp["B_reformed_market"], cmp["B2_ambitious_cooperative_market"], cmp["C_unira"]
    charts.append(grouped("UNIRA closes gaps; a reformed market economy does not",
                          "Share of the world shortfall closed, same resources (energy and health by year 15, housing by year 30)",
                          ["Energy (year 15)", "Health workers (year 15)", "Housing (year 30)"],
                          [("B market", [B["energy_closed_y15"], B["health_closed_y15"], B["housing_closed_y30"]], "mut"),
                           ("B2 cooperative", [B2["energy_closed_y15"], B2["health_closed_y15"], B2["housing_closed_y30"]], "mut"),
                           ("C UNIRA", [C["energy_closed_y15"], C["health_closed_y15"], C["housing_closed_y30"]], "acc")]))
    co = json.loads((U / "v69" / "outputs" / "coordination.json").read_text())
    order = [("C_perfect", "UNIRA, perfect"), ("C_best_observed", "UNIRA, best observed"), ("C_strong_safeguards", "UNIRA, strong safeguards"),
             ("C_no_safeguards", "UNIRA, no safeguards"), ("C_worst_observed", "UNIRA, worst observed")]
    rowsco = [(lab, co["results"][k]["health_closed_y15"]["p50"]) for k, lab in order if k in co["results"]]
    b2h = co["market_reference"]["B2_ambitious_cooperative_market"]["health_closed_y15"]
    rowsco.append(("Cooperative market (B2)", b2h))
    erows = [(lab, co["results"][k]["energy_closed_y15"]["p50"]) for k, lab in order if k in co["results"]]
    erows.append(("Cooperative market (B2)", co["market_reference"]["B2_ambitious_cooperative_market"]["energy_closed_y15"]))
    charts.append(bar_chart("With strong safeguards, needs-first allocation keeps most of its advantage",
                            "Energy shortfall closed by year 15 (median of 30 runs); dashed line = cooperative market (B2)",
                            [(l, max(v, 0.001)) for l, v in erows], ref=erows[-1][1], ref_label="B2 market", maxv=0.8))
    hz = json.loads((U / "v70" / "outputs" / "housing.json").read_text())["cases"]
    hrows = [("Today's capacity", hz["today_capacity"]["embodied_co2_gt_30y"]),
             ("+10%/yr, concrete", hz["ramp_10pct"]["embodied_co2_gt_30y"]),
             ("+10%/yr, stock-first, concrete", hz["ramp_10pct_stock_first"]["embodied_co2_gt_30y"]),
             ("+10%/yr, stock-first, low-carbon", hz["ramp_10pct_stock_first_low_carbon"]["embodied_co2_gt_30y"])]
    charts.append(bar_chart("Low-carbon homes keep housing for all within the climate budget",
                            "Embodied CO2 of 30 years of home building (Gt); dashed line = 1/3 of the 1.5 C budget (43 Gt)",
                            hrows, ref=43, ref_label="1/3 of 1.5 C budget", maxv=60).replace('class="acc"', 'class="tmp"').replace('class="mut"', 'class="acc"').replace('class="tmp"', 'class="mut"'))
    tiles = [("20.1%", "France: extra output per hour needed for 30 h with no new workers"),
             ("0%", "France gap with universal work at 88% employment"),
             ("1.27x", "World energy vs comfortable 40 GJ for everyone"),
             ("~59 m", "Health workers missing for EU-level care worldwide"),
             ("~65 bn m2", "New homes needed for 27 m2 per person"),
             ("18-42 yrs", "Until EU-level care for all, ambitious plan"),
             ("~90%", "Share of new capacity a market world must direct by need to match UNIRA on energy"),
             ("year 27", "Comfortable homes for all, with building +5-10%/yr and low-carbon materials"),
             ("86%", "Share of humanity that gains materially by joining UNIRA"),
             ("50%", "Share of people in France and Germany better off even at the lowest UNIRA salary")]
    paper = (U / "v67" / "WORKING_PAPER_02.md").read_text()
    body = (f"<div class='wrap'><header><p>UNIRA research · physical feasibility · generated from model outputs</p>"
            f"<h1>One Earth, 30 Hours</h1><p>Dashboard and Working Paper 02 (V6.2–V6.7). Opens offline in any browser.</p></header>"
            "<nav><a href='#key'>Key numbers</a><a href='#charts'>Charts</a><a href='#paper'>Working paper</a></nav>"
            "<h2 id='key'>Key numbers</h2><div class='tiles'>" +
            "".join(f"<div class='tile'><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>" for a, b in tiles) +
            "</div><h2 id='charts'>Charts</h2>" + "".join(f"<div class='card'>{c}</div>" for c in charts) +
            "<p class='note'>Every number is regenerated by <code>python3 v63/run_all.py</code> and this page by "
            "<code>python3 v67/dashboard/build_dashboard.py</code>.</p>"
            "<div id='paper'>" + md_to_html(paper) + "</div></div>")
    page = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>UNIRA Dashboard</title><style>{CSS}</style></head><body>{body}</body></html>")
    (HERE / "index.html").write_text(page, encoding="utf-8")
    # Word copy of the paper (macOS textutil); charts stay in the HTML dashboard
    paper_html = ("<html><head><meta charset='utf-8'><title>UNIRA Working Paper 02</title></head><body>"
                  + md_to_html(paper) + "</body></html>")
    tmp = HERE / "paper_tmp.html"
    tmp.write_text(paper_html, encoding="utf-8")
    if shutil.which("textutil"):
        subprocess.run(["textutil", "-convert", "docx", str(tmp), "-output", str(HERE / "WORKING_PAPER_02.docx")], check=True)
    tmp.unlink()
    print("wrote", HERE / "index.html")


if __name__ == "__main__":
    main()
