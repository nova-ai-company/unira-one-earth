import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from unira_circuit import lifecycle  # noqa: E402
import run_lifecycle  # noqa: E402


def small(cfg, cap=True, variant=None, g=0.0):
    c = run_lifecycle.sim_config(cfg, g, cap, variant)
    c["sample_size"], c["years"] = 800, 25
    return c


class TestLifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = json.loads((ROOT / "config" / "circuit_config.json").read_text())

    def test_deterministic_with_seed(self):
        a = lifecycle.simulate(small(self.cfg), seed=7)
        b = lifecycle.simulate(small(self.cfg), seed=7)
        self.assertEqual(a, b)

    def test_cap_bounds_deposits_vs_no_cap(self):
        with_cap = lifecycle.simulate(small(self.cfg, True, "cap_low_credit"), 3)
        no_cap = lifecycle.simulate(small(self.cfg, False), 3)
        self.assertLess(with_cap[-1]["deposits_months_of_consumption"], no_cap[-1]["deposits_months_of_consumption"])
        self.assertGreater(no_cap[-1]["deposits"], no_cap[5]["deposits"])

    def test_no_deposit_exceeds_cap_after_cap_step(self):
        r = lifecycle.simulate(small(self.cfg, True, "cap_low_credit"), 5)
        for row in r:
            self.assertLessEqual(row["deposits"], row["cap_u"] * 800 + 1e-6)

    def test_automation_reduces_hours_never_increases(self):
        r = lifecycle.simulate(small(self.cfg, True, None, 0.02), 1)
        self.assertLess(r[-1]["weekly_hours"], 30.0)
        self.assertTrue(all(x["weekly_hours"] <= 30.0 for x in r))

    def test_max_two_homes_in_simulated_population(self):
        for variant in (None, "cap_low_credit"):
            _, people = lifecycle.simulate(small(self.cfg, True, variant), 4, return_people=True)
            self.assertLessEqual(max(p.homes for p in people), 2)
            self.assertGreater(sum(p.homes for p in people), 0)


if __name__ == "__main__":
    unittest.main()
