# worker_advice.md — old advice on the agent harness (saved 2026-09-14)

Status: ADVISORY, not gospel. Triaged into the build where useful; rejected
items logged at the bottom with reasons. Source: design discussion.

The key distinction is:

$$
\boxed{\text{Invariants constrain reality; axioms constrain cognition.}}
$$

`ACTUALITY`, frozen acceptance, grants, receipts, `UNKNOWN`, append-only history, etc. should **not** live merely in `AGENTS.md`. The agent should be physically unable to bypass them.

`AGENTS.md` should instead teach an arbitrary frontier model **how to behave intelligently inside those walls**.

I would make the following the canonical agent harness.

# Autobuild Agent Harness

## 0. Core model

An autonomous worker is a speculative execution engine.

It may:

```text
reason
search
invent
reuse
code
run tools
test hypotheses
try alternate routes
recommend strategy
generate new ideas
```

It may not:

```text
define success
declare success
alter frozen acceptance
self-attest reality
mint authority
promote its own observations to truth
erase failed attempts
```

The surrounding system owns truth.

```text
                    FROZEN CONTRACT
                           │
                           ▼
                     ACTUALITY DAG
                           │
                           ▼
                    READY TARGET
                           │
                           ▼
                 ┌──────────────────┐
                 │      AGENT       │
                 │ speculative CPU  │
                 └────────┬─────────┘
                          │
            research / attempts / code
                          │
                          ▼
                       A-LOGS
                 observations only
                          │
                          ▼
                     VALIDATORS
                          │
                          ▼
                         QP
                          │
                  TRUE/FALSE/UNKNOWN
                          │
                          ▼
                   state may advance
```

The model can hallucinate that it has succeeded forever.

Nothing happens unless reality agrees.

---

# 1. Three separate layers of rules

## Layer A — Structural invariants

These are not instructions.

They must be enforced by code.

Examples:

```text
ACTUALITY
NO SELF-PROOF
FROZEN CONTRACT
UNKNOWN NEVER PASSES
GRANTS FOR CONSEQUENCES
APPEND-ONLY HISTORY
INDEPENDENT EVALUATOR
NO SILENT ACCEPTANCE CHANGE
ONLY VERIFIED TRANSITIONS ADVANCE STATE
```

If an agent ignores these, nothing happens.

This is the strongest class of rule.

---

## Layer B — Agent axioms

These belong in the worker policy / `AGENTS.md`.

They describe the desired cognitive strategy.

Examples:

```text
Be concise.
Prefer evidence over explanation.
Search before rebuilding.
When blocked, generate multiple distinct solutions.
Test cheap reversible approaches first.
Never hide uncertainty.
Separate observation from inference.
Do not retry an already falsified route without new evidence.
Produce reusable structured knowledge on every run.
Think beyond the current implementation and surface high-value future ideas.
Rank autonomous next work by impact.
```

Violating these does not directly corrupt canonical state because Layer A still protects it.

But we record policy adherence so we can later determine which agent policies work best.

---

## Layer C — Dynamic policy

This changes according to target.

Examples:

```text
maximum spend
maximum attempts
allowed tools
allowed repositories
whether web research is permitted
whether consequential actions are permitted
latency budget
human escalation rules
```

These should be structured data, not buried in prompts.

---

# 2. `AGENTS.md` should itself be generated

Do not make hand-written prose the canonical policy.

Create:

```text
agent_policy.json
```

and derive:

```text
AGENTS.md
SYSTEM_PROMPT.md
```

as human/model-readable projections.

Canonical policy:

```json
{
  "policy_id": "autobuild-worker-v1",

  "communication": {
    "clarity": "high",
    "verbosity": "low",
    "unsupported_claims": "forbidden"
  },

  "problem_solving": {
    "search_before_build": true,
    "distinct_solutions_when_blocked": 3,
    "prefer_reversible_tests": true,
    "prefer_existing_components": true
  },

  "learning": {
    "record_failed_routes": true,
    "record_negative_facts": true,
    "record_new_ideas": true,
    "record_uncertainties": true
  },

  "planning": {
    "next_tasks_max": 10,
    "rank_by": "expected_verified_progress_per_cost"
  },

  "truth": {
    "agent_may_declare_success": false,
    "agent_may_promote_facts": false
  }
}
```

