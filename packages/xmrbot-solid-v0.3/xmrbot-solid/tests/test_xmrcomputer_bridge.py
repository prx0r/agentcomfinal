import pytest
from xmrcomputer.models.domain import MachineProfile
from xmrbot.core.types import NetworkSnapshot
from xmrbot.integrations.xmrcomputer import opportunities

@pytest.mark.asyncio
async def test_randomx_is_available_as_reserve_bid():
    n=NetworkSnapshot(height=1,difficulty=5.9e9*120,estimated_hashrate_hs=5.9e9,reward_xmr=.6,xmr_usd=500)
    m=MachineProfile(cpu_model='test',hashrate_hs=26900,watts_at_load=160,electricity_usd_kwh=.1)
    d=await opportunities(m,n)
    assert d['selected']['offer']['market']=='randomx'
    assert d['selected']['offer']['job_id']=='reserve-bid'
