from xmrcomputer.core.economics import RandomXNetwork, randomx_gross_usd_hour
from xmrcomputer.markets.base import MarketAdapter
from xmrcomputer.models.domain import MachineProfile, MarketOffer, TrustLevel


class RandomXAdapter(MarketAdapter):
    name = "randomx"

    def __init__(self, network: RandomXNetwork):
        self.network = network

    async def offers(self, machine: MachineProfile, *, xmr_usd: float) -> list[MarketOffer]:
        gross = randomx_gross_usd_hour(machine.hashrate_hs, self.network, xmr_usd)
        return [MarketOffer(
            market=self.name,
            job_id="reserve-bid",
            gross_usd_hour=gross,
            fees_usd_hour=0,
            trust=TrustLevel.LOCAL,
            metadata={
                "network_hashrate_hs": self.network.network_hashrate_hs,
                "block_reward_xmr": self.network.block_reward_xmr,
            },
        )]
