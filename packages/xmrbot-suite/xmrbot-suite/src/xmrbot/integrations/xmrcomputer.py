from __future__ import annotations
from xmrcomputer.core.economics import RandomXNetwork
from xmrcomputer.core.scheduler import Scheduler
from xmrcomputer.markets.randomx import RandomXAdapter
from xmrcomputer.markets.mock_compute import MockComputeAdapter
from xmrcomputer.models.domain import MachineProfile
from xmrcomputer.models.settings import Policy
from xmrbot.core.types import NetworkSnapshot


async def opportunities(machine: MachineProfile, net: NetworkSnapshot, *, include_mock: bool = False) -> dict:
    randomx_network = RandomXNetwork(
        network_hashrate_hs=net.estimated_hashrate_hs,
        block_reward_xmr=net.reward_xmr,
        block_time_seconds=net.target_seconds,
    )
    adapters = [RandomXAdapter(randomx_network)]
    if include_mock:
        adapters.append(MockComputeAdapter())
    scheduler = Scheduler(adapters, Policy())
    decision = await scheduler.decide(machine, xmr_usd=net.xmr_usd)
    return decision.model_dump(mode="json")
