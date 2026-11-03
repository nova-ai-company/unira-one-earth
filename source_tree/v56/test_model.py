import unittest
from model import Economy,simulate
class Tests(unittest.TestCase):
 def test_issue_conserves(self):
  e=Economy();e.issue('firms',100,'start');self.assertEqual(sum(e.deposits.values()),100)
 def test_transfer_conserves(self):
  e=Economy();e.issue('firms',100,'start');e.transfer('firms','households',60,'wages');self.assertEqual(sum(e.deposits.values()),100)
 def test_overdraft_rejected(self):
  e=Economy();self.assertRaises(ValueError,e.transfer,'firms','households',1,'invalid')
 def test_negative_rejected(self):
  e=Economy();self.assertRaises(AssertionError,e.issue,'firms',-1,'invalid')
 def test_baseline_balanced(self):self.assertTrue(simulate()['ledger_balances'])
 def test_public_gap(self):self.assertGreater(simulate()['public_unpaid_U'],0)
 def test_funded_public(self):self.assertEqual(simulate(public_cost=150_000)['public_unpaid_U'],0)
 def test_food_shortage(self):self.assertEqual(simulate(food_supply=70)['food_unmet_units'],30)
 def test_labour_shortage(self):self.assertEqual(simulate(work_hours=1000)['labour_shortfall_hours'],2000)
 def test_more_money_not_food(self):self.assertEqual(simulate(initial_issue=1500000,food_supply=70)['food_unmet_units'],30)
 def test_sector_flows_equal_deposits(self):
  r=simulate();self.assertEqual(sum(r['sector_net_flows_U'].values()),r['total_issued_U'])
 def test_no_implicit_money(self):
  r=simulate();self.assertEqual(sum(r['closing_deposits_U'].values()),r['total_issued_U'])
if __name__=='__main__':unittest.main()
