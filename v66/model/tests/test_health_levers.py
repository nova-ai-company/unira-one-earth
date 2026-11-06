import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import run_health_levers as lv  # noqa: E402


class TestHealthLevers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = lv.main(write=False)
        cls.L = cls.out["levers"]

    def test_reproducible(self):
        again = lv.main(write=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_baseline_equals_published_ambitious_scenario(self):
        pub = json.loads((HERE.parent / "outputs" / "health_plan.json").read_text())["results"]
        for cap in ("low", "central", "high"):
            self.assertEqual(self.L["ambitious"]["years"][cap], pub[f"{cap}|{lv.BASE}"]["years_to_close"])

    def test_each_lever_never_delays(self):
        base = self.L["ambitious"]["years"]
        for key, r in self.L.items():
            for cap in ("low", "central", "high"):
                if base[cap] is None:
                    continue
                self.assertIsNotNone(r["years"][cap], key)
                self.assertLessEqual(r["years"][cap], base[cap], key)

    def test_lower_target_is_faster(self):
        c = {k: self.L[k]["years"]["central"] for k in ("ambitious", "target_100", "target_80", "target_decent")}
        self.assertGreaterEqual(c["ambitious"], c["target_100"])
        self.assertGreaterEqual(c["target_100"], c["target_80"])
        self.assertGreaterEqual(c["target_80"], c["target_decent"])
        self.assertEqual(c["target_decent"], 0)  # the world total is already above the WHO threshold

    def test_all_levers_at_least_as_fast_as_any_single_one(self):
        for cap in ("low", "central", "high"):
            singles = [self.L[k]["years"][cap] for k in ("retention_2pct", "courses_3y", "capacity_4x", "capacity_5x_exp15")]
            self.assertLessEqual(self.L["all"]["years"][cap], min(singles))

    def test_capacity_binds_more_than_course_length(self):
        # shorter courses barely help because the intake cap, not the pipeline, limits the stock
        base = self.L["ambitious"]["years"]["central"]
        self.assertGreaterEqual(self.L["courses_2y"]["years"]["central"], base - 3)
        self.assertLess(self.L["capacity_5x_exp15"]["years"]["central"], self.L["courses_2y"]["years"]["central"])


if __name__ == "__main__":
    unittest.main()
