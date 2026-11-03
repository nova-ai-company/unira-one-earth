import unittest
from model import load,optimize
class ModelTests(unittest.TestCase):
 def setUp(self):self.a=load()
 def test_exact_demand(self):self.assertEqual(optimize(self.a)['units'],100)
 def test_stock_first(self):self.assertLessEqual(optimize(self.a,stock_first=True)['new_build'],optimize(self.a,carbon_price=10000)['new_build'])
 def test_no_unconsented(self):
  a=self.a+[dict(self.a[0],id='BAD',cost_eur='0',capacity='100',consent='no')]
  self.assertNotIn('BAD',optimize(a)['allocation'])
 def test_infeasible(self):self.assertEqual(optimize(self.a,demand={'small':10000})['status'],'infeasible')
 def test_budget(self):self.assertEqual(optimize(self.a,budget=1)['status'],'infeasible')
 def test_operational_sensitivity(self):self.assertNotEqual(optimize(self.a,carbon_price=1000,carbon_scale=.5)['carbon_30y_t'],optimize(self.a,carbon_price=1000,carbon_scale=1.5)['carbon_30y_t'])
 def test_exact_lexicographic(self):
  x=optimize(self.a,stock_first=True,carbon_price=0);y=optimize(self.a,stock_first=True,carbon_price=10000)
  self.assertEqual(x['new_build'],y['new_build'])
if __name__=='__main__':unittest.main()