This is important because eventually we can test:

```text
worker-policy-v1
worker-policy-v2
worker-policy-v3
```

against identical ContractRoots.

The prompt itself becomes experimentally optimizable.

---

# 3. The worker should see the contract but not control the judge

The agent should **not** be completely blind.

It needs to know:

```text
desired state
requirements
public acceptance criteria
available evidence
current failures
dependencies
budgets
```

otherwise it cannot solve efficiently.

But separate:

```text
VISIBLE CONTRACT
```

from:

```text
INDEPENDENT VALIDATION
```

And eventually add:

```text
HIDDEN HOLDOUT INVARIANTS
```

So:

```text
agent knows:
"checkout must create a real order"

agent cannot alter:
the validator proving it

agent may know:
order must be readable through provider API

agent does not necessarily know:
all adversarial tests run against checkout
```

This prevents overfitting.

Conceptually:

$$
Validation =
PublicContract
\land
HiddenInvariants
\land
ExternalReadback
$$

This is analogous to training tests versus held-out evaluation.

---

# 4. Worker state machine

Every worker run should follow the same high-level machine:

```text
OBSERVE
   ↓
ORIENT
   ↓
SELECT TARGET
   ↓
ATTEMPT
   ↓
PROBE REALITY
   ↓
VALIDATION RESULT?
   │
   ├── TRUE ─────→ HAND BACK EVIDENCE
   │
   ├── FALSE ────→ DIAGNOSE
   │
   └── UNKNOWN ──→ ACQUIRE INFORMATION
                         │
                         ▼
                     DISCOVERY
                         │
                         ▼
                    3 SOLUTIONS
                         │
                         ▼
                   TEST SOLUTIONS
                         │
                         ▼
                      REPEAT
```

The worker does not decide when the target is complete.

QP/A-Task state causes the target to disappear from its READY queue.

---

# 5. The blocked-target primitive

This should become a major harness primitive.

When the agent encounters:

```text
FAIL
UNKNOWN
BLOCKED
```

it should not just continue generating code.

It enters:

```text
DISCOVERY_MODE
```

Default discovery sequence:

```text
1. inspect local implementation/repo
2. inspect existing project knowledge
3. ask GitGoblin for existing capability
4. search official documentation
5. search GitHub implementations/issues
6. search broader web
7. search arXiv/papers if the problem is conceptual/novel
```

Not every problem requires every source.

But the output must be structured.

---

# 6. Three-solution rule

For a genuine blocker, require three **materially different** candidate solutions.

Not:

```text
solution 1: change timeout to 5s
solution 2: change timeout to 6s
solution 3: change timeout to 7s
```

But:

```text
A. repair current library integration
B. replace component with existing alternative
C. change architecture to remove dependency
```

Each candidate becomes:

```json
{
  "solution_id": "sol-03",

  "hypothesis":
    "The websocket library is incompatible with this runtime.",

  "intervention":
    "Replace library X with maintained library Y.",

  "why_it_might_work": [
    "Y supports the target runtime",
    "Y has passing upstream integration tests"
  ],

  "predicted_gate_effect": [
    "req.websocket_connect => TRUE"
  ],

  "cost": {
    "estimated_minutes": 12,
    "money": 0
  },

  "risk": "LOW",

  "reversibility": "HIGH",

  "new_dependencies": [],

  "evidence_supporting": [],

  "falsifier":
    "Same connection failure occurs with Y under identical probe."
}
```

This is valuable data even before testing.

---

# 7. Solution ordering

Do not let the model arbitrarily pick its favorite.

Rank candidate interventions.

Initial formula:

$$
S_i =
\frac{
P_i
\times I_i
\times R_i
\times L_i
}{
1 + C_i + H_i
}
$$

where:

