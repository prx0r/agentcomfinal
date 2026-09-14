# Frontier peer review — 2026-09-14

## Verdict

Autobuild's **core architecture is directionally correct**, but v0.1 overstated how close it was to a complete autonomous build system.

The deterministic specification core works. The full external stack is not yet proven until the generated artifacts are actually executed through the current `/gitgoblin`, `/qp`, and `/atask` repos.

Use these levels:

```text
L0 idea only                         PASSED
L1 deterministic compiler           PASSED
L2 internal mock end-to-end          PASSED
L3 real GitGoblin prebuild           NOT YET PROVEN
L4 real QP gate/receipt settlement   NOT YET PROVEN
L5 real A-Task queue/stoplight       NOT YET PROVEN
L6 autonomous project delivery       NOT YET PROVEN
L7 economic outcome feedback         NOT YET PROVEN
```

## What current frontier work confirms

### 1. Structured planning before execution is correct

Recent harness work reports that constraining plans to a fixed schema before tools are invoked can dramatically increase reproducibility and task success.

Implication: `PlanSpec -> TargetSpec` is the right boundary. Free-text plans should never directly drive consequential work.

Reference: arXiv 2608.26197, *Harness Engineering for Predictable Agentic Systems*.

### 2. Requirement compilation is already becoming a commodity layer

ARC compiles requirement documents into architecture, tests, and traceability. TDDev turns high-level requirements into structured acceptance tests before code, then deploys and browser-tests the result. `agent-spec` now has an intent compiler, deterministic work bundles, digests, traceability, replay, quality gates, and provenance.

Implication: **Autobuild must not define its moat as generic spec compilation.** Treat `compiler.py` as a replaceable reference provider.

The durable Autobuild-specific composition is:

```text
Seesaw strategic admission
+ minimum moat path
+ GitGoblin reuse/prebuild
+ QP truth/authority settlement
+ A-Task execution boundary
+ outcome/accretion data
```

References:
- arXiv 2602.13723, ARC.
- arXiv 2605.17242, TDDev.
- ZhangHanDong/agent-spec (MIT), 2026 releases.

### 3. Acceptance criteria -> deterministic tests is frontier-consistent

SWE-Skills-Bench explicitly maps requirement acceptance criteria to execution-based deterministic verification. It also finds that most generic skills do not improve pass rates and some make performance worse.

Implication:
- keep acceptance criteria explicit;
- never infer `PASS` from a plausible skill/component;
- GitGoblin output is only `CANDIDATE_REUSE` until integration validation succeeds.

Reference: arXiv 2603.15401.

### 4. Runs should generate reusable experience

Trajectory-Informed Memory, PILOT, Prime Agent, Continual Harness, and Harness Continual Learning all point toward persistent experience outside model weights.

Implication: the additive-run thesis is strong.

But additive must mean:

```text
preserve observation
-> validate
-> replay
-> promote only if it generalizes
```

not:

```text
agent noticed thing
-> permanent skill
```

### 5. Persistent skills can poison future behavior

2026 empirical work shows that seemingly relevant agent skills can produce functional failures and efficiency regressions.

Implication: v0.1's `promote after N uses` idea was unsafe. v0.2 changes promotion to require held-out replay and zero/limited regressions.

### 6. Failed runs must stay in the denominator

Current evaluation systems increasingly retain failed, timed-out, and cancelled trajectories rather than letting a system selectively report wins.

Implication: Autobuild's failed-run accretion behavior is correct. Operational failure and information yield must remain separate fields.

## v0.1 adversarial findings

The first peer-review pass found these real defects:

1. A non-empty but meaningless validator object could pass the spec gate.
2. A missing requirement id could crash validation instead of failing closed.
3. A feature dependency cycle could recurse until `RecursionError`.
4. Prebuild could label an UNKNOWN-license/UNKNOWN-rights component as 100% reusable.
5. The accretion ledger treated the same semantic fact with different evidence metadata as new knowledge.
6. Opposing facts were stored without an explicit conflict record.
7. The JSON Schema was too shallow to reject a malformed validator.
8. QP bridge ids looked canonical even though QP constructors own canonical ids.
9. Primitive promotion used project-use count without held-out regression evidence.
10. Economic validation was stored mostly as prose formula strings rather than a structured QP circuit.

All ten are changed in v0.2. Deeper adversarial testing then found and fixed four more architectural defects: feature-level dependency edges were not projected into the execution DAG; malformed non-finite targets could throw during hashing; Autobuild could superficially mint `VERIFIED_EXTERNALLY` from caller-supplied booleans; and the old TargetRoot mixed immutable success semantics with replaceable reuse/execution planning.

## v0.2 hardening changes

### Spec admission

- validator kinds/parameters checked recursively;
- missing ids fail closed;
- feature and requirement cycles fail deterministically;
- ALL_HARD circuit must exactly cover hard requirements;
- claimed economic validation requires a structured QP-compatible circuit;
- target JSON schema now rejects malformed validator shape.

### Reuse

- explicit rights/license classification required;
- UNKNOWN rights cannot contribute to Existing Capability Coverage;
- blocked candidates become missing delta.

### Accretion

- semantic dedupe ignores evidence provenance for identical claims;
- contradictory proposition values emit explicit `CONFLICT` records;
- ledger is hash-chained and tamper checked;
- all run-derived knowledge is stored as `UNVERIFIED_OBSERVATION` by default;
- verified knowledge must cross an external verifier boundary (normally QP).

### Promotion

A reusable primitive now requires:
- repeated project use;
- held-out replay cases;
- minimum held-out pass rate;
- bounded regression count.

Count alone can never promote.

### Frozen contract vs replaceable plan

