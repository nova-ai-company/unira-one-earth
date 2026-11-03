import json
import sys
import unittest
from pathlib import Path

V79 = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(V79 / "allocation"), str(V79 / "prices"), str(V79 / "money")]
import formula  # noqa: E402
import location  # noqa: E402

OUT = V79 / "outputs"


class TestLocation(unittest.TestCase):
    def test_min_cost_flow_is_optimal_on_small_case(self):
        supply = {"A": 5.0, "B": 5.0}
        demand = {"X": 4.0, "Y": 4.0}
        cost = {("A", "X"): 1, ("A", "Y"): 10, ("B", "X"): 10, ("B", "Y"): 1}
        f = location.min_cost_flow(supply, demand, cost)
        self.assertAlmostEqual(f.get(("A", "X"), 0), 4.0)
        self.assertAlmostEqual(f.get(("B", "Y"), 0), 4.0)
        self.assertNotIn(("A", "Y"), f)

    def test_flows_respect_supply_and_cover_demand(self):
        supply = {"A": 3.0, "B": 10.0}
        demand = {"X": 5.0, "Y": 6.0}
        cost = {("A", "X"): 1, ("A", "Y"): 2, ("B", "X"): 3, ("B", "Y"): 4}
        f = location.min_cost_flow(supply, demand, cost)
        for i, s in supply.items():
            self.assertLessEqual(sum(v for (a, _), v in f.items() if a == i), s + 1e-9)
        for j, d in demand.items():
            self.assertAlmostEqual(sum(v for (_, b), v in f.items() if b == j), d)

    def test_food_result(self):
        r = json.loads((OUT / "food_location.json").read_text())
        self.assertLess(r["optimised"]["mean_km_per_kcal"], r["pro_rata"]["mean_km_per_kcal"])


class TestFormula(unittest.TestCase):
    def test_two_pass_never_worse_for_decent(self):
        r = json.loads((OUT / "allocation_formula.json").read_text())["results"]
        one, two = r["single_pass_v67"], r["two_pass"]
        for d in ("energy", "health", "housing"):
            self.assertLessEqual(two["person_years_below_decent_bn"][d], one["person_years_below_decent_bn"][d])
            self.assertLessEqual(two["year_everyone_decent"][d], one["year_everyone_decent"][d])
            self.assertAlmostEqual(two["comfortable_gap_closed_y30"][d], one["comfortable_gap_closed_y30"][d], places=2)

    def test_health_weights_average_one(self):
        regions = formula.compare.rt.load_regions()
        w = formula.health_weights(regions)
        mean = sum(w[k] * regions[k]["pop0"] for k in regions) / sum(r["pop0"] for r in regions.values())
        self.assertAlmostEqual(mean, 1.0)


class TestPricesAndCap(unittest.TestCase):
    def test_price_ratios_average_one(self):
        r = json.loads((OUT / "price_rule.json").read_text())["all"]
        self.assertAlmostEqual(sum(x["household_spending_share"] * x["hours_price_vs_market"] for x in r), 1.0, places=2)

    def test_thermostat_limit_and_no_blocked_first_homes(self):
        r = json.loads((OUT / "thermostat.json").read_text())["results"]
        for k, v in r.items():
            if k.endswith("limited_10pct"):
                self.assertLessEqual(v["max_yearly_cap_change_pct"], 10.0 + 1e-6)
            self.assertEqual(v["first_homes_blocked_by_cap"], 0)
            self.assertLess(abs(v["deposits_months_final"] - 12), 1.0)

    def test_cap_levels(self):
        r = json.loads((OUT / "cap_level.json").read_text())["results"]
        rush = [r[f"cap_{c}y/accounts"]["rush_extra_demand_pct_of_year"] for c in ("1", "1.5", "2", "3", "5")]
        self.assertEqual(rush, sorted(rush))  # more free money, larger possible rush
        for k, v in r.items():
            self.assertEqual(v["first_homes_blocked_by_cap"], 0)
            if k.endswith("/accounts"):
                self.assertGreater(v["protected_months"], 0)
            else:
                self.assertEqual(v["protected_months"], 0)

    def test_protected_accounts_respect_limits(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("cap_level", V79 / "money" / "cap_level.py")
        cl = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cl)
        cfg = json.loads((V79.parent / "v64" / "config" / "circuit_config.json").read_text())
        c = cl.rl.sim_config(cfg, 0.0, True, "cap_low_credit")
        c.update({"cap_floor_years": 1.5, "years": 30, "sample_size": 1500,
                  "home_account_max": cl.HOME_MAX, "retirement_account_max": cl.RET_MAX})
        _, people = cl.rl.lifecycle.simulate(c, 1, return_people=True)
        self.assertTrue(all(p.home_acc <= cl.HOME_MAX + 1e-6 and p.ret_acc <= cl.RET_MAX + 1e-6 for p in people))
        self.assertTrue(all(p.home_acc >= -1e-6 and p.ret_acc >= -1e-6 and p.dep >= -1e-6 for p in people))


if __name__ == "__main__":
    unittest.main()
