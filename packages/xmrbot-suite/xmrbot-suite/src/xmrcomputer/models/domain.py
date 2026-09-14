from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field


class TrustLevel(str, Enum):
    LOCAL = "local"
    VERIFIED = "verified"
    UNTRUSTED = "untrusted"


class MachineProfile(BaseModel):
    cpu_model: str = "unknown"
    hashrate_hs: float = Field(gt=0)
    watts_at_load: float = Field(ge=0)
    electricity_usd_kwh: float = Field(ge=0)
    hardware_cost_usd: float = Field(default=0, ge=0)
    amortization_hours: float = Field(default=0, ge=0)

    @property
    def energy_usd_hour(self) -> float:
        return (self.watts_at_load / 1000.0) * self.electricity_usd_kwh

    @property
    def amortization_usd_hour(self) -> float:
        if self.hardware_cost_usd <= 0 or self.amortization_hours <= 0:
            return 0.0
        return self.hardware_cost_usd / self.amortization_hours


class MarketOffer(BaseModel):
    market: str
    job_id: str
    gross_usd_hour: float = Field(ge=0)
    fees_usd_hour: float = Field(default=0, ge=0)
    trust: TrustLevel = TrustLevel.UNTRUSTED
    requires_direct_network: bool = False
    metadata: dict = Field(default_factory=dict)


class RankedOffer(BaseModel):
    offer: MarketOffer
    gross_xmr_hour: float
    net_xmr_hour: float
    net_usd_hour: float
    accepted: bool
    reason: str


class Decision(BaseModel):
    selected: RankedOffer | None
    ranked: list[RankedOffer]
