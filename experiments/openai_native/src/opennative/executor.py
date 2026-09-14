"""Scripted executor: OpenAIAgentsExecutor v0 (offline-first).

Runs a scripted tool session against our MCP gateway and records normalized
session events (session.py shape). No key, no network: scripted fixtures
stand in for the live Agents API until credentials exist — then ONLY the
transport swaps (script runner -> real session stream), never the record
shape. Real-SDK construction is proven separately (test_wire_live.py).
"""
from . import mcp_servers, session


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
