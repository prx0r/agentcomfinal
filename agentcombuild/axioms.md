# axioms.md — what structurally bounds the agent (enforced, not asked)

$$
\boxed{\text{Invariants constrain reality; axioms constrain cognition.}}
$$

Two layers run this system. This file is the first: **bounds the agent
cannot break even if it tries** — enforced by code, gates, and review.
The second layer is `agents.md`: principles the agent is *instructed* to
follow (plus Layer C dynamic policy — spend/attempt/tool/repo budgets as
structured data in `agentloop/agent_policy.json`, never buried in prompts).
Confusion between the two is the root of most agent-system failures:
never enforce by prompt what you can enforce by structure, and never leave
to structure what only judgment can do.

## AX-0 — Actuality (the one axiom)

> An agent can propose any state transition it likes; the only route to
> progress is externally produced evidence satisfying frozen deterministic
> gates.

Operationally: NO A-LOG → NO EVIDENCE → UNKNOWN → NO RECEIPT → NO STATE
ADVANCE. The agent can lie forever; it gains nothing.
Enforced by: ab1 gates + ab3 stoplight + DAG (`actuality.py`).

## The bounding set

| ID | Bound (structural) | Enforced by |
|---|---|---|
| AX-1 | Probes observe, judges decide. No verdict field from a probe is ever read as a verdict. | `judges.py` reads fixed fields only; R9 test |
| AX-2 | Three-valued logic. UNKNOWN blocks progress; it is never a pass and never a score. | `actuality.evaluate_dag`; ACT4 tests |
| AX-3 | Consequential actions need independent readback. Same-channel success is UNKNOWN. | `readback.py` + `independent-readback-v1` |
| AX-4 | No self-proof. There is no status field to set; verdicts are recomputed, planted ones ignored. | `stoplight.acheck` recomputes; planted-verdict test |
| AX-5 | Gates fail closed. Unknown id, raised exception, missing evidence → FAIL. | registry `execute`; R6/R8 tests |
| AX-6 | Identity is content. Ids are hashes of canonical bytes; tampering breaks verification loudly. | `canonical.py`; tamper/evil-line tests |
| AX-7 | Secrets never enter the tree or the log. Secret-shaped evidence is refused at the boundary. | `alog` refusal + secret tests |
| AX-8 | Authority is granted, not claimed. Consequential without a valid in-scope grant is REFUSED. | `grants.py` + L1 gates; G1/G2 tests |
| AX-9 | The contract is frozen. Acceptance edits mint a new ContractRoot; implementations only move PlanRoot. | R7 test; ab4 gate specified |
| AX-10 | The model is replaceable. No model id lives inside contract/receipt bytes; the durable chain is strategy→contract→reuse→authority→execution→trajectory. | D3 review |

## What axioms are NOT

- Not style guides (those live in `agents.md`).
- Not task lists (those are RUN records, compiled per project).
- Not validators for specific claims (those live in the registry).
- Not unchangeable: an axiom changes only by a governed transition with a
  reasoned record — never by a single run's convenience.

> **Agents speculate. Reality validates. QP commits. History compounds.**
