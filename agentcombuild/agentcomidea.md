# agentcomidea.md — founding brief (saved 2026-09-14)

I think `agentcomfinal` is now one architectural cleanup away from being the actual **operating shell for the whole system**.

The repo already has most of the right pieces, but its audit correctly identifies the problem: three overlapping control planes, duplicated schemas, and separate plugin/compiler packages that currently overlap responsibilities.  The strongest existing runtime is `scarce-state-control-plane-v3`: it already has Seesaw → world selection → underengineering → ATask → QP → outcomes → scheduler as its north star.

The main correction I would make is: **AgentCom should not itself become another truth/runtime kernel.** QP explicitly requires one-way flow—proposal → evidence → gates → receipt → state—and the kernel never calls outward.  So AgentCom should orchestrate references to QP truth rather than reproduce QP semantics.

Also, use `agentcom-uk` as the first end-to-end proof. Its own frozen spec already gives the perfect four-step pilot: pick one real SMB pain, obtain the minimum delegated permission, execute one real bounded action, then read back the outcome.

Here is the build brief I would give the coding agent.

# AgentComFinal — Canonical Integration Build Plan

## Mission

Turn `prx0r/agentcomfinal` from a collection of overlapping research packages into the canonical **portfolio orchestration and autonomous-build control plane** for the user's projects.

Do **not** create another agent runtime.

Do **not** recreate QP.

Do **not** recreate A-Task.

Do **not** recreate GitGoblin.

Do **not** make the ChatGPT plugin layer central.

The system should compose:

```text
WORLD / NEW INFORMATION
        |
        v
     SEESAW
 strategic admission
        |
        v
StrategicDecision
        |
        v
  AGENTCOM CONTROL
 portfolio + worlds
        |
        v
  UNDERENGINEER
 minimum moat path
        |
        v
    AUTOBUILD
 frozen success contract
        |
        v
    GITGOBLIN
 prebuild / reuse search
        |
        v
  Execution Plan
        |
    +---+---+
    |       |
    v       v
   QP     A-TASK
 truth    work queue
    |       |
    +---+---+
        |
      workers
        |
        v
 external reality
        |
        v
 evidence / outcomes
        |
    +---+---+
    |       |
    v       v
   QP     SEESAW
 receipt  repricing
        |
        v
 AGENTCOM SCHEDULER
```

The central AgentCom responsibility is:

> **Choose what project should move, what real-world outcome should be targeted next, compile that into a frozen target, dispatch bounded work, and project verified external outcomes back into portfolio state.**

---

# 1. Freeze the architectural boundaries first

Before changing code, create `CANONICAL.md` at repository root.

It must declare these boundaries.

## Seesaw

Owns:

```text
should we?
what became scarce?
what became commodity?
what is the durable asset?
what would falsify the thesis?
what is the first moat-producing event?
```

Output:

```text
StrategicDecision
```

Seesaw is strategic policy.

It does not execute work.

It does not prove technical completion.

---

## AgentCom

Owns:

```text
portfolio
projects
campaigns
scarce assets
target profiles
experiment worlds
resource constraints
project selection
world selection
minimum live path
cross-project bottlenecks
outcome projection
portfolio scheduling
```

AgentCom answers:

> **What verified external state should the system try to change next?**

It is an orchestration layer.

---

## Autobuild

Owns:

```text
approved plan
→ frozen TargetSpec
→ ContractRoot
→ execution PlanRoot
→ requirements
→ evidence contracts
→ deterministic validator specs
→ dependency graph
```

Autobuild answers:

> **What exactly must become observably true?**

The compiler implementation itself is replaceable.

The `ContractRoot` is not.

---

## GitGoblin

Owns:

```text
what already exists?
which implementation is reusable?
license?
quality?
maintenance?
security?
fit?
integration cost?
what exactly remains missing?
```

GitGoblin answers:

> **How little code actually needs to be created?**

It must return structured `ReusePlan` data.

---

## QP / A-COM

Owns:

```text
canonical objects
evidence
claims
gates
grants
state transitions
receipts
cryptographic verification
```

QP answers:

> **Did the claimed transition actually occur, and was it authorized?**