* \(P_i\) = estimated probability of resolving blocker;
* \(I_i\) = number/value of blocked gates potentially unlocked;
* \(R_i\) = reversibility;
* \(L_i\) = knowledge value if attempted;
* \(C_i\) = cost;
* \(H_i\) = human burden.

Store every input separately.

Do not hide the score behind prose.

Then test highest-value reversible route first.

Later these probabilities can be learned from actual histories.

---

# 8. Runs should generate data, not reports

Do not let the canonical output of an agent run be:

> “I fixed several issues and checkout mostly works.”

That is nearly worthless.

Every run should return a machine-readable `RunIntelligence` object.

Example:

```json
{
  "schema": "run-intelligence-v1",

  "run_id": "R-...",
  "contract_root": "...",
  "plan_root": "...",
  "worker_policy": "autobuild-worker-v1",
  "model": "...",

  "target": {
    "requirement_id": "checkout.order_created",
    "starting_state": "FALSE"
  },

  "actions": [],

  "research": [],

  "hypotheses": [],

  "solutions_considered": [],

  "attempts": [],

  "observations": [],

  "validation_results": [],

  "new_facts": [],

  "negative_facts": [],

  "unknowns": [],

  "conflicts": [],

  "components_evaluated": [],

  "new_fixtures": [],

  "ideas": [],

  "risks": [],

  "next_tasks": [],

  "cost": {},

  "worker_summary": {}
}
```

The prose summary is generated from this data.

Not vice versa.

---

# 9. Every attempted action becomes an object

Example:

```json
{
  "attempt_id": "ATT-14",

  "target": "checkout.order_created",

  "solution_id": "SOL-3",

  "action": {
    "kind": "CODE_CHANGE",
    "description": "Replace fake checkout callback with live backend call"
  },

  "input_state_root": "...",

  "output_state_root": "...",

  "observed_effect": {
    "api_status": 201,
    "readback_found": true,
    "latency_ms": 421
  },

  "validation": {
    "status": "PENDING_QP"
  },

  "cost": {
    "duration_ms": 38721,
    "tokens": 14021
  }
}
```

Now years later you can answer:

> Which kinds of interventions resolve checkout failures most reliably?

Because you have actual data.

---

# 10. Research itself becomes structured

A web/GitHub/arXiv search must not disappear into context.

Record:

```json
{
  "research_id": "RES-18",
  "question": "Why does websocket reconnect fail on Cloudflare Workers?",

  "source_type": "GITHUB",

  "query": "...",

  "sources": [
    {
      "ref": "...",
      "relevance": 0.91
    }
  ],

  "claims_extracted": [
    {
      "claim": "Library X relies on Node APIs unavailable in Workers.",
      "confidence": 0.96,
      "evidence_refs": ["..."]
    }
  ],

  "decision_effect":
    "Raised score of solution SOL-2."
}
```

This means future agents do not need to repeat the research blindly.

---

# 11. Separate facts, hypotheses and ideas

This is extremely important.

Do not throw them all into “memory.”

Use at least:

```text
FACT
NEGATIVE_FACT
HYPOTHESIS
UNKNOWN
IDEA
RISK
PREDICTION
DECISION
OBSERVATION
```

For example:

```json
{
  "type": "NEGATIVE_FACT",
  "subject": "library:x",
  "predicate": "works_on",
  "object": "cloudflare-workers",
  "value": false,
  "scope": {
    "version": "3.1.4"
  },
  "evidence": ["A-LOG-..."]
}
```

versus:

```json
{
  "type": "IDEA",
  "title": "Replace websocket architecture with event stream",
  "horizon": "FUTURE",
  "expected_value": 0.7,
  "why": "...",
  "dependencies": [],
  "origin_run": "R-..."
}
```

The first can eventually become verified knowledge.

The second remains speculative.

---

# 12. Visionary ideas should absolutely be captured

I think your “20 ideas by run 4” example is valuable.

Give every worker an explicit side-channel:

```text
IDEA_BUFFER
```

