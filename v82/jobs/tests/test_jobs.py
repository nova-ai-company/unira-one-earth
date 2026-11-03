import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import simulate  # noqa: E402


class TestJobs(unittest.TestCase):
    def test_deterministic_and_within_5x(self):
        a = simulate.run("both", 1.2, 1, n=3000)
        self.assertEqual(a, simulate.run("both", 1.2, 1, n=3000))
        self.assertLessEqual(a["mean_multiplier"], 5.0)

    def test_levers_reduce_unwilling_hard_work(self):
        base = simulate.run("knowledge_only", 1.2, 1, n=4000)["unwilling_hard_jobs"]
        pay = simulate.run("hardship_pay", 1.2, 1, n=4000)["unwilling_hard_jobs"]
        allx = simulate.run("both_better_conditions", 1.2, 1, n=4000)["unwilling_hard_jobs"]
        self.assertLess(pay, base)
        self.assertLess(allx, pay)

    def test_shorter_hours_cost_hours(self):
        self.assertLess(simulate.run("shorter_hours", 1.2, 1, n=3000)["hours_needed_covered"], 1.0)


if __name__ == "__main__":
    unittest.main()
