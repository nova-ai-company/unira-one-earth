import csv, pathlib, unittest
P=pathlib.Path(__file__).parent
class TestEvidence(unittest.TestCase):
 def setUp(self):
  with (P/'city_evidence.csv').open() as f:self.rows=list(csv.DictReader(f))
 def test_five_cities(self):self.assertEqual({r['city'] for r in self.rows},{'Paris','London','New York','Tokyo','Cairo'})
 def test_missing_cairo(self):self.assertEqual(next(r for r in self.rows if r['city']=='Cairo')['status'],'missing')
 def test_provenance(self):self.assertTrue(all(r['source'].startswith('https://') for r in self.rows if r['status']=='verified'))
 def test_london_subset(self):
  x=[r for r in self.rows if r['city']=='London'];self.assertLess(int(x[1]['value']),int(x[0]['value']))
 def test_tokyo_subset(self):
  x=[r for r in self.rows if r['city']=='Tokyo'];self.assertLess(int(x[1]['value']),int(x[0]['value']))
if __name__=='__main__':unittest.main()
