from datetime import datetime, timedelta, timezone
from xmrbot.procurement.models import ProviderAction, QPGrant
from xmrbot.procurement.policy import evaluate_grant
from xmrbot.procurement.receipts import make_receipt, verify_receipt
from xmrbot.procurement.registry import ProviderRegistry
from xmrbot.procurement.service import ProcurementService


def _grant(action, approved=True):
    return QPGrant(id="g1",capability="test",approved=approved,max_atomic_xmr=100,allowed_providers=[action.provider_id],allowed_actions=[action.action],exact_payload_hash=action.canonical_hash(),expires_at=datetime.now(timezone.utc)+timedelta(minutes=5))


def test_gate_rejects_missing_or_unapproved_grant():
    a=ProviderAction(provider_id="orbitswap",action="create_transaction",payload={"amount":1})
    assert not evaluate_grant(a,None).allowed
    assert not evaluate_grant(a,_grant(a,False)).allowed


def test_gate_binds_exact_payload_and_budget():
    a=ProviderAction(provider_id="orbitswap",action="create_transaction",payload={"amount":1,"to":"x"})
    g=_grant(a)
    assert evaluate_grant(a,g,amount_atomic_xmr=99).allowed
    assert not evaluate_grant(a,g,amount_atomic_xmr=101).allowed
    mutated=ProviderAction(provider_id="orbitswap",action="create_transaction",payload={"amount":2,"to":"x"})
    assert not evaluate_grant(mutated,g).allowed


def test_grant_request_is_not_approved_and_exactly_bound():
    s=ProcurementService(ProviderRegistry())
    payload={"coinFrom":"BTC","coinTo":"XMR","amount":0.1,"withdrawalAddress":"x"}
    g=s.grant_request("orbitswap","create_transaction",payload,max_xmr=.5)
    assert g["approved"] is False
    a=ProviderAction(provider_id="orbitswap",action="create_transaction",payload=payload)
    assert g["exact_payload_hash"] == a.canonical_hash()


def test_receipt_integrity_roundtrip_and_tamper_detection():
    a=ProviderAction(provider_id="1gwei",action="order_status",payload={"id":"abc"})
    response={"status":"sent","tx":"0x1"}
    receipt=make_receipt(a,"completed",response,"g1")
    assert verify_receipt(receipt,a,response)["valid"]
    assert not verify_receipt(receipt,a,{"status":"sent","tx":"0x2"})["valid"]
