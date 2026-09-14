"""Minimal independent-attestation reference semantics.

Production deployments should place the attestor outside the worker's trust boundary
and preferably use QP public-key TransitionReceipts. HMAC is provided only as a
stdlib reference implementation for local active probes/tests.
"""
from __future__ import annotations
import hashlib, hmac, json, os

EVIDENCE_STRENGTH = {
    'fixture': 0,
    'replay': 1,
    'artifact_hash': 2,
    'local_active_probe': 3,
    'external_sandbox_probe': 4,
    'external_readback': 5,
    'signed_third_party_receipt': 6,
    'real_economic_outcome': 7,
}

def canonical_event(event: dict) -> bytes:
    body={k:v for k,v in event.items() if k not in {'attestation','_line'}}
    return json.dumps(body,sort_keys=True,separators=(',',':')).encode()

def sign_for_attestor(event: dict, key: str) -> str:
    return hmac.new(key.encode(),canonical_event(event),hashlib.sha256).hexdigest()

def verify_attestation(event: dict, env=None) -> tuple[bool,str]:
    att=event.get('attestation') or {}
    if att.get('scheme')!='hmac-sha256': return False,'missing_or_unsupported_attestation'
    key=(env or os.environ).get('CCP_ATTESTATION_KEY')
    if not key: return False,'attestation_key_unavailable'
    sig=att.get('signature','')
    expected=sign_for_attestor(event,key)
    return hmac.compare_digest(sig,expected),('verified' if hmac.compare_digest(sig,expected) else 'bad_signature')

def meets_class(actual: str, minimum: str) -> bool:
    return EVIDENCE_STRENGTH.get(actual,-1) >= EVIDENCE_STRENGTH.get(minimum,999)
