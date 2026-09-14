from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from typing import Any
from pydantic import BaseModel, Field

ATOMIC_UNITS = 10**12

class IntegrationMode(str, Enum):
    NATIVE_API = "native_api"
    LOCAL_API = "local_api"
    READ_ONLY_WEB = "read_only_web"
    MANUAL_BRIDGE = "manual_bridge"
    UPCOMING_API = "upcoming_api"

class CapabilityClass(str, Enum):
    DISCOVER = "discover"
    QUOTE = "quote"
    PROPOSE = "propose"
    EXECUTE = "execute"
    STATUS = "status"
    VERIFY = "verify"

class ProviderCapability(BaseModel):
    name: str
    capability_class: CapabilityClass
    mode: IntegrationMode
    state_changing: bool = False
    requires_grant: bool = False
    description: str
    endpoint_hint: str | None = None

class ProviderDescriptor(BaseModel):
    id: str
    name: str
    category: list[str]
    canonical_url: str
    accepts_xmr: bool = True
    status: str = "active"
    agentability: float = Field(ge=0, le=1)
    privacy_notes: list[str] = []
    capabilities: list[ProviderCapability]
    source_urls: list[str] = []
    caveats: list[str] = []

class ProcurementIntent(BaseModel):
    objective: str
    category: str | None = None
    max_xmr: float | None = Field(default=None, ge=0)
    max_usd: float | None = Field(default=None, ge=0)
    privacy_weight: float = Field(default=0.8, ge=0, le=1)
    escrow_required: bool = False
    max_kyc_level: int | None = Field(default=None, ge=0, le=4)
    preferred_providers: list[str] = []

class ProviderAction(BaseModel):
    provider_id: str
    action: str
    payload: dict[str, Any] = {}

    def canonical_hash(self) -> str:
        raw = json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
        return sha256(raw.encode()).hexdigest()

class QPGrant(BaseModel):
    id: str
    capability: str
    approved: bool = False
    max_atomic_xmr: int | None = Field(default=None, ge=0)
    max_usd: float | None = Field(default=None, ge=0)
    allowed_providers: list[str] = []
    allowed_actions: list[str] = []
    exact_payload_hash: str | None = None
    expires_at: datetime | None = None
    predicates: list[str] = []

    def is_expired(self) -> bool:
        return bool(self.expires_at and datetime.now(timezone.utc) >= self.expires_at.astimezone(timezone.utc))

class GateResult(BaseModel):
    allowed: bool
    checks: list[dict[str, Any]]
    action_hash: str
    grant_id: str | None = None

class ActionProposal(BaseModel):
    proposal_id: str
    action: ProviderAction
    action_hash: str
    provider: ProviderDescriptor
    requires_grant: bool
    executable_now: bool = False
    notes: list[str] = []

class ActionReceipt(BaseModel):
    receipt_id: str
    provider_id: str
    action: str
    action_hash: str
    grant_id: str | None = None
    status: str
    response_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    proof_type: str = "deterministic_hash_receipt"
    response_summary: dict[str, Any] = {}

class ProviderResult(BaseModel):
    provider_id: str
    action: str
    data: dict[str, Any]
    source: str
    mode: IntegrationMode
    live: bool = False
