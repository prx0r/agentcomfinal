
import unittest
from runtime.model import projects,portfolio
class T(unittest.TestCase):
 def test_counts(self):
  ps=projects(); self.assertEqual(len(ps),11); self.assertEqual(sum(len(p['checkpoints']) for p in ps),132)
 def test_contracts(self):
  for p in projects():
   self.assertTrue(p['core_thesis']); self.assertTrue(p['falsifiers'])
   for cp in p['checkpoints']:
    for k in ['user_behavior','implies','evidence_contract','validator','reward','authority','minimum_proof_level']: self.assertIn(k,cp)
 def test_repo_binding_rule(self):
  self.assertIn('GitHub code presence is not behavioral proof.',portfolio()['invariants'])
if __name__=='__main__': unittest.main()
