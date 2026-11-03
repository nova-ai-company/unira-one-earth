"""Assemble the public website (GitHub Pages, /docs) from the research outputs.
All pages are plain HTML (no external resources) so they work offline and in older browsers.
python3 build_site.py"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
DOCS = U / "docs"
sys.path.insert(0, str(U / "v67" / "dashboard"))
from build_dashboard import CSS, md_to_html  # noqa: E402


def page(title, body, width=980):
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{title}</title><style>{CSS} .wrap{{max-width:{width}px}} p,li{{line-height:1.65}}</style></head>"
            f"<body><div class='wrap'><p><a href='index.html'>← UNIRA home</a></p>{body}</div></body></html>")


def main():
    subprocess.run([sys.executable, str(HERE / "build_grids.py")], check=True)
    subprocess.run([sys.executable, str(HERE / "build_explorer.py")], check=True)
    subprocess.run([sys.executable, str(U / "v77" / "review" / "build_review.py")], check=True)
    DOCS.mkdir(exist_ok=True)
    (DOCS / "downloads").mkdir(exist_ok=True)
    shutil.copy(HERE / "explorer.html", DOCS / "simulator.html")
    shutil.copy(U / "v67" / "dashboard" / "index.html", DOCS / "dashboard.html")
    shutil.copy(U / "v73" / "book" / "book.html", DOCS / "book.html")
    shutil.copy(U / "v75" / "constitution" / "constitution.html", DOCS / "constitution.html")
    paper = (U / "v67" / "WORKING_PAPER_02.md").read_text(encoding="utf-8")
    (DOCS / "paper.html").write_text(page("UNIRA Working Paper 02", md_to_html(paper), 820), encoding="utf-8")
    for src, name in ((U / "v67" / "dashboard" / "WORKING_PAPER_02.docx", "UNIRA_Working_Paper_02.docx"),
                      (U / "v73" / "book" / "UNIRA_Book_Draft.docx", "UNIRA_Book_Draft.docx"),
                      (U / "v75" / "constitution" / "UNIRA_Constitution_Draft.docx", "UNIRA_Constitution_Draft.docx")):
        if src.exists():
            shutil.copy(src, DOCS / "downloads" / name)
    if (U / "v81" / "prices" / "prices.html").exists():
        shutil.copy(U / "v81" / "prices" / "prices.html", DOCS / "prices.html")
    pilot = U / "v80" / "pilot"
    if (pilot / "PILOT_PLAN.md").exists():
        body = md_to_html((pilot / "PILOT_SUMMARY.md").read_text(encoding="utf-8")) + "<hr>" + \
            md_to_html((pilot / "PILOT_PLAN.md").read_text(encoding="utf-8"))
        (DOCS / "pilot.html").write_text(page("UNIRA Pilot Proposal", body, 860), encoding="utf-8")
    review = U / "v77" / "review"
    if (review / "REVIEW_INDEX.html").exists():
        shutil.copy(review / "REVIEW_INDEX.html", DOCS / "review.html")
    home = """
<header><p>Open research · free for public discussion</p><h1>UNIRA — One Humanity, One Future</h1>
<p>A proposal for one world federation of equal regions, with a 30-hour week, fixed prices, allocation by need and no war,
tested against real data. Everything here is open: the data, the code, the results and their limits.</p></header>
<div class='tiles'>
<div class='tile'><b><a href='simulator.html'>Simulator</a></b><span>Change the assumptions and see the results</span></div>
<div class='tile'><b><a href='dashboard.html'>Dashboard</a></b><span>Key numbers and charts</span></div>
<div class='tile'><b><a href='paper.html'>Working Paper 02</a></b><span>The scientific paper</span></div>
<div class='tile'><b><a href='constitution.html'>Constitution</a></b><span>Draft Constitution of One Earth</span></div>
<div class='tile'><b><a href='book.html'>Book draft</a></b><span>UNIRA: One Humanity, One Future</span></div>
<div class='tile'><b><a href='review.html'>For reviewers</a></b><span>Review brief, questions and feedback form</span></div>
<div class='tile'><b><a href='prices.html'>Prices</a></b><span>What things cost in U, and in hours of work</span></div>
<div class='tile'><b><a href='pilot.html'>Pilot proposal</a></b><span>A 30-hour, full-employment town, tested against UNIRA's predictions</span></div>
</div>
<h2>Take part</h2>
<p>This is research in progress, published so that anyone can check it, criticise it and improve it.
Every number can be traced to an official source and reproduced with the open code (Python, standard library only).
To discuss, report an error or suggest better data, open an issue or a discussion in the <a href='https://github.com/nova-ai-company/unira-one-earth'>project repository</a>.</p>
<p class='note'>Downloads: <a href='downloads/UNIRA_Working_Paper_02.docx'>paper (Word)</a> ·
<a href='downloads/UNIRA_Book_Draft.docx'>book draft (Word)</a> · <a href='downloads/UNIRA_Constitution_Draft.docx'>constitution (Word)</a></p>
"""
    (DOCS / "index.html").write_text(page("UNIRA — One Humanity, One Future", home).replace("<p><a href='index.html'>← UNIRA home</a></p>", ""),
                                     encoding="utf-8")
    (DOCS / ".nojekyll").write_text("")
    print("site built in", DOCS)


if __name__ == "__main__":
    main()
