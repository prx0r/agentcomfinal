# autobuild0 — qp principles (binding on all attempts)

Distilled from `~/qp` (`theses/northstar.md` frozen thesis + `acom/` +
`seesaw/` + `killfeed/`). Attempt code must obey these; violations fail
validation criterion §2/§3 of DEV_PLAN.

## Objects (7, no more without a frozen-schema change)

STATE (replay-derived, never stored) · CLAIM (content-hash id, dupes
impossible) · EVIDENCE (immutable, no verdict) · TASK (status only via
receipts) · RUN (tokens/cost/duration first-class) · GATE (id→pure predicate,
program_hash = sha256(source)) · GRANT (capability + constraints + expiry).

## Lifecycle (one-way, one state path)

propose → attach evidence → execute gates (all-PASS) → settle receipt →
append → replay. FAIL receipts stored (retry evidence). TASK completes iff
required gates PASS. `S_t+1 = T(S_t,P)` iff ∧G_i = PASS.

## Rules

1. Stdlib only. Pure functions. No network/clock/random in kernel — inject.
2. Canonical bytes (sorted keys, no whitespace, UTF-8); ids are content hashes.
3. Unknown gate = FAIL. Raising gate = FAIL. Missing = UNKNOWN, never FALSE.
4. Evidence ≠ inference (verdicts live in CLAIM/receipt, never in evidence).
5. New logic = new id (rule change is itself a transition).
6. Secrets in env/caller only; kernel never persists keys, never calls out,
   never touches domains (game truth lives in pogtown/demos).
7. No spend, ever. Consequential action needs a grant (attempts ≥2).
8. Prose never terminal: JSON artifacts are truth; markdown/stdout are views.
9. Stores append-only + verifiable (evil-line test must fail loudly).
10. Small diffs, verified before claimed. No trust-only tasks: acceptance
    without declared proof is refused at creation (atask rule, adopted).

## Reuse (exact paths)

- `~/qp/acom/canonical.py` — canonical/sha256_hex/obj_id/merkle_root
- `~/qp/acom/objects.py` — make_claim/evidence/task/run/gate/grant/state
- `~/qp/acom/gates.py` — registry, execute, program_hash
- `~/qp/acom/receipts.py` — transition/sign/settle/verify
- `~/qp/acom/store.py` — append/verify_chain/replay
- `~/qp/acom/grants.py` — verify_grant (fail-closed)
- `~/qp/acom/ed25519.py` — vendored signer (attempt 2+)
- `~/qp/seesaw/graph.py` — score_node/ai_exposure/binding_constraint/divergence
- `~/qp/seesaw/beliefs.py` — belief graph, propagate, expected_impact
- `~/qp/seesaw/classes.py` — 10 scarcity classes
- `~/qp/killfeed/circuit.py` — 25-op claim circuits (UNKNOWN-poisoning)
- `~/qp/killfeed/verify_all.py` — Definition of Done pattern
- `~/qp/schemas/acom.json` — the 7 object schemas
- `~/atask/atask.py` + `driver.py pulse` — run layer + promotion rule
- `~/atask/ATASK.md` — portable control language (one page)
