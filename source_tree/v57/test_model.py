import unittest
from model import Model,simulate
class TestModel(unittest.TestCase):
 def test_balances(self): self.assertTrue(simulate()['audited'])
 def test_loans_create_deposits(self):
  m=Model();m.lend('firms',100);self.assertEqual(m.deposits['firms'],100);self.assertEqual(m.loans['firms'],100)
 def test_repayment(self):
  m=Model();m.lend('firms',100);m.repay('firms',40);self.assertEqual(m.loans['firms'],60)
 def test_overdraft(self): self.assertRaises(ValueError,Model().transfer,'firms','households',1,'bad')
 def test_inventory(self): self.assertEqual(simulate()['physical']['inventory_left_units'],10)
 def test_food_shortage(self): self.assertEqual(simulate(food_supply=70)['physical']['food_unmet'],30)
 def test_labour_shortage(self): self.assertGreater(simulate(hours_available=9000)['physical']['food_unmet'],0)
 def test_public_gap(self): self.assertGreater(simulate(public_services_U=450000,government_credit_U=0)['finance']['government_unpaid_U'],0)
 def test_credit_not_food(self): self.assertEqual(simulate(food_supply=70,government_credit_U=500000)['physical']['food_unmet'],30)
 def test_depreciation(self): self.assertEqual(simulate()['finance']['capital_book_value_U'],45000)
 def test_bank_identity(self):
  b=simulate()['finance']['balance_sheets']['bank'];self.assertEqual(b['assets_U'],b['liabilities_U']+b['equity_U'])
 def test_authority_identity(self):
  b=simulate()['finance']['balance_sheets']['monetary_authority'];self.assertEqual(b['assets_U'],b['liabilities_U'])
 def test_reject_overproduction(self):
  m=Model();self.assertRaises(ValueError,m.produce,100,1000,500,100)
if __name__=='__main__': unittest.main()
