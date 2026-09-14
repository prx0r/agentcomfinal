import unittest
from runtime.model import projects,portfolio
class T(unittest.TestCase):
 def test_counts(self):
  ps=projects(); self.assertEqual(len(ps),12); self.assertEqual(sum(len(p['checkpoints']) for p in ps),144)
 def test_v2_contracts(self):
  for p in projects():
   for k in ['core_thesis','software_substitution_test','strategic_role','scarce_assets','underengineer','priority_inputs']: self.assertIn(k,p)
   u=p['underengineer']; self.assertEqual(u['primitive'],'UNDERENGINEER/1.0'); self.assertTrue(u['first_real_moat_event']); self.assertLessEqual(len(u['steps']),6); self.assertTrue(u['explicitly_not_now'])
   for cp in p['checkpoints']:
    self.assertEqual(cp['validator']['kind'],'attested_event')
    self.assertIn('minimum_evidence_class',cp['validator'])
 def test_strategic_invariant(self):
  pf=portfolio(); self.assertEqual(pf['version'],'2.0.0'); self.assertIn('Can OpenAI destroy this',pf['strategic_invariant'])
if __name__=='__main__': unittest.main()
