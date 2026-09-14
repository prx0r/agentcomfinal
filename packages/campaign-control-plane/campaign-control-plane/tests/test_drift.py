import unittest
from runtime.drift import repo_drift
class T(unittest.TestCase):
 def test_repo_never_proves_behavior(self):
  d=repo_drift('breadup'); self.assertFalse(d['behavioral_proof_from_repo']); self.assertEqual(d['thesis_checkpoint_count'],12)
if __name__=='__main__': unittest.main()
