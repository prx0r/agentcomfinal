import unittest,tempfile,json,os
from pathlib import Path
from unittest.mock import patch
from runtime.model import project,ROOT
from runtime.validators import validate_checkpoint
from runtime.attestation import sign_for_attestor
class T(unittest.TestCase):
 def test_fixture_never_proven(self):
  p=project('breadup'); r=validate_checkpoint(p['checkpoints'][0],ROOT/'data/fixtures/events/breadup.jsonl')
  self.assertEqual(r['result'],'PASS'); self.assertEqual(r['proof_state'],'VALIDATOR_PASS_FIXTURE_ONLY')
 def test_self_reported_live_cannot_prove(self):
  p=project('breadup'); cp=p['checkpoints'][0]
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'e.jsonl'; path.write_text(json.dumps({'ts':'x','source':'live','evidence_class':'external_readback','event_type':cp['validator']['event_type'],'checkpoint_id':cp['id'],'ok':True,'run_id':'r1'})+'\n')
   r=validate_checkpoint(cp,path); self.assertNotEqual(r['proof_state'],'PROVEN'); self.assertEqual(r['proof_state'],'UNATTESTED_CLAIM')
 def test_attested_live_can_prove(self):
  p=project('breadup'); cp=p['checkpoints'][0]; key='test-attestor-key'
  ev={'ts':'x','source':'live','evidence_class':cp['validator']['minimum_evidence_class'],'event_type':cp['validator']['event_type'],'checkpoint_id':cp['id'],'ok':True,'run_id':'r1'}
  ev['attestation']={'scheme':'hmac-sha256','signature':sign_for_attestor(ev,key)}
  with tempfile.TemporaryDirectory() as d, patch.dict(os.environ,{'CCP_ATTESTATION_KEY':key}):
   path=Path(d)/'e.jsonl'; path.write_text(json.dumps(ev)+'\n'); r=validate_checkpoint(cp,path); self.assertEqual(r['proof_state'],'PROVEN')
 def test_weak_evidence_class_cannot_prove(self):
  p=project('breadup'); cp=p['checkpoints'][0]; key='test-attestor-key'
  ev={'ts':'x','source':'live','evidence_class':'artifact_hash','event_type':cp['validator']['event_type'],'checkpoint_id':cp['id'],'ok':True,'run_id':'r1'}
  ev['attestation']={'scheme':'hmac-sha256','signature':sign_for_attestor(ev,key)}
  with tempfile.TemporaryDirectory() as d, patch.dict(os.environ,{'CCP_ATTESTATION_KEY':key}):
   path=Path(d)/'e.jsonl'; path.write_text(json.dumps(ev)+'\n'); self.assertNotEqual(validate_checkpoint(cp,path)['proof_state'],'PROVEN')
if __name__=='__main__': unittest.main()
