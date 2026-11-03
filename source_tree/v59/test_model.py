import unittest
from model import BASE,SECTORS,gross_requirements,simulate,run_all
class TestModel(unittest.TestCase):
 def test_sector_count(self):self.assertEqual(len(SECTORS),6)
 def test_io_gross_above_final(self):
  g=gross_requirements({s:100 for s in SECTORS});self.assertTrue(all(g[s]>=100 for s in SECTORS))
 def test_baseline_years(self):self.assertEqual(len(simulate()),20)
 def test_nonnegative_unmet(self):self.assertTrue(all(r['unmet_total_index']>=0 for r in simulate()))
 def test_no_replacement_worse(self):self.assertGreater(sum(r['unmet_total_index'] for r in simulate(replacement=False)),sum(r['unmet_total_index'] for r in simulate()))
 def test_labor_limit(self):self.assertTrue(all(r['hours_used']<=9000.01 for r in simulate(annual_labor_hours=9000)))
 def test_shock(self):self.assertGreater(simulate(shock_year=5,shock_fraction=.35)[4]['unmet_total_index'],simulate()[4]['unmet_total_index'])
 def test_budget_binding(self):self.assertTrue(all(r['investment_spent_U']<=4000 for r in simulate(annual_investment_budget=4000)))
 def test_growth(self):self.assertGreater(simulate(growth=.025)[-1]['demand_total_index'],simulate()[ -1]['demand_total_index'])
 def test_all_cases(self):self.assertEqual(len(run_all()),6)
if __name__=='__main__':unittest.main()
