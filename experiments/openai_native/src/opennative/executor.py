"""Scripted + LIVE executor: OpenAIAgentsExecutor v0/v1.

SCRIPTED (default): scripted tool session against our MCP gateway, normalized
session events. No key, no network.
LIVE: real managed Agents API session via the official `openai` client
(beta.agents.sessions): environment type none, lineage in metadata, event
stream normalized through the SAME adapter. Requires OPENAI_API_KEY and a
supported client version; otherwise raises NotConfigured (never faked).
"""
import os

from . import mcp_servers, session


class NotConfigured(RuntimeError):
    pass


def live_available():
    """Probe the live path without network: package + API surface + key."""
    try:
        import openai  # noqa: F401
        from openai import OpenAI  # noqa: F401
    except ImportError:
        return False, "no-openai-package"
    if not os.environ.get("OPENAI_API_KEY"):
        return False, "no-api-key"
    try:
        client = OpenAI()
        beta = getattr(client, "beta", None)
        agents = getattr(beta, "agents", None)
        sessions = getattr(agents, "sessions", None)
        if not callable(getattr(sessions, "create", None)):
            return False, "no-sessions-create"
    except Exception as exc:  # noqa: BLE001
        return False, "client-error:%s" % type(exc).__name__
    return True, "ok"


def run_scripted(script, lineage=None, session_id="sess-sim0"):
    """script: [{tool, args}]. Each step calls the MCP gateway (which
    enforces QP itself) and normalizes one session event. Returns
    {events, trajectory, errors}. Unknown tools fail closed via gateway."""
    lineage = lineage or {}
    events, errors = [], []
    for i, step in enumerate(script or []):
        tool = step.get("tool", "")
        try:
            out = mcp_servers.call(tool, step.get("args", {}))
            events.append({"id": "evt-%d" % i, "type": "tool.call",
                           "tool": tool, "session_id": session_id,
                           "turn_id": "turn-0",
                           "args": step.get("args", {}),
                           "output": {"ok": True,
                                      "keys": sorted(out.keys())[:8]}})
        except Exception as exc:  # noqa: BLE001 - errors are events
            events.append({"id": "evt-%d" % i, "type": "tool.error",
                           "tool": tool, "session_id": session_id,
                           "turn_id": "turn-0", "output": {"error": str(exc)[:160]}})
            errors.append(tool)
    traj = session.events_to_trajectory(events, lineage)
    return {"events": events, "trajectory": traj, "errors": errors,
            "mode": "SCRIPTED-OFFLINE"}


def build_session_kwargs(user_input, lineage=None, model="gpt-4o",
                         instructions="", vault_ids=()):
    """Session-create payload in the INSTALLED openai schema (verified
    against openai==3.13.0: agent config under `agent=`, NOT top-level
    model/tools). Pure constructor — no network, always testable."""
    lineage = lineage or {}
    metadata = {k: str(lineage[k]) for k in
                ("project", "campaign", "contract", "plan", "policy")
                if lineage.get(k)}
    return {"environment": {"type": "none"},
            "agent": {"model": model, "instructions": instructions},
            "input": user_input, "metadata": metadata,
            "vault_ids": list(vault_ids or [])}


def normalize_typed_event(event, session_id=""):
    """Provider event object -> plain dict. model_dump when present;
    plain dicts pass through; anything else is RECORDED as unmapped
    (refuse_unknown_event_type — never silently dropped)."""
    if hasattr(event, "model_dump"):
        try:
            raw = event.model_dump(mode="json")
        except Exception as exc:  # noqa: BLE001
            return {"unmapped": True, "reason": "dump-failed:%s"
                    % type(exc).__name__, "session_id": session_id}
    elif isinstance(event, dict):
        raw = event
    else:
        return {"unmapped": True,
                "type": type(event).__qualname__ if hasattr(type(event),
                                                            "__qualname__")
                else str(type(event))[:80],
                "session_id": session_id}
    if not isinstance(raw, dict):
        return {"unmapped": True, "type": "non-dict-dump",
                "session_id": session_id}
    raw = dict(raw)
    raw.setdefault("session_id", session_id)
    return raw


def run_live(user_input, lineage=None, model="gpt-4o", instructions="",
             vault_ids=()):
    """LIVE managed session: create -> stream events -> normalize -> close.

    environment type none (no sandbox). Lineage bound as session metadata
    lookup keys. Raises NotConfigured without package/surface/key — the
    caller decides (NOT_CONFIGURED is a result, never PASS). No
    consequential actions happen here: this transport only talks and reads
    tool results.
    """
    ok, reason = live_available()
    if not ok:
        raise NotConfigured(reason)
    import openai  # noqa: E402
    lineage = lineage or {}
    kwargs = build_session_kwargs(user_input, lineage, model, instructions,
                                  vault_ids)
    client = openai.OpenAI()
    sess = client.beta.agents.sessions.create(**kwargs)
    events, unmapped = [], 0
    try:
        stream = client.beta.agents.sessions.events.stream(sess.id)
        for event in stream:
            raw = normalize_typed_event(event, getattr(sess, "id", ""))
            if raw.get("unmapped"):
                unmapped += 1
            events.append(raw)
    finally:
        try:
            stream.close()
        except Exception:  # noqa: BLE001
            pass
    texts = [str(e.get("text", "")) for e in events
             if isinstance(e, dict) and e.get("text")]
    usage = None
    for e in events:
        if isinstance(e, dict) and isinstance(e.get("usage"), dict):
            usage = e["usage"]
    traj = session.events_to_trajectory(events, lineage)
    return {"mode": "LIVE", "session_id": getattr(sess, "id", ""),
            "provider": "openai", "events": events,
            "event_count": len(events), "unmapped": unmapped,
            "output": " ".join(texts)[:2000], "usage": usage,
            "trajectory": traj, "errors": []}
