"""Integration interface for the V6.2/V6.3 labour-reserve model (stdlib only)."""
import csv
from pathlib import Path

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "outputs" / "takeup_rates.csv"


def load_takeup(csv_path=None):
    """All rows of takeup_rates.csv; takeup_rate is float or None (MISSING)."""
    with Path(csv_path or DEFAULT_CSV).open(newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["year"] = int(r["year"])
        r["takeup_rate"] = float(r["takeup_rate"]) if r["takeup_rate"] else None
    return rows


def get_takeup(geo, year, pool, role="proposed", csv_path=None, rows=None):
    """Annual take-up share (0..1) of `pool` in {'T1','T2','T3'} for `geo` (Eurostat code,
    'EU27_2020' or 'TOP3_MEAN' with role='benchmark'). Returns None if MISSING/absent.
    role: 'proposed' | 'lower_bound' | 'alternative' | 'cross_check' | 'benchmark'.
    For roles with several rows (cross_check, benchmark) the first row is returned."""
    for r in rows if rows is not None else load_takeup(csv_path):
        if (r["geo"], r["year"], r["pool"], r["role"]) == (geo, int(year), pool, role):
            return r["takeup_rate"]
    return None
