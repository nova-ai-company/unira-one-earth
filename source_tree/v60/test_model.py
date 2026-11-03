import unittest
from model import scenario, run, BASE_PRODUCTION_TWH, BASE_WEATHER_ADJUSTED_CONSUMPTION_TWH
class TestModel(unittest.TestCase):
    def test_reference(self): self.assertEqual(scenario()['index_gap'],0)
    def test_growth(self): self.assertEqual(scenario(.1)['demand_index'],110)
    def test_loss(self): self.assertEqual(scenario(0,.1)['production_index'],90)
    def test_efficiency(self): self.assertAlmostEqual(scenario(.1,0,.1)['demand_index'],99)
    def test_no_false_balance(self): self.assertNotEqual(BASE_PRODUCTION_TWH, BASE_WEATHER_ADJUSTED_CONSUMPTION_TWH)
    def test_scenarios(self): self.assertEqual(len(run()),5)
    def test_bad_inputs(self):
        with self.assertRaises(AssertionError): scenario(generation_loss=1.2)
if __name__=='__main__': unittest.main()
