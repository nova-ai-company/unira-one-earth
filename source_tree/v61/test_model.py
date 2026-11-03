import unittest
from model import evaluate
class TestLabourModel(unittest.TestCase):
    def test_equal_hours(self): self.assertAlmostEqual(evaluate(1380)['required_productivity_increase_pct'],0)
    def test_1656(self): self.assertAlmostEqual(evaluate(1656)['required_productivity_increase_pct'],20)
    def test_lower_hours(self): self.assertLess(evaluate(1200)['required_productivity_increase_pct'],0)
    def test_invalid(self):
        with self.assertRaises(ValueError): evaluate(0)
    def test_workers(self): self.assertAlmostEqual(evaluate(1656,workers=100)['additional_workers_at_unchanged_productivity'],20)
if __name__=='__main__': unittest.main()