During work it can emit ideas that are **not allowed to change the current target**.

Examples:

```text
better architecture
product extension
new moat
new use case
cross-project primitive
future automation
new monetization path
possible bottleneck
research question
```

This prevents scope creep while preserving creativity.

A structured idea:

```json
{
  "idea_id": "...",

  "title":
    "Use validator traces as training corpus for automatic requirement decomposition",

  "origin": {
    "project": "breadup",
    "run": "R-14",
    "trigger":
      "Repeated manual decomposition of marketplace postconditions"
  },

  "thesis": "...",

  "expected_upside": 4,

  "novelty": 3,

  "confidence": 0.46,

  "time_horizon": "LATER",

  "would_change_current_scope": true,

  "action": "STORE_NOT_EXECUTE"
}
```

Then scope discipline remains intact.

---

# 13. The idea compiler

Periodically take accumulated ideas:

```text
Run 1  ─┐
Run 2   ├──→ Idea Ledger
Run 3   │
Run 4  ─┘
```

and cluster:

```text
duplicates
reinforcing ideas
contradictions
dependencies
recurring bottlenecks
cross-project primitives
strategic opportunities
```

Then send high-value clusters to Seesaw.

So:

```text
worker creativity
     ↓
IDEA ledger
     ↓
clustering
     ↓
Seesaw
     ↓
BUILD / VALIDATE / WATCH / DROP
```

A worker cannot scope-creep its own idea into existence.

Excellent separation.

---

# 14. Every run should recommend autonomous next work

At the end of every run, emit up to 10 tasks.

Not necessarily exactly 10 if only 4 real tasks exist.

Each:

```json
{
  "task_id": "...",

  "objective":
    "Verify provider readback after checkout.",

  "target_requirements": [
    "checkout.external_readback"
  ],

  "why_now":
    "Blocks two downstream requirements and currently UNKNOWN.",

  "expected_progress": 0.82,

  "information_value": 0.91,

  "cost": 0.18,

  "human_needed": false,

  "reversibility": 1.0,

  "dependencies": [],

  "recommended_mode":
    "RESEARCH_THEN_TEST",

  "priority_score": 3.89
}
```

Then AgentCom/A-Task—not the model—chooses which becomes READY.

---

# 15. Task ranking should reward verified progress, not motion

Something like:

$$
Priority(t)=
\frac{
P(\Delta Actuality)
\times
BottleneckCentrality
\times
InformationGain
\times
StrategicValue
}{
1+
Cost+
HumanBurden+
Irreversibility
}
$$

Most importantly:

$$
P(\Delta Actuality)
$$

not:

```text
probability agent can write some code
```

A tiny API probe that resolves a critical UNKNOWN might outrank three hours of feature implementation.

Good.

---

# 16. Introduce the `Blocker` object

Whenever progress halts:

```json
{
  "blocker_id": "...",

  "requirement_id": "...",

  "state": "FALSE",

  "failure_class": "API_INCOMPATIBILITY",

  "observed": [],

  "known_causes": [],

  "unknowns": [],

  "attempted_solutions": [],

  "untried_solutions": [],

  "research_state": "NEEDS_EXTERNAL_DISCOVERY"
}
```

This becomes durable.

If another project hits the same blocker later, GitGoblin/AgentCom can retrieve prior solutions.

---

# 17. Microprocessor analogy becomes precise

This is now genuinely useful rather than metaphorical.

## Contract

Instruction definition.

## Requirement

Register target.

## Actual state

Register value.

## Validator

Logic gate.

## Grant

Permission bit.

## Worker

Speculative execution unit.

## A-Task

Instruction scheduler.

## QP

Commit/retirement unit.

## A-log

Observation bus.

## Run ledger

Trace buffer.

## GitGoblin/web/arXiv

External memory/cache hierarchy.

## Agent policy

Branch/search policy.

## Autobuild

Compiler.

## AgentCom

Control plane / scheduler.

The important CPU analogy is speculative execution.

A CPU can execute work speculatively.

But architecture state is not committed until the instruction retires correctly.

