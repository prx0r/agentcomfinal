import pytest
from fastapi.testclient import TestClient
from xmrbot.app import app, registry, mcp

client=TestClient(app)

def test_provider_api_and_router():
    p=client.get('/v1/providers'); assert p.status_code==200; assert len(p.json()['providers'])>=20
    x=client.get('/v1/providers/xmrbazaar'); assert x.status_code==200; assert x.json()['id']=='xmrbazaar'
    r=client.post('/v1/procurement/route',json={'objective':'hire a designer','escrow_required':True}); assert r.status_code==200; assert r.json()['routes']


def test_state_changing_api_returns_proposal_not_execution():
    r=client.post('/v1/providers/orbitswap/read',json={'action':'create_transaction','payload':{'amount':1}})
    assert r.status_code==200
    assert r.json()['requires_grant'] is True
    assert 'executed' not in r.json()

@pytest.mark.asyncio
async def test_mcp_provider_resources_and_tools():
    tools=await mcp.handle({'jsonrpc':'2.0','id':1,'method':'tools/list'})
    names={x['name'] for x in tools['result']['tools']}
    assert {'xmr_provider_list','xmr_procurement_route','xmr_provider_propose','qp_grant_request','qp_gate_evaluate','qp_receipt_verify'} <= names
    resources=await mcp.handle({'jsonrpc':'2.0','id':2,'method':'resources/list'})
    uris={x['uri'] for x in resources['result']['resources']}
    assert 'xmrbot://providers' in uris
    call=await mcp.handle({'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'xmr_provider_get','arguments':{'provider_id':'1gwei'}}})
    assert call['result']['structuredContent']['id']=='1gwei'
