import unittest
from model import allocate
class Tests(unittest.TestCase):
 def test_zero(self):self.assertEqual(allocate(0),([],0))
 def test_supply(self):
  rows,missing=allocate(1600)
  self.assertEqual(sum(x['units'] for x in rows)+missing,1600)
 def test_reject_unsafe(self):
  rows,missing=allocate(2,options=[{'name':'unsafe','capacity':20,'cost':1,'carbon':1,'quality':False,'consent':True}])
  self.assertEqual((rows,missing),([],2))
 def test_reject_nonconsent(self):
  rows,missing=allocate(2,options=[{'name':'unconsented','capacity':20,'cost':1,'carbon':1,'quality':True,'consent':False}])
  self.assertEqual((rows,missing),([],2))
 def test_invalid(self):
  with self.assertRaises(ValueError):allocate(-1)
if __name__=='__main__':unittest.main()
