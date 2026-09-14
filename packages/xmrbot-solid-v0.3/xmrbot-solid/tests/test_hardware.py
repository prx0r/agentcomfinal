from xmrbot.hardware.catalog import catalog
from xmrbot.core.types import NetworkSnapshot


def test_catalog_has_expected_reference_cpus():
    assert catalog.get("amd-ryzen-9-7950x") is not None
    assert catalog.search("5950X")[0].model == "Ryzen 9 5950X"


def test_rankings_are_derived():
    n=NetworkSnapshot(height=1,difficulty=5.9e9*120,estimated_hashrate_hs=5.9e9,reward_xmr=.6,xmr_usd=500)
    rows=catalog.rankings(n)
    assert rows
    assert "hashrate_per_usd" in rows[0]
    assert "effective_cost_per_xmr_usd" in rows[0]
