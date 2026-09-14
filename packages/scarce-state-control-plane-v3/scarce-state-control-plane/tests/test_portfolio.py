import unittest
from runtime.model import projects,portfolio
class T(unittest.TestCase):
 def test_counts(self):
  ps=projects(); self.assertEqual(len(ps),13); self.assertEqual(sum(len(p['checkpoints']) for p in ps),156)
 def test_v3_contracts(self):
  for p in projects():
   for k in ['core_thesis','software_substitution_test','strategic_role','scarce_assets','underengineer','priority_inputs','experiment_strategy']: self.assertIn(k,p)
   u=p['underengineer']; self.assertEqual(u['primitive'],'UNDERENGINEER/2.0'); self.assertTrue(u['first_real_moat_event']); self.assertLessEqual(len(u['steps']),6); self.assertTrue(u['explicitly_not_now'])
   self.assertTrue(p['experiment_strategy']['candidates'])
   for cp in p['checkpoints']:
    self.assertEqual(cp['validator']['kind'],'attested_event'); self.assertIn('minimum_evidence_class',cp['validator'])
 def test_invariants(self):
  pf=portfolio(); self.assertEqual(pf['version'],'3.0.0'); self.assertIn('Can OpenAI destroy this',pf['strategic_invariant']); self.assertIn('human',pf['human_endgame'].lower()); self.assertEqual(len(pf['experiment_classes']),4)
if __name__=='__main__': unittest.main()
