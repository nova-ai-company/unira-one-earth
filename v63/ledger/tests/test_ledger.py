import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import ledger  # noqa: E402


class TestLedger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = ledger.load_inputs()
        cls.rows = [ledger.ledger(reg, n, c, cls.inputs) for reg in ("FR", "EU27_2020") for n, c in ledger.CASES.items()]

    def test_accounting_identity(self):
        for r in self.rows:
            parts = r["covered_by_theta_ths"] + r["covered_by_mobilisation_ths"] + r["covered_by_avoidable_output_ths"]
            if not r["gap_fully_covered"]:
                self.assertAlmostEqual(parts + r["uncovered_hours_ths"], r["hours_gap_ths"], places=3)
            else:
                self.assertEqual(r["uncovered_hours_ths"], 0.0)

    def test_cases_monotone(self):
        for reg in ("FR", "EU27_2020"):
            u = [next(r for r in self.rows if r["region"] == reg and r["case"] == c)["uncovered_share_of_all_hours"]
                 for c in ("low", "central", "optimistic", "maximal")]
            self.assertEqual(u, sorted(u, reverse=True))

    def test_universal_work_monotone(self):
        for reg in ("FR", "EU27_2020"):
            u = [next(r for r in self.rows if r["region"] == reg and r["case"] == c)["uncovered_share_of_all_hours"]
                 for c in ("universal_84", "universal_88", "universal_92")]
            self.assertEqual(u, sorted(u, reverse=True))

    def test_takeup_increments_valid(self):
        for v in ("best_practice_gap", "best_practice_full", "job_guarantee"):
            for rate in ledger.mobilisation_rates(self.inputs["flows"], "FR", v):
                self.assertGreaterEqual(rate, 0.0)
                self.assertLessEqual(rate, 1.0)

    def test_fr_gap_matches_v62(self):
        fr = next(r for r in self.rows if r["region"] == "FR" and r["case"] == "central")
        self.assertAlmostEqual(fr["hours_before_ths"] / fr["hours_gap_ths"], 1 / (1 - 1 / 1.201), delta=0.05)


if __name__ == "__main__":
    unittest.main()
