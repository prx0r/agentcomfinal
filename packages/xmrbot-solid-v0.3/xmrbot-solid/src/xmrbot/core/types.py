from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class RiskClass(str, Enum):
    R0 = "R0-read"
    R1 = "R1-local-change"
    R2 = "R2-sensitive-financial"
    DISABLED = "disabled"


class SourceRef(BaseModel):
    name: str
    kind: str = "derived"
    url: str | None = None


class Observed(BaseModel, Generic[T]):
    value: T
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: SourceRef
    confidence: float = Field(default=1.0, ge=0, le=1)
    methodology: str | None = None


class NetworkSnapshot(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    height: int = Field(ge=0)
    difficulty: float = Field(gt=0)
    target_seconds: float = Field(default=120, gt=0)
    estimated_hashrate_hs: float = Field(gt=0)
    reward_xmr: float = Field(default=0.6, gt=0)
    xmr_usd: float = Field(gt=0)
    mempool_transactions: int = Field(default=0, ge=0)
    fee_per_byte_atomic: int = Field(default=0, ge=0)
    source: str = "seed"
    confidence: float = Field(default=0.5, ge=0, le=1)

    @property
    def blocks_per_day(self) -> float:
        return 86400.0 / self.target_seconds

    @property
    def daily_emission_xmr(self) -> float:
        return self.reward_xmr * self.blocks_per_day

    @property
    def hashprice_xmr_per_khs_day(self) -> float:
        return (1000.0 / self.estimated_hashrate_hs) * self.daily_emission_xmr

    @property
    def hashprice_usd_per_khs_day(self) -> float:
        return self.hashprice_xmr_per_khs_day * self.xmr_usd


class CPURecord(BaseModel):
    slug: str
    manufacturer: str
    model: str
    architecture: str
    cores: int = Field(gt=0)
    threads: int = Field(gt=0)
    l3_mb: float = Field(ge=0)
    tdp_w: float = Field(gt=0)
    benchmark_hashrate_hs: float = Field(gt=0)
    benchmark_watts: float | None = Field(default=None, gt=0)
    reference_price_usd: float | None = Field(default=None, ge=0)
    source: str
    verified: bool = False


class ProfitabilityRequest(BaseModel):
    hashrate_hs: float = Field(gt=0)
    watts: float = Field(ge=0)
    electricity_usd_kwh: float = Field(ge=0)
    hardware_cost_usd: float = Field(default=0, ge=0)
    amortization_months: float = Field(default=0, ge=0)
    xmr_usd: float | None = Field(default=None, gt=0)
    pool_fee_pct: float = Field(default=0, ge=0, lt=100)


class ProfitabilityResult(BaseModel):
    expected_xmr_day: float
    expected_xmr_month: float
    expected_xmr_year: float
    gross_usd_day: float
    electricity_usd_day: float
    depreciation_usd_day: float
    pool_fee_usd_day: float
    net_usd_day: float
    effective_cost_per_xmr_usd: float | None
    break_even_xmr_price_usd: float | None
    network_hashrate_hs: float
    methodology: str = "randomx-profitability-v1"


class MineOrBuyRequest(BaseModel):
    budget_usd: float = Field(gt=0)
    hardware_cost_usd: float = Field(gt=0)
    hashrate_hs: float = Field(gt=0)
    watts: float = Field(ge=0)
    electricity_usd_kwh: float = Field(ge=0)
    months: int = Field(default=24, gt=0, le=120)
    monthly_difficulty_growth_pct: float = Field(default=0)
    residual_value_pct: float = Field(default=30, ge=0, le=100)
    xmr_usd: float | None = Field(default=None, gt=0)


class ToolMeta(BaseModel):
    name: str
    description: str
    risk_class: RiskClass
    requires_user_approval: bool
    touches_private_keys: bool = False
    moves_funds: bool = False
    network_access: bool = False
    input_schema: dict[str, Any]
