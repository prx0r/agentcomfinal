# agentcomdevplan.md — canonical endstate plan (saved 2026-09-14)

Status: BINDING NORTHSTAR. This supersedes serial autobuild forks: ab1–ab3
are frozen experimental history; future experiments run as Seed0 lanes.
`agentcombuild/` history is preserved. New canonical work goes in
`core/ contracts/ autobuild/ adapters/ experiments/ trajectory/
domainpacks/` per §20.

The progress is good, but the repo is at the point where **more parallel implementations will start hurting** unless you freeze the architecture now.

The biggest new conclusion from reviewing `/seed0` is that Seed0 already owns most of what we were about to invent as the “learning/tournament/agent-policy optimization layer.” Its stated purpose is a project-shape standard plus tournament harness, explicitly *not* an orchestrator; it logs measured runs, content-addresses receipts, runs competing seeds against the same idea, and turns shared failures into proposed criteria without silently applying them. That is almost exactly the missing layer between AgentCom’s orchestration and QP’s hard truth.

Here is the review/build spec I would hand directly to the coding agent.

# AgentComFinal — Canonical Endstate

## 0. Terminal state first

Do not define success as:

> “The control plane is implemented.”

The terminal externally verifiable state is:

```text
IDEA / WORLD CHANGE
        ↓
SEESAW makes a strategic admission
        ↓
AGENTCOM selects one real scarce-state target
        ↓
AUTOBUILD freezes what success means
        ↓
GITGOBLIN removes already-solved implementation
        ↓
SEED0 chooses/tests competing execution strategies
        ↓
A-TASK dispatches bounded work
        ↓
WORKER acts
        ↓
A-LOG records observations
        ↓
ACTUALITY validators judge reality
        ↓
QP settles or refuses transition
        ↓
REAL external consequence/readback
        ↓
QP outcome receipt
        ↓
AGENTCOM updates scarce-state/portfolio state
        ↓
SEED0 learns which route worked
        ↓
SEESAW reprices future allocation
        ↓
NEXT RUN uses accumulated knowledge
```

The full system is PROVEN only when the second comparable run is measurably better because of information produced by the first.

That means the actual end-to-end acceptance test is:

```text
RUN 1
→ verified external transition
→ structured learning generated

RUN 2
→ retrieves that learning
→ selects a better route
→ reaches equivalent actuality
→ lower expected cost/time/failure count
```

Without that final loop, we have autonomous execution.

With it, we have the thing you actually want:

$$
\boxed{\text{an empirically improving autonomous economic builder}}
$$

---

# 1. Current progress verdict

The repo has progressed considerably beyond the imported package pile.

The current `GO.sh` now runs ab1, ab2, ab3, reviews, demos, red-team checks and the new agentloop suite/review. Importantly, the script explicitly labels the entire chain **simulation only**, with no external actions or spend. That honesty is correct.

Current proven layers are approximately:

| Layer                               | Current state                   | Verdict                |
| ----------------------------------- | ------------------------------- | ---------------------- |
| Structured plan/spec                | ab1                             | GOOD                   |
| Grants/signatures                   | ab2                             | GOOD PROTOTYPE         |
| A-log + stoplight                   | ab3                             | STRONG                 |
| Actuality axiom                     | axioms.md                       | STRONG                 |
| Worker search harness               | agentloop                       | EARLY                  |
| Structured run output               | agentloop                       | GOOD DIRECTION         |
| Portfolio worlds/scheduler          | scarce-state-v3                 | STRONG PROTOTYPE       |
| Actual `/qp` settlement             | not yet demonstrated end-to-end | OPEN                   |
| Actual `/atask` execution           | not yet demonstrated end-to-end | OPEN                   |
| Actual GitGoblin prebuild           | not yet in canonical chain      | OPEN                   |
| Seed0 tournaments                   | exists separately               | SHOULD INTEGRATE       |
| Live external campaign              | absent                          | OPEN                   |
| Compounding improvement across runs | absent                          | **CORE OPEN QUESTION** |

Ab3 is particularly strong conceptually. It already has the important property that the worker appends telemetry but cannot set task status, and the stoplight independently re-runs declared evidence. A planted verdict is ignored and DONE is derived rather than declared.

The new `axioms.md` also captures the right constitution: probes observe, judges decide; UNKNOWN blocks; consequential actions need independent readback; contracts are frozen; the model is replaceable.

