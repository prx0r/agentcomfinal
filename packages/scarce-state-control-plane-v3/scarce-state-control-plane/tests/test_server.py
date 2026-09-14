import unittest
from runtime.model import portfolio
from runtime.scheduler import schedule
from runtime.hdesk import queue
class T(unittest.TestCase):
 def test_dashboard_data(self):
  p=portfolio(); self.assertEqual(p['version'],'3.0.0'); self.assertIn('UNDERENGINEER',p['underengineer_invariant'])
 def test_command_center_sources(self): self.assertIn('live_queue',schedule()); self.assertIn('open',queue())
if __name__=='__main__': unittest.main()
