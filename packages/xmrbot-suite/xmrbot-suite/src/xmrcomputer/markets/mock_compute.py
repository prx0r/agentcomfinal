from xmrcomputer.markets.base import MarketAdapter
from xmrcomputer.models.domain import MachineProfile, MarketOffer, TrustLevel


class MockComputeAdapter(MarketAdapter):
    name = "mock-compute"

    def __init__(self, usd_per_core_equivalent_hour: float = 0.08):
        self.rate = usd_per_core_equivalent_hour

    async def offers(self, machine: MachineProfile, *, xmr_usd: float) -> list[MarketOffer]:
        # MVP stand-in: infer a coarse 'core-equivalent' from RandomX hashrate.
        equivalents = max(machine.hashrate_hs / 2000.0, 1.0)
        return [MarketOffer(
            market=self.name,
            job_id="demo-useful-compute",
            gross_usd_hour=equivalents * self.rate,
            fees_usd_hour=0.01,
            trust=TrustLevel.VERIFIED,
            metadata={"note": "simulated paid CPU task"},
        )]
