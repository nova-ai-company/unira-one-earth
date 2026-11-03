import unittest
from model import solve
class Tests(unittest.TestCase):
 def test_balanced(self):
  r=solve();self.assertEqual(sum(r['allocation'].values()),100)
 def test_capacities(self):
  r=solve();self.assertLessEqual(r['allocation']['repair_adapt'],20)
 def test_budget(self):
  r=solve(budget=8_000_000);self.assertLessEqual(r['cost_eur'],8_000_000)
 def test_shortfall_visible(self):
  r=solve(demand=200,budget=100000);self.assertGreater(r['unmet'],0)
 def test_stock_first(self):
  a=solve();b=solve(stock_first=True);self.assertLessEqual(b['new_homes'],a['new_homes'])
 def test_emissions_nonnegative(self):
  self.assertGreaterEqual(solve()['carbon_t_co2e'],0)
if __name__=='__main__':unittest.main()
