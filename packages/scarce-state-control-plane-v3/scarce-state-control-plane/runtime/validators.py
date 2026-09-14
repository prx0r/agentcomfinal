import json
from .eventlog import read_jsonl, evidence_root
from .attestation import verify_attestation, meets_class, EVIDENCE_STRENGTH

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
    """Claim-level matcher. It may test fixtures, but can never itself establish live proof."""
    candidates=[e for e in events if e.get('event_type')==spec.get('event_type') and _match_where(e,spec.get('where'))]
    if not candidates: return 'UNKNOWN', {'matched':0,'trust':'claim_only'}
    if any(e.get('ok') is False for e in candidates): return 'FAIL', {'matched':len(candidates),'trust':'claim_only'}
    if any(e.get('ok') is True for e in candidates): return 'PASS', {'matched':len(candidates),'trust':'claim_only'}
    return 'UNKNOWN', {'matched':len(candidates),'trust':'claim_only'}

def attested_event(spec, events):
    candidates=[e for e in events if e.get('event_type')==spec.get('event_type') and _match_where(e,spec.get('where'))]
    if not candidates: return 'UNKNOWN', {'matched':0,'trusted':0}
    if any(e.get('ok') is False for e in candidates): return 'FAIL', {'matched':len(candidates),'trusted':0}
    minimum=spec.get('minimum_evidence_class','local_active_probe')
    trusted=[]; fixture=[]; rejected=[]
    for e in candidates:
        cls=e.get('evidence_class') or ('fixture' if e.get('source')=='fixture' else 'unknown')
        if e.get('source')=='fixture':
            fixture.append(e); continue
        verified,reason=verify_attestation(e)
        if verified and meets_class(cls,minimum): trusted.append(e)
        else: rejected.append({'evidence_class':cls,'reason':reason,'meets_class':meets_class(cls,minimum)})
    if trusted:
        return 'PASS', {'matched':len(candidates),'trusted':len(trusted),'minimum_evidence_class':minimum,'max_strength':max(EVIDENCE_STRENGTH.get(e.get('evidence_class',''),-1) for e in trusted),'rejected':rejected}
    if fixture:
        return 'PASS', {'matched':len(candidates),'trusted':0,'fixture':len(fixture),'minimum_evidence_class':minimum,'rejected':rejected}
    return 'UNKNOWN', {'matched':len(candidates),'trusted':0,'minimum_evidence_class':minimum,'rejected':rejected}

def artifact_exists(spec, events):
    target=spec.get('path')
    matches=[e for e in events if e.get('event_type')=='artifact.created' and e.get('payload',{}).get('path')==target]
    return ('PASS' if matches else 'UNKNOWN'), {'matched':len(matches),'trust':'artifact_presence_only'}

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
    if kind=='attested_event': return attested_event(spec,events)
    if kind=='artifact_exists': return artifact_exists(spec,events)
    if kind=='all_of': return all_of(spec,events)
    return 'UNKNOWN', {'error':f'unknown validator kind {kind!r}'}

def validate_checkpoint(checkpoint, event_path):
    events=read_jsonl(event_path)
    result, detail=validate_spec(checkpoint['validator'],events)
    relevant=[e for e in events if e.get('checkpoint_id')==checkpoint['id']]
    sources={e.get('source','unknown') for e in relevant}
    if sources=={'fixture'}: source_class='fixture'
    elif any(e.get('source')=='live' for e in relevant): source_class='live'
    elif 'replay' in sources: source_class='replay'
    else: source_class='unknown'
    trusted_live = result=='PASS' and source_class=='live' and isinstance(detail,dict) and detail.get('trusted',0)>0
    receipt={
      'checkpoint_id':checkpoint['id'],
      'validator_id':checkpoint['validator']['kind']+':'+checkpoint['id'],
      'result':result,'evidence_root':evidence_root(events),'source_class':source_class,
      'detail':detail,
      'proof_state':('PROVEN' if trusted_live else
                     'VALIDATOR_PASS_FIXTURE_ONLY' if result=='PASS' and source_class=='fixture' else
                     'UNATTESTED_CLAIM' if result=='UNKNOWN' and source_class=='live' else result)
    }
    return receipt
