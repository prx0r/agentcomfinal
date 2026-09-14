EVIDENCE_MULTIPLIER={
 'fixture':0.0,'replay':0.0,'artifact_hash':0.1,'local_active_probe':0.35,
 'external_sandbox_probe':0.5,'external_readback':0.7,'signed_third_party_receipt':0.9,'real_economic_outcome':1.0
}

def capability_score(receipt,cost=None,duration=None):
    if receipt.get('proof_state')!='PROVEN': return 0.0
    penalty=0.0
    if cost is not None: penalty += min(float(cost),1.0)*0.05
    if duration is not None: penalty += min(float(duration)/3600.0,1.0)*0.05
    return max(0.9,1.0-penalty)

def scarce_state_score(delta_units,economic_value,evidence_class,human_minutes=0,cost=0,risk=1):
    """Business-campaign reward: real scarce-state gain first; software volume is irrelevant."""
    e=EVIDENCE_MULTIPLIER.get(evidence_class,0.0)
    if e<=0 or delta_units<=0: return 0.0
    denom=max(1.0,1.0+float(human_minutes)/60.0+float(cost)+max(0.0,float(risk)-1.0))
    return round(float(delta_units)*float(economic_value)*e/denom,6)

def infrastructure_score(enabled_scarce_state_score,human_minutes=0,cost=0):
    denom=max(1.0,1.0+float(human_minutes)/60.0+float(cost))
    return round(float(enabled_scarce_state_score)/denom,6)

# Backwards-compatible alias for old callers.
def score(receipt,cost=None,duration=None): return capability_score(receipt,cost,duration)
