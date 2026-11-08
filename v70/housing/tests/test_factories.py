import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import factories as fc  # noqa: E402


class TestFactories(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = fc.main(write=False)

    def test_reproducible(self):
        again = fc.main(write=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_peak_demand_matches_published_housing_case(self):
        pub = json.loads((ROOT.parent / "outputs" / "housing.json").read_text())["cases"][fc.BASE_CASE]
        self.assertAlmostEqual(self.out["peak_world_demand_bn_m2_per_yr"], pub["peak_bn_m2_per_yr"], places=2)

    def test_plants_ordered_and_consistent(self):
        p = self.out["plants_needed_world"]
        self.assertGreater(p["low"], p["central"])
        self.assertGreater(p["central"], p["high"])
        pub = json.loads((ROOT.parent / "outputs" / "housing.json").read_text())["cases"][fc.BASE_CASE]
        self.assertAlmostEqual(p["central"], pub["peak_bn_m2_per_yr"] * 1e9 / (1200 * 80), delta=1)

    def test_distance_shares_sum_to_one(self):
        for key, shares in self.out["share_of_deficit_population_by_distance_to_nearest_supplier"].items():
            self.assertAlmostEqual(sum(shares.values()), 1.0, places=3, msg=key)
        s, a = (self.out["share_of_deficit_population_by_distance_to_nearest_supplier"][k] for k in ("surplus_industrial", "any_industrial"))
        # a larger pool of possible suppliers can only bring more people within reach
        self.assertGreaterEqual(a["within_module_radius"] + a["within_panel_radius"], s["within_module_radius"] + s["within_panel_radius"])

    def test_homes_must_be_made_where_needed(self):
        s = self.out["share_of_deficit_population_by_distance_to_nearest_supplier"]["surplus_industrial"]
        self.assertGreater(s["beyond"], 0.5)
        self.assertLess(s["within_module_radius"], 0.2)

    def test_materials_are_a_fraction_of_world_output(self):
        sh = self.out["materials_share_of_world_production"]
        for m, x in sh.items():
            self.assertGreater(x, 0.02, m)
            self.assertLess(x, 0.3, m)

    def test_factory_benchmark_needs_fewer_workers(self):
        w = self.out["workforce_at_peak_m"]
        self.assertLess(w["factory_value_chain_13_h_per_m2"], w["site_built_48_h_per_m2"] / 3)

    def test_regions_table_sorted_by_need(self):
        shares = [r["need_share"] for r in self.out["regions"]]
        self.assertEqual(shares, sorted(shares, reverse=True))
        self.assertTrue(all(r["nearest_surplus_industrial_km"] >= 0 for r in self.out["regions"]))


if __name__ == "__main__":
    unittest.main()
