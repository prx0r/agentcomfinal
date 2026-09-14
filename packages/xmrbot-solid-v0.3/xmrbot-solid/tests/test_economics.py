import math
from xmrbot.core.economics import profitability, mine_or_buy
from xmrbot.core.types import NetworkSnapshot, ProfitabilityRequest, MineOrBuyRequest


def net():
    return NetworkSnapshot(height=1, difficulty=5.9e9*120, estimated_hashrate_hs=5.9e9, reward_xmr=0.6, xmr_usd=500)


def test_hashprice_identity():
    n=net()
    assert math.isclose(n.hashprice_xmr_per_khs_day, 1000/5.9e9*432, rel_tol=1e-12)


def test_profitability_production():
    r=profitability(ProfitabilityRequest(hashrate_hs=26900,watts=0,electricity_usd_kwh=0),net())
    expected=26900/5.9e9*432
    assert math.isclose(r.expected_xmr_day, expected, rel_tol=1e-12)
    assert math.isclose(r.gross_usd_day, expected*500, rel_tol=1e-12)


def test_power_cost():
    r=profitability(ProfitabilityRequest(hashrate_hs=26900,watts=100,electricity_usd_kwh=.10),net())
    assert math.isclose(r.electricity_usd_day,.24,rel_tol=1e-12)


def test_mine_or_buy_returns_scenario():
    r=mine_or_buy(MineOrBuyRequest(budget_usd=800,hardware_cost_usd=480,hashrate_hs=26900,watts=160,electricity_usd_kwh=.10,months=24,monthly_difficulty_growth_pct=1),net())
    assert r["decision"] in {"mine","buy"}
    assert len(r["monthly"])==24
    assert r["buy_xmr"]==1.6


def test_hardware_over_budget_forces_buy():
    r=mine_or_buy(MineOrBuyRequest(budget_usd=100,hardware_cost_usd=200,hashrate_hs=10000,watts=100,electricity_usd_kwh=.1),net())
    assert r["decision"]=="buy"
