import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model  # noqa: E402


class TestCredit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = model.wm.regions()

    def test_no_credit_no_stock(self):
        r = model.run(self.reg, 0.06, 0.0)
        self.assertEqual(r["peak_credit_stock_years_of_world_consumption"], 0.0)

    def test_bigger_credit_bigger_stock(self):
        a = model.run(self.reg, 0.06, 0.25)["peak_credit_stock_years_of_world_consumption"]
        b = model.run(self.reg, 0.06, 0.5)["peak_credit_stock_years_of_world_consumption"]
        self.assertLess(a, b)

    def test_quarter_credit_paid_with_faster_release(self):
        r = model.run(self.reg, 0.06, 0.25, model.RELEASE_CAP_AFTER)
        self.assertIsNotNone(r["year_credits_paid"])
        self.assertLess(r["year_credits_paid"], 60)

    def test_reserves_absorb_shocks(self):
        shocks = {5: 0.05, 15: 0.10, 21: 0.05}
        r = model.run(self.reg, 0.04, 0.25, model.RELEASE_CAP_AFTER, shocks=shocks)
        self.assertEqual(r["shortage_years_after_reserves"], 0)

    def test_liability_ceiling_bounds_promises(self):
        r = model.run(self.reg, 0.02, 0.25, model.RELEASE_CAP_AFTER, rich_growth=0.005, liability_ceiling=2.0)
        self.assertLess(r["peak_credit_stock_years_of_world_consumption"], 2.2)


if __name__ == "__main__":
    unittest.main()
