import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from unira_health import fetch, model  # noqa: E402


class TestHealth(unittest.TestCase):
    def test_implied_exits(self):
        stock = {2020: 100.0, 2023: 109.0}
        grads = {2021: 10.0, 2022: 10.0, 2023: 10.0}
        self.assertAlmostEqual(model.implied_exits(grads, stock, 2020, 2023), 7.0)

    def test_years_to_close(self):
        self.assertEqual(model.years_to_close(100, 50, 0.5, 3), 3 + 4)
        self.assertEqual(model.years_to_close(0, 50, 0.5, 3), 0)
        self.assertEqual(model.years_to_close(10, 50, 0.0, 3), math.inf)

    def test_year1_shortfall(self):
        self.assertEqual(model.year1_shortfall(10, 4), 6)
        self.assertEqual(model.year1_shortfall(10, 40), 0)

    def test_hashes(self):
        self.assertEqual(fetch.verify_manifest(ROOT / "data" / "raw"), [])

    def test_outputs_positive_exits(self):
        import csv
        rows = list(csv.DictReader((ROOT / "outputs" / "health_staffing.csv").open()))
        for r in rows:
            if r.get("implied_exits_per_year") not in (None, ""):
                self.assertGreater(float(r["implied_exits_per_year"]), 0, r["occupation"])


if __name__ == "__main__":
    unittest.main()
