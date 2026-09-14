"""Qubic integration seam.

A production adapter should query only official/authorized Qubic endpoints and map
available useful-compute/mining opportunities into MarketOffer objects. No Qubic
protocol assumptions are hard-coded into the core scheduler.
"""
from xmrcomputer.markets.base import MarketAdapter
from xmrcomputer.models.domain import MachineProfile, MarketOffer


class QubicAdapter(MarketAdapter):
    name = "qubic"

    async def offers(self, machine: MachineProfile, *, xmr_usd: float) -> list[MarketOffer]:
        return []
