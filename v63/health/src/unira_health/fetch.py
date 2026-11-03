"""Frozen Eurostat health-workforce snapshots for France (reuses the V6.2 fetcher)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "v62" / "src"))
from unira_v62 import fetch as v62fetch  # noqa: E402

QUERIES = [
    ("health_personnel_fr", "hlth_rs_prs2", {"geo": "FR", "unit": "NR", "sinceTimePeriod": "2012"}),
    ("health_graduates_fr", "hlth_rs_grd2", {"geo": "FR", "unit": "NR", "sinceTimePeriod": "2012"}),
    ("hospital_employment_fr", "hlth_rs_prshp2", {"geo": "FR", "unit": ["FTE", "HC"], "sinceTimePeriod": "2018"}),
    ("vacancy_rate_q_fr", "jvs_a_rate_r2", {"geo": "FR", "nace_r2": "Q", "sizeclas": "TOTAL", "unit": "AVG_A"}),
]


def fetch_all(raw_dir):
    return v62fetch.fetch_all(raw_dir, QUERIES)


verify_manifest = v62fetch.verify_manifest
