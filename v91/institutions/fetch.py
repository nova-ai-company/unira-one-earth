"""Download the raw data of V9.1 (run once): World Bank Worldwide Governance Indicators (estimates, 1996-2024),
GDP per capita (PPP) 1996-2024, and the UCDP/PRIO Armed Conflict, UCDP Battle-Related Deaths (conflict level) and
UCDP One-Sided Violence datasets, version 25.1. python3 fetch.py"""
import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(__file__).resolve().parent / "data" / "raw"
INDICATORS = {
    "GOV_WGI_VA.EST": "Voice and Accountability",
    "GOV_WGI_PV.EST": "Political Stability and Absence of Violence/Terrorism",
    "GOV_WGI_GE.EST": "Government Effectiveness",
    "GOV_WGI_RQ.EST": "Regulatory Quality",
    "GOV_WGI_RL.EST": "Rule of Law",
    "GOV_WGI_CC.EST": "Control of Corruption",
}
URL = "https://api.worldbank.org/v2/country/all/indicator/{}?source=3&format=json&per_page=20000&date=1996:2024"
GDP = ("NY.GDP.PCAP.PP.KD", "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.KD?format=json&per_page=20000&date=1996:2024")
UCDP = {  # Uppsala Conflict Data Program, CC BY 4.0 (https://ucdp.uu.se/downloads/)
    "ucdp-prio-acd-251-csv.zip": "UCDP/PRIO Armed Conflict Dataset v25.1 (Davies et al. 2025; Gleditsch et al. 2002)",
    "ucdp-brd-conf-251-csv.zip": "UCDP Battle-Related Deaths Dataset v25.1, conflict level",
    "ucdp-onesided-251-csv.zip": "UCDP One-Sided Violence Dataset v25.1 (Eck & Hultman 2007)"}
UCDP_URL = {"ucdp-prio-acd-251-csv.zip": "https://ucdp.uu.se/downloads/ucdpprio/ucdp-prio-acd-251-csv.zip",
            "ucdp-brd-conf-251-csv.zip": "https://ucdp.uu.se/downloads/brd/ucdp-brd-conf-251-csv.zip",
            "ucdp-onesided-251-csv.zip": "https://ucdp.uu.se/downloads/nsos/ucdp-onesided-251-csv.zip"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "UNIRA-research"}), timeout=120) as r:
        return r.read()


def row(file, dataset, url, body, licence):
    return {"file": file, "dataset": dataset, "url": url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body), "license": licence}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for code, name in INDICATORS.items():
        url = URL.format(code)
        body = get(url)
        (RAW / f"wb_{code}.json").write_bytes(body)
        rows.append(row(f"wb_{code}.json", f"World Bank Worldwide Governance Indicators {code} ({name}, estimate -2.5 to +2.5)",
                        url, body, "World Bank Open Data, CC BY 4.0"))
        print(code, len(body))
    body = get(GDP[1])
    (RAW / f"wb_{GDP[0]}.json").write_bytes(body)
    rows.append(row(f"wb_{GDP[0]}.json", "World Bank WDI NY.GDP.PCAP.PP.KD (GDP per capita, PPP, constant 2021 international $)",
                    GDP[1], body, "World Bank Open Data, CC BY 4.0"))
    for f, name in UCDP.items():
        body = get(UCDP_URL[f])
        (RAW / f).write_bytes(body)
        rows.append(row(f, name, UCDP_URL[f], body, "UCDP, CC BY 4.0"))
        print(f, len(body))
    with (RAW / "raw_manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
