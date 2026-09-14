from xmrbot.procurement.registry import ProviderRegistry
from xmrbot.procurement.models import IntegrationMode

EXPECTED={
    "kycnot","xmrbazaar","monerojobs","haveno","orbitswap","trocador","1gwei","basicswap",
    "wallet_rpc","xmrcheckout","kuno","njalla","hosting1984","serversguru","silentlink",
    "anonymouslabels","xmrcards","coinsbee","shopinbit","btcpay"
}

def test_registry_contains_full_provider_set():
    r=ProviderRegistry()
    ids={p.id for p in r.all()}
    assert EXPECTED <= ids
    assert len(ids) >= 20


def test_every_provider_is_documented_and_capability_typed():
    r=ProviderRegistry()
    for p in r.all():
        assert p.source_urls, p.id
        assert p.capabilities, p.id
        assert 0 <= p.agentability <= 1
        for c in p.capabilities:
            assert isinstance(c.mode, IntegrationMode)
            assert c.description


def test_every_provider_capability_can_be_proposed():
    r=ProviderRegistry()
    for p in r.all():
        a=r.adapter(p.id)
        for c in p.capabilities:
            proposal=a.propose(c.name,{"fixture":True})
            assert proposal.action.provider_id == p.id
            assert proposal.action.action == c.name
            assert len(proposal.action_hash)==64
            assert proposal.requires_grant == c.requires_grant
