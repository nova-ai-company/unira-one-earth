import unittest
from model import Params,run,SCENARIOS
class TestModel(unittest.TestCase):
 def test_twenty_periods(self):self.assertEqual(len(run(Params())),20)
 def test_inventory_nonnegative(self):self.assertTrue(all(x['closing_inventory']>=0 for x in run(Params())))
 def test_credit_deposit_identity(self):self.assertTrue(all(abs(x['deposits_U']-x['total_debt_U'])<.01 for x in run(Params())))
 def test_shock_produces_shortage(self):self.assertGreater(sum(x['shortage'] for x in run(SCENARIOS['food_supply_shock'])),0)
 def test_shortage_not_fixed_by_credit(self):
  a=run(Params(supply_shock_year=5,supply_shock_fraction=.9,borrowing_limit_U=0))
  b=run(Params(supply_shock_year=5,supply_shock_fraction=.9,borrowing_limit_U=1e12))
  self.assertEqual([x['shortage'] for x in a],[x['shortage'] for x in b])
 def test_no_overdelivery(self):self.assertTrue(all(x['delivered']<=x['households'] for x in run(Params())))
 def test_work_limit(self):self.assertTrue(all(x['hours_used']<=x['hours_available'] for x in run(SCENARIOS['labor_shock'])))
 def test_growth_pressure(self):self.assertGreater(sum(x['shortage'] for x in run(SCENARIOS['population_growth'])),sum(x['shortage'] for x in run(Params())))
 def test_credit_limit_flag(self):self.assertTrue(any(x['credit_limit_breached'] for x in run(SCENARIOS['restricted_credit'])))
 def test_bad_inputs(self):
  with self.assertRaises(ValueError):run(Params(hours_per_unit=0))
if __name__=='__main__':unittest.main()
