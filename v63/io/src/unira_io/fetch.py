"""Frozen Eurostat snapshots for V6.3 (reuses the tested V6.2 fetcher)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "v62" / "src"))
from unira_v62 import fetch as v62fetch  # noqa: E402

YEARS = ["2019", "2022"]
QUERIES = [
    ("io_symmetric_fr", "naio_10_cp1700",
     {"geo": "FR", "time": YEARS, "unit": "MIO_EUR", "stk_flow": ["DOM", "IMP", "TOTAL"]}),
    ("hours_a64_fr", "nama_10_a64_e",
     {"geo": "FR", "time": YEARS, "unit": ["THS_HW", "THS_PER"], "na_item": ["EMP_DC", "SAL_DC"]}),
]


def fetch_all(raw_dir):
    return v62fetch.fetch_all(raw_dir, QUERIES)


verify_manifest = v62fetch.verify_manifest
