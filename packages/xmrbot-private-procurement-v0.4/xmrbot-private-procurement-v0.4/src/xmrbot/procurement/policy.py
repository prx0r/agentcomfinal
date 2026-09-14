from __future__ import annotations
from .models import GateResult, ProviderAction, QPGrant


def evaluate_grant(action: ProviderAction, grant: QPGrant | None, amount_atomic_xmr: int | None = None, amount_usd: float | None = None) -> GateResult:
    h = action.canonical_hash()
    checks: list[dict] = []
    if grant is None:
        return GateResult(allowed=False, action_hash=h, checks=[{"check":"grant_present","ok":False}])

    def add(name: str, ok: bool, detail=None):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    add("grant_approved", grant.approved)
    add("grant_not_expired", not grant.is_expired())
    add("provider_allowed", not grant.allowed_providers or action.provider_id in grant.allowed_providers)
    add("action_allowed", not grant.allowed_actions or action.action in grant.allowed_actions)
    add("payload_bound", grant.exact_payload_hash is None or grant.exact_payload_hash == h)
    if grant.max_atomic_xmr is not None and amount_atomic_xmr is not None:
        add("xmr_budget", amount_atomic_xmr <= grant.max_atomic_xmr, {"amount":amount_atomic_xmr,"limit":grant.max_atomic_xmr})
    if grant.max_usd is not None and amount_usd is not None:
        add("usd_budget", amount_usd <= grant.max_usd, {"amount":amount_usd,"limit":grant.max_usd})
    return GateResult(allowed=all(c["ok"] for c in checks), checks=checks, action_hash=h, grant_id=grant.id)
