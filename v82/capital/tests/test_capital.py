import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model  # noqa: E402


class TestCapital(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = model.facts()

    def test_facts_plausible(self):
        self.assertGreater(self.f["gfcf_share_gdp"], self.f["depreciation_share_gdp"])
        self.assertTrue(0.1 < self.f["investment_share_of_hours_2022"] < 0.3)
        self.assertTrue(2 < self.f["net_fixed_assets_years_of_gdp"] < 6)

    def test_today_is_30_hours(self):
        net = self.f["investment_share_of_hours_2022"] * (1 - self.f["maintenance_share_of_investment"])
        self.assertAlmostEqual(model.path(self.f, 0.0, net, 10)[0], 30.0, places=6)

    def test_better_payback_shortens_week_more(self):
        w6 = model.path(self.f, 0.0, 0.03, 6)[30]
        w15 = model.path(self.f, 0.0, 0.03, 15)[30]
        self.assertLess(w6, w15)

    def test_savings_level_off_after_equipment_life(self):
        w = model.path(self.f, 0.0, 0.03, 10)
        self.assertAlmostEqual(w[model.LIFE_YEARS], w[model.YEARS], places=6)


if __name__ == "__main__":
    unittest.main()
