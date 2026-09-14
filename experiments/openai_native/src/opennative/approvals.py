"""Approvals: OpenAI approval is the first belt, QP the authoritative one.

approval != authority (boxed, brief). Flow: agent proposes action ->
OpenAI approval gate (pause/resume) -> AgentCom qp.authorize callback ->
QP grant/scope/budget/asset/freshness checks -> PASS/REFUSE. The MCP
gateway enforces independently (enforce()), so bypassing the approval
layer changes nothing.
"""
from . import mcp_servers


# Tool registry: consequence class + capability. Closed world — anything
# not listed here REFUSES (fail closed). Only explicitly classified
# NON_CONSEQUENTIAL tools bypass QP authority.
TOOL_REGISTRY = {
    "company.send_email": ("consequential", "email.send"),
    "marketplace.purchase": ("consequential", "marketplace.purchase"),
    "company.lookup": ("non-consequential", None),
    "business.lookup": ("non-consequential", None),
    "gg.search": ("non-consequential", None),
}


def request_approval(action, approval_policy="always"):
    """First belt: does this action need human approval? Pure policy.
    Unknown policies REFUSE-safe (needed=True); only explicit "never"
    opts out, and opting out never affects the QP belt."""
    if approval_policy == "always":
        return {"needed": True, "belt": "openai-approval"}
    if approval_policy == "consequential-only":
        return {"needed": bool(action.get("consequential", False)),
                "belt": "openai-approval"}
    if approval_policy == "never":
        return {"needed": False, "belt": "none"}
    return {"needed": True, "belt": "unknown-policy-refuse"}


def authorize(action, grant, facts, now, deps=None):
    """Authoritative belt: real QP grant validation via the gateway.
    The full action dict travels (capability + spend/risk fields) — never
    a bare capability string, which would blind the constraint checks."""
    return mcp_servers.call("qp.authorize",
                            {"action": dict(action or {}),
                             "grant": grant, "facts": facts, "now": now}, deps)


def decide(action, grant, facts, now, approval="granted", deps=None):
    """Both belts. approval must be exactly "granted" to proceed —
    denied, skipped, missing, or anything else REFUSES. Either belt
    refuses -> REFUSE."""
    belts = {"approval": approval}
    if approval != "granted":
        return {"decision": "REFUSE", "belts": belts,
                "reason": "approval-not-granted:%s" % (approval,)}
    auth = authorize(action, grant, facts, now, deps)
    belts["qp"] = "PASS" if auth.get("authorized") else "REFUSE"
    if not auth.get("authorized"):
        return {"decision": "REFUSE", "belts": belts,
                "reason": auth.get("reason", "qp-refused")}
    return {"decision": "PROCEED", "belts": belts, "reason": "both-belts-pass"}


def enforce(tool, params, deps=None):
    """Independent MCP-side enforcement. Called by the server on every
    tool invocation regardless of prior approvals. Unknown tools REFUSE;
    only registry-declared NON_CONSEQUENTIAL tools bypass QP."""
    entry = TOOL_REGISTRY.get(tool)
    if entry is None:
        return {"authorized": False, "reason": "unknown-tool:REFUSE"}
    kind, cap = entry
    if kind != "consequential":
        return {"authorized": True, "reason": "non-consequential"}
    return mcp_servers.call(
        "qp.authorize",
         {"action": cap, "grant": (params or {}).get("grant", {}),
          "facts": (params or {}).get("facts", {}),
          "now": (params or {}).get("now", "")}, deps)
