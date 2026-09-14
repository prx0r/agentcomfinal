# openai_native.md — SDK surface map (verified 0.22.2, 2026-09-14)

Source docs: `autobuild0/vendor_docs/openai-agents/` + `~/acom-openai`
(mapping precedent: lazy imports, keyless tests, SDK owns mechanics).

| Doc | Verdict | Use here |
|---|---|---|
| tracing | ADAPTED | `agentloop/src/loop/tracing.py`: RUN→trace, attempts→custom spans, usage→generation shape, mirror fallback |
| guardrails | ADAPT | tripwire→NOGO mapping; input/output/tool guardrails become gates + CEL judges + registry entries (ab5+) |
| handoffs | ADAPT | transfers are gated delegation records with receipts (ab5+); never bare LLM routing |
| sessions / conversations | ADAPT | trace `group_id` threads runs per project; server conversations out of scope |
| MCP | ADAPT | research backends + plugin tools fronted by ab2 grants; `require_approval` mirrors our grant gate |
| human_in_the_loop | ADAPT | interruptions→RunState→approve→resume maps to A-ask/H-task; `needs_approval` precedent in acom-openai |
| results | ADAPT | `final_output` vs audit split mirrors prose-vs-artifact; usage feeds calibration |
| context | ADAPT | identity/budget ride policy+compiler state; secrets never serialized |
| models | REFERENCE | routing/retries background for policy model selection |
| testing | ADOPTED | ScriptedModel offline policy tests (`experiments/policies/test_sdk_policy.py`, venv) |
| ref/tracing | ADAPT | processor/exporter interface behind mirror + reconciler |

Rule: native where the SDK owns mechanics (execution, tracing, testing);
ours where truth lives (gates, receipts, scheduler). Never both.
