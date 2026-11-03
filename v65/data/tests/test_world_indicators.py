"""Tests for the V6.5 world indicators dataset.  Run from v65/data:
    python3 -I -m unittest discover -s tests -v
"""
import csv
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DATA))

import build  # noqa: E402
from fetch_world import verify_manifest  # noqa: E402

CSV = DATA / "world_indicators.csv"
BOUNDS = build.PLAUSIBLE


def rows():
    with CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestWorldIndicators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = rows()

    def test_raw_hashes_match_manifest(self):
        self.assertEqual(verify_manifest(DATA / "raw"), [])

    def test_columns(self):
        with CSV.open(newline="", encoding="utf-8") as f:
            self.assertEqual(next(csv.reader(f)), build.COLS)

    def test_no_duplicate_iso3_indicator(self):
        c = Counter((r["iso3"], r["indicator_id"]) for r in self.rows)
        self.assertEqual([k for k, n in c.items() if n > 1], [])

    def test_iso3_and_evidence(self):
        for r in self.rows:
            self.assertRegex(r["iso3"], r"^[A-Z]{3}$")
            self.assertIn(r["evidence_class"], {"VERIFIED_OFFICIAL", "REPORTED_NEEDS_RECHECK"})
            self.assertIn(r["indicator_id"], build.INDICATORS)
            if "ourworldindata" in r["source_url"] or "owid" in r["source_url"]:
                self.assertEqual(r["evidence_class"], "REPORTED_NEEDS_RECHECK")
            else:
                self.assertEqual(r["evidence_class"], "VERIFIED_OFFICIAL")

    def test_no_regional_aggregates(self):
        aggregates = {"AFE", "AFW", "ARB", "EUU", "HIC", "LMC", "OED", "SSF", "EAS", "ECS"}
        self.assertFalse(aggregates & {r["iso3"] for r in self.rows})

    def test_population_sums_to_world_total(self):
        pop = [r for r in self.rows if r["indicator_id"] == "pop_total"]
        world = float(next(r["value"] for r in pop if r["iso3"] == "WLD"))
        total = sum(float(r["value"]) for r in pop if r["iso3"] != "WLD")
        self.assertLess(abs(total - world) / world, 0.02)

    def test_plausible_bounds(self):
        for r in self.rows:
            b = BOUNDS.get(r["indicator_id"])
            if b and r["iso3"] != "WLD":
                v = float(r["value"])
                self.assertTrue(b[0] <= v <= b[1], f"{r['iso3']} {r['indicator_id']} {v}")

    def test_years_present_and_current(self):
        for r in self.rows:
            if r["iso3"] == "WLD" and "-" in r["year"]:
                continue
            y = int(r["year"])
            self.assertTrue(2015 <= y <= 2025, r)

    def test_rebuild_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "w.csv"
            build.build(out_csv=out, out_md=None)
            self.assertEqual(out.read_bytes(), CSV.read_bytes())


if __name__ == "__main__":
    unittest.main()
