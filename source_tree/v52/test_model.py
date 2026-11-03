import unittest
from model import hypothetical_screening,DATA
class Tests(unittest.TestCase):
 def test_conservation(self):
  x=hypothetical_screening(100,40,30,10)
  self.assertEqual(sum(x[k] for k in ('voluntary_rehousing','upgraded_in_place','new_suitable_homes','remaining_need')),100)
 def test_no_double_count(self):
  x=hypothetical_screening(10,20,20,20);self.assertEqual(x['remaining_need'],0);self.assertEqual(x['voluntary_rehousing'],10)
 def test_unmet(self):self.assertEqual(hypothetical_screening(100,0,0,0)['remaining_need'],100)
 def test_nonnegative(self):
  with self.assertRaises(AssertionError):hypothetical_screening(-1,0,0,0)
 def test_source_registry(self):self.assertTrue(all(x['source'].startswith('https://') for x in DATA))
if __name__=='__main__':unittest.main()
