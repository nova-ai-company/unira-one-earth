import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import simulate  # noqa: E402


class TestEnterprise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        col, hrs, lab = simulate.io_data()
        f = simulate.facts()
        cls.acc = {n: simulate.firm_accounts(n, s, col, hrs, lab, f) for n, s in simulate.FIRMS.items()}

    def test_accounts_balance(self):
        for a in self.acc.values():
            parts = a["inputs_u"] + a["equipment_and_premises_wear_u"] + a["salaries_u"] + a["community_share_u"]
            self.assertLessEqual(abs(parts - a["sales_u"]), 3)

    def test_viable_at_normal_demand(self):
        for a in self.acc.values():
            self.assertGreater(a["community_share_u"], 0)
            self.assertLess(a["break_even_share_of_normal_demand"], 1.0)

    def test_salaries_follow_rules(self):
        for a in self.acc.values():
            self.assertLessEqual(a["average_multiplier"], 5.0)
            self.assertGreaterEqual(a["average_multiplier"], 1.0)

    def test_most_inputs_priced(self):
        for a in self.acc.values():
            self.assertLess(a["unpriced_input_share"], 0.02)

    def test_meal_price_matches_calculator(self):
        prices = json.loads((simulate.U / "v81" / "outputs" / "prices.json").read_text())
        meal = [e for e in prices["examples"] if e["item"] == "restaurant meal"][0]["u_price"]
        self.assertAlmostEqual(self.acc["restaurant"]["one_meal"]["price_u"], meal, delta=0.2)


if __name__ == "__main__":
    unittest.main()
