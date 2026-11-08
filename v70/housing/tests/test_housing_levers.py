import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run_levers as lv  # noqa: E402


class TestHousingLevers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = lv.main(write=False)
        cls.L = cls.out["levers"]

    def test_reproducible(self):
        again = lv.main(write=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_base_equals_published_case(self):
        pub = json.loads((ROOT.parent / "outputs" / "housing.json").read_text())["cases"][lv.BASE_CASE]
        b = self.L["base"]
        self.assertEqual(b["housing_all_by"], pub["housing_all_by"])
        self.assertAlmostEqual(b["peak_construction_workers_m"], pub["peak_construction_workers_m"], places=1)
        self.assertAlmostEqual(b["housing_closed_y30"], pub["housing_closed_y30"], places=4)

    def test_factory_building_cuts_workers_not_dates(self):
        b, f20, f35 = self.L["base"], self.L["factory_20"], self.L["factory_35"]
        self.assertEqual(b["housing_all_by"], f20["housing_all_by"])
        self.assertAlmostEqual(f20["peak_construction_workers_m"], b["peak_construction_workers_m"] * 0.8, places=1)
        self.assertLess(f35["peak_construction_workers_m"], f20["peak_construction_workers_m"])

    def test_self_build_cuts_professional_workers_only(self):
        b, s50, s65 = self.L["base"], self.L["self_build_50"], self.L["self_build_65"]
        self.assertEqual(s50["peak_construction_workers_m"], b["peak_construction_workers_m"])
        self.assertLess(s50["peak_professional_workers_m"], b["peak_professional_workers_m"])
        self.assertLess(s65["peak_professional_workers_m"], s50["peak_professional_workers_m"])
        self.assertGreater(s50["household_hours_bn_30y"], 0)
        self.assertEqual(b["household_hours_bn_30y"], 0)

    def test_increment_share_between_zero_and_one(self):
        s = self.out["increment_above_decent_share_of_need"]
        self.assertGreater(s, 0.3)
        self.assertLess(s, 1.0)

    def test_decent_core_is_reached_no_later_than_comfortable(self):
        d, b = self.L["decent_core_first"], self.L["base"]
        self.assertIsNotNone(d["housing_all_by"])
        if b["housing_all_by"] is not None:
            self.assertLessEqual(d["housing_all_by"], b["housing_all_by"])
        self.assertGreaterEqual(d["housing_closed_y15"], b["housing_closed_y15"])

    def test_faster_growth_never_later(self):
        b, g15, g15r = self.L["base"], self.L["growth_15"], self.L["growth_15_record_1_5x"]
        self.assertGreaterEqual(g15["housing_closed_y15"], b["housing_closed_y15"])
        self.assertGreaterEqual(g15r["housing_closed_y15"], g15["housing_closed_y15"])
        if b["housing_all_by"] is not None and g15["housing_all_by"] is not None:
            self.assertLessEqual(g15["housing_all_by"], b["housing_all_by"])

    def test_all_levers_best_on_workers(self):
        a = self.L["all"]
        for k, r in self.L.items():
            if k == "decent_core_first":
                continue
            self.assertLessEqual(a["peak_professional_workers_m"] / max(a["peak_bn_m2_per_yr"], 1e-9),
                                 r["peak_professional_workers_m"] / max(r["peak_bn_m2_per_yr"], 1e-9) + 1e-9, k)


if __name__ == "__main__":
    unittest.main()
