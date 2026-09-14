from __future__ import annotations
from xmrbot.config import settings
from xmrbot.data.db import connect
from xmrbot.data.repository import Repository
from xmrbot.data.seed import ensure_seed
from xmrbot.integrations.monerod import MoneroRPCClient
from xmrbot.procurement.registry import ProviderRegistry
from xmrbot.procurement.service import ProcurementService


class Services:
    def __init__(self, db_path: str | None = None):
        self.conn = connect(db_path)
        self.repo = Repository(self.conn)
        ensure_seed(self.repo)
        self.procurement = ProcurementService(ProviderRegistry())

    def current_network(self):
        return self.repo.latest_network()

    def network_derived(self):
        n = self.current_network()
        return {
            "daily_emission_xmr": n.daily_emission_xmr,
            "hashprice_xmr_per_khs_day": n.hashprice_xmr_per_khs_day,
            "hashprice_usd_per_khs_day": n.hashprice_usd_per_khs_day,
            "methodologies": ["estimated-network-hashrate-v1", "xmr-hashprice-v1"],
        }

    async def refresh_network(self):
        if not settings.monerod_enabled:
            return {"updated": False, "reason": "XMRBOT_MONEROD_ENABLED=0", "snapshot": self.current_network().model_dump(mode="json")}
        snap = await MoneroRPCClient().snapshot(xmr_usd=settings.xmr_usd)
        self.repo.add_network(snap)
        return {"updated": True, "snapshot": snap.model_dump(mode="json")}