Likewise:

```text
agent can do arbitrary speculative work

but

project state changes only when QP retires the transition
```

That is a very clean model.

---

# 18. Search is the agent's cache-miss handler

This gives us a simple behavioral rule.

When the agent reaches something it cannot solve from local state:

```text
CACHE MISS
```

it invokes discovery.

Suggested hierarchy:

```text
L0 current target/run context
L1 project knowledge
L2 cross-project primitive/failure library
L3 GitGoblin
L4 official docs
L5 GitHub
L6 web
L7 papers/arXiv
L8 human
```

Escalate only as needed.

This should reduce repeated external research substantially over time.

---

# 19. `AGENTS.md` can be surprisingly small

Most safety/correctness should come from structure.

So the canonical agent-facing policy might only need something like:

```text
You are an untrusted speculative worker inside Autobuild.

Your objective is to maximize verified progress and reusable information
per unit cost.

You cannot declare completion. Only external validation can advance state.

Always:
1. Inspect the current target, dependencies, known facts and prior attempts.
2. Prefer existing proven components to new implementation.
3. When genuinely blocked, research the cause and produce three materially
   distinct candidate solutions.
4. Test the cheapest high-information reversible solution first.
5. Never repeat a falsified route without identifying new evidence.
6. Separate observations, facts, hypotheses, unknowns and ideas.
7. Preserve failures as useful structured data.
8. Emit future ideas without expanding current scope.
9. Finish every run with ranked autonomous next actions.
10. Be concise; evidence and structured state matter more than narration.
```

That's enough.

Because the hard constitution is elsewhere.

---

# 20. The canonical run artifact

I would ultimately require every model invocation to produce:

```text
RunIntelligence
├── context
├── target
├── current_actuality
│
├── reasoning_outputs
│   ├── hypotheses
│   ├── solution_candidates
│   └── decisions
│
├── work
│   ├── actions
│   ├── attempts
│   └── research
│
├── reality
│   ├── observations
│   ├── probes
│   └── validator_results
│
├── learning
│   ├── facts
│   ├── negative_facts
│   ├── unknowns
│   ├── conflicts
│   ├── fixtures
│   └── component_performance
│
├── creativity
│   ├── ideas
│   ├── opportunities
│   └── risks
│
├── planning
│   └── next_tasks[0..10]
│
└── economics
    ├── tokens
    ├── wall_time
    ├── api_cost
    ├── human_minutes
    └── useful_yield
```

Note `next_tasks[0..10]` — up to ten, not exactly ten.

---

# 21. This becomes very interesting after thousands of runs

Eventually you have:

```text
problem class
worker model
agent policy
research sequence
solutions considered
solution attempted
libraries used
validator
failure
success
cost
latency
actuality delta
future ideas
```

Then we can learn:

$$
P(solution\ succeeds
\mid
problem,\ context,\ component,\ model)
$$

and:

$$
P(research\ source\ yields\ useful\ solution
\mid
blocker\ type)
$$

and:

$$
E(cost\ to\ resolve\ requirement)
$$

and even:

$$
\text{best worker policy}
\mid
\text{task class}
$$

At that point AgentCom stops using fixed heuristics and starts routing based on empirical trajectories.

---

# 22. The endgame

The system gradually moves from:

```text
agent thinks of random solution
```

to:

```text
blocker classified
      ↓
retrieves 47 historical analogous blockers
      ↓
knows solution family B succeeded 81% of time
      ↓
knows model X performs best on this requirement class
      ↓
knows component Y has lowest verified failure rate
      ↓
attempts best route
      ↓
actuality gate
      ↓
new trajectory added
```

That is the Qubic-ant property you were pointing at.

Every traversal changes the future search landscape.

But critically, the terrain is not altered by the agent merely *believing* something.

It changes only through recorded observations, implied verified transitions and later promoted reusable knowledge.

The canonical mantra I'd put on Autobuild is therefore:

> **Agents speculate. Reality validates. QP commits. History compounds.**

That captures the whole system.
