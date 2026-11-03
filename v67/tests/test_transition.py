import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import transition as tr  # noqa: E402


class TestAllocate(unittest.TestCase):
    def test_proportional_and_capped(self):
        g = tr.allocate(10, {"a": 4, "b": 12, "c": 0})
        self.assertAlmostEqual(g["a"] + g["b"], 10)
        self.assertLessEqual(g["a"], 4 + 1e-9)
        self.assertEqual(g["c"], 0)

    def test_pool_larger_than_need(self):
        g = tr.allocate(100, {"a": 4, "b": 12})
        self.assertAlmostEqual(g["a"], 4)
        self.assertAlmostEqual(g["b"], 12)


class TestRun(unittest.TestCase):
    def regions(self):
        return {"RICH": {"pop0": 100, "pop50": 100, "energy_gj": 80, "health_10k": 150, "floor_m2": 45, "kcal": 3500},
                "POOR": {"pop0": 300, "pop50": 300, "energy_gj": 5, "health_10k": 10, "floor_m2": 8, "kcal": 2400}}

    def params(self, **kw):
        p = {"energy_target": 40, "health_target": 131, "floor_target": 27, "excess_decline": 0.02,
             "energy_new_ej_per_yr": 1e-6, "health_net_new": lambda t: 0.5, "floor_new_m2_per_yr": 500,
             "kcal_eaten": {"decent": 2100, "comfortable": 2470}, "waste_now": 0.19, "waste_unira": 0.095, "waste_years": 10}
        p.update(kw)
        return p

    def test_poor_region_converges(self):
        rows, reached = tr.run(self.regions(), self.params(), 30)
        self.assertIn("energy", reached["RICH"])
        self.assertIn("energy", reached["POOR"])          # 1000 GJ/yr new vs 10,500 GJ deficit -> ~11 yrs
        self.assertLess(reached["POOR"]["energy"], 30)

    def test_rich_never_below_target(self):
        rows, _ = tr.run(self.regions(), self.params(), 30)
        self.assertGreaterEqual(rows[-1]["energy_share_pop_at_target"], 0.25)

    def test_no_capacity_no_progress(self):
        _, reached = tr.run(self.regions(), self.params(energy_new_ej_per_yr=0, health_net_new=lambda t: 0,
                                                         floor_new_m2_per_yr=0), 10)
        self.assertNotIn("energy", reached["POOR"])
        self.assertNotIn("housing", reached["POOR"])


if __name__ == "__main__":
    unittest.main()
