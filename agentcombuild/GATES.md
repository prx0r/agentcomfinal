# GATES.md — the full gate catalog (all layers)

Conventions (qp law): unknown gate id = FAIL, raising gate = FAIL,
missing evidence = UNKNOWN/FAIL (never PASS), `program_hash` = sha256 of the
gate source, new logic = new gate id. Attempt 1 implements L0; attempt 2
adds L1; L2+ are specified here so later attempts don't reinvent them.

## L0 — plan/spec/seesaw gates (ab1, live)

| id | inputs | PASS iff |
|---|---|---|
| `specgate-v1` | spec_verdict | plan valid: goal + acceptance, every feature has acceptance + declared kind+ref evidence |
| `evidence-declared-v1` | features[] | every feature carries ≥1 {kind, ref} evidence |
| `two-sources-v1` | sources[] | ≥2 distinct source ids |
| `score-threshold-v1` | value, min | RETIRED from canonical path (devplan §3): heuristic scores are priorities, never proof. Kept in frozen ab1 only; canonical compiler ranks via `autobuild/compiler/seesaw.py` (proposal, no verdict). |
| `no-duplicate-v1` | items[] | ids unique |
| `plugin-lint-v1` (specgate.check_plugin) | plugin spec | name+version, tools with name+description, provider{name,tos} for third-party/auth tools |

## L1 — authority gates (ab2, live after this session)

| id | inputs | PASS iff |
|---|---|---|
| `grant-valid-v1` | grant, now | signature verifies, not expired, subject matches |
| `grant-scope-v1` | grant, action, facts | capability matches, constraints (max_risk_usd/max_calls/asset) hold, predicates evaluate true; unknown constraint key = FAIL |
| `consequential-requires-grant-v1` | action, grant? | non-consequential → PASS; consequential without valid in-scope grant → REFUSED/FAIL |
| `receipt-signed-v1` | receipt, pubkey | receipt id recomputes AND ed25519 signature verifies |

## L2 — contract/lineage gates (attempts 4–5)

| id | PASS iff |
|---|---|
| `contract-invariant-v1` | same WHAT + new HOW → ContractRoot unchanged, PlanRoot changed |
| `acceptance-frozen-v1` | worker-edited acceptance produces new ContractRoot; old task id cannot adopt it |
| `lineage-complete-v1` | all 7 roots present and hash-linked for the run |
| `proven-requires-receipt-v1` | PROVEN display backed by verified QP receipt, else NOT PROVEN |
| `prebuild-mandatory-v1` | ReusePlan exists (or recorded exemption) before BUILD enters A-Task |

## L3 — evidence/world gates (attempts 5–8)

| id | PASS iff |
|---|---|
| `world-ceiling-v1` | claim class ≤ world evidence ceiling (A_TRUTH < B_DEMAND < C_ECONOMIC < D_SCARCE_STATE) |
| `no-sim-graduation-v1` | market/economic claims never graduate from simulation worlds |
| `circuits-separate-v1` | TechnicalCircuit and EconomicCircuit evaluated independently; eng success ≠ market proof |
| `verified-outcomes-only-v1` | stats ingest only qp.verify==PASS outcomes |
| `missing-readback-unknown-v1` | action ok + no readback → outcome UNKNOWN |
| `commits-not-proof-v1` | repo activity alone → CODE_PRESENT, never PROVEN |

## L4 — scheduler/human gates (attempts 5–8)

| id | PASS iff |
|---|---|
| `infra-cannot-outbid-v1` | infrastructure never wins a scarce permission over an asset campaign; pulled only as support |
| `two-queues-v1` | human items typed StrategicQuestion xor execution H-task, rendered on one surface |
| `promotion-governed-v1` | primitive promotion carries its own receipt |

## Adversarial suite (idea §24 → tests)

self-attest → NOT PROVEN · no grant → REFUSED · wrong scope → REFUSED ·
route swap → PlanRootΔ/ContractRoot= · acceptance edit → new ContractRoot ·
missing readback → UNKNOWN · commits only → CODE_PRESENT.