QP remains the **sole canonical truth/authority layer**.

Never let AgentCom produce fake QP IDs or fake QP receipts.

Never accept an AgentCom `PROVEN` flag as canonical truth.

QP's existing invariant remains law:

```text
agent output != canonical state
```

and missing evidence remains:

```text
UNKNOWN
```

not PASS.

---

## A-Task

Owns:

```text
goal
bounded tasks
dependency DAG
runs
attempts
declared rerunnable evidence
worker measurements
execution blockers
human execution boundaries
stoplight
```

A-Task answers:

> **What bounded work is executable now, and did its rerunnable proof pass?**

---

# 2. Declare the canonical packages

Do not run all 12 imported packages as peers.

Use this hierarchy.

```text
CANONICAL RUNTIME
└── scarce-state-control-plane-v3

CANONICAL COMPILER
└── autobuild-v0.2

DOMAIN PACK
└── agentcom-plugin-canonical

LIVE PRODUCT/WORLD PACKAGES
├── xmrbot-private-procurement-v0.4
├── BreadUp project definitions
├── AgentCom UK
├── PogPet
├── GeoDrop
└── other asset campaigns

REFERENCE / RESEARCH
├── seesaw-agent-module
├── personal-seesaw
├── agent-plugin-factory
└── thesisdesk

ARCHIVE AFTER EXTRACTION
├── campaign-control-plane
├── scarce-state-control-plane-v2
├── xmrbot-solid-v0.3
└── xmrbot-suite
```

Do not delete historical packages immediately.

Extract useful primitives first.

---

# 3. What to extract from the overlapping control planes

`campaign-control-plane` has the cleanest checkpoint vocabulary:

```text
CampaignSpec
CapabilityCheckpoint
EvidenceContract
Validator
proof state
checkpoint DAG
```

Its architecture correctly defines a checkpoint as one observable behavior with dependencies, exact implications, evidence contracts, deterministic validator, authority class and proof level.

Preserve that ontology.

Do **not** preserve its separate runtime as canonical.

Move its useful schemas/concepts into the new AgentCom contracts.

---

`scarce-state-control-plane-v3` should remain the active orchestration shell because it adds:

```text
experiment worlds
WORLD_SELECT
resource constraints
UNDERENGINEER
portfolio scheduler
strategy families
real-outcome performance
scarce-state ledger
human strategic desk
```

Its scheduler contains an excellent invariant:

> infrastructure cannot outbid an asset campaign for a scarce account/store/permission; infrastructure is pulled into the selected campaign as support.

Keep this.

---

`scarce-state-control-plane-v2` contributes the richer UI.

Port useful views later.

Do not port v2's control semantics.

Views are projections.

---

# 4. Remove duplicated truth systems

This is critical.

The current v3 contains:

```text
runtime/attestation.py
runtime/validators.py
runtime/qp_adapter.py
```

These are useful prototypes, but **must not remain the live canonical proof path**.

`attestation.py` itself already says HMAC is only a local reference and production should use QP public-key TransitionReceipts.

Likewise the current `qp_adapter.py` merely checks checkpoint scope and proof-level values; it is not QP's cryptographic grant verification.

Therefore:

```text
runtime/attestation.py
→ tests/reference_attestation.py

runtime/qp_adapter.py
→ replace with adapters/qp.py

runtime/validators.py
→ validator-spec/reference semantics only
```

Canonical proof becomes:

```text
external observation
        ↓
QP EVIDENCE
        ↓
QP gate
        ↓
QP transition settlement
        ↓
TransitionReceipt
        ↓
AgentCom projection
```

AgentCom may display:

```text
PROVEN
```

only as a derived view from a verified QP receipt.

---

# 5. Create one root contract layer

Add:

```text
contracts/
```

The contracts directory should contain only orchestration-level objects.

Do not copy QP's seven canonical objects.

Reference QP's version instead.

Create:

```text
contracts/
├── strategic_decision.schema.json
├── campaign.schema.json
├── scarce_asset.schema.json
├── target_binding.schema.json
├── prebuild_request.schema.json
├── reuse_plan.schema.json
├── execution_binding.schema.json
├── experiment.schema.json
├── outcome_observation.schema.json
├── trajectory.schema.json
├── strategic_question.schema.json
└── adapter_receipt.schema.json
```

