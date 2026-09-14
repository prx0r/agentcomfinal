import unittest
from runtime.scarcity import declared_assets,ledger
from runtime.reward import scarce_state_score
class T(unittest.TestCase):
 def test_declared_assets_do_not_increment_ledger(self):
  self.assertTrue(declared_assets()); self.assertEqual(ledger()['assets'],[])
 def test_reward_requires_real_delta_and_evidence(self):
  self.assertEqual(scarce_state_score(0,5,'real_economic_outcome'),0)
  self.assertEqual(scarce_state_score(1,5,'fixture'),0)
  self.assertGreater(scarce_state_score(1,5,'real_economic_outcome'),0)
if __name__=='__main__': unittest.main()
