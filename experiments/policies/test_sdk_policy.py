"""Offline policy-orchestration test via ScriptedModel (venv only).

Proves the OpenAI-native testing path: deterministic multi-turn tool loops
with zero network. System python skips (no SDK); .venvs/agentcom runs live.
"""
import sys

import pytest

agents = pytest.importorskip("agents")


def test_scripted_policy_choice():
    import asyncio

    from agents import Agent, RunConfig, Runner, function_tool
    from agents.testing import (ScriptedModel, assistant_message,
                                function_call)

    @function_tool
    def check_readback(order_id: str) -> str:
        """Independent readback probe (scripted, never executed)."""
        return "found:" + order_id

    model = ScriptedModel([
        [function_call("check_readback", {"order_id": "order_9"},
                       call_id="call_1")],
        [assistant_message("VERDICT:TRUE")],
    ])
    agent = Agent(name="W-seeker3", model=model, tools=[check_readback])
    result = asyncio.run(Runner.run(
        agent, "Prove order_9 exists via independent readback.",
        run_config=RunConfig(tracing_disabled=True)))
    assert result.final_output == "VERDICT:TRUE"
    model.assert_complete()
    _ = sys.version  # silence linters about unused import in skip path
