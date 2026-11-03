"""Download WHO healthy life expectancy (HALE) at birth for all countries (frozen snapshot, run once).
python3 fetch.py"""
import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(__file__).resolve().parent / "data" / "raw"
URL = ("https://xmart-api-public.who.int/GHO/FACT?$filter=INDICATOR_CODE+eq+'WHOSIS_000002'"
       "&$select=INDICATOR_CODE,PERIOD_CODE,LOCATION_CODE,LOCATION_TYPE,DIMENSION_1,DIMENSION_MEMBER_1,VALUE_NUMERIC")


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(URL, headers={"User-Agent": "UNIRA-research"})
    with urllib.request.urlopen(req, timeout=120) as r:
        body = r.read()
    (RAW / "who_WHOSIS_000002.json").write_bytes(body)
    with (RAW / "raw_manifest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["file", "dataset", "url", "retrieved_at_utc", "sha256", "bytes", "license"])
        w.writeheader()
        w.writerow({"file": "who_WHOSIS_000002.json", "dataset": "WHO GHO WHOSIS_000002 Healthy life expectancy (HALE) at birth (years)",
                    "url": URL, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                    "license": "WHO GHO data, CC BY-NC-SA 3.0 IGO (WHO data policy)"})
    print(len(body), "bytes")


if __name__ == "__main__":
    main()
