import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import level2  # noqa: E402


class TestLiving(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads((HERE.parent / "outputs" / "livingstandard.json").read_text())["scenarios"]

    def test_faster_scenarios_are_not_slower(self):
        c, m, a = (self.r[s]["essential_99pct"][0] for s in ("conservative", "moderate", "accelerated"))
        self.assertGreaterEqual(c, m)
        self.assertGreaterEqual(m, a)

    def test_energy_within_today(self):
        for s in self.r.values():
            self.assertEqual(s["environment"]["energy_check"], "pass")

    def test_automation_reduces_hours(self):
        for s in self.r.values():
            self.assertLessEqual(s["labour"]["year_60"]["hours_per_worker_week"], s["labour"]["year_0"]["hours_per_worker_week"])

    def test_car_energy_independent_of_ownership(self):
        self.assertAlmostEqual(level2.cars(1.0)["energy_gj_per_person"], level2.cars(1 / 3)["energy_gj_per_person"])


if __name__ == "__main__":
    unittest.main()
