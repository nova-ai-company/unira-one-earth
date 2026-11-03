"""Download Eurostat national accounts for France: GDP, investment (GFCF), consumption of fixed capital (depreciation)
and net fixed assets (run once). python3 fetch.py"""
import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(__file__).resolve().parent / "data" / "raw"
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
QUERIES = {"nama_10_gdp_fr.json": ("nama_10_gdp", "geo=FR&unit=CP_MEUR&na_item=B1GQ&na_item=P51G&na_item=P51C&sinceTimePeriod=2015"),
           "nasa_10_nf_tr_fr.json": ("nasa_10_nf_tr", "geo=FR&unit=CP_MEUR&sector=S1&na_item=B1GQ&na_item=B1NQ&sinceTimePeriod=2015"),
           "nama_10_nfa_st_fr.json": ("nama_10_nfa_st", "geo=FR&unit=CRC_MEUR&asset10=N11N&asset10=N111N&asset10=N11KN&nace_r2=TOTAL&sinceTimePeriod=2015")}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for fname, (ds, q) in QUERIES.items():
        url = f"{BASE}{ds}?format=JSON&lang=EN&{q}"
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "UNIRA-research"}), timeout=120) as r:
            body = r.read()
        (RAW / fname).write_bytes(body)
        rows.append({"file": fname, "dataset": ds, "url": url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                     "license": "Eurostat reuse policy (Commission Decision 2011/833/EU; CC BY 4.0)"})
        print(fname, len(body))
    with (RAW / "raw_manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
