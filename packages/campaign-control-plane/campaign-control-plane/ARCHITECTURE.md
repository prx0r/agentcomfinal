
# Architecture

## 1. CampaignSpec
A frozen project thesis: user/job, why-now, distribution, moat, falsifiers, repo binding, shared components and checkpoint DAG.

## 2. CapabilityCheckpoint
One observable behavior. It contains: dependencies, user behavior, exact implication, input/output data types, evidence contract, deterministic validator, M/H/A authority class, minimum proof level and reward.

## 3. Evidence stream
Runs emit normalized JSONL events. External adapters should log request intent, sanitized request metadata, response identifiers/status, artifact hashes, active probes and security decisions. Secrets never enter the stream.

## 4. Validator
Reference semantics are stdlib Python today. Validators are deliberately tiny and deterministic. Production target: compile the same validator IR to WASM with no network/clock/random imports. A WASM ABI sketch is included.

## 5. Proof state
Suggested lattice:
`UNSTARTED → CODE_PRESENT → EVIDENCED → VALIDATED → PROVEN` plus `BLOCKED`.
Only live evidence can produce PROVEN. GitHub polling may support CODE_PRESENT. Fixture/replay evidence can validate the gate but not the product.

## 6. Autonomy loop
```text
read canonical campaign state
→ derive READY checkpoints
→ rank by value / bottleneck / reuse
→ acquire grant or emit H-task
→ run one or more workers
→ ingest evidence
→ run validator
→ if live PASS: commit receipt + unlock dependents
→ else retry / decompose / challenge / escalate
```

## 7. Human loop
The dashboard should not ask the human to supervise agent prose. It should surface only bounded choices, missing authority, real-world KYC/OTP, ambiguous product decisions, or structural bottlenecks. Each H-task records estimated human minutes and whether the same class recurs.

## 8. Learning loop
Seed0-style tournaments compare successful variants under identical gates. Cost/time are tie-breakers only after correctness. The system can later learn which model/tool/decomposition works for which checkpoint class without weakening the gate.
