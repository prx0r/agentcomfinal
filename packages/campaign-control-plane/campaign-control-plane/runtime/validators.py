
import json, re, hashlib
from pathlib import Path
from .eventlog import read_jsonl, evidence_root

RESULTS={'PASS','FAIL','UNKNOWN'}

def _match_where(event, where):
    for k,v in (where or {}).items():
        cur=event
        for part in k.split('.'):
            if not isinstance(cur,dict) or part not in cur: return False
            cur=cur[part]
        if cur != v: return False
    return True

def event_match(spec, events):
    candidates=[e for e in events if e.get('event_type')==spec.get('event_type') and _match_where(e,spec.get('where'))]
    if not candidates: return 'UNKNOWN', {'matched':0}
    # Explicit matching failure dominates; latest matching success otherwise.
    if any(e.get('ok') is False for e in candidates): return 'FAIL', {'matched':len(candidates)}
    if any(e.get('ok') is True for e in candidates): return 'PASS', {'matched':len(candidates)}
    return 'UNKNOWN', {'matched':len(candidates)}

def artifact_exists(spec, events):
    target=spec.get('path')
    matches=[e for e in events if e.get('event_type')=='artifact.created' and e.get('payload',{}).get('path')==target]
    return ('PASS' if matches else 'UNKNOWN'), {'matched':len(matches)}

def all_of(spec, events):
    details=[]
    for child in spec.get('validators',[]):
        r,d=validate_spec(child,events); details.append({'result':r,'detail':d})
        if r=='FAIL': return 'FAIL',details
        if r!='PASS': return 'UNKNOWN',details
    return 'PASS',details

def validate_spec(spec, events):
    kind=spec.get('kind')
    if kind=='event_match': return event_match(spec,events)
    if kind=='artifact_exists': return artifact_exists(spec,events)
    if kind=='all_of': return all_of(spec,events)
    return 'UNKNOWN', {'error':f'unknown validator kind {kind!r}'}

def validate_checkpoint(checkpoint, event_path):
    events=read_jsonl(event_path)
    result, detail=validate_spec(checkpoint['validator'],events)
    sources={e.get('source','unknown') for e in events if e.get('checkpoint_id')==checkpoint['id']}
    source_class='live' if sources=={'live'} else ('fixture' if 'fixture' in sources else ('replay' if 'replay' in sources else 'unknown'))
    receipt={
      'checkpoint_id':checkpoint['id'],
      'validator_id':checkpoint['validator']['kind']+':'+checkpoint['id'],
      'result':result,'evidence_root':evidence_root(events),'source_class':source_class,
      'detail':detail,
      'proof_state':'PROVEN' if result=='PASS' and source_class=='live' else ('VALIDATOR_PASS_FIXTURE_ONLY' if result=='PASS' and source_class=='fixture' else result)
    }
    return receipt
