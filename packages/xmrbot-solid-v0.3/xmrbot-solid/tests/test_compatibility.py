import math
from xmrcomputer.core.economics import RandomXNetwork, randomx_xmr_per_hour
from xmrbot.core.economics import profitability
from xmrbot.core.types import NetworkSnapshot, ProfitabilityRequest


def test_randomx_math_matches_original_package():
    h=26900
    old=RandomXNetwork(network_hashrate_hs=5.9e9,block_reward_xmr=.6,block_time_seconds=120)
    old_day=randomx_xmr_per_hour(h,old)*24
    net=NetworkSnapshot(height=1,difficulty=5.9e9*120,estimated_hashrate_hs=5.9e9,reward_xmr=.6,target_seconds=120,xmr_usd=500)
    new=profitability(ProfitabilityRequest(hashrate_hs=h,watts=0,electricity_usd_kwh=0),net)
    assert math.isclose(old_day,new.expected_xmr_day,rel_tol=1e-12)
