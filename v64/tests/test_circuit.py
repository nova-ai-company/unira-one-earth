import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from unira_circuit import fetch, model  # noqa: E402


class TestRules(unittest.TestCase):
    def test_child_benefit_spec_formula(self):
        self.assertEqual(model.child_benefit(3, 10000), 3000)        # under threshold
        self.assertEqual(model.child_benefit(3, 13500), 1500)        # capped by means test
        self.assertEqual(model.child_benefit(2, 20000), 0)           # above threshold
        self.assertEqual(model.child_benefit(5, 0), 5000)

    def test_years_to_buy(self):
        self.assertAlmostEqual(model.years_to_buy(100000, 5000, 0.5), 100000 / 30000)
        self.assertAlmostEqual(model.years_to_buy(300000, 5000, 0.5, earners=2), 5.0)

    def test_multiplier_cap(self):
        d = model.wage_distribution({"A": 1, "B": 1}, {"A": 7.0, "B": 1.0}, 5.0)
        self.assertEqual(d["A"][1], 5.0)
        self.assertAlmostEqual(model.mean_multiplier(d), 3.0)

    def test_expected_child_benefit_bounds(self):
        dist = {"x": (1.0, 1.0)}
        # one adult always employed at 5000: benefit = min(2000, 10000) = 2000
        self.assertAlmostEqual(model.expected_child_benefit(2, 1, dist, 1.0, 5000, 1000, 15000), 2000)
        # two adults both at 5000 -> 10000 income -> min(3000, 5000)
        self.assertAlmostEqual(model.expected_child_benefit(3, 2, dist, 1.0, 5000, 1000, 15000), 3000)


class TestCircuit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import run
        cls.cfg = json.loads((ROOT / "config" / "circuit_config.json").read_text())
        cls.inp = run.build_inputs(cls.cfg)
        cls.c = model.annual_circuit(cls.inp, cls.cfg)

    def test_hashes(self):
        self.assertEqual(fetch.verify_manifest(ROOT / "data" / "raw"), [])

    def test_stock_flow_consistency(self):
        rows, cols = model.transaction_matrix(self.c)
        for r in rows.values():
            self.assertAlmostEqual(sum(r.values()), 0.0, delta=1e-3)
        self.assertAlmostEqual(sum(cols.values()), 0.0, delta=1e-3)

    def test_unspent_saving_mirrors_one_earth_financing(self):
        self.assertAlmostEqual(self.c["reg_balance"], -self.c["unspent_saving"], delta=1.0)

    def test_saving_equal_to_home_capacity_balances_region(self):
        cfg = json.loads(json.dumps(self.cfg))
        c0 = self.c
        adults = c0["wages"] + c0["disability_guarantees"]
        cfg["saving_rate_adults_20_64"]["value"] = c0["new_home_capacity_u"] / adults
        c1 = model.annual_circuit(self.inp, cfg, pi=None)
        # with saving matched to home capacity (at the new pi), unspent saving shrinks sharply
        self.assertLess(c1["unspent_saving"], 0.3 * c0["unspent_saving"])

    def test_fixed_price_creep_creates_excess_demand(self):
        d = model.dynamics(self.inp, self.cfg, 0.01, 0.0)
        self.assertGreater(d[-1]["excess_demand_share"], 0.2)
        d0 = model.dynamics(self.inp, self.cfg, 0.0, 0.0)
        self.assertAlmostEqual(d0[-1]["excess_demand_share"], 0.0, places=9)


if __name__ == "__main__":
    unittest.main()
