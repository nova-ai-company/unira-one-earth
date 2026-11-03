import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run  # noqa: E402


class TestHousing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = run.params()
        cls.cmp = run.compare.load_config()
        cls.regions = run.compare.rt.load_regions()
        cls.cap = json.loads((ROOT.parents[1] / "v66" / "construction" / "capacity.json").read_text())
        cls.r = {n: run.run_case(c, cls.cfg, cls.regions, cls.cmp, cls.cap) for n, c in cls.cfg["cases"].items()}

    def test_faster_ramp_closes_more_by_year15(self):
        self.assertLessEqual(self.r["today_capacity"]["housing_closed_y15"], self.r["ramp_5pct"]["housing_closed_y15"])
        self.assertLessEqual(self.r["ramp_5pct"]["housing_closed_y15"], self.r["ramp_10pct"]["housing_closed_y15"])

    def test_delivered_not_above_need(self):
        # total delivered over 30 years cannot exceed the 30-year need (backlog + growth) by much
        need_bn = sum(max(0.0, 27 - v["floor_m2"]) * v["pop0"] + 27 * max(0.0, v["pop50"] - v["pop0"])
                      for v in self.regions.values()) / 1e9
        r = self.r["ramp_10pct"]
        self.assertLessEqual(r["new_bn_m2_30y"] + r["upgraded_bn_m2_30y"], need_bn * 1.05)

    def test_low_carbon_cuts_co2(self):
        self.assertLess(self.r["ramp_10pct_stock_first_low_carbon"]["embodied_co2_gt_30y"],
                        self.r["ramp_10pct_stock_first"]["embodied_co2_gt_30y"])

    def test_capacity_never_above_max_rate(self):
        for r in self.r.values():
            pop_need = sum(v["pop50"] for v in self.regions.values())
            self.assertLessEqual(r["peak_bn_m2_per_yr"] * 1e9, 1.5 * pop_need * 1.1)


if __name__ == "__main__":
    unittest.main()
