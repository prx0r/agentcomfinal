from __future__ import annotations
from xmrbot.procurement.models import ProcurementIntent
from xmrbot.procurement.registry import ProviderRegistry

CATEGORY_ALIASES={
    "server":["vps","hosting","infrastructure"],
    "domain":["domains","infrastructure"],
    "hire":["labor","jobs","freelance","services"],
    "buy":["marketplace","goods","gift_cards","concierge"],
    "gas":["gas","evm"],
    "swap":["swap","exchange"],
    "esim":["esim","connectivity"],
    "shipping":["shipping","logistics"],
    "fundraise":["fundraising","crowdfunding"],
}


def route(intent: ProcurementIntent, registry: ProviderRegistry) -> dict:
    text=(intent.objective+" "+(intent.category or "")).lower()
    wanted=set()
    for token,cats in CATEGORY_ALIASES.items():
        if token in text: wanted.update(cats)
    if intent.category: wanted.add(intent.category.lower())
    rows=[]
    for p in registry.all():
        category_match = (not wanted) or bool(wanted.intersection(set(p.category)))
        preferred_bonus = .15 if p.id in intent.preferred_providers else 0
        escrow_bonus = .12 if intent.escrow_required and any("escrow" in (c.name+c.description).lower() for c in p.capabilities) else 0
        mode_bonus = .08 if any(c.mode.value in {"native_api","local_api"} for c in p.capabilities) else 0
        score = p.agentability*.55 + intent.privacy_weight*.20 + preferred_bonus + escrow_bonus + mode_bonus
        if category_match:
            rows.append({"provider":p.model_dump(mode="json"),"score":round(min(score,1),4),"why":{"category_match":category_match,"agentability":p.agentability,"api_bonus":mode_bonus,"escrow_bonus":escrow_bonus,"preferred_bonus":preferred_bonus}})
    rows.sort(key=lambda x:x["score"],reverse=True)
    return {"intent":intent.model_dump(mode="json"),"routes":rows[:12],"note":"Routing optimizes provider fit/agentability/privacy metadata. It does not guarantee legality, anonymity, availability, price, or counterparty safety."}
