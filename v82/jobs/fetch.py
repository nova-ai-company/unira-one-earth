"""Download Eurostat job vacancy rates by economic activity (jvs_a_rate_r2), France and EU27, 2019-2025 (run once).
python3 fetch.py"""
import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(__file__).resolve().parent / "data" / "raw"
URL = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/jvs_a_rate_r2?format=JSON&lang=EN"
       "&geo=FR&geo=EU27_2020&sizeclas=TOTAL&unit=AVG_A&sinceTimePeriod=2019")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(URL, headers={"User-Agent": "UNIRA-research"})
    with urllib.request.urlopen(req, timeout=120) as r:
        body = r.read()
    (RAW / "jvs_a_rate_r2.json").write_bytes(body)
    with (RAW / "raw_manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["file", "dataset", "url", "retrieved_at_utc", "sha256", "bytes", "license"])
        w.writeheader()
        w.writerow({"file": "jvs_a_rate_r2.json", "dataset": "jvs_a_rate_r2", "url": URL,
                    "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                    "license": "Eurostat reuse policy (Commission Decision 2011/833/EU; CC BY 4.0)"})
    print(len(body), "bytes")


if __name__ == "__main__":
    main()
