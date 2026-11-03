import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sufficiency as s  # noqa: E402

ROWS = [{"region": "A", "population": 100, "supply_pc": 3000},
        {"region": "B", "population": 300, "supply_pc": 2000},
        {"region": "C", "population": 100, "supply_pc": None}]


class TestSufficiency(unittest.TestCase):
    def test_known_answer(self):
        r = s.domain_summary(ROWS, 2200)
        self.assertEqual(r["population_covered"], 400)
        self.assertAlmostEqual(r["world_supply"], 900000)
        self.assertAlmostEqual(r["sufficiency_ratio"], 900000 / 880000)
        self.assertEqual(r["people_below_threshold"], 300)
        self.assertAlmostEqual(r["shortfall_volume"], 60000)
        self.assertAlmostEqual(r["surplus_volume"], 80000)
        self.assertTrue(r["needs_first_feasible"])
        self.assertAlmostEqual(r["equal_share_per_person"], 2250)
        self.assertAlmostEqual(r["volume_moved_equal_share"], 75000)

    def test_moved_is_symmetric(self):
        r = s.domain_summary(ROWS, 2200)
        a = r["equal_share_per_person"]
        recv = sum(max(0, a - x["supply_pc"]) * x["population"] for x in ROWS if x["supply_pc"] is not None)
        self.assertAlmostEqual(recv, r["volume_moved_equal_share"])

    def test_infeasible(self):
        r = s.domain_summary(ROWS, 3000)
        self.assertFalse(r["needs_first_feasible"])

    def test_region_change(self):
        c = s.region_change(ROWS, "A", 2200)
        self.assertAlmostEqual(c["change_pct"], 100 * (2250 / 3000 - 1))
        self.assertIsNone(s.region_change(ROWS, "C"))

    def test_years(self):
        self.assertEqual(s.years_to_close_nontradable(0, 5), 0.0)
        self.assertEqual(s.years_to_close_nontradable(10, 0), float("inf"))
        self.assertAlmostEqual(s.years_to_close_nontradable(10, 4), 2.5)


if __name__ == "__main__":
    unittest.main()


class TestWorldRun(unittest.TestCase):
    def test_world_outputs(self):
        import json
        import subprocess
        root = Path(__file__).resolve().parents[1]
        subprocess.run([sys.executable, "run.py"], cwd=root, check=True, capture_output=True)
        out = json.loads((root.parent / "outputs" / "world_sufficiency.json").read_text())
        d = out["domains"]
        # population covered close to World Bank world total (8.14 bn) for food and energy
        for k in ("food|decent|consumer_waste_status_quo", "energy|decent"):
            self.assertGreater(d[k]["population_covered"], 7.9e9)
        # equal-share kcal equals population-weighted world mean reported by the data build (~3,017)
        self.assertAlmostEqual(d["food|decent|consumer_waste_status_quo"]["equal_share_per_person"], 3017, delta=15)
        self.assertGreater(d["labour"]["hours_coverage_share_of_employment"], 0.6)
