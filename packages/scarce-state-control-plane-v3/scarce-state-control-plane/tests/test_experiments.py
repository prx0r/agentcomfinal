import unittest
from runtime.experiments import catalog,select_world,experiment_value
from runtime.simulation import simulate_project
class T(unittest.TestCase):
 def test_four_classes(self): self.assertEqual({x['id'] for x in catalog()['classes']},{'A_TRUTH','B_DEMAND','C_ECONOMIC','D_SCARCE_STATE'})
 def test_world_select(self):
  x=select_world('pogpet'); self.assertTrue(x['ranked_worlds']); self.assertEqual(x['target_profile'],'etsy_marketplace'); self.assertTrue(all('score' in w for w in x['ranked_worlds']))
 def test_simulation_cannot_prove(self):
  s=simulate_project('breadup'); self.assertEqual(s['proof_state'],'SIMULATION_ONLY'); self.assertEqual(s['canonical_effect'],'NONE')
 def test_score_positive(self): self.assertGreater(experiment_value(catalog()['worlds'][0]),0)
if __name__=='__main__': unittest.main()