These contracts connect systems.

They do not compete with them.

---

# 6. Define identity/lineage explicitly

Every campaign run must preserve the whole causal chain.

Use:

```text
StrategicRoot
    |
CampaignRoot
    |
ContractRoot
    |
PlanRoot
    |
RunRoot
    |
QP TransitionReceipt
    |
OutcomeRoot
```

Definitions:

```text
StrategicRoot
= hash(Seesaw StrategicDecision)

CampaignRoot
= hash(project + scarce asset + experiment objective)

ContractRoot
= hash(WHAT must become true)

PlanRoot
= hash(HOW we currently intend to achieve it)

RunRoot
= hash(one execution attempt)

OutcomeRoot
= hash(real observed consequence)
```

A different library/model/repository may change:

```text
PlanRoot
```

while leaving:

```text
ContractRoot
```

unchanged.

That is required for meaningful replay and optimization.

---

# 7. Build thin adapters, not copies

Create:

```text
adapters/
├── qp.py
├── atask.py
├── gitgoblin.py
├── autobuild.py
├── seesaw.py
├── github.py
└── projects/
```

Each adapter has exactly three responsibilities:

```text
detect compatible external version
translate AgentCom object → external request
translate external verified result → AgentCom reference
```

No business logic belongs in adapters.

---

# 8. QP adapter

The QP adapter is the most important.

It should consume Autobuild constructor specs.

It should call actual `/qp` constructors.

QP creates:

```text
CLAIM ids
TASK ids
GATE ids/hashes
GRANT ids
RUN ids
TransitionReceipts
```

AgentCom never fabricates these.

The adapter returns references such as:

```json
{
  "contract_root": "...",
  "requirement_id": "...",
  "qp_claim_id": "...",
  "qp_task_id": "...",
  "qp_gate_id": "...",
  "minimum_proof_level": 9
}
```

All consequential state transitions are then settled by QP.

---

# 9. A-Task adapter

Autobuild already emits an A-Task bridge.

Translate it into the actual `/atask` queue.

Each AgentCom requirement should map to:

```text
target requirement
→ A-Task acceptance index
→ one or more A-tasks
→ declared rerunnable evidence
```

Preserve dependencies.

Never mark a task DONE in AgentCom.

AgentCom reads A-Task state.

A-Task remains authoritative for execution completion.

---

# 10. GitGoblin becomes mandatory prebuild

No BUILD task should enter A-Task until GitGoblin has been queried unless explicitly exempted.

Flow:

```text
TargetSpec
   ↓
PrebuildRequest
   ↓
GitGoblin
   ↓
ReusePlan
   ↓
Autobuild APPLY_REUSE_PLAN
   ↓
new PlanRoot
same ContractRoot
```

Every required capability becomes:

```text
REUSE
BUY
BUILD
BLOCK
```

Only `BUILD` or integration deltas produce engineering work.

Every evaluated repository/component becomes durable structured evidence.

This is where the LEGO property starts to compound.

---

# 11. Make the campaign graph a projection of frozen contracts

The existing v3 project files contain long 12-checkpoint capability ladders.

Keep them as capability libraries.

Do **not** execute them sequentially by default.

The repo already recognizes this: the full roadmap is a capability library and UNDERENGINEER chooses the live minimum path.

The active graph should instead be generated from:

```text
StrategicDecision
+
first moat event
+
selected experiment world
+
Autobuild Contract
+
ReusePlan
```

Then render:

```text
required now
blocked
deferred
proven
invalidated
```

---

# 12. Preserve WORLD_SELECT

`runtime/experiments.py` is useful.

Its principle is correct:

> choose the cheapest reality capable of answering the question.

It already scores worlds from:

```text
information_gain
× feedback_quality
× economic_relevance
-------------------------------------
money × time × human × irreversibility
```

and explicitly warns that simulation cannot graduate a market claim.

Keep this as a planning heuristic.

Do not make WORLD_SELECT canonical truth.

---

# 13. Keep four evidence worlds

