import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model  # noqa: E402


class TestAutomation(unittest.TestCase):
    def test_hours_fall_and_guaranteed_income_rises(self):
        rows = model.run(40, 0.9)
        self.assertLess(rows[100]["weekly_hours"], rows[0]["weekly_hours"])
        self.assertGreater(rows[100]["guaranteed_share_of_income"], rows[0]["guaranteed_share_of_income"])

    def test_income_shares_add_up(self):
        for r in model.run(25, 0.9):
            self.assertAlmostEqual(r["guaranteed_share_of_income"] + r["work_pay_share_of_income"], 1.0)

    def test_human_work_never_vanishes(self):
        self.assertLessEqual(max(model.automation(t, 25, 0.95) for t in range(200)), 1 - model.HUMAN_ONLY + 1e-9)


if __name__ == "__main__":
    unittest.main()
