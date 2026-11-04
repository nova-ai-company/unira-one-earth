"""Download World Bank indicators for the UNIRA living-standard inventory, 2000-2024 (run once). python3 fetch.py"""
import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(__file__).resolve().parent / "data" / "raw"
INDICATORS = {
    "EG.ELC.ACCS.ZS": "Access to electricity (% of population)",
    "SH.H2O.BASW.ZS": "People using at least basic drinking water services (% of population)",
    "SH.H2O.SMDW.ZS": "People using safely managed drinking water services (% of population)",
    "SH.STA.BASS.ZS": "People using at least basic sanitation services (% of population)",
    "IT.NET.USER.ZS": "Individuals using the Internet (% of population)",
    "SH.MED.PHYS.ZS": "Physicians (per 1,000 people)",
    "SE.SEC.ENRR": "School enrollment, secondary (% gross)",
    "SP.POP.0014.TO.ZS": "Population ages 0-14 (% of total population)",
    "SP.POP.65UP.TO.ZS": "Population ages 65 and above (% of total population)",
    "EG.CFT.ACCS.ZS": "Access to clean fuels and technologies for cooking (% of population)",
}
URL = "https://api.worldbank.org/v2/country/all/indicator/{}?format=json&per_page=20000&date=2000:2024"


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for code, name in INDICATORS.items():
        url = URL.format(code)
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "UNIRA-research"}), timeout=180) as r:
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