I would therefore **stop changing these fundamental ideas** and start connecting them to reality.

---

# 2. The canonical modules

The final system should have nine major logical modules.

They may reside in separate repositories, but AgentCom knows their interfaces.

```text
┌──────────────────────────────────────────────────┐
│ 1. SEESAW                                        │
│ strategy / scarcity / capital allocation         │
├──────────────────────────────────────────────────┤
│ 2. AGENTCOM                                      │
│ portfolio / campaign / world / resource control  │
├──────────────────────────────────────────────────┤
│ 3. AUTOBUILD                                     │
│ intent → immutable Actuality Contract            │
├──────────────────────────────────────────────────┤
│ 4. GITGOBLIN                                     │
│ prebuild / component archaeology / reuse         │
├──────────────────────────────────────────────────┤
│ 5. SEED0                                         │
│ execution-science / tournaments / policy search  │
├──────────────────────────────────────────────────┤
│ 6. A-TASK                                        │
│ bounded executable work DAG                      │
├──────────────────────────────────────────────────┤
│ 7. PROBE + VALIDATOR REGISTRY                     │
│ reality acquisition + deterministic judges       │
├──────────────────────────────────────────────────┤
│ 8. QP                                            │
│ truth / authority / canonical settlement         │
├──────────────────────────────────────────────────┤
│ 9. TRAJECTORY BANK                               │
│ verified experience / failures / primitives      │
└──────────────────────────────────────────────────┘
```

Everything else is a domain pack or view.

ChatGPT plugins, XMR commerce, BreadUp, Cmail, PogPet, Shopify, websites, etc. plug into this.

---

# 3. Exact responsibility of each module

## Seesaw — SHOULD

Seesaw owns:

```text
what changed?
what became abundant?
what became scarce?
what survives software commoditization?
what should we OWN?
what should we REUSE?
what is worth testing?
```

Output:

```text
StrategicDecision
```

It must never prove engineering completion.

Its numbers are priorities, not truth.

This matters because `GATES.md` currently includes `score-threshold-v1` as a hard gate.

I would demote that.

A heuristic Seesaw score must not become QP truth.

Better:

```text
Seesaw ranking
→ strategic proposal
→ accepted StrategicDecision
```

The decision may cite score components, but the score itself is not proof.

---

## AgentCom — WHAT NEXT

AgentCom is the macro control plane.

It owns:

```text
portfolio
projects
scarce assets
experiment worlds
resource capacity
campaign state
cross-project dependencies
world selection
scheduler
human strategic questions
```

Its job is:

> Choose the highest-value verified external state transition to pursue next.

The v3 scheduler already has one of the best invariants in the repo:

> scarce-asset campaigns own external experiment slots; infrastructure is pulled in as support and cannot outbid them.

Keep that unchanged.

---

## Autobuild — WHAT COUNTS AS TRUE

Autobuild owns compilation:

```text
approved intent
→ capability graph
→ requirement DAG
→ Actuality DAG
→ evidence contracts
→ validator references
→ ContractRoot
```

Autobuild does **not** need to own clever cognition.

Any future OpenAI compiler could replace the front half.

The durable artifact is:

```text
ContractRoot
```

which says exactly what reality must look like.

---

## GitGoblin — WHAT ALREADY EXISTS

Before implementation:

```text
Requirement DAG
      ↓
GitGoblin
      ↓
component candidates
      ↓
REUSE / BUY / BUILD / BLOCK
```

Then only uncovered deltas become A-Tasks.

GitGoblin should also ingest historical component outcomes:

```text
library worked
library failed
runtime compatibility
actual integration latency
license problem
security issue
maintenance problem
```

So prebuild improves with usage.

---

# 4. Seed0 has a very specific role

This is the major architectural update.

Seed0 should become:

$$
\boxed{\text{the experimental optimizer of execution strategies}}
$$

Not AgentCom.

Not QP.

Not A-Task.

Not Autobuild.

Seed0's northstar is already strikingly aligned: frozen goal/acceptance, bounded A-task DAG, rival tournament lanes, limited validator attempts, logs with re-executable evidence, and DONE only after the stoplight passes.

Its tournament already accepts multiple seeds for the same idea and mechanically ranks compliance, tests and evidence.

