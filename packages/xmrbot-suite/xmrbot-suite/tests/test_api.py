from fastapi.testclient import TestClient
from xmrbot.app import app

client=TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200 and r.json()["ok"]

def test_network_has_methodologies():
    r=client.get('/v1/network'); assert r.status_code==200
    j=r.json(); assert "hashprice_xmr_per_khs_day" in j and "methodologies" in j

def test_profitability_api():
    r=client.post('/v1/mining/profitability',json={"hashrate_hs":26900,"watts":160,"electricity_usd_kwh":.1})
    assert r.status_code==200 and r.json()["expected_xmr_year"]>0

def test_cpu_page_api_and_html():
    assert client.get('/v1/hardware/cpus/amd-ryzen-9-7950x').status_code==200
    html=client.get('/cpu/amd-ryzen-9-7950x')
    assert html.status_code==200 and 'RandomX hardware' in html.text

def test_web_surfaces_load():
    for path, needle in [('/', 'Monero,'),('/terminal','XMR Terminal'),('/mine','Mine, or buy?'),('/ask','Ask XMRBot')]:
        r=client.get(path); assert r.status_code==200 and needle in r.text

def test_http_mcp():
    r=client.post('/mcp',json={"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}})
    assert r.status_code==200
    assert any(t["name"]=='xmr_search' for t in r.json()["result"]["tools"])

def test_node_and_wallet_plan():
    n=client.post('/v1/node/plan',json={"tor":True,"prune":True,"public_rpc":False}); assert n.status_code==200
    w=client.post('/v1/wallet/plan',json={"hardware_wallet":False}); assert w.status_code==200
    assert w.json()["cloud_receives_seed"] is False

def test_metric_query_and_privacy_profile():
    q=client.post('/v1/query',json={"metric":"hashprice_usd","limit":10})
    assert q.status_code==200 and q.json()["series"]
    bad=client.post('/v1/query',json={"metric":"addresses","limit":10})
    assert bad.status_code==400
    p=client.get('/v1/privacy/profile')
    assert p.status_code==200 and p.json()["wallet"]=='local-only'
