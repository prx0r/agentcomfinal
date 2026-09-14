# CANONICAL.md — module ownership (frozen 2026-09-14)

Nine modules, one owner each. Anything not listed is a domain pack or a
view. Experimental history lives in `agentcombuild/autobuild{1,2,3}` and
`agentcombuild/agentloop` — frozen, tested, referenced, never extended.
New canonical work goes only in the paths below.

| # | Module | Owns | Canonical path | Status |
|---|---|---|---|---|
| 1 | SEESAW | strategy, scarcity, allocation; outputs StrategicDecision | `autobuild/compiler/seesaw.py` (ranking→proposal, never proof) | CANONICAL |
| 2 | AGENTCOM | portfolio, campaigns, worlds, scheduler | `core/` | CANONICAL (thin) |
| 3 | AUTOBUILD | intent → immutable Actuality Contract | `autobuild/` | CANONICAL |
| 4 | GITGOBLIN | prebuild archaeology → ReusePlan | `adapters/gitgoblin.py` + local index | CANONICAL (local backend) |
| 5 | SEED0 | tournaments, policy search, candidate lessons | `adapters/seed0.py`, lanes in `experiments/policies/` | ADAPTER |
| 6 | A-TASK | bounded work DAG, DONE authority | `adapters/atask.py` (subprocess, sandbox) | ADAPTER |
| 7 | REGISTRY | probes + deterministic judges | `autobuild/registry/`, `autobuild/actuality/` | CANONICAL |
| 8 | QP | truth, authority, settlement | `adapters/qp.py` (real constructors) | ADAPTER |
| 9 | TRAJECTORY | verified experience, L0–L5 ladder | `trajectory/` + `trajectory.py` | CANONICAL |

Constitution: workers propose, probes observe, validators judge, QP
commits, Seed0 compares, Seesaw allocates. Per-module prohibitions are
listed in `agentcombuild/agentcomdevplan.md` §30 and enforced by review
(`core/tests/test_core.py` asserts the structural ones).

OpenAI-native: tracing via the Agents SDK adapter
(`agentcombuild/agentloop/src/loop/tracing.py`); guardrails map to gates +
CEL judges; handoffs are gated transfers; sessions thread by
`group_id`; policy orchestration is tested offline with ScriptedModel
(see `agentcombuild/openai_native.md`).
