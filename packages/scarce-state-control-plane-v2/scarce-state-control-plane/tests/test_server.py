import unittest
from runtime.model import portfolio
class T(unittest.TestCase):
 def test_dashboard_data(self):
  p=portfolio(); self.assertEqual(p['version'],'2.0.0'); self.assertIn('UNDERENGINEER',p['underengineer_invariant'])
if __name__=='__main__': unittest.main()
