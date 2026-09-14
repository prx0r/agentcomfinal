# domainpacks/chatgpt — ChatGPT/Codex plugin conformance (reference, not root)

Canonical kit: `packages/agentcom-plugin-canonical/` (schemas, lint,
prompts, rubric) + `packages/agent-plugin-factory/` (scorer/packetizer).
This pack does NOT define AgentCom's universal ontology (devplan §19).

A plugin target extends a generic Autobuild contract with: routing evals,
submission constraints, tool schema, auth, CSP, review cases. Plugin state
remains an adapter/distribution concern. Factory work (E-phase) will wire
`agent-plugin-factory` to consume the canonical schemas directly.
