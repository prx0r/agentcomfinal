"""Approvals: OpenAI approval is the first belt, QP the authoritative one.

approval != authority (boxed, brief). Flow: agent proposes action ->
OpenAI approval gate (pause/resume) -> AgentCom qp.authorize callback ->
QP grant/scope/budget/asset/freshness checks -> PASS/REFUSE. The MCP
gateway enforces independently (enforce()), so bypassing the approval
layer changes nothing.
"""
from . import mcp_servers


def request_approval(action, approval_policy="always"):
    """First belt: does this action need human approval? Pure policy."""
    if approval_policy == "always":
        return {"needed": True, "belt": "openai-approval"}
    if approval_policy == "consequential-only":
        return {"needed": bool(action.get("consequential", False)),
                "belt": "openai-approval"}
    return {"needed": False, "belt": "none"}


def authorize(action, grant, facts, now, deps=None):
    """Authoritative belt: QP grant validation via the gateway."""
    return mcp_servers.call("qp.authorize",
                            {"action": action.get("capability", ""),
                             "grant": grant, "facts": facts, "now": now}, deps)


def decide(action, grant, facts, now, approval="granted", deps=None):
    """Both belts. approval in granted|denied|skipped. Returns
    {decision: PROCEED|REFUSE, belts: {...}}. Either belt refuses -> REFUSE."""
    belts = {"approval": approval}
    if approval == "denied":
        return {"decision": "REFUSE", "belts": belts, "reason": "approval-denied"}
    auth = authorize(action, grant, facts, now, deps)
    belts["qp"] = "PASS" if auth.get("authorized") else "REFUSE"
    if not auth.get("authorized"):
        return {"decision": "REFUSE", "belts": belts,
                "reason": auth.get("reason", "qp-refused")}
    return {"decision": "PROCEED", "belts": belts, "reason": "both-belts-pass"}


def enforce(tool, params, deps=None):
    """Independent MCP-side enforcement. Called by the server on every
    consequential tool invocation regardless of prior approvals."""
    if tool in ("company.send_email", "marketplace.purchase"):
        cap = {"company.send_email": "email.send",
               "marketplace.purchase": "marketplace.purchase"}[tool]
        return mcp_servers.call(
            "qp.authorize",
            {"action": cap, "grant": (params or {}).get("grant", {}),
             "facts": (params or {}).get("facts", {}),
             "now": (params or {}).get("now", "")}, deps)
    return {"authorized": True, "reason": "non-consequential"}
