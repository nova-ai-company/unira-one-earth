import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import sizes  # noqa: E402


class TestSizes(unittest.TestCase):
    def test_outputs(self):
        sizes.main()
        r = json.loads((HERE / "outputs" / "sizes.json").read_text())
        a = r["energy_allowance"]
        self.assertAlmostEqual(a["allowance_kwh_per_person_year_start"], 0.8 * a["france_home_energy_kwh_per_person_2024"], delta=10)
        self.assertLess(a["target_kwh_after_renovation"], a["allowance_kwh_per_person_year_start"])
        self.assertLessEqual(r["pension"]["max_u_month"], 5000)
        self.assertGreater(r["reserves"]["essential_goods_stock_months"], r["reserves"]["spending_rush_extra_demand_months"] - 0.5)


if __name__ == "__main__":
    unittest.main()
