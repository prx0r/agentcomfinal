from __future__ import annotations
from datetime import datetime, timedelta, timezone
import uuid
from xmrbot.procurement.models import ProcurementIntent, ProviderAction, QPGrant, ATOMIC_UNITS
from xmrbot.procurement.registry import ProviderRegistry
from xmrbot.procurement.router import route
from xmrbot.procurement.policy import evaluate_grant
from xmrbot.procurement.receipts import verify_receipt


class ProcurementService:
    def __init__(self, registry: ProviderRegistry): self.registry=registry
    def providers(self, query=""): return [p.model_dump(mode="json") for p in self.registry.search(query)]
    def provider(self, provider_id): return self.registry.get(provider_id).model_dump(mode="json")
    def route(self, **kwargs): return route(ProcurementIntent(**kwargs), self.registry)
    def propose(self, provider_id, action, payload): return self.registry.adapter(provider_id).propose(action,payload).model_dump(mode="json")
    async def invoke_read(self, provider_id, action, payload):
        cap=self.registry.adapter(provider_id).capability(action)
        if cap.state_changing: return self.propose(provider_id,action,payload)
        return (await self.registry.adapter(provider_id).invoke(action,payload)).model_dump(mode="json")
    def grant_request(self, provider_id: str, action: str, payload: dict, max_xmr: float | None=None, max_usd: float | None=None, ttl_minutes: int=30):
        pa=ProviderAction(provider_id=provider_id,action=action,payload=payload)
        return QPGrant(
            id="grant_"+uuid.uuid4().hex[:16], capability=f"provider.{provider_id}.{action}", approved=False,
            max_atomic_xmr=int(max_xmr*ATOMIC_UNITS) if max_xmr is not None else None, max_usd=max_usd,
            allowed_providers=[provider_id], allowed_actions=[action], exact_payload_hash=pa.canonical_hash(),
            expires_at=datetime.now(timezone.utc)+timedelta(minutes=ttl_minutes),
            predicates=["exact provider", "exact action", "exact payload hash", "budget bound", "expiry bound"],
        ).model_dump(mode="json")
    def gate(self, action: dict, grant: dict | None, amount_atomic_xmr=None, amount_usd=None):
        return evaluate_grant(ProviderAction(**action), QPGrant(**grant) if grant else None, amount_atomic_xmr, amount_usd).model_dump(mode="json")
    def verify_receipt(self, receipt: dict, action: dict, response: dict):
        from xmrbot.procurement.models import ActionReceipt
        return verify_receipt(ActionReceipt(**receipt), ProviderAction(**action), response)
