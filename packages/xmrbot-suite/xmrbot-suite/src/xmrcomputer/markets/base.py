from __future__ import annotations
from abc import ABC, abstractmethod
from xmrcomputer.models.domain import MachineProfile, MarketOffer


class MarketAdapter(ABC):
    name: str

    @abstractmethod
    async def offers(self, machine: MachineProfile, *, xmr_usd: float) -> list[MarketOffer]:
        raise NotImplementedError
