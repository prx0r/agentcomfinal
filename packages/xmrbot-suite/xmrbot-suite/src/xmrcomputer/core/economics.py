from __future__ import annotations
from dataclasses import dataclass
from xmrcomputer.models.domain import MachineProfile, MarketOffer, RankedOffer


@dataclass(frozen=True)
class RandomXNetwork:
    network_hashrate_hs: float
    block_reward_xmr: float = 0.6
    block_time_seconds: float = 120.0

    @property
    def blocks_per_hour(self) -> float:
        return 3600.0 / self.block_time_seconds


def randomx_xmr_per_hour(worker_hashrate_hs: float, network: RandomXNetwork) -> float:
    return (worker_hashrate_hs / network.network_hashrate_hs) * network.blocks_per_hour * network.block_reward_xmr


def randomx_gross_usd_hour(worker_hashrate_hs: float, network: RandomXNetwork, xmr_usd: float) -> float:
    return randomx_xmr_per_hour(worker_hashrate_hs, network) * xmr_usd


def rank_offer(offer: MarketOffer, machine: MachineProfile, xmr_usd: float) -> RankedOffer:
    gross_usd = offer.gross_usd_hour
    net_usd = gross_usd - offer.fees_usd_hour - machine.energy_usd_hour - machine.amortization_usd_hour
    gross_xmr = gross_usd / xmr_usd
    net_xmr = net_usd / xmr_usd
    return RankedOffer(
        offer=offer,
        gross_xmr_hour=gross_xmr,
        net_xmr_hour=net_xmr,
        net_usd_hour=net_usd,
        accepted=True,
        reason="economically eligible",
    )
