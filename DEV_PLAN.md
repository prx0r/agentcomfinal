# DEV_PLAN — autobuild program (agentcomfinal)

Goal: a working protocol stack for **seesaw + qp + the rest**, built as
**autobuild**: plan → scored → gated → receipt → built. Ten attempts,
`autobuild1`…`autobuild10`, each a full-system try with its own hypothesis.
`autobuild0/` holds the references every attempt shares. `autobuild1` is the
oneshot: stdlib-only Python, qp principles, self-defined validation.

## 1. What each zip is (condensed dossier, full text in AUDIT.md)

**Plugin pipeline (distribution adapters, not the company)**
- `agent-plugin-factory` — MCP→ChatGPT plugin pipeline: scores candidates,
  optimizes tool surface, evals routing, emits submission packet.
  Run: `python -m factory.cli score|packet|registry`. Stdlib. 0 tests.
- `agentcom-plugin-canonical` — conformance kit: plugin_spec schema, provider
  ledger, lint + schema validators, BUILD/REVIEW/ROUTING prompts, rubric.
  Run: `python checks/run_all.py plugin_spec.json`. Stdlib. 0 tests.
  Rule: factory should consume canonical schemas; currently parallel.

**Compiler (intent → provable target)**
- `autobuild-v0.2` — strategy→TargetSpec compiler + specgate/plangate +
  bridges + accretion ledger + peer review. Sits Seesaw→Underengineer→QP.
  Run: `python -m autobuild.cli compile plan.json --out build/x`; `make test`.
  Stdlib. 34 tests pass. Honest VALIDATION (real GitGoblin/QP NOT_PROVEN).

**Control planes (execution/portfolio layer — one fork chain, not three)**
- `campaign-control-plane` v1 — 11 theses → 132 checkpoints → evidence
  contracts → validators → H-tasks/receipts. `cli.py check|project|next`,
  `server.py` :8787, web dashboard. 5 test files.
- `scarce-state-control-plane-v2` — v1 + software-substitution gate +
  UNDERENGINEER to earliest moat event + attested-evidence ladder +
  scarce-asset ledger. 18 tests pass, 144 fixture contracts, TEST_REPORT.
- `scarce-state-control-plane-v3` — v2 + WORLD_SELECT (TRUTH/DEMAND/ECONOMIC/
  SCARCE_STATE) + scheduler + H-desk + Seesaw Market Lab + BreadUp self-lab.
  32 tests pass, 156/156 fixtures, 0 fake PROVEN. **Canonical of the three.**

**Seesaw (where is the binding constraint)**
- `seesaw-agent-module` — executable scorer: capability-delta →
  constraint/shadow-price → OWN/BUILD/REUSE/BUY/VALIDATE/WATCH/DROP per
  feature. `seesaw portfolio|project|features|report`. Stdlib. 3 tests.
- `personal-seesaw` — life-allocation theory (market/human/option ledgers),
  single-file scorer, 6 theory docs. 0 tests. Standalone, no code overlap.

**Desk demo** — `thesisdesk`: static trade cockpit (target/horizon/
conviction/falsifiers + localStorage log). `python3 -m http.server`. 0 tests.

**XMRBot (first external economy — one chain, 0.4 is superset)**
- `xmrbot-suite` — base: RandomX economics, CPU catalog, knowledge router,
  blog, MCP+REST. FastAPI stack. 8/8 validation.
- `xmrbot-solid-v0.3` — suite + visual system + blog→video/social pipeline.
  11/11 validation.
- `xmrbot-private-procurement-v0.4` — solid + 20 provider adapters +
  route→propose→QP-grant→gate→execute→receipt, grant-bound spend. 57 tests,
  15/15 validation. **Canonical.**

## 2. qp kernel — what autobuild inherits (non-negotiable)

From `~/qp` (A-COM kernel, stdlib-only, frozen `theses/northstar.md`):
- 7 objects only: STATE (derived by replay, never stored), CLAIM (id =
  content hash, dupes impossible), EVIDENCE (immutable, carries no verdict),
  TASK (READY→RUNNING→DONE/FAILED **only via receipts**), RUN (cost/time
  first-class), GATE (registry id→pure predicate, `program_hash` = sha of
  source, new logic = new id), GRANT (capability + constraints + expiry).
