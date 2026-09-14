import json, os
import httpx
import pytest
from xmrbot.procurement.registry import ProviderRegistry
from xmrbot.procurement.models import ProviderAction, QPGrant


def transport(handler): return httpx.MockTransport(handler)

def registry_for(handler): return ProviderRegistry(http=httpx.AsyncClient(transport=transport(handler)))

@pytest.mark.asyncio
async def test_orbitswap_public_rate_contract():
    def h(req):
        assert req.url.path == "/api/v2/rate"
        assert req.url.params["coinFrom"] == "BTC"
        return httpx.Response(200,json={"fromAmount":.1,"toAmount":2.8,"rate":28,"minAmount":.001,"maxAmount":5})
    r=registry_for(h); a=r.adapter("orbitswap")
    out=await a.invoke("rate",{"coinFrom":"BTC","coinTo":"XMR","amount":.1})
    assert out.data["toAmount"] == 2.8
    await r.http.aclose()

@pytest.mark.asyncio
async def test_orbitswap_state_change_requires_exact_grant(monkeypatch):
    monkeypatch.setenv("ORBITSWAP_API_KEY","test-key")
    def h(req):
        assert req.headers["X-API-Key"] == "test-key"
        assert req.url.path == "/api/v2/transactions"
        return httpx.Response(200,json={"id":"swap1","status":"wait","deposit_address":"bc1q"})
    r=registry_for(h); a=r.adapter("orbitswap")
    payload={"coinFrom":"BTC","coinTo":"XMR","amount":.1,"withdrawalAddress":"48abc"}
    blocked=await a.execute("create_transaction",payload,None)
    assert blocked["executed"] is False
    pa=ProviderAction(provider_id="orbitswap",action="create_transaction",payload=payload)
    g=QPGrant(id="g",capability="swap",approved=True,allowed_providers=["orbitswap"],allowed_actions=["create_transaction"],exact_payload_hash=pa.canonical_hash())
    ok=await a.execute("create_transaction",payload,g)
    assert ok["executed"] is True
    assert ok["result"]["data"]["id"] == "swap1"
    await r.http.aclose()

@pytest.mark.asyncio
async def test_1gwei_agent_api_contract():
    def h(req):
        if req.url.path == "/api/quote": return httpx.Response(200,json={"invoiceUsd":1.1,"chain":"base"})
        raise AssertionError(req.url)
    r=registry_for(h); out=await r.adapter("1gwei").invoke("quote",{"chain":"base","ethAmount":"0.0003"})
    assert out.data["invoiceUsd"] == 1.1
    await r.http.aclose()

@pytest.mark.asyncio
async def test_trocador_indirect_anonpay_contract():
    def h(req):
        assert req.url.path == "/anonpay/"
        assert req.url.params["direct"] == "False"
        return httpx.Response(200,json={"ID":"anon1","URL":"https://trocador.app/anonpay/anon1"})
    r=registry_for(h); out=await r.adapter("trocador").invoke("create_invoice",{"ticker_to":"xmr","network_to":"Mainnet","address":"48abc","amount":.1})
    assert out.data["ID"] == "anon1"
    await r.http.aclose()

@pytest.mark.asyncio
async def test_kycnot_query_method_and_auth(monkeypatch):
    monkeypatch.setenv("KYCNOT_API_KEY","kycnot_test")
    def h(req):
        assert req.method == "QUERY"
        assert req.headers["Authorization"] == "Bearer kycnot_test"
        return httpx.Response(200,json={"id":1,"slug":"svc","kycLevel":0,"verificationStatus":"APPROVED"})
    r=registry_for(h); out=await r.adapter("kycnot").invoke("service_get",{"slug":"svc"})
    assert out.data["kycLevel"] == 0
    await r.http.aclose()

@pytest.mark.asyncio
async def test_wallet_rpc_jsonrpc_contract():
    def h(req):
        body=json.loads(req.content)
        assert body["method"] == "get_balance"
        return httpx.Response(200,json={"jsonrpc":"2.0","id":"xmrbot","result":{"balance":123}})
    r=registry_for(h); out=await r.adapter("wallet_rpc").invoke("balance",{"account_index":0})
    assert out.data["balance"] == 123
    await r.http.aclose()

@pytest.mark.asyncio
async def test_basicswap_local_json_contract(monkeypatch):
    monkeypatch.setenv("BASICSWAP_URL","http://127.0.0.1:12700")
    monkeypatch.setenv("BASICSWAP_PASSWORD","pw")
    def h(req):
        assert req.url.path == "/json/wallets"
        return httpx.Response(200,json={"XMR":{"balance":1}})
    r=registry_for(h); out=await r.adapter("basicswap").invoke("wallets",{})
    assert "XMR" in out.data
    await r.http.aclose()

@pytest.mark.asyncio
async def test_xmrcheckout_local_contract(monkeypatch):
    monkeypatch.setenv("XMRCHECKOUT_URL","http://checkout.local")
    monkeypatch.setenv("XMRCHECKOUT_API_KEY","token1")
    def h(req):
        assert req.url.path == "/api/v1/server/info"
        assert req.headers["Authorization"] == "token token1"
        return httpx.Response(200,json={"version":"1"})
    r=registry_for(h); out=await r.adapter("xmrcheckout").invoke("server_info",{})
    assert out.data["version"] == "1"
    await r.http.aclose()

@pytest.mark.asyncio
async def test_haveno_local_bridge_contract(monkeypatch):
    monkeypatch.setenv("XMRBOT_HAVENO_BRIDGE_URL","http://haveno-bridge.local")
    def h(req):
        assert req.url.path == "/invoke"
        return httpx.Response(200,json={"offers":[]})
    r=registry_for(h); out=await r.adapter("haveno").invoke("market",{"currency":"USD"})
    assert out.data == {"offers":[]}
    await r.http.aclose()
