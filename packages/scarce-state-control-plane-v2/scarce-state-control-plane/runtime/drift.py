import json
from .model import ROOT,project

def repo_drift(project_id):
    p=project(project_id)
    snaps=json.loads((ROOT/'data/repo_snapshots.json').read_text()).get('snapshots',[])
    s=next((x for x in snaps if x.get('repo')==p.get('repo')),None)
    return {
      'project_id':project_id,
      'repo':p.get('repo'),
      'snapshot':s,
      'thesis_checkpoint_count':len(p['checkpoints']),
      'behavioral_proof_from_repo':False,
      'interpretation':'Repo snapshot measures implementation drift only. Behavioral state requires checkpoint receipts.'
    }