- One output: TransitionReceipt. One state path: propose → attach evidence →
  execute gates → settle → append → replay. FAIL receipts stored too.
- Gates: all-PASS required, unknown id = FAIL, raise = FAIL.
- Missing = UNKNOWN, never FALSE/zero. Evidence ≠ inference.
- Determinism: pure functions, canonical bytes, no network/clock/random in
  kernel (timestamps injected). Double-execute refuses on byte-diff.
- Secrets in vault/env/caller memory only. Kernel never touches domains,
  never calls outward, never persists keys. No spend, ever.
- Prose never terminal: JSON artifacts are truth, markdown/stdout are views.
- Small diffs, verified before claimed.
- Reuse: `~/qp/schemas/acom.json`, `acom/canonical.py`, `acom/gates.py`,
  `acom/receipts.py`, `acom/store.py`, `seesaw/graph.py` (score_node,
  ai_exposure, binding_constraint, divergence), `seesaw/beliefs.py`.

## 3. atask + plugin (fresh clones 2026-09-14)

- `~/atask` (prx0r/atask) — control language for one agent: goal → tasks with
  DECLARED evidence (no trust-only tasks) → runs with cost → stoplight proof
  (validators fail tasks, never excuse) → bounded human keypad 0–9. Stdlib.
  Autobuild adopts: **acceptance without declared proof is refused at creation**,
  DONE derived-never-declared, unknown stays null.
- `~/plugin` (prx0r/plugin) — astra-plugin-factory counterpart; pairs with the
  two plugin zips above.

## 4. Protocols (frozen for all 10 attempts)

- **Seesaw protocol:** feature → score S=(E·X·F·N·T·β)/cost → classify
  OWN/BUILD/REUSE/BUY/VALIDATE/WATCH/DROP → project value = Σ, binding =
  argmax. Magnitudes illustrative, ORDERINGS asserted.
- **qp protocol:** proposal + evidence → gates (all-PASS) → receipt →
  append-only store → replay. Unsigned V0 in attempt 1; signed later.
- **Plugin protocol:** candidate + MCP snapshot → score → canonical lint →
  packet. Canonical schemas win over copies.
- **Autobuild protocol:** PLAN → specgate → seesaw → gates → RECEIPT →
  report. Every stage emits JSON; reports are views.
- **Control-plane protocol:** thesis → checkpoints → evidence events →
  validators → PROVEN (attested) or H-task; v3 worlds for simulation.

## 5. Attempt roadmap

- `autobuild1` — ONESHOT: full pipeline in stdlib Python per §4 + VALIDATION.
- `autobuild2` — signed receipts (vendored Ed25519 a la qp) + grant-gated spend.
- `autobuild3` — atask-native: atask dir as the run layer, stoplight as gate.
- `autobuild4` — wasm validators (deterministic gate programs, atask VALIDATORS).
- `autobuild5` — control-plane merge: v3 worlds + scheduler as execution layer.
- `autobuild6` — plugin-factory × canonical unification (factory consumes schemas).
- `autobuild7` — procurement path: XMRBot-0.4 provider fabric behind qp grants.
- `autobuild8` — BreadUp headless service (scanners/watchers/economics).
- `autobuild9` — multi-agent: parallel workers, cost ledger, VOI scheduling.
- `autobuild10` — freeze candidate: best of 1–9, hardened, documented, tagged.

Rule: each attempt keeps its own README (hypothesis + result); shared refs
stay in `autobuild0/`; never copy schemas — import or vendor with provenance.

## 6. Validation criteria (apply to every attempt)

1. Determinism: same input → byte-identical output (run twice, diff).
2. Gates fail closed: unknown gate, raising gate, missing evidence → FAIL,
   state unchanged.
3. No trust-only work: plan feature without acceptance + declared evidence is
   refused at specgate.
4. Receipts verify: recompute id from bytes; tampered copy fails.
5. Chain verifies: append-only store replays; evil-line test breaks it loudly.
6. Seesaw sane: higher-moat feature outranks substitutable one; substitutable
   software never classifies OWN.
7. Suite green: `python3 -m pytest tests/ -q` all pass, recorded in
   VALIDATION.json with counts (no NOT_PROVEN claims).
