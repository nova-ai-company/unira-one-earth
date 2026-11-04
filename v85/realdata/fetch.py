"""Download World Bank indicators of production capacity by sector for all countries (run once). python3 fetch.py"""
import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(__file__).resolve().parent / "data" / "raw"
INDICATORS = {
    "NY.GDP.PCAP.PP.KD": "GDP per capita, PPP (constant 2021 international $)",
    "NV.AGR.TOTL.ZS": "Agriculture, forestry, and fishing, value added (% of GDP)",
    "NV.IND.TOTL.ZS": "Industry (including construction), value added (% of GDP)",
    "NV.IND.MANF.ZS": "Manufacturing, value added (% of GDP)",
    "NV.SRV.TOTL.ZS": "Services, value added (% of GDP)",
    "SL.AGR.EMPL.ZS": "Employment in agriculture (% of total employment) (modeled ILO estimate)",
    "SL.IND.EMPL.ZS": "Employment in industry (% of total employment) (modeled ILO estimate)",
    "SL.SRV.EMPL.ZS": "Employment in services (% of total employment) (modeled ILO estimate)",
    "SL.TLF.TOTL.IN": "Labor force, total",
    "SH.MED.BEDS.ZS": "Hospital beds (per 1,000 people)",
    "SE.PRM.ENRL.TC.ZS": "Pupil-teacher ratio, primary",
}
URL = "https://api.worldbank.org/v2/country/all/indicator/{}?format=json&per_page=20000&date=2010:2024"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for code, name in INDICATORS.items():
        url = URL.format(code)
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "UNIRA-research"}), timeout=120) as r:
            body = r.read()
        (RAW / f"wb_{code}.json").write_bytes(body)
        rows.append({"file": f"wb_{code}.json", "dataset": f"World Bank WDI {code} ({name})", "url": url,
                     "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body), "license": "World Bank Open Data, CC BY 4.0"})
        print(code, len(body))
    with (RAW / "raw_manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
