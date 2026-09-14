from __future__ import annotations
from abc import ABC
from typing import Any
import httpx
from xmrbot.procurement.models import ActionProposal, ProviderAction, ProviderDescriptor, ProviderResult, QPGrant
from xmrbot.procurement.policy import evaluate_grant
from xmrbot.procurement.receipts import make_receipt


class ProviderAdapter(ABC):
    descriptor: ProviderDescriptor

    def __init__(self, http: httpx.AsyncClient | None = None):
        self.http = http

    def capability(self, action: str):
        for c in self.descriptor.capabilities:
            if c.name == action:
                return c
        raise KeyError(f"{self.descriptor.id} does not support {action}")

    def propose(self, action: str, payload: dict[str, Any]) -> ActionProposal:
        cap = self.capability(action)
        pa = ProviderAction(provider_id=self.descriptor.id, action=action, payload=payload)
        return ActionProposal(
            proposal_id=pa.canonical_hash()[:24],
            action=pa,
            action_hash=pa.canonical_hash(),
            provider=self.descriptor,
            requires_grant=cap.requires_grant,
            executable_now=not cap.state_changing,
            notes=["State-changing operations require a QP grant and provider credentials/local daemon where applicable."] if cap.state_changing else [],
        )

    async def invoke(self, action: str, payload: dict[str, Any]) -> ProviderResult:
        raise NotImplementedError(f"{self.descriptor.id}:{action} has no direct invocation adapter")

    async def execute(self, action: str, payload: dict[str, Any], grant: QPGrant | None = None, *, amount_atomic_xmr: int | None = None, amount_usd: float | None = None):
        cap = self.capability(action)
        pa = ProviderAction(provider_id=self.descriptor.id, action=action, payload=payload)
        if cap.state_changing or cap.requires_grant:
            gate = evaluate_grant(pa, grant, amount_atomic_xmr=amount_atomic_xmr, amount_usd=amount_usd)
            if not gate.allowed:
                return {"executed": False, "gate": gate.model_dump(mode="json"), "proposal": self.propose(action, payload).model_dump(mode="json")}
        result = await self.invoke(action, payload)
        receipt = make_receipt(pa, "completed", result.model_dump(mode="json"), grant.id if grant else None)
        return {"executed": True, "result": result.model_dump(mode="json"), "receipt": receipt.model_dump(mode="json")}
