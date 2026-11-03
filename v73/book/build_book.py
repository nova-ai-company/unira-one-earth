"""Build the book draft as an offline HTML page (Safari-friendly) and a Word file.
python3 build_book.py"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "v67" / "dashboard"))
from build_dashboard import CSS, md_to_html  # noqa: E402


def main():
    parts = [HERE / "OUTLINE.md"] + sorted(HERE.glob("CHAPTER_*.md")) + [HERE / "BIBLIOGRAPHY.md"]
    md = "\n\n".join(p.read_text(encoding="utf-8") for p in parts)
    body = ("<div class='wrap'><header><p>Draft manuscript · generated from the UNIRA research</p>"
            "<h1>UNIRA: One Humanity, One Future</h1></header>" + md_to_html(md) + "</div>")
    page = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>UNIRA Book Draft</title><style>{CSS} .wrap{{max-width:760px}} p{{font-size:17px;line-height:1.7}}</style></head><body>{body}</body></html>")
    (HERE / "book.html").write_text(page, encoding="utf-8")
    tmp = HERE / "tmp_book.html"
    tmp.write_text("<html><head><meta charset='utf-8'><title>UNIRA: One Humanity, One Future</title></head><body>"
                   + md_to_html(md) + "</body></html>", encoding="utf-8")
    if shutil.which("textutil"):
        subprocess.run(["textutil", "-convert", "docx", str(tmp), "-output", str(HERE / "UNIRA_Book_Draft.docx")], check=True)
    tmp.unlink()
    words = len(md.split())
    print(f"wrote book.html and UNIRA_Book_Draft.docx ({words} words)")


if __name__ == "__main__":
    main()