Its learning system clusters shared failures across seeds and emits *proposals* for new criteria rather than applying them automatically.

That is almost exactly QP's no-self-promotion doctrine.

So formalize Seed0 as:

```text
ContractRoot fixed
       ↓
N candidate execution policies
       ↓
N isolated lanes
       ↓
same gates
       ↓
QP-valid outcomes only
       ↓
tournament
       ↓
winner + failure corpus
       ↓
candidate lesson
       ↓
replay / holdout
       ↓
QP-governed promotion
```

Seed0 becomes the scientific laboratory in which Autobuild strategies evolve.

---

# 5. Current AgentLoop should become a Seed0 policy, not a new framework

This is an important peer-review finding.

Current `agentloop` implements:

```text
SEARCH
→ propose 3
→ validate
→ log
→ compile run banks
```

which is directionally right.

But do not let it become another autonomous runtime.

Instead define execution-policy seeds:

```text
policy.direct
policy.seeker3
policy.gitgoblin_first
policy.test_first
policy.redteam_first
policy.repair_first
policy.replace_component
```

`agentloop` becomes:

```text
policy.seeker3
```

inside Seed0.

Then when blocked you can actually test:

```text
same blocker
same ContractRoot

lane A = seeker3
lane B = GitGoblin-first
lane C = direct repair
lane D = architectural replacement
```

and measure which works.

That is much more powerful than deciding in advance that “three solutions” is always optimal.

---

# 6. Current Seeker has one major weakness

The current implementation does not genuinely produce three engineered solutions.

It takes the first three research hits and largely turns their summaries/sources directly into three candidate records.

So:

```text
three search results
```

is currently being treated somewhat like:

```text
three solution mechanisms
```

Those are not equivalent.

The next version should separate:

```text
RESEARCH EVIDENCE
        ↓
CAUSE HYPOTHESES
        ↓
SOLUTION MECHANISMS
        ↓
EXECUTION PLANS
        ↓
TESTS
```

A proper solution object needs:

```text
mechanism
required changes
expected affected requirements
cost
reversibility
dependencies
evidence supporting hypothesis
falsifier
```

Then Seed0 can tournament actual implementations.

---

# 7. Do not force `next10` into canonical work

The current run schema requires exactly ten next tasks and at least one visionary idea.

This is fine as an **agent cognition exercise**.

It is dangerous as a scheduler input.

If only three real high-value tasks exist, forcing ten produces seven pieces of synthetic work.

So preserve:

```text
next10 = creative/proposal channel
```

but never:

```text
next10 → A-Task directly
```

Instead:

```text
agent proposals
       ↓
dedupe
       ↓
bind to requirements
       ↓
calculate expected Actuality delta
       ↓
AgentCom scheduler
       ↓
A-Task
```

The agent can always brainstorm ten.

The system does not have to execute ten.

---

# 8. Current run compiler is too gameable for scheduling

`compile.py` currently deduplicates tasks by normalized text and increases their priority by **summing self-reported impact scores across runs**.

That means repeated agent enthusiasm can increase a task's rank.

This cannot feed the production scheduler.

Replace eventual scheduler score with something like:

$$
Priority(t)=
\frac{
P(\Delta Actuality_t)
\times
B_t
\times
IG_t
\times
SV_t
}{
1+C_t+H_t+I_t
}
$$

where:

```text
ΔActuality = expected number/value of UNKNOWN/FALSE leaves made TRUE
B = bottleneck centrality
IG = information gain
SV = Seesaw strategic value
C = execution cost
H = human burden
I = irreversibility
```

Initially estimated.

Eventually learned from Seed0 trajectories.

The agent's 1–5 `impact` becomes one weak feature, not the score.

---

# 9. Seed0's tournament scoring also needs upgrading

Seed0 currently heavily rewards:

```text
tests_green
compliance
number of evidence files
```

That made sense for project-shape benchmarking.

It is insufficient for Autobuild.

The AgentCom-specific Seed0 tournament should be:

```text
GATE FIRST:

same ContractRoot?
QP-valid?
all hard Actuality leaves TRUE?
no authority violation?
hidden holdouts pass?

ONLY THEN RANK:

cost
wall time
tokens
attempt cost
external calls
human minutes
new reusable knowledge
maintainability
```

Correctness is lexicographically prior to efficiency.

This matches Seed0's own doctrine that gates dominate objectives.

