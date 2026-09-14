# openai-native-0 — OpenAI owns cognition (working sim)

Implements `agentcombuild/gptnative.md` §§1–6 as simulated substrate:
BusinessBundle compiler, policy→Skill generator, session binder with
lineage metadata keys, event adapter → normalized telemetry, stdio MCP
servers (QP gateway enforcing independently + GitGoblin archaeology),
Vault/QP secret split, two-belt approvals, and the acceptance chain
(session→MCP→QP→readback→trajectory).

Deferred honestly: live Agents API calls (no key on box), GPT-Live-1
telephony, ChatGPT Plugin surface generation, OPA/Rego + WASM judges.

```bash
cd /agentcomfinal/experiments/openai_native
PYTHONPATH=src:/agentcomfinal/agentcombuild/agentloop/src:/agentcomfinal python3 -m pytest tests/ -q
```