Retain v3's world classes:

```text
A_TRUTH
B_DEMAND
C_ECONOMIC
D_SCARCE_STATE
```

Interpret them as increasing evidence ceilings.

### A_TRUTH

Can establish:

```text
forecast calibration
technical facts
paper outcomes
```

Cannot establish demand.

### B_DEMAND

Can establish:

```text
user intent
usage
repetition
activation
```

Cannot establish willingness to pay unless real money moves.

### C_ECONOMIC

Can establish:

```text
sale
margin
CAC
conversion
retention
```

### D_SCARCE_STATE

Can establish:

```text
delegated authority
private operational history
physical observations
network participants
real controlled assets
```

This hierarchy is central to Seesaw.

---

# 14. Separate technical proof from economic proof

For each campaign maintain two circuits.

```text
TechnicalCircuit
```

asks:

> Does the system perform the claimed behavior?

and:

```text
EconomicCircuit
```

asks:

> Did reality validate the business thesis?

Example:

```text
TechnicalCircuit = TRUE
EconomicCircuit = FALSE
```

means:

> product works; business thesis failed.

Never let engineering success masquerade as market evidence.

---

# 15. Replace `performance.record()` trust with QP-verified outcomes

The current v3 performance layer correctly requires `receipt_ref` for resolved real outcomes.

Strengthen it.

Do not merely check that:

```text
receipt_ref != null
```

Require:

```text
qp.verify(receipt_ref) == PASS
```

before a real result enters:

```text
SUCCESS
FAIL
```

Then strategy-family statistics are based only on verified real outcomes.

---

# 16. Human interaction: one surface, two semantics

Do not retain multiple independent human queues.

There are two distinct human objects.

## StrategicQuestion

Owned by AgentCom.

Examples:

```text
Which customer segment should we test?
Do we value growth vs cash flow here?
Which project should receive the one available Etsy store?
```

These are bounded strategic decisions.

They can change a StrategicSpec or allocation.

They do not themselves authorize external action.

---

## Execution H-task

Owned by A-Task.

Examples:

```text
OTP
KYC
physical action
secret
authorization boundary
identity
```

These unblock execution.

---

The current v3 `hdesk.py` should become a **unified projection/view**, not its own competing source of execution truth. It currently keeps its own `human_tasks.json`; demote that store once the adapters exist.

---

# 17. The additive-run system

Every attempt must emit two separate outputs:

```text
OperationalResult
KnowledgeContribution
```

Operational result:

```text
COMPLETED
FAILED
BLOCKED
ABANDONED
```

Knowledge contribution may contain:

```text
positive facts
negative facts
component evaluations
API constraints
latencies
costs
dependency edges
failure fixtures
new external observations
real outcomes
contradictions
UNKNOWNs
```

Failures are not deleted.

No run should have to rediscover a previously stable failed route.

But do not automatically promote learned observations into reusable skills.

Use:

```text
OBSERVATION
    ↓
CANDIDATE_FACT
    ↓
QP verification
    ↓
CANDIDATE_PRIMITIVE
    ↓
replay / held-out worlds
    ↓
PROMOTED_PRIMITIVE
```

Promotion must itself be a governed transition.

---

# 18. Build a primitive registry

Create:

```text
data/primitives/
```

Each reusable LEGO brick should have:

```json
{
  "id": "...",
  "version": "...",
  "provides": [],
  "requires": [],
  "input_schema": "...",
  "output_schema": "...",
  "validator": "...",
  "evidence_level": "...",
  "implementations": [],
  "performance": {},
  "promotion_receipt": null
}
```

Examples:

```text
send_verified_email
create_marketplace_listing
read_marketplace_outcome
domain_control_check
business_identity_verify
xmr_escrow
company_lookup
security_secret_scan
```

GitGoblin discovers implementations.

Autobuild composes primitives.

QP governs consequential use.

A-Task executes composition.

---

# 19. Plugin canonical becomes a domain pack

Do not let `agentcom-plugin-canonical` define root AgentCom schemas.

It is specifically a ChatGPT/Codex plugin conformance kit with routing requirements, source evidence, lint and submission gates.

Move conceptually to:

```text
domainpacks/chatgpt-plugin/
```

A plugin target can extend a generic Autobuild contract with:

```text
routing evals
OpenAI submission constraints
tool schema
auth
CSP
review cases
```

But ChatGPT plugin state remains an adapter/distribution concern.

---

# 20. First real end-to-end proof: AgentCom UK

Do not start with the whole portfolio.

Do not start by improving dashboards.

Use:

```text
agentcom-uk
```

The existing Seesaw analysis is already correct:

```text
destroyed by perfect AI:
- generic receptionist code
- dashboard
- public business enrichment
- generic CRM

survives:
- delegated authority
- private operating state
- customer/job history
- relationship
- verified action outcomes
```

Execute exactly this experiment:

```text
1 real UK business
        ↓
1 high-frequency painful workflow
        ↓
1 minimum delegated permission
        ↓
1 real bounded case
        ↓
1 external outcome readback
```

Candidate workflow:

```text
incoming lead
→ reply/qualification
→ booking
```

or another single Cmail-backed workflow.

Do not build:

```text
full CRM
full CompanyGraph
tax
accounting suite
voice + email + WhatsApp
all trade verticals
separate dashboard
```

before the first real outcome.

---

# 21. The first live acceptance chain

The system is not considered wired until this exact sequence happens.

```text
A. Seesaw approves AgentCom UK experiment
        ↓
StrategicRoot exists

B. AgentCom binds:
   project
   scarce asset
   first moat event
   external world
        ↓
CampaignRoot exists

C. Autobuild compiles minimum plan
        ↓
ContractRoot exists

D. GitGoblin prebuild runs
        ↓
ReusePlan exists

E. Autobuild applies ReusePlan
        ↓
PlanRoot exists
ContractRoot unchanged

F. QP adapter materializes real:
   CLAIMS
   TASKS
   GATES
   GRANT requirement

G. A-Task queue created

H. Human supplies minimum real permission

I. QP issues/verifies scoped grant

J. Agent executes one external action

K. Independent external readback occurs

L. QP settles transition

M. TransitionReceipt verifies

N. AgentCom records:
   business authority delta
   action
   outcome
   cost
   human minutes

O. Seesaw consumes outcome

P. Scheduler reprices next action
```

That single chain proves the architecture better than another 100 unit tests.

---

# 22. Root CLI

Create one thin orchestration CLI.

Suggested commands:

```text
agentcom check

agentcom portfolio
agentcom project agentcom-uk

agentcom select
agentcom worlds agentcom-uk

agentcom admit agentcom-uk
agentcom underengineer agentcom-uk

agentcom compile agentcom-uk
agentcom prebuild agentcom-uk

agentcom dispatch agentcom-uk

agentcom status agentcom-uk
agentcom evidence agentcom-uk

agentcom settle agentcom-uk

agentcom outcome agentcom-uk

agentcom schedule

agentcom lineage <campaign/run/receipt>
```

The CLI orchestrates.

It does not implement external kernels.

---

# 23. Root test runner

The audit explicitly notes there is no root runner today.

Create:

```text
make check
```

It should run:

```text
root schema checks
Autobuild tests
control-plane tests
plugin-domain checks
XMRBot canonical tests

integration contract tests:
  QP adapter
  A-Task adapter
  GitGoblin adapter

lineage/hash tests
no-self-proof tests
UNKNOWN tests
grant bypass tests
ContractRoot invariance tests
```

Do not require every historical/archive package to pass.

Only canonicals.

---

# 24. Mandatory adversarial integration tests

Implement these before live external action.

### Agent cannot self-attest

Worker emits:

```text
source=live
ok=true
```

Expected:

```text
NOT PROVEN
```

### Missing QP grant

Attempt consequential action.

Expected:

```text
REFUSED
```

### Wrong grant scope

Grant allows:

```text
email.send
```

worker attempts:

```text
marketplace.purchase
```

Expected:

```text
REFUSED
```

### Prebuild route changes

Swap GitHub library.

Expected:

```text
PlanRoot changes
ContractRoot unchanged
```

### Worker edits acceptance

Expected:

```text
new ContractRoot required
old task cannot silently adopt it
```