---

# 10. Actuality needs to become the universal interface

This is the strongest thing built since the original imported packages.

Current axiom:

```text
NO A-LOG
→ NO EVIDENCE
→ UNKNOWN
→ NO RECEIPT
→ NO STATE ADVANCE
```

Make this the interface between all modules.

Everything should eventually compile to:

```text
CLAIM
  |
  v
Actuality node
  |
  ├─ dependencies
  ├─ probe
  ├─ evidence schema
  ├─ judge
  ├─ freshness
  ├─ evidence class
  └─ required authority
```

Then:

```text
website works
```

becomes:

```text
page reachable
AND render successful
AND core action available
AND API returns expected output
AND external state changed
AND independent readback confirms state
AND latency threshold passes
AND security gates pass
```

This is the universal target language.

---

# 11. Important hardening needed in ab3

The conceptual design is strong, but do not promote the current implementation unchanged.

The current A-log uses a truncated `sha12` content identifier.

For canonical identity, switch to full SHA-256/QP canonical IDs.

There is no reason to accept 48-bit identity in the real evidence path.

Also, the stoplight allows commands based on the executable's **basename**.

Production rerunnable command evidence should bind:

```text
resolved executable
executable digest/version
argv
cwd
environment allowlist/hash
repo revision
input artifact hashes
timeout
```

Otherwise:

```text
python3 test.py
```

today may not mean the same thing as the same command tomorrow.

Reproducibility requires an execution envelope.

---

# 12. Validator architecture

The current ab3 spec still permits arbitrary Python task validators.

Treat Python as the development/reference implementation.

The durable validator representation should be:

```text
simple structure
→ JSON Schema / CUE

simple predicate
→ CEL

policy
→ Rego

arbitrary deterministic custom judge
→ sandboxed WASM
```

The probe can remain effectful Python/Node/etc.

The judge must be pure.

---

# 13. QP duplication must now stop

`GATES.md` currently describes local:

```text
grant-valid-v1
grant-scope-v1
receipt-signed-v1
```

These were appropriate while prototyping ab2.

They must not become a second authority kernel.

Production:

```text
AgentCom/Autobuild asks QP

QP:
constructs grant
verifies grant
executes registered gate
settles transition
verifies receipt
```

AgentCom stores references.

The `/qp` architecture explicitly says receipts are the sole state path and its kernel does not call outward.

Respect that separation literally.

---

# 14. Define the lineage precisely

`GATES.md` currently mentions a “full 7-root lineage” but does not define all seven roots in the gate catalog.

Freeze the lineage now.

I recommend:

```text
StrategicRoot
    ↓
CampaignRoot
    ↓
ContractRoot
    ↓
PlanRoot
    ↓
RunRoot
    ↓
EvidenceRoot
    ↓
QPReceiptID
    ↓
OutcomeRoot
```

Eight identities.

Meaning:

| Root          | Meaning                                    |
| ------------- | ------------------------------------------ |
| StrategicRoot | Why this deserves resources                |
| CampaignRoot  | Which external experiment/state target     |
| ContractRoot  | What counts as success                     |
| PlanRoot      | Current implementation/reuse route         |
| RunRoot       | One attempted execution                    |
| EvidenceRoot  | What was actually observed                 |
| QPReceiptID   | What truth/authority transition QP settled |
| OutcomeRoot   | Downstream real consequence                |

Then add a ninth optional identity:

```text
PromotionReceiptID
```

for learned primitive/policy promotions.

Do not compress the chain merely to preserve “7.”

---

# 15. The Trajectory object becomes extremely important

Every run should ultimately normalize to:

```text
STATE_BEFORE
      ↓
CONTEXT
      ↓
POLICY / MODEL / COMPONENTS
      ↓
ACTION / ATTEMPT SEQUENCE
      ↓
A-LOG OBSERVATIONS
      ↓
VALIDATOR RESULTS
      ↓
QP RECEIPT
      ↓
STATE_AFTER
      ↓
ECONOMIC OUTCOME
      ↓
COST
```

Canonical object conceptually:

```json
{
  "contract_root": "...",
  "plan_root": "...",

  "problem_class": "...",
  "policy_id": "seeker3",
  "model": "...",

  "components": [],
  "attempts": [],

  "actuality_before": {},
  "actuality_after": {},

  "qp_receipts": [],

  "economic_outcome": null,

  "cost": {
    "tokens": null,
    "wall_ms": null,
    "usd": null,
    "human_minutes": null
  }
}
```

