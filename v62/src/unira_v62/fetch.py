"""Download raw Eurostat snapshots for V6.2 and record provenance.

Run once (network required): `python3 run_all.py --fetch`.
Every later step reads ONLY the frozen files in data/raw/, so results are
reproducible offline and auditable against data/raw/raw_manifest.csv.
"""
import csv
import hashlib
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
SECTIONS = ["TOTAL", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
            "M", "N", "O", "P", "Q", "R", "S", "T", "U"]

# (file stem, dataset code, query parameters). Lists become repeated params.
QUERIES = [
    ("na_employment_hours", "nama_10_a64_e",
     {"geo": "FR", "sinceTimePeriod": "2015", "unit": ["THS_HW", "THS_PER"],
      "na_item": ["EMP_DC", "SAL_DC", "SELF_DC"], "nace_r2": SECTIONS}),
    ("na_output", "nama_10_a64",
     {"geo": "FR", "sinceTimePeriod": "2015", "unit": ["CP_MEUR", "CLV20_MEUR"],
      "na_item": ["B1G", "P1"], "nace_r2": SECTIONS}),
    ("lfs_usual_hours", "lfsa_ewhun2",
     {"geo": "FR", "sinceTimePeriod": "2019", "sex": "T", "age": "Y_GE15",
      "wstatus": ["EMP", "SAL", "NSAL"], "nace_r2": SECTIONS}),
    ("lfs_actual_hours", "lfsa_ewhan2",
     {"geo": "FR", "sinceTimePeriod": "2019", "sex": "T", "age": "Y_GE15",
      "wstatus": ["EMP", "SAL", "NSAL"], "nace_r2": SECTIONS}),
    ("lfs_parttime_persons", "lfsa_epgan2",
     {"geo": "FR", "sinceTimePeriod": "2019", "sex": "T", "nace_r2": SECTIONS}),
    ("lfs_slack", "lfsi_sla_a",
     {"geo": "FR", "sinceTimePeriod": "2019", "sex": "T", "age": "Y15-74",
      "unit": "THS_PER"}),
]


# Multi-country labour reserve (EU27 + EEA/EFTA). Aggregates are fetched but
# excluded from benchmarks in labour_reserve.py.
GEOS = ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU",
        "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK",
        "IS", "NO", "CH", "EU27_2020"]
YEARS = ["2023", "2024"]
QUERIES_RESERVE = [
    ("eu_na_hours_total", "nama_10_a64_e",
     {"geo": GEOS, "time": YEARS, "unit": ["THS_HW", "THS_PER"],
      "na_item": ["EMP_DC", "SAL_DC", "SELF_DC"], "nace_r2": "TOTAL"}),
    ("eu_lfs_usual_hours_total", "lfsa_ewhun2",
     {"geo": GEOS, "time": YEARS, "sex": "T", "age": "Y_GE15",
      "wstatus": ["EMP", "SAL", "NSAL"], "nace_r2": "TOTAL"}),
    ("eu_lfs_slack", "lfsi_sla_a",
     {"geo": GEOS, "time": YEARS, "sex": "T", "age": ["Y15-74", "Y20-64"], "unit": "THS_PER"}),
    ("eu_lfs_employment", "lfsi_emp_a",
     {"geo": GEOS, "time": YEARS, "sex": "T", "indic_em": "EMP_LFS",
      "age": ["Y20-64", "Y25-54", "Y55-64"], "unit": ["THS_PER", "PC_POP"]}),
    ("eu_lfs_parttime_reason", "lfsa_epgar",
     {"geo": GEOS, "time": YEARS, "sex": "T", "age": "Y20-64"}),
    ("eu_lfs_inactive_reason", "lfsa_igar",
     {"geo": GEOS, "time": YEARS, "sex": "T", "age": "Y20-64", "unit": "PC_POP"}),
]


def build_url(dataset, params):
    pairs = [("format", "JSON"), ("lang", "EN")]
    for k, v in params.items():
        pairs += [(k, x) for x in (v if isinstance(v, list) else [v])]
    return API + dataset + "?" + urllib.parse.urlencode(pairs)


def fetch_all(raw_dir, queries=None):
    """Download `queries` (default: all) and merge their rows into the manifest;
    rows for files not re-fetched are kept unchanged."""
    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for stem, dataset, params in (queries if queries is not None else QUERIES + QUERIES_RESERVE):
        url = build_url(dataset, params)
        req = urllib.request.Request(url, headers={"User-Agent": "UNIRA-V6.2-research"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read()
        path = raw_dir / f"{stem}.json"
        path.write_bytes(body)
        rows.append({"file": path.name, "dataset": dataset, "url": url,
                     "retrieved_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body),
                     "license": "Eurostat reuse policy (Commission Decision 2011/833/EU; CC BY 4.0)"})
        print(f"fetched {dataset} -> {path.name} ({len(body)} bytes)")
    manifest = raw_dir / "raw_manifest.csv"
    merged = {}
    if manifest.exists():
        with manifest.open() as f:
            merged = {r["file"]: r for r in csv.DictReader(f)}
    merged.update({r["file"]: r for r in rows})
    with manifest.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(merged.values())
    return rows


def verify_manifest(raw_dir):
    """Return list of files whose sha256 no longer matches the manifest."""
    raw_dir = Path(raw_dir)
    bad = []
    with (raw_dir / "raw_manifest.csv").open() as f:
        for row in csv.DictReader(f):
            digest = hashlib.sha256((raw_dir / row["file"]).read_bytes()).hexdigest()
            if digest != row["sha256"]:
                bad.append(row["file"])
    return bad
