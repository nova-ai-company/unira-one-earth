import unittest
from model import load,solve
class TestAllocation(unittest.TestCase):
    def setUp(self):self.a=load();self.d={'small':45,'family':35,'accessible':20}
    def test_demand_met(self):
        r=solve(self.a,self.d);self.assertEqual(r['status'],'optimal');self.assertGreaterEqual(r['units'],100)
    def test_no_unsafe(self):
        r=solve(self.a,self.d);self.assertNotIn('A_unsafe',[x['id'] for x in r['allocation']])
    def test_no_nonconsent(self):
        r=solve(self.a,self.d);self.assertNotIn('F_nonconsent',[x['id'] for x in r['allocation']])
    def test_insufficient_capacity(self):self.assertEqual(solve(self.a,{'accessible':1000})['status'],'infeasible')
    def test_budget(self):self.assertEqual(solve(self.a,self.d,budget=1000)['status'],'infeasible')
    def test_stock_priority(self):
        a=solve(self.a,self.d);b=solve(self.a,self.d,stock_first=True)
        self.assertLessEqual(b['new_build'],a['new_build'])
    def test_cohort_matching(self):
        r=solve(self.a,self.d)
        for cohort,n in self.d.items():self.assertGreaterEqual(sum(x['units'] for x in r['allocation'] if x['cohort']==cohort),n)
if __name__=='__main__':unittest.main()
