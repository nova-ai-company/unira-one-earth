import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import materials as mt  # noqa: E402


class TestMaterials(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = mt.main(write=False)
        cls.M = cls.out["mixes"]

    def test_reproducible(self):
        again = mt.main(write=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_shares_sum_to_one_and_inventory_is_weighted(self):
        for name, shares in mt.MIXES.items():
            self.assertAlmostEqual(sum(shares.values()), 1.0, places=9, msg=name)
        inv = mt.mix_inventory({"rc_conventional": 0.5, "earth_vault": 0.5})
        self.assertAlmostEqual(inv["cement_kg"], 0.5 * mt.CONV_CEMENT + 0.5 * 8.0)

    def test_conventional_cement_is_about_a_quarter_of_world_output(self):
        c = self.M["all_rc_conventional"]
        self.assertGreater(c["cement_share_of_world"], 0.18)
        self.assertLess(c["cement_share_of_world"], 0.30)
        self.assertAlmostEqual(c["steel_share_of_world"], 0.10, delta=0.02)

    def test_lc3_saves_little_at_building_level(self):
        a, b = self.M["all_rc_conventional"], self.M["all_rc_lc3"]
        self.assertLess(b["co2_gt_30y"], a["co2_gt_30y"])
        self.assertGreater(b["co2_gt_30y"], 0.85 * a["co2_gt_30y"])
        self.assertEqual(a["cement_mt_per_yr"], b["cement_mt_per_yr"])

    def test_regional_mix_cuts_cement_steel_and_co2(self):
        a, r = self.M["all_rc_conventional"], self.M["regional_mix"]
        self.assertLess(r["cement_mt_per_yr"], 0.45 * a["cement_mt_per_yr"])
        self.assertLess(r["steel_mt_per_yr"], 0.40 * a["steel_mt_per_yr"])  # about 36%
        self.assertLess(r["co2_gt_30y"], 0.45 * a["co2_gt_30y"])
        self.assertAlmostEqual(r["peak_workers_m"], a["peak_workers_m"], delta=0.15 * a["peak_workers_m"])  # about the same hours

    def test_single_bio_materials_hit_resource_limits(self):
        t, b = self.M["all_timber_frame"], self.M["all_bamboo"]
        self.assertGreater(t["wood_share_of_industrial_roundwood"], 0.5)
        self.assertGreater(b["bamboo_mha_needed_vs_existing_area"], 0.4)
        self.assertGreater(b["bamboo_mha_needed"]["low"], 0.8 * mt.WORLD["bamboo_area_mha"]["value"])
        r = self.M["regional_mix"]
        self.assertLess(r["wood_share_of_industrial_roundwood"], t["wood_share_of_industrial_roundwood"])
        self.assertLess(r["wood_share_of_industrial_roundwood"], 0.5)
        self.assertLess(r["bamboo_mha_needed_vs_existing_area"], 0.5)

    def test_latitude_shares_ordered(self):
        s = self.out["deficit_population_by_latitude"]
        self.assertLessEqual(s["within_tropics_23_5"], s["within_30_degrees"])
        self.assertGreater(s["within_30_degrees"], 0.5)


if __name__ == "__main__":
    unittest.main()