This is what Seed0 should optimize over.

---

# 16. Learning hierarchy

Do not maintain separate ad-hoc memories.

Use:

```text
L0 Observation
L1 Verified Fact
L2 Repeated Pattern
L3 Candidate Primitive
L4 Replay-Proven Primitive
L5 Promoted Policy/Primitive
```

Transitions:

```text
worker emits observation
        ↓
QP establishes fact
        ↓
Seed0 sees pattern across runs
        ↓
candidate lesson/primitive
        ↓
replay against historical + holdout contracts
        ↓
promotion gate
        ↓
QP-governed promotion
```

This extends Seed0's current `learn.py`, which correctly stops at `status: proposed`.

Eventually humans need not manually promote every pattern.

But nothing self-promotes.

---

# 17. What Seed0 should contribute directly

Do not import Seed0 wholesale.

Create an adapter and reuse these conceptual primitives:

| Seed0 primitive               | AgentCom role                       |
| ----------------------------- | ----------------------------------- |
| `runs.py` / measured receipts | execution measurement               |
| `agentrun.py`                 | model/substrate measurement wrapper |
| `budgets.py`                  | attempt budgets                     |
| `tournament.py`               | competing execution strategies      |
| `learn.py`                    | shared failure → candidate lesson   |
| seed variants                 | execution-policy families           |
| content-addressed runs        | reproducibility                     |
| frozen briefs/rubrics         | ContractRoot-aligned experiments    |
| max retry / replan breaker    | stuck-loop bound                    |
| human instrument ideas        | later H-interface                   |

Seed0's thesis explicitly says it is not an orchestrator or runtime; it standardizes and inspects autonomous work.

That is exactly why it fits cleanly.

---

# 18. Simplify the current numbered Autobuild roadmap

The current `DEV_PLAN` defines ab1 through ab10 as sequential implementations.

I would stop treating all ten as future production generations.

ab1–ab3 have done their job:

```text
ab1 discovered compiler/gate shape
ab2 discovered authority/signature issues
ab3 discovered Actuality/A-log shape
```

Freeze those as experimental history.

Then create:

```text
autobuild-core/
```

by promoting only their surviving primitives.

Future experiments should run through Seed0 as **lanes**, rather than becoming `autobuild4`, `autobuild5`, etc. production forks.

For example:

```text
experiment:
validator_runtime

lane A:
Python validators

lane B:
CEL

lane C:
WASM

ContractRoot:
identical

actuality corpus:
identical

Seed0:
tournament results
```

That is much cleaner scientifically.

---

# 19. Backward roadmap from terminal state

The roadmap should be driven backward from the externally proven system.

| Stage | Required state                | Hard acceptance                                                                         |
| ----- | ----------------------------- | --------------------------------------------------------------------------------------- |
| E9    | self-improvement demonstrated | second comparable contract solved measurably better using prior verified trajectory     |
| E8    | governed learning active      | Seed0 candidate primitive/policy passes replay+holdout and receives promotion receipt   |
| E7    | live economic feedback        | verified outcome changes Seesaw/scheduler decision                                      |
| E6    | first scarce-state event      | real external action + independent readback + QP receipt                                |
| E5    | real execution stack          | actual QP + actual A-Task adapters used, not copies                                     |
| E4    | optimizer connected           | Seed0 runs ≥2 execution strategies against same ContractRoot                            |
| E3    | prebuild active               | GitGoblin ReusePlan changes PlanRoot while ContractRoot remains unchanged               |
| E2    | Actuality contract            | plan compiles to dependency DAG with probes/judges and no unprovable hard leaf          |
| E1    | strategic selection           | one real asset campaign admitted by Seesaw and selected by AgentCom                     |
| E0    | canonicalization              | one production implementation per responsibility; experiments/archive clearly separated |

Build in reverse order operationally:

```text
E0
→ E1
→ E2
→ E3
→ E4
→ E5
→ E6
→ E7
→ E8
→ E9
```

But never work on an E8 feature while E5 is still fake.

---

# 20. Immediate next milestone: E0

Before adding capabilities:

```text
FREEZE CURRENT:

ab1
ab2
ab3
agentloop

CREATE:

core/
contracts/
adapters/
domainpacks/
experiments/
trajectory/
```

