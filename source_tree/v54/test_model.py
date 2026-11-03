import unittest
from model import evaluate,SCENARIOS
class TestModel(unittest.TestCase):
 def test_all_demand_met(self):
  for s in SCENARIOS:self.assertEqual(evaluate(s)['unmet_homes'],0)
 def test_unmet_detected(self):
  s={**SCENARIOS[0], 'housing_need':101};self.assertEqual(evaluate(s)['unmet_homes'],1)
 def test_excess_detected(self):
  s={**SCENARIOS[0], 'housing_need':99};self.assertEqual(evaluate(s)['excess_homes'],1)
 def test_labour_constraint(self):
  s={**SCENARIOS[0], 'available_workers':1};self.assertFalse(evaluate(s)['feasible'])
 def test_material_shortage(self):
  s={**SCENARIOS[0], 'resource_limits':{**SCENARIOS[0]['resource_limits'],'cement_t':0}};self.assertGreater(evaluate(s)['shortages']['cement_t'],0)
 def test_nominal_pay_no_effect_on_resources(self):
  s={**SCENARIOS[0], 'monthly_base_salary_u':25000};self.assertEqual(evaluate(s)['cement_t'],evaluate(SCENARIOS[0])['cement_t'])
 def test_shorter_hours_restrict_capacity(self):
  self.assertLess(evaluate(SCENARIOS[2])['labour_capacity_hours'],evaluate(SCENARIOS[0])['labour_capacity_hours'])
if __name__=='__main__':unittest.main()
