import unittest
from runtime.scheduler import schedule
from runtime.resources import resource_map
class T(unittest.TestCase):
 def test_resource_capacity(self):
  s=schedule(); rm=resource_map(); counts=s['resource_allocations']
  for rid,n in counts.items():
   if rm.get(rid,{}).get('parallelism')==1: self.assertLessEqual(n,1)
 def test_market_lab_present(self):
  s=schedule(); self.assertTrue(any(x['project_id']=='seesaw-market-lab' and x['world']=='paper_trading' for x in s['live_queue']))
 def test_infrastructure_cannot_take_external_slot(self):
  s=schedule(); self.assertFalse(any(x['strategic_role']=='infrastructure' for x in s['live_queue'])); self.assertFalse(any(x['project_id']=='cmail-onboarding' for x in s['live_queue'])); self.assertTrue(any(x['project_id']=='agentcom-uk' for x in s['live_queue']))
 def test_simulation_preflight_noncanonical(self):
  s=schedule(); self.assertTrue(s['simulation_preflight']); self.assertTrue(all(x['proof_ceiling']=='SIMULATION_ONLY' for x in s['simulation_preflight']))
if __name__=='__main__': unittest.main()
