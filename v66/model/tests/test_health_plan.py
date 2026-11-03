import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import health_plan as hp  # noqa: E402

BASE = {"stock0": 100.0, "base_intake": 10.0, "lead_time": 2, "exit_rate": 0.1, "expansion": 0.0,
        "ramp_years": 0, "intake_capacity_multiple": 10.0, "military_pool": 0.0, "military_volunteer_share": 0.0,
        "conversion_years": 1, "tau_per_10k": 1e4, "population": {0: 100.0},
        "preventable_share": {0: 0.0}}


class TestPlan(unittest.TestCase):
    def test_steady_state(self):
        rows, closed = hp.simulate(BASE, 10)   # graduates 10 = exits 10% of 100
        self.assertAlmostEqual(rows[-1]["stock"], 100.0)
        self.assertEqual(closed, 0)               # need = 100 = stock

    def test_gap_closes_with_expansion(self):
        p = dict(BASE, population={0: 150.0}, expansion=0.1, ramp_years=10)
        rows, closed = hp.simulate(p, 60)
        self.assertIsNotNone(closed)
        self.assertGreater(closed, p["lead_time"])

    def test_capacity_cap_binds(self):
        p = dict(BASE, population={0: 1000.0}, expansion=1.0, ramp_years=20, intake_capacity_multiple=2.0)
        rows, _ = hp.simulate(p, 80)
        self.assertLessEqual(rows[-1]["stock"], 2 * 10 / 0.1 + 1e-6)   # steady state at capped intake

    def test_prevention_reduces_need(self):
        p = dict(BASE, preventable_share={0: 0.0, 10: 0.2})
        rows, _ = hp.simulate(p, 12)
        self.assertAlmostEqual(rows[10]["need"], 80.0)

    def test_military_conversion_adds_graduates(self):
        p = dict(BASE, population={0: 200.0}, military_pool=50.0, military_volunteer_share=1.0, conversion_years=5)
        with_mil = hp.simulate(p, 20)[0][-1]["stock"]
        without = hp.simulate(dict(p, military_pool=0.0), 20)[0][-1]["stock"]
        self.assertGreater(with_mil, without)

    def test_interp(self):
        self.assertAlmostEqual(hp.interp({0: 0, 10: 1}, 5), 0.5)
        self.assertEqual(hp.interp({0: 0, 10: 1}, 20), 1)


if __name__ == "__main__":
    unittest.main()


class TestWorldPlan(unittest.TestCase):
    def test_lever_ordering_central(self):
        import run_health
        stock0, wld, prev = run_health.world_inputs()
        sc = run_health.scenarios(stock0, wld, prev)
        yrs = {k: hp.simulate(p, 80)[1] for k, p in sc.items() if k.startswith("central|")}
        self.assertIsNone(yrs["central|1_status_quo_training"])
        self.assertLessEqual(yrs["central|5_ambitious_10pct_50pct_prevention_high"],
                             yrs["central|4_plus_prevention_central"])
        self.assertLessEqual(yrs["central|4_plus_prevention_central"], yrs["central|2_expand_training_7pct_15y"])
