from __future__ import annotations
import asyncio
from xmrcomputer.core.economics import rank_offer
from xmrcomputer.core.policy import apply_policy
from xmrcomputer.markets.base import MarketAdapter
from xmrcomputer.models.domain import Decision, MachineProfile
from xmrcomputer.models.settings import Policy


class Scheduler:
    def __init__(self, adapters: list[MarketAdapter], policy: Policy):
        self.adapters = adapters
        self.policy = policy

    async def decide(self, machine: MachineProfile, *, xmr_usd: float) -> Decision:
        batches = await asyncio.gather(*(a.offers(machine, xmr_usd=xmr_usd) for a in self.adapters))
        ranked = []
        for offers in batches:
            for offer in offers:
                ranked.append(apply_policy(rank_offer(offer, machine, xmr_usd), self.policy))
        ranked.sort(key=lambda r: r.net_xmr_hour, reverse=True)
        selected = next((r for r in ranked if r.accepted), None)
        return Decision(selected=selected, ranked=ranked)
