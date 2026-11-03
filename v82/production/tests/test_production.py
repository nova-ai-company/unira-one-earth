import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import simulate  # noqa: E402


class TestProduction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = dict(simulate.load_config(), months=60, products=30, seeds=[1])

    def test_deterministic(self):
        self.assertEqual(simulate.run(self.cfg, "unira", 1), simulate.run(self.cfg, "unira", 1))

    def test_shares_are_valid(self):
        for r in simulate.REGIMES:
            res = simulate.run(self.cfg, r, 1)
            for k in ("served_within_1_month", "served_within_3_months", "lost_or_lapsed", "waste_share_of_production"):
                self.assertGreaterEqual(res[k], 0.0, (r, k))
                self.assertLessEqual(res[k], 1.0 + 1e-9, (r, k))
            self.assertLessEqual(res["served_within_1_month"], res["served_within_3_months"] + 1e-9)
            self.assertLessEqual(res["hours_used_share"], 1.0 + 1e-9)

    def test_waiting_lists_reveal_demand(self):
        a = simulate.run(self.cfg, "unira", 1)
        b = simulate.run(self.cfg, "unira_sales", 1)
        self.assertLess(a["lost_or_lapsed"], b["lost_or_lapsed"])

    def test_market_prices_out_the_poorer_first(self):
        m = simulate.run(self.cfg, "market", 1)
        self.assertGreater(m["priced_out_share_of_desire"], 0.0)
        self.assertGreater(m["priced_out_share_in_poorer_half"], 0.5)


if __name__ == "__main__":
    unittest.main()
