"""Frozen Eurostat snapshots for the V6.4 money circuit (reuses the V6.2 fetcher)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "v62" / "src"))
from unira_v62 import fetch as v62fetch  # noqa: E402

QUERIES = [
    ("population_age_fr", "demo_pjan", {"geo": "FR", "time": "2024", "sex": "T", "unit": "NR"}),
    ("households_children_fr", "lfst_hhnhtych", {"geo": "FR", "time": "2023", "agechild": "TOTAL", "unit": "THS_HH"}),
    ("employment_isco_fr", "lfsa_egais", {"geo": "FR", "time": "2023", "sex": "T", "age": "Y20-64", "wstatus": "EMP"}),
    ("tenure_fr", "ilc_lvho02", {"geo": "FR", "time": "2023", "rskpovth": "TOTAL", "unit": "PC"}),
]


def fetch_all(raw_dir):
    return v62fetch.fetch_all(raw_dir, QUERIES)


verify_manifest = v62fetch.verify_manifest
