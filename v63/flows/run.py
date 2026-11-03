"""Regenerate outputs/ from the frozen snapshots in data/raw/ (offline).

    python3 run.py           # verify hashes, compute, write outputs/
    python3 run.py --fetch   # re-download snapshots first (network; changes hashes)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from takeup import compute, queries  # noqa: E402
from takeup._v62 import fetch  # noqa: E402

RAW, OUT = ROOT / "data" / "raw", ROOT / "outputs"


def main(argv):
    if "--fetch" in argv:
        fetch.fetch_all(RAW, queries.QUERIES)
    bad = compute.verify_snapshots(RAW)
    if bad:
        sys.exit(f"snapshot hash mismatch: {bad}")
    fl, rows = compute.compute(RAW)
    compute.write_outputs(rows, compute.summary(fl, rows), OUT)
    print(f"wrote {len(rows)} rows -> {OUT / 'takeup_rates.csv'} and summary.json")


if __name__ == "__main__":
    main(sys.argv[1:])
