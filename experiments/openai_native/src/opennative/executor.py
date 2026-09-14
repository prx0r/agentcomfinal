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


def run_live(user_input, lineage=None, model="gpt-4o", tools=()):
    """LIVE managed session: create -> stream events -> normalize -> close.

    environment type none (no sandbox). Lineage bound as session metadata
    lookup keys. Raises NotConfigured without package/surface/key — the
    caller decides (tests skip; CLI refuses to fake it). No consequential
    actions happen here: this transport only talks and reads tool results.
    """
    ok, reason = live_available()
    if not ok:
        raise NotConfigured(reason)
    import openai  # noqa: E402
    lineage = lineage or {}
    metadata = {k: str(lineage[k]) for k in
                ("project", "campaign", "contract", "plan", "policy")
                if lineage.get(k)}
    client = openai.OpenAI()
    sess = client.beta.agents.sessions.create(
        model=model, tools=list(tools or []),
        environment={"type": "none"}, metadata=metadata, input=user_input)
    events = []
    try:
        stream = client.beta.agents.sessions.events.stream(sess.id)
        for event in stream:
            if isinstance(event, dict):
                event = dict(event)
                event.setdefault("session_id", sess.id)
                events.append(event)
    finally:
        try:
            stream.close()
        except Exception:  # noqa: BLE001
            pass
    traj = session.events_to_trajectory(events, lineage)
    return {"session_id": sess.id, "events": events, "trajectory": traj,
            "errors": [], "mode": "LIVE"}
