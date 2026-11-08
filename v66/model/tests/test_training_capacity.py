import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import health_plan as hp  # noqa: E402
import run_health as rh  # noqa: E402
import training_capacity as tc  # noqa: E402


class TestTrainingCapacity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = tc.main(write=False)
        cls.D = cls.out["designs"]

    def test_reproducible(self):
        again = tc.main(write=False)
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(self.out, sort_keys=True))

    def test_published_design_equals_published_plan(self):
        pub = json.loads((HERE.parent / "outputs" / "health_plan.json").read_text())["results"]
        for cap in ("low", "central", "high"):
            self.assertEqual(self.D["published"]["years"][cap], pub[f"{cap}|{tc.BASE}"]["years_to_close"])

    def test_scaling_cap_off_changes_nothing(self):
        stock0, wld, prev = rh.world_inputs()
        sc = rh.scenarios(stock0, wld, prev)
        p = sc[f"central|{tc.BASE}"]
        a = hp.simulate(p, 60)
        b = hp.simulate(dict(p, capacity_scales_with_stock=False), 60)
        self.assertEqual(a, b)

    def test_educators_bind_when_only_facilities_rotate(self):
        for lvl in ("low", "central", "high"):
            cap, binding, comps = tc.effective_cap(lvl)
            self.assertEqual(binding, "educators")
            self.assertGreater(cap, tc.PUBLISHED_CAP)
            self.assertEqual(min(comps.values()), cap)

    def test_each_design_never_delays(self):
        base = self.D["published"]["years"]
        keys = [k for k, _, _ in tc.DESIGNS]
        for a, b in zip(keys, keys[1:]):  # designs are cumulative
            for cap in ("low", "central", "high"):
                self.assertLessEqual(self.D[b]["years"][cap], self.D[a]["years"][cap], (a, b, cap))
        for cap in ("low", "central", "high"):
            self.assertLessEqual(self.D["rotation_every_hospital_exp15_retention2"]["years"][cap], base[cap])

    def test_every_hospital_teaches_beats_same_educators(self):
        s = self.out["sensitivity_central_intake"]
        for lvl in ("low", "central", "high"):
            self.assertLessEqual(s[f"multipliers_{lvl}|every_hospital_teaches"], s[f"multipliers_{lvl}|same_educators"])


if __name__ == "__main__":
    unittest.main()
