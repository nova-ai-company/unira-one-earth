"""Build the draft constitution as an offline HTML page (Safari) and a Word file: python3 build.py"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "v67" / "dashboard"))
from build_dashboard import CSS, md_to_html  # noqa: E402

md = (HERE / "UNIRA_CONSTITUTION_DRAFT.md").read_text(encoding="utf-8")
page = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>One Earth Constitution</title><style>{CSS} .wrap{{max-width:760px}} p,li{{font-size:16.5px;line-height:1.65}}</style></head>"
        f"<body><div class='wrap'>{md_to_html(md)}</div></body></html>")
(HERE / "constitution.html").write_text(page, encoding="utf-8")
tmp = HERE / "tmp.html"
tmp.write_text("<html><head><meta charset='utf-8'><title>The Constitution of One Earth</title></head><body>" + md_to_html(md) + "</body></html>", encoding="utf-8")
if shutil.which("textutil"):
    subprocess.run(["textutil", "-convert", "docx", str(tmp), "-output", str(HERE / "UNIRA_Constitution_Draft.docx")], check=True)
tmp.unlink()
print("articles:", md.count("**Article "), "words:", len(md.split()))
