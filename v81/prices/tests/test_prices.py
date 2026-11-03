import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import calculator  # noqa: E402


class TestPrices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = calculator.calculate()

    def test_hour_price_is_the_fixed_one(self):
        summary = json.loads((calculator.U / "v64" / "outputs" / "summary.json").read_text())
        self.assertAlmostEqual(self.r["hour_price_u"], round(summary["fixed_price"]["pi_u_per_hour_equivalent"], 2))

    def test_resource_goods_never_cheaper_than_today(self):
        for k in calculator.RESOURCE_GROUPS:
            self.assertGreaterEqual(self.r["products"][k]["relative_to_today"], 0.999, k)

    def test_other_goods_have_no_surcharge(self):
        for k, v in self.r["products"].items():
            if k not in calculator.RESOURCE_GROUPS:
                self.assertEqual(v["resource_surcharge_pct"], 0.0, k)
                self.assertAlmostEqual(v["u_per_euro"], v["u_per_euro_work"], places=3)

    def test_price_is_hours_times_hour_price(self):
        t = self.r["products"]["CPA_A01"]
        self.assertAlmostEqual(t["u_per_euro"], t["hours_per_1000_eur"] / 1000 * self.r["hour_price_u"], places=2)

    def test_homes_excluded(self):
        for k in calculator.EXCLUDED:
            self.assertNotIn(k, self.r["products"])

    def test_examples_scale_with_euro_price(self):
        e = {x["item"]: x for x in self.r["examples"]}
        self.assertAlmostEqual(e["tomatoes"]["u_price"], 3.0 * self.r["products"]["CPA_A01"]["u_per_euro"], places=1)


if __name__ == "__main__":
    unittest.main()