### Missing external outcome

Action succeeded but readback unavailable.

Expected:

```text
technical state may pass
economic/outcome claim = UNKNOWN
```

### GitHub activity only

Repo has new commits.

Expected:

```text
CODE_PRESENT
not PROVEN
```

The existing campaign control plane already states this distinction explicitly.

---

# 25. Migration order

Execute in this order.

## Phase 0 — freeze

Tag current `agentcomfinal`.

No semantic mutations to imported raw archives.

---

## Phase 1 — canonical declaration

Add:

```text
CANONICAL.md
ARCHITECTURE.md
contracts/
```

Mark active/reference/archive packages.

**Gate:** exactly one owner for each responsibility.

---

## Phase 2 — root schemas

Create orchestration contracts.

Do not duplicate QP objects.

**Gate:** schema validation + deterministic canonical hashes.

---

## Phase 3 — external adapters

Implement actual:

```text
QP adapter
A-Task adapter
GitGoblin adapter
```

against current repos.

**Gate:** integration tests run against real local repositories.

---

## Phase 4 — Autobuild integration

Control plane:

```text
underengineer
→ PlanSpec
→ Autobuild
→ GitGoblin
→ PlanRoot
```

**Gate:** same strategic target + different reusable implementation preserves ContractRoot.

---

## Phase 5 — control-plane consolidation

Make v3 canonical.

Extract campaign primitives.

Demote local proof/attestation systems.

**Gate:** no live canonical state can be advanced without QP receipt.

---

## Phase 6 — AgentCom UK dry run

Use fake/sandbox external action.

**Gate:** complete end-to-end lineage exists.

---

## Phase 7 — AgentCom UK real action

One owner.
One permission.
One case.
One outcome.

**Gate:** valid QP TransitionReceipt tied to real external readback.

---

## Phase 8 — feedback loop

Outcome updates:

```text
scarce asset ledger
strategy performance
Seesaw
portfolio scheduler
```

**Gate:** next scheduled action actually changes based on verified outcome.

---

## Phase 9 — second campaign

Use BreadUp or XMRBot.

The second project must reuse at least one primitive learned/proven in the first.

**Gate:** measurable reuse.

---

# 26. Final architecture criterion

The architecture is correct only if replacing a worker model does not change the hard system.

This:

```text
GPT
DeepSeek
Muse
Gemini
future model
```

must be replaceable.

The durable chain is:

```text
Seesaw strategy
        ↓
frozen success contract
        ↓
external capability reuse
        ↓
QP authority/truth
        ↓
A-Task execution
        ↓
real world
        ↓
verified trajectory
```

The model is a speculative execution unit inside that structure.

---

# 27. Definition of DONE for this integration project

Do not declare the integration complete because the monorepo is cleaner.

DONE means:

```text
one real asset campaign
one frozen StrategicRoot
one frozen ContractRoot
one GitGoblin ReusePlan
one real A-Task DAG
one QP grant
one consequential external action
one independent outcome readback
one valid QP TransitionReceipt
one scarce-state delta
one Seesaw update
one scheduler reallocation
```

All linked by machine-readable identifiers and hashes.

Anything less is:

```text
IMPLEMENTED_UNVERIFIED
```

not complete.

The north-star test is:

> **Can I click one project and deterministically trace why it exists, what scarcity it is trying to own, what exact success contract governs it, what existing components were reused, what work was attempted, what authority allowed the action, what reality actually happened, and how that evidence changed the next allocation decision?**

If yes, AgentCom is working.

If not, do not add features. Fix the missing link.

The biggest change from the current repo is therefore conceptual: **`agentcomfinal` becomes a ledger/orchestrator of the whole autonomous economic loop, not a giant merged codebase.**

And I would resist the audit's older recommendation to make the plugin canonical schemas globally canonical. The plugin kit is excellent, but it is explicitly a ChatGPT/Codex submission/conformance system; it should become a domain pack underneath Autobuild rather than define AgentCom's universal ontology.

The strongest thing already inside v3 is the idea that **infrastructure exists to be pulled by a live scarce-asset experiment**, never to win the scheduler on its own. Keep that invariant absolutely intact.
