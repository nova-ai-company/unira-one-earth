import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model  # noqa: E402


class TestWorldMoney(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = model.regions()

    def test_france_defines_full_scale(self):
        self.assertIn("FRA", self.reg)
        self.assertGreater(len(self.reg), 150)

    def test_capacity_rule_never_short(self):
        for r in model.run(self.reg, 0.04, True, 30):
            self.assertLessEqual(r["world_shortage_share"], 1e-6)

    def test_fixed_schedule_reaches_full_scale_in_20_years(self):
        rows = model.run(self.reg, 0.04, False)
        self.assertAlmostEqual(rows[20]["mean_salary_factor_pop_weighted"], 1.0, places=6)

    def test_faster_growth_converges_sooner(self):
        y = lambda e: next((r["year"] for r in model.run(self.reg, e, True, 50) if r["mean_salary_factor_pop_weighted"] >= 0.99), 99)
        self.assertLess(y(0.06), y(0.04))


if __name__ == "__main__":
    unittest.main()
