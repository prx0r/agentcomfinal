
import unittest,tempfile,json
from pathlib import Path
from runtime.model import project,ROOT
from runtime.validators import validate_checkpoint
class T(unittest.TestCase):
 def test_fixture_never_proven(self):
  p=project('breadup'); r=validate_checkpoint(p['checkpoints'][0],ROOT/'data/fixtures/events/breadup.jsonl')
  self.assertEqual(r['result'],'PASS'); self.assertEqual(r['proof_state'],'VALIDATOR_PASS_FIXTURE_ONLY')
 def test_live_can_prove(self):
  p=project('breadup'); cp=p['checkpoints'][0]
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'e.jsonl'; path.write_text(json.dumps({'ts':'x','source':'live','event_type':cp['validator']['event_type'],'checkpoint_id':cp['id'],'ok':True,'run_id':'r1'})+'\n')
   r=validate_checkpoint(cp,path); self.assertEqual(r['proof_state'],'PROVEN')
 def test_wrong_event_unknown(self):
  p=project('breadup'); cp=p['checkpoints'][0]
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'e.jsonl'; path.write_text(json.dumps({'ts':'x','source':'live','event_type':'wrong','checkpoint_id':cp['id'],'ok':True,'run_id':'r1'})+'\n')
   self.assertEqual(validate_checkpoint(cp,path)['result'],'UNKNOWN')
if __name__=='__main__': unittest.main()