Recommended canonical structure:

```text
agentcomfinal/
│
├── core/
│   ├── portfolio.py
│   ├── campaigns.py
│   ├── worlds.py
│   ├── scheduler.py
│   └── lineage.py
│
├── contracts/
│   ├── strategic.schema.json
│   ├── campaign.schema.json
│   ├── actuality.schema.json
│   ├── trajectory.schema.json
│   └── promotion.schema.json
│
├── autobuild/
│   ├── compiler/
│   ├── actuality/
│   └── registry/
│
├── adapters/
│   ├── qp.py
│   ├── atask.py
│   ├── gitgoblin.py
│   ├── seed0.py
│   └── seesaw.py
│
├── experiments/
│   └── policies/
│
├── domainpacks/
│   ├── chatgpt/
│   ├── commerce/
│   ├── communications/
│   └── xmr/
│
├── trajectory/
│   ├── observations/
│   ├── verified/
│   ├── candidates/
│   └── promoted/
│
└── archive/
    ├── ab1/
    ├── ab2/
    └── ab3/
```

Not necessarily physically move all files immediately.

But establish ownership.

---

# 21. E1: pick exactly one real campaign

Still use:

```text
agentcom-uk
```

because its current underengineering is nearly perfect.

Its target is:

> acquire one real permission and use it to solve one painful business job.

Its minimum live path is already defined as one UK trade business, one painful workflow, one minimum delegated permission, one real bounded case, then outcome measurement.

Do not write more portfolio infrastructure until that gets through the full stack.

---

# 22. E2: compile that one campaign into Actuality

Example:

```text
GOAL:
Handle one real inbound business lead.

ACTUALITY DAG:

business identity verified
AND
delegated send/reply authority exists
AND
incoming lead observed
AND
agent response constructed
AND
outbound response actually sent
AND
provider readback confirms send
AND
customer/business outcome observed
```

Each leaf needs:

```text
probe
evidence schema
judge
freshness
evidence class
authority class
```

No leaf can be “agent judges quality.”

---

# 23. E3: GitGoblin before implementation

Ask GitGoblin:

```text
what already exists for:
email receive
email send
provider readback
business identity
thread state
webhooks
OAuth
```

Then produce:

```text
ReusePlan
```

Required gate:

```text
same ContractRoot before/after
different PlanRoot
```

No GitGoblin result means no engineering BUILD task unless an explicit exemption exists.

---

# 24. E4: first Seed0 Autobuild tournament

Take one difficult leaf.

Example:

```text
reliably prove provider send + independent readback
```

Freeze ContractRoot.

Run:

```text
Lane A: direct worker
Lane B: seeker3
Lane C: GitGoblin-first
```

Same model initially.

Then compare only after each faces the same Actuality gates.

This is the first serious Seed0 integration.

---

# 25. E5: real adapters

This is the point where prototypes stop counting.

Use actual:

```text
prx0r/qp
prx0r/atask
prx0r/qp
prx0r/seed0
```

No local clone of semantics.

A QP gate/receipt is produced by QP.

A-Task DONE comes from A-Task.

A GitGoblin ReusePlan is produced by GitGoblin.

Seed0 tournament data is produced by Seed0.

AgentCom stores lineage references.

---

# 26. E6 is the most important milestone in the entire roadmap

One consequential action.

Not simulation.

For example:

```text
real company identity
        ↓
real inbound lead
        ↓
QP-scoped grant
        ↓
agent sends bounded real reply
        ↓
provider confirms message exists
        ↓
reply/outcome later observed
        ↓
QP receipt
```

Once this happens:

$$
\boxed{\text{the architecture has touched reality}}
$$

Until then it is an excellent simulator.

---

# 27. E7: outcome must alter scheduling

After outcome:

```text
success/failure
cost
human minutes
latency
customer consequence
scarce asset delta
```

Seesaw gets new evidence.

AgentCom must show that the next selected task/campaign changes because of it.

If an outcome enters the database but changes no decision, the feedback loop isn't functioning.

---

# 28. E8: Seed0 learns

Suppose `GitGoblin-first` wins repeatedly for API integration blockers.

Seed0 detects:

```text
blocker_class = external API integration
policy = gitgoblin-first
success rate = ...
cost = ...
```