Autobuild now separates three roots:

```text
ContractRoot = normative WHAT counts as success
PlanRoot     = current HOW/reuse/execution route
LineageRoot  = strategic/compiler ancestry
```

A prebuild/reuse change must change PlanRoot while leaving ContractRoot stable. This is essential for fair replay, A/B tests, and LEGO-like component substitution.

### QP bridge

Autobuild no longer emits fake QP canonical object ids.

It emits `*_CONSTRUCTOR_SPEC` records. The adapter must call current QP constructors and retain the returned QP ids. QP remains sole owner of canonical claim/task/gate/grant identities.

### A-Task bridge

- dependency edges preserved as `blocked_by`;
- file-evidence validators can be materialized as stdlib-only A-Task validators;
- A-Task remains the only promoter to DONE.

## Internal tests performed

### Standard suite

```text
34 passed
```

### Determinism

100 identical compiles -> exactly one ContractRoot and one PlanRoot.

### Malformed input fuzz

1,000 deliberately malformed TargetSpecs plus 500 malformed PlanSpecs across:
- missing ids;
- invalid validator kinds;
- invalid criticality;
- missing dependencies;
- feature dependency errors;
- empty evidence contracts;
- invalid completion circuits;
- missing economic circuits.

Result:

```text
TargetSpec: 1000 / 1000 failed closed
PlanSpec:    500 / 500 failed closed
0 malformed specs accepted
0 boundary crashes
```

### End-to-end internal target simulation

Breadup minimum-moat plan:

```text
PlanSpec
-> Strategic admission
-> Underengineer
-> TargetSpec
-> Prebuild fixture
-> MissingDelta
-> requirement evidence
-> requirement states
-> completion circuit
```

Observed:

```text
all evidence passes -> TRUE
one evidence object absent -> UNKNOWN
listing status wrong -> FALSE
```

This is the required bool3 behavior.

### Tamper test

Hash-chained accretion ledger:

```text
clean ledger -> PASS
modify earlier record bytes -> FAIL
```

### Semantic duplicate test

Same proposition, new evidence metadata:

```text
new knowledge = 0
accretion gate = FAIL if the run consumed resources
```

### Contradiction test

Same proposition, opposite value:

```text
CONFLICT appended
status = UNRESOLVED
```

No silent last-write-wins.

### A-Task validator code generation

A generated stdlib-only file validator was executed as a subprocess against a real evidence JSON fixture and returned the expected binary result.

## What still does NOT work yet

### 1. Natural language -> PlanSpec

Autobuild starts from structured PlanSpec. The hard extraction/reverse-interview stage remains external.

This is acceptable architecturally but means `"build me X" -> autonomous project` does not exist yet.

### 2. Real GitGoblin integration

The current prebuild test uses a fixture with the intended GitGoblin output contract.

No live GitGoblin scan was executed in this environment.

### 3. Real QP settlement

The bridge was peer-reviewed against current QP constructors and corrected so QP owns ids, hashes, grants, and receipts.

But Autobuild has not yet registered its generated validators inside a live QP checkout and settled a real TransitionReceipt.

### 4. Real A-Task queue creation

The bridge follows current A-Task concepts (goal indices, evidence, blocked_by, validators), and generated validator scripts obey the documented stdlib/binary contract.

But an actual `.atask` queue has not yet been created and driven green from Autobuild output in this environment.

### 5. Economic circuit runtime

Autobuild now requires a structured QP-compatible economic circuit for claimed economic validation.

QP must execute it over real economic evidence. Autobuild does not duplicate QP's circuit runtime.

### 6. Underengineer is a heuristic

`underengineer-v2` is deterministic and inspectable, but greedy. It does **not** prove a globally minimal build path.

Do not describe it as mathematical global optimization.

### 7. Shell-command evidence remains a legacy boundary

Some PlanSpec fixtures still use `command: "..."` strings because current A-Task evidence works that way.

A stronger future adapter should store executable + argv + cwd + timeout structurally and materialize a safe wrapper for A-Task rather than making shell strings canonical in Autobuild.

### 8. Information yield can still be Goodharted

Semantic dedupe removes trivial exact inflation, but an agent could still manufacture many superficially distinct observations.

Therefore yield must never itself authorize primitive promotion or consequential action. QP verification + replay gates remain required.

## Recommended canonical boundary after peer review

```text
SEESAW
  decides scarce strategic target
        |
        v
AUTOBUILD CORE
  admission + TargetSpec + transformation receipts
        |
        +---- compiler provider (replaceable)
        |       reference compiler / agent-spec / future ARC-like compiler
        |
        v
GITGOBLIN
  candidate reuse only
        |
        v
AUTOBUILD
  missing delta + bridge specs
        |
      +-+----------------+
      |                  |
      v                  v
     QP                A-TASK
 authoritative        execution DAG
 truth/authority      + stoplight
      |                  |
      +--------+---------+
               v
        RUN OBSERVATIONS
               |
               v
       ACCRETION LEDGER
       (unverified first)
               |
               v
       QP/replay promotion
               |
               v
      reusable primitives
```

## Bottom line

**Keep Autobuild. Do not treat the generic compiler as the moat.**

The strongest part is the separation of:

```text
strategic truth
specification truth
reuse evidence
execution
canonical verification
real-world outcome learning
```

The next milestone is not more compiler features.

It is one real run:

```text
real PlanSpec
-> real GitGoblin prebuild
-> real QP gates
-> real A-Task queue
-> real worker
-> real TransitionReceipt
-> failed/success trajectory accrued
-> replay the second run and measure whether accumulated data improved it
```

Until that passes, call Autobuild a **working deterministic compiler with unproven live integrations**, not a finished autonomous builder.
