from xmrcomputer.models.domain import RankedOffer, TrustLevel
from xmrcomputer.models.settings import Policy


def apply_policy(ranked: RankedOffer, policy: Policy) -> RankedOffer:
    offer = ranked.offer
    accepted, reason = True, "accepted"
    if offer.market not in policy.allowed_markets:
        accepted, reason = False, "market not allowlisted"
    elif offer.trust == TrustLevel.UNTRUSTED and not policy.allow_untrusted_jobs:
        accepted, reason = False, "untrusted jobs disabled"
    elif offer.requires_direct_network and not policy.privacy.allow_direct_network:
        accepted, reason = False, "direct network prohibited by privacy profile"
    elif ranked.net_xmr_hour < policy.minimum_net_xmr_hour:
        accepted, reason = False, "below minimum net XMR/hour"
    return ranked.model_copy(update={"accepted": accepted, "reason": reason})
