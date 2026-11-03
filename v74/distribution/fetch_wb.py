"""Download World Bank income-distribution and consumption indicators for all countries (frozen snapshot).
python3 fetch_wb.py   (run once; run.py works offline from the saved files and checks their hashes)"""
import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(__file__).resolve().parent / "data" / "raw"
INDICATORS = {
    "SI.DST.FRST.10": "Income share held by lowest 10%",
    "SI.DST.FRST.20": "Income share held by lowest 20%",
    "SI.DST.02ND.20": "Income share held by second 20%",
    "SI.DST.03RD.20": "Income share held by third 20%",
    "SI.DST.04TH.20": "Income share held by fourth 20%",
    "SI.DST.05TH.20": "Income share held by highest 20%",
    "SI.DST.10TH.10": "Income share held by highest 10%",
    "NE.CON.PRVT.PP.KD": "Households and NPISHs final consumption expenditure, PPP (constant 2021 international $)",
    "SP.POP.TOTL": "Population, total",
}
URL = "https://api.worldbank.org/v2/country/all/indicator/{}?format=json&per_page=20000&date=2005:2024"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = RAW / "raw_manifest.csv"
    with manifest.open() as f:
        rows = {r["file"]: r for r in csv.DictReader(f)}
    for code, name in INDICATORS.items():
        url = URL.format(code)
        req = urllib.request.Request(url, headers={"User-Agent": "UNIRA-research"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read()
        path = RAW / f"wb_{code}.json"
        path.write_bytes(body)
        rows[path.name] = {"file": path.name, "dataset": f"World Bank WDI {code} ({name})", "url": url,
                           "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                           "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                           "license": "World Bank Open Data, CC BY 4.0"}
        print("fetched", code, len(body), "bytes")
    with manifest.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(next(iter(rows.values()))))
        w.writeheader()
        w.writerows(rows.values())


if __name__ == "__main__":
    main()