It proposes:

```text
candidate policy:
for external API blockers, run GitGoblin before general web search
```

Then test that proposal against historical/held-out contracts.

Only after it passes do we mint:

```text
PromotionReceipt
```

Then WorkerPolicy v2 changes.

That is real self-improvement.

---

# 29. E9: the decisive benchmark

Take another external integration leaf.

Run it with promoted policy.

Compare with pre-promotion history.

Hard metrics:

```text
success probability
attempts to Actuality=TRUE
tokens
wall time
USD
external calls
human minutes
regressions
```

The whole Autobuild thesis is empirically validated only if those improve without weakening gates.

---

# 30. Root invariants for the final system

The current QP invariants plus Actuality are almost enough.

The production system should structurally enforce one constitution:

> Workers propose. Probes observe. Validators judge. QP commits. Seed0 compares. Seesaw allocates.

Everything else follows.

In particular:

```text
workers do not decide truth

validators do not perform external actions

probes do not issue verdicts

Seed0 does not weaken gates to win tournaments

AgentCom does not mint QP truth

Seesaw does not call heuristic scores facts

A-Task does not invent acceptance

GitGoblin does not decide strategic ownership

Autobuild does not choose portfolio allocation

QP does not decide what business should exist
```

That is the architecture.

---

# 31. Highest-priority work from here

| Priority | Work                                                   | Why                                   |
| -------: | ------------------------------------------------------ | ------------------------------------- |
|        1 | Freeze canonical module ownership                      | Prevent architectural entropy         |
|        2 | Import Seed0 as optimizer adapter                      | Stop reinventing learning/tournaments |
|        3 | Promote ab1–3 winners into one `autobuild-core`        | End experimental fork proliferation   |
|        4 | Define exact 8-root lineage                            | Remove current lineage ambiguity      |
|        5 | Replace local QP semantics with actual `/qp` adapter   | Establish real truth boundary         |
|        6 | Replace local execution semantics with actual `/atask` | Establish real execution boundary     |
|        7 | Add GitGoblin prebuild to every BUILD                  | Make reuse mandatory                  |
|        8 | Compile AgentCom UK into Actuality DAG                  | First real target                     |
|        9 | Seed0 tournament one difficult leaf                    | First empirical policy comparison     |
|       10 | Execute one live bounded AgentCom UK action            | First proof system touches reality    |

Do not prioritize dashboard polish, generic plugin features, more schemas, more project definitions, or a richer scheduler before these.

---

# 32. Overall peer-review verdict

The project is no longer vague.

There is now a coherent architecture.

The strongest parts are:

```text
QP separation of cognition/truth/authority
Actuality
A-log / stoplight
frozen contract
world evidence ceilings
Underengineer
asset-campaign-first scheduling
structured agent run records
Seed0 tournament + learning philosophy
```

The weakest part is now **integration reality**.

You currently have excellent local demonstrations of each concept, but too many ideas still exist as parallel prototypes.

The highest-value move is therefore not invention.

It is:

$$
\boxed{\textbf{collapse prototypes into one real closed loop}}
$$

And Seed0 resolves an important missing question:

> Who optimizes the worker, prompt, search strategy, decomposition and implementation route?

Answer:

$$
\boxed{\textbf{Seed0 does — under frozen Autobuild contracts and QP truth.}}
$$

So the canonical endstate is:

```text
SEESAW
   ↓
AGENTCOM
   ↓
AUTOBUILD
   ↓
GITGOBLIN
   ↓
SEED0
   ↓
A-TASK / WORKER
   ↓
ACTUALITY
   ↓
QP
   ↓
REALITY
   ↓
TRAJECTORY
   ↓
SEED0 learns execution
   +
SEESAW learns allocation
   ↓
AGENTCOM schedules again
```

That is the system I would now freeze as the northstar.

The next milestone is not `autobuild4`.

It is:

$$
\boxed{\textbf{one ContractRoot → one real QP-authorized action → one independently read-back outcome}}
$$

with Seed0 running the first genuine competing execution strategies on part of that chain.

The key change I'd make immediately is to reinterpret your numbered Autobuild attempts as **experimental history**. You now have enough primitives to stop evolving architecture by serial forks. Seed0 gives you the better method: freeze the target, run competing implementations/policies as lanes, let identical gates judge them, bank the failures, and promote only what survives.
