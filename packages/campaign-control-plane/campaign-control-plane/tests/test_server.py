
import unittest
from runtime.model import portfolio
class T(unittest.TestCase):
 def test_dashboard_data(self):
  p=portfolio(); self.assertEqual(p['version'],'1.0.0'); self.assertGreater(len(p['northstar']),20)
if __name__=='__main__': unittest.main()
