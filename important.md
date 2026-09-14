# IMPORTANT — briefing for an external reviewing agent

To: whoever reviews this repo next (human or agent).
From: the building session, 2026-09-14.
Repo: `prx0r/agentcomfinal`, public, branch `main`.
Ask: read this file, then `agentcombuild/actuality.md`, then answer the
 numbered questions at the bottom. File your reply as review notes or open
 issues — blunt is welcome.

## What this is

An R2 bucket dump (`agentcom`) turned into a working factory for autonomous
builds. Thesis: an agent may propose anything, but progress happens only via
externally produced evidence satisfying frozen deterministic gates
(`agentcombuild/actuality.md`, treated as system AXIOM).

## Everything built so far

- **R2 import**: 60 bucket objects → 30 unique files in `docs/` (+ manifest).
  13 zips + 17 raw idea docs (one live-pattern Pinterest token found and
  redacted before push — rotate it if it was ever real).
- **12 packages unpacked** into `packages/`, each with an import README;
  full dossier in `AUDIT.md` (fork chains identified: control-plane v1→v2→v3
  with v3 canonical; XMRBot suite→solid→procurement-0.4 canonical).
- **16 theses** curated into `notes/` with sanitized names.
- **Factory shell** (`agentcombuild/`): founding brief (`agentcomidea.md`),
  axiom (`actuality.md`), binary rubric (`agentcomcriteria.md`, seed0 style:
  ID + statement + exact verification), full gate catalog L0–L4 (`GATES.md`),
  dev plan (`DEV_PLAN.md`), shared refs (`autobuild0/`: repo inventory,
  schema index, qp principles, shared `reviewkit.py`, red-team harness).
- **autobuild1** (stdlib): PLAN→specgate→seesaw→gates→receipt→report.
  17/17 tests. Receipts unsigned V0 by design.
- **autobuild2** (stdlib + vendored Ed25519): signed V1 receipts, fail-closed
  grants (expiry/scope/unknown-constraint/limits/predicates), consequential
  actions REFUSED without grant. 15/15 tests.
- **autobuild3** (stdlib): atask-native a-log telemetry (hash-chained,
  refusals for unknown tasks/bad indices/secrets) + stoplight that
  re-executes every claim (command allowlist, file hashes, validator
  contract with timeout/additive-only rules) + Actuality core: probe/judge
  split, L0 schema + L1 CEL-subset judges (three-valued, UNKNOWN blocks),
  Actuality DAG, independent-readback rule, 6-primitive validator registry.
  29/29 tests.
- **agentloop** (stdlib): the agent harness — shape-enforced RUN records
  (exactly-10 next tasks, ≥1 visionary idea, validations/fixtures named),
  seeker stuck-loop (research → 3 candidates → test each → log all, dark
  validation), research backends (sim + GitHub/arXiv over urllib, injectable
  fetcher), compiler (ideas bank, decisions, merged next-10 leaderboard).
  15/15 tests.
- **Review machinery**: every attempt/harness has `review/` (criteria check
  → `VERDICT.json` + `NEXT.md`); `PEER_REVIEW.md` (4 bugs found and fixed
  by self-review, incl. 2 real fail-opens); `REDTEAM.md` (R1–R12, all held,
  2 documented-known-opens: caller clock trust, fabricated-judgment shape
  vs provenance); `GO.sh` one-click chain — currently 12/12 green.
- **Agent doctrine**: `axioms.md` (structural bounds, enforced) vs
  `agents.md` (adhered principles, reviewed) — deliberate split, plus the
  microprocessor instruction set and stuck-loop program.

## Standing decisions you should pressure-test

1. AgentCom orchestrates *references* to QP/atask truth, never its own
   truth kernel (idea §1). Is the boundary drawn in the right place, or
   will orchestration pressure quietly re-create a kernel?
2. Judges: CEL-subset now, OPA/Rego later, WASM for custom validators.
   Right ladder order? Is our CEL-subset expressive enough for real
   acceptance predicates, or will everything escape to L3?
3. QP/atask/aworker/aloop are referenced (local checkouts in `autobuild0/`),
   not vendored — except Ed25519. Should the QP adapter call real `~/qp`
   constructors now (ab3 scope said live adapter), or is simulation still
   the right call pre-pilot?
4. RUN records enforce exactly-10 next tasks and ≥1 visionary idea. Too
   rigid (forces filler) or the correct forcing function?
5. Telemetry gap (next build): wire atask usage receipts + aloop USAGE
   trailers + opencode_db calibration into RUN records; budget brake +
   aworker grant-ledger adapters after. Right order? Anything missing?
6. Pilot readiness: what in this repo is *not yet true* that must be true
   before the agentcom-uk one-permission-one-outcome pilot (idea §21)?
7. Biggest cheating vector we haven't closed, in your view. The two we
   know: caller-supplied clock, fabricated judgments accepted only inside
   the pipeline. What else?

## How to verify (all stdlib, no installs)

```bash
bash agentcombuild/GO.sh   # full chain: suites + reviews + demos + redteam
python3 agentcombuild/autobuild0/redteam_ab12.py
```

Reply with: (a) verdict per question, (b) any FAIL you can actually
demonstrate (command + output), (c) your ranked next-10 for this repo with
one-line justifications. Concrete beats clever.
