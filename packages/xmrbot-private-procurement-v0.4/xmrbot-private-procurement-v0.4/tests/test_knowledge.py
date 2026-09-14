from xmrbot.knowledge.engine import engine


def test_search_returns_provenance():
    rows=engine.search("P2Pool mining")
    assert rows
    assert rows[0]["source"]


def test_resource_router_wallet():
    r=engine.resource_find("create wallet programmatically")
    assert r["recommended"]["resource"]=="monero-wallet-rpc"
    assert r["recommended"]["risk"].startswith("R2")


def test_resource_router_mining():
    r=engine.resource_find("mine monero")
    assert "XMRig" in r["recommended"]["resource"]
