# BUILD_NOTES — openai-native-0 (2026-09-14)

## What was built (vs brief §§1–6)

- BusinessBundle compiler (`bundle.py`): full layout incl. agent/skills/mcp/
  plugin/voice/security/telemetry/evals; refuses specs without contract
  lineage. Voice/GPT-Live sections are structural placeholders (no telephony
  on box — deferred honestly, brief §§7–8 out of scope this turn).
- Skill generator (`skill.py`): policy → deployable Skill (SKILL.md +
  policy.json + resources). Projections render from the canonical JSON;
  hand-edits impossible by construction (write path only).
- Session binder + event adapter (`session.py`): lineage travels as the 5
  metadata lookup keys; full lineage stays local. Unknown event types pass
  through (acom-openai precedent), normalized schema is ours permanently.
- MCP servers (`mcp_servers.py`): stdlib stdio JSON-RPC with qp.authorize /
  qp.verify / gg.search. Gateway enforces QP itself per call (proven: approval
  granted + no grant → still REFUSED).
- Vault split (`vault.py`): read-only → Vault, mutation/value/identity → QP
  gateway. Brief's six examples encoded as law.
- Approvals (`approvals.py`): two belts, either refuses. `enforce()` is the
  independent server-side check (bypass-proof by test).
- Acceptance chain (`chain.py`): session→read→grant→enforce→readback→
  trajectory, all SIMULATED and labeled. Disagreeing readback stops the
  chain AFTER auth passed — the exact technical-vs-economic split (§14
  of the idea doc family).

## Peer review per the brief

1. "No new kernel" — PASS: zero gate/receipt/grant semantics invented;
   everything delegates to ab1/ab2/ab3/trajectory/adapters.
2. "Approval != authority" — PASS by test (`test_both_belts_and_bypass_proof`).
3. "Agent never sees raw write credential" — PASS by construction: chain
   holds only the demo seed (labeled), server takes grants not keys.
4. "Normalize, don't adopt, event schema" — PASS: fixed normalized record,
   raw_type preserved, unknowns pass through.
5. Bugs found by tests (fixed): tool→capability key swap in `enforce`,
   two wrong relative-path depths (`skill.py`, `chain.py`), one Cyrillic
   token in a template string (repo now scanned clean).
6. Honest gaps: live Agents API (no key), GPT-Live-1, plugin surface
   generation, OPA/Rego+WASM judges — all deferred, none faked.

## Verification

14/14 tests (`test_openai_native.py`), plus GO.sh chain. Simulation only:
no network, no key, no spend.
