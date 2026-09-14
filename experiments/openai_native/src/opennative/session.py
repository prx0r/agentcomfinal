"""Session binder + OpenAIEventAdapter (telemetry normalizer).

Binder: lineage + contract -> Agents API session-create-shaped payload.
model/tools/vault_ids/environment/input travel; lineage travels as metadata
lookup keys (limited map — full lineage stays in our event store).

Adapter: every session event -> normalized AgentCom telemetry record
(brief schema). Our schema is permanent; the provider schema is not, so a
later provider routes through the same normalizer. Unknown event types pass
through unmapped, never silently dropped (acom-openai precedent).
"""
import hashlib
import json

METADATA_KEYS = ("project", "campaign", "contract", "plan", "policy")


def session_payload(model, tools, lineage, vault_ids=None, environment=None,
                    user_input=""):
    """Returns (payload, warnings[]). lineage: {project, campaign, contract,
    plan, policy, ...}. Unknown lineage keys stay local (map is limited)."""
    lineage = lineage or {}
    missing = [k for k in ("project", "campaign", "contract") if not lineage.get(k)]
    if missing:
        raise ValueError("lineage missing:%s" % ",".join(missing))
    metadata = {k: str(lineage[k]) for k in METADATA_KEYS if lineage.get(k)}
    return {"model": model, "tools": list(tools or []),
            "vault_ids": list(vault_ids or []),
            "environment": environment or {},
            "metadata": metadata, "input": user_input}, []


def _h(obj):
    return hashlib.sha256(json.dumps(
        obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]


def normalize_event(event, lineage=None):
    """Provider session event -> normalized telemetry record. Pure."""
    lineage = lineage or {}
    event = event if isinstance(event, dict) else {}
    etype = str(event.get("type", "unknown"))
    rec = {"event_id": str(event.get("id", "evt:" + _h(event))),
           "source": "openai.agents",
           "session_id": event.get("session_id", ""),
           "turn_id": event.get("turn_id", ""),
           "subagent_id": event.get("subagent_id", ""),
           "contract_root": lineage.get("contract", ""),
           "plan_root": lineage.get("plan", ""),
           "event_type": etype,
           "tool": event.get("tool", event.get("name", "")),
           "args_hash": _h(event.get("args", event.get("input", ""))),
           "output_hash": _h(event.get("output", "")),
           "guardrail": event.get("guardrail"),
           "approval": event.get("approval"),
           "tokens": event.get("tokens"),
           "latency_ms": event.get("latency_ms"),
           "cost_usd": event.get("cost_usd"),
           "observed_at": event.get("observed_at", ""),
           "qp_receipt": None,
           "raw_type": etype}
    return rec


def events_to_trajectory(events, lineage=None, contract_root=""):
    """Session event list -> trajectory-shaped evidence (feeds trajectory/
    bank + Seed0 lanes). Pure."""
    recs = [normalize_event(e, lineage) for e in events or []]
    tools = sorted({r["tool"] for r in recs if r["tool"]})
    return {"contract_root": contract_root or (lineage or {}).get("contract", ""),
            "events": recs, "tools_seen": tools,
            "event_count": len(recs)}
