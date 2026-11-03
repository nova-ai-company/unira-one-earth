import unittest
from model import Household, child_allowance, income, scenarios, evaluate
class Tests(unittest.TestCase):
 def test_child_allowance(self): self.assertEqual(child_allowance(Household((5000,5000),3)),3000)
 def test_child_cap(self): self.assertEqual(child_allowance(Household((9000,5000),3)),1000)
 def test_adult_earnings_not_capped(self): self.assertEqual(income(Household((25000,5000),3)),30000)
 def test_disability_counts_as_income(self): self.assertEqual(child_allowance(Household((5000,5000),6)),5000)
 def test_no_children(self): self.assertEqual(child_allowance(Household((5000,),0)),0)
 def test_negative_rejected(self):
  with self.assertRaises(ValueError):child_allowance(Household((-1,),1))
 def test_shock_shortage(self): self.assertGreater(evaluate(scenarios()[1])['goods']['food']['physical_gap_units'],0)
 def test_housing_shortage(self): self.assertGreater(evaluate(scenarios()[3])['goods']['housing_services']['physical_gap_units'],0)
 def test_fund_gap(self): self.assertGreater(evaluate(scenarios()[4])['public_fund_shortfall_u'],0)
 def test_hours_reduced(self): self.assertLess(evaluate(scenarios()[2])['total_labour_hours'],evaluate(scenarios()[0])['total_labour_hours'])
 def test_annual_base_payroll(self): self.assertEqual(evaluate(scenarios()[0])['worker_base_payroll_u'],7200000)
if __name__=='__main__':unittest.main()
