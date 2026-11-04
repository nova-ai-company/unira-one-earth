import json
import random
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import model  # noqa: E402


class TestConflict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = model.main(runs=3, write=False, sens=False)
        cls.s = cls.out["scenarios"]

    def test_reproducible(self):
        again = model.main(runs=3, write=False, sens=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_observed_gradient_poorest_fight_most(self):
        q = self.out["observed_conflict_rate_today_by_living_standard_quartile"]
        self.assertGreater(q[0], q[3])
        self.assertGreater(self.out["fitted_beta"], 0)

    def test_scenarios_ordered_by_conflict_burden(self):
        cy = [self.s[n]["conflict_country_years_80y"] for n in model.SCEN]
        self.assertEqual(cy, sorted(cy, reverse=True))

    def test_scenario_A_keeps_todays_number_of_conflicts(self):
        c = self.s["A_no_reduction"]["countries_in_conflict"]
        today = self.out["countries_in_conflict_today"]
        self.assertLess(abs(sum(c[f"year_{t}"] for t in (20, 40, 60, 80)) / 4 - today), 0.35 * today)

    def test_only_D_has_hypothetical_diplomacy(self):
        self.assertEqual([n for n, p in model.SCEN.items() if p["diplomacy"]], ["D_long_term_peace"])

    def test_no_reduction_means_risk_ignores_living_standards(self):
        ls0 = {"X": [0.2] * (model.YEARS + 1), "Y": [0.9] * (model.YEARS + 1)}
        better = {"X": [0.9] * (model.YEARS + 1), "Y": [0.9] * (model.YEARS + 1)}
        a = model.Risk(model.SCEN["A_no_reduction"] | {"beta": 4.0}, 0.01, ls0)
        self.assertEqual(a.onset("X", ls0, 10, False, False), a.onset("X", better, 10, False, False))
        c = model.Risk(model.SCEN["C_strong"] | {"beta": 4.0}, 0.01, ls0)
        self.assertLess(c.onset("X", better, 10, False, False), c.onset("X", ls0, 10, False, False))
        self.assertGreater(c.onset("X", ls0, 10, False, False), c.onset("Y", ls0, 10, False, False))
        # backlash only in exposed countries and programme years 1-3; relapse risk raised
        self.assertGreater(c.onset("X", ls0, 2, False, True), c.onset("X", ls0, 2, False, False))
        self.assertEqual(c.onset("X", ls0, 5, False, True), c.onset("X", ls0, 5, False, False))
        self.assertGreater(c.onset("X", ls0, 5, True, False), c.onset("X", ls0, 5, False, False))

    def test_dates_not_earlier_than_if_all_conflicts_ended_now(self):
        ref = self.out["v89_reference"]["accelerated_if_all_conflicts_end_now"]
        for s in self.s.values():
            for L in ("L1", "L2"):
                m = s[f"{L}_dates"]["90pct"]["median"]
                self.assertTrue(m is None or m >= ref[L]["90pct"] - 2)

    def test_coverage_valid(self):
        for s in self.s.values():
            for t, v in s["L2_mean_coverage"].items():
                self.assertTrue(0 <= v <= s["L1_mean_coverage"][t] + 1e-9 <= 1 + 1e-9)


if __name__ == "__main__":
    unittest.main()
