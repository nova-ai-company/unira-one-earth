import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model  # noqa: E402


class TestEssential(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inv = model.inventory()

    def test_inventory_has_major_countries(self):
        for k in ("COD", "ETH", "NGA", "PAK", "IND", "IDN"):
            self.assertIn(k, self.inv)
        self.assertEqual(self.inv["COD"]["status"], "conflict")

    def test_longer_and_bigger_reach_more(self):
        a = model.plan(self.inv, 5, 1, "decentralised")["services"]["basic_water"]["share_reached"]
        b = model.plan(self.inv, 15, 3, "decentralised")["services"]["basic_water"]["share_reached"]
        self.assertLess(a, b)

    def test_decentralised_cheaper_and_faster(self):
        d = model.plan(self.inv, 10, 2, "decentralised")
        c = model.plan(self.inv, 10, 2, "centralised")
        self.assertLess(d["total_capital_usd_bn_per_year"], c["total_capital_usd_bn_per_year"])
        self.assertGreaterEqual(d["services"]["basic_sanitation"]["share_reached"], c["services"]["basic_sanitation"]["share_reached"])

    def test_participation_improves_durability(self):
        w = model.plan(self.inv, 10, 2, "decentralised", True)["services"]["basic_water"]["durably_served_m"]
        wo = model.plan(self.inv, 10, 2, "decentralised", False)["services"]["basic_water"]["durably_served_m"]
        self.assertGreater(w, wo)


if __name__ == "__main__":
    unittest.main()
