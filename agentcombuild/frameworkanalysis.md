# frameworkanalysis.md — frontier substrate review (saved 2026-09-14)

Status: ADVISORY. Verdict adopted: do NOT go Harbor/Letta native; steal
what works (ATIF export, memory projection, OTel mapping, ScriptedModel
executor pattern); `/cg` is the canonical local experiment runner;
OpenAI Agents API is the cognition harness. Sandbox/container layers wait
until isolation is a measured bottleneck.

Yes. The frontier suggests we are missing a few **concrete substrate pieces**, but importantly we do **not** need another grand architecture. The cleanest additions are Harbor for trials/environments, Letta-style context/memory, and standard trajectory/telemetry formats.

The biggest insight is that we currently conflate three kinds of history:

$$
\boxed{
\text{truth} \neq \text{experience} \neq \text{memory}
}
$$

QP owns **truth**. Harbor/AgentCom owns **full-fidelity experience**. Letta-style context owns **compressed working memory**.

That separation is worth adding.

### What I would steal/import

| Frontier project                     | What it already solves                                                                                           | What AgentCom should do                                       |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Harbor Framework**                 | agent trials, tasks, verifiers, Docker/cloud environments, parallel rollouts, arbitrary coding agents, RL traces | Make it Seed0's execution/eval backend                        |
| **Harbor ATIF**                      | full-fidelity standard agent trajectory format                                                                   | Export every AgentCom run to ATIF                             |
| **Letta `trajectory`**               | compact cross-harness experience format designed for agents to reread                                            | Use as the token-efficient memory projection                  |
| **Letta Context Repository / MemFS** | Git-versioned long-term agent memory/context                                                                     | Steal the pattern for Business/Worker memory                  |
| **Letta memory evals**               | memory retrieval + memory-generation quality                                                                     | Add memory quality gates to Seed0                             |
| **Temporal**                         | crash-resumable, long-running workflows/HITL                                                                     | Consider later for durable external workflows                 |
| **OpenTelemetry GenAI**              | emerging provider-neutral tracing vocabulary                                                                     | Map our telemetry outward to it                               |
| **Braintrust**                       | trace UI, online scoring, production failure→eval datasets                                                       | Optional visualization/eval frontend; don't rebuild one       |
| **Agent Harbor**                     | isolated concurrent coding agents, recording/replay, copy-on-write workspaces                                    | Evaluate as replacement for home-grown worktree orchestration |

The strongest immediate steals are **Harbor + Letta trajectory**, not Temporal or Braintrust.

---

## 1. Harbor is basically the thing we were about to build around Seed0

This is the big one.

Harbor, from the Terminal-Bench team, already supports arbitrary agents including Codex, Claude Code, OpenHands, etc.; standardized tasks with test/verifier scripts; Docker and cloud environments; thousands of parallel experiments through Daytona/Modal/etc.; and rollout generation for RL. ([GitHub][1])

A Harbor task is essentially:

```text
instruction
+
environment
+
agent
+
verifier
=
trial
```

That is dangerously close to:

```text
ContractRoot
+
Git candidate
+
WorkerPolicy
+
Actuality validator
=
Seed0 lane
```

So **do not build our own general trial runtime**.

Instead:

```text
                    SEED0
            chooses competing lanes
                       │
                       ▼
                    HARBOR
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
   Codex/OpenAI     Claude Code      Worker X
   worktree A       worktree B       worktree C
       │               │               │
       └───────────────┼───────────────┘
                       ▼
              same frozen verifier
                       │
                       ▼
                 Harbor result
                       │
                       ▼
               QP verification
                       │
                       ▼
                Seed0 tournament
```

Harbor even gives us a registry of environments and supports Daytona, Modal and other sandbox providers. ([GitHub][1])

This massively simplifies Seed0.

**Seed0 should choose experiments. Harbor should execute experiments.**

---

# 2. Git still remains important

Harbor does **not** replace the Git architecture we discussed.

Git answers:

> What exact source state did the agent create?

Harbor answers:

> What happened when an agent tried this task in this environment?

QP answers:

> Is the claimed result canonically established?

So:

```text
Git commit SHA
      │
      ▼
Harbor Trial
      │
      ▼
ATIF trajectory
      │
      ▼
Actuality validator
      │
      ▼
QP Receipt
```

This is cleaner than using Git worktrees as our entire experiment framework.

Start with worktrees because they cost nothing.

Once parallelism becomes painful, let Harbor manage environment execution.

---

# 3. Harbor has already standardized the full trajectory format we need

This is a major thing we were missing.

Harbor's **Agent Trajectory Interchange Format — ATIF** is a JSON standard specifically for complete replayable agent trajectories. It stores agent messages, tool calls, observations, cost/token metrics, subagent trajectories and RL fields. Current ATIF also supports embedded subagent trajectories and multimodal content. ([Harbor][2])

So instead of inventing our own mega-schema forever:

```text
OpenAI Events
Codex logs
Seed0
Harbor
Claude
etc
```

should normalize into:

```text
ATIF
```

Then our **AgentCom envelope** only needs to add:

```json
{
  "contract_root": "...",
  "plan_root": "...",
  "candidate_sha": "...",
  "policy_id": "...",
  "qp_receipts": [],
  "actuality_delta": {},
  "scarce_asset_delta": {}
}
```

ATIF handles the actual agent interaction trace.

This would remove a lot of schema maintenance.

---

# 4. But Letta identified a clever reason ATIF is not enough

This is where Letta is especially relevant.

Letta released its own `trajectory` package in July specifically because **full replay trajectories are too expensive for another agent to consume as memory**.

They explicitly contrast their format with Harbor's ATIF:

* ATIF = full replay/benchmark/training.
* Letta trajectory = token-efficient representation for agents learning from old experience. ([Letta][3])

They report their normalized representation can reduce trajectory token size by roughly 5× in sampled sessions. ([GitHub][4])

So I would adopt a **two-view trajectory system**:

```text
                   RAW RUN
                      │
                      ▼
              FULL EXPERIENCE
                  Harbor ATIF
                      │
       ┌──────────────┴──────────────┐
       ▼                             ▼
   replay/evals                 memory compiler
   Seed0/RL                           │
                                     ▼
                              Letta trajectory
                                     │
                                     ▼
                                 AGENT
```

That's excellent.

And `@letta-ai/trajectory` already supports Codex, Claude Code, Letta Code and other harnesses; there is also a Python wrapper. ([GitHub][4])

So we should seriously consider importing it rather than recreating the compact-memory formatter.

---

# 5. The biggest architectural thing Letta exposes: memory is not truth

Letta's work is almost the perfect complement to QP.

Letta's position is that long-running agents need persistent identity, active memory formation and retrieval, rather than just conversation history. Their Context Constitution treats context management as the mechanism by which a stateless model becomes a persistent agent. ([Letta][5])

But in our system:

```text
Letta-style memory
=
what the agent currently believes is useful

QP
=
what the system has established as true
```

These must stay separate.

An agent might remember:

> “Library X was flaky last time.”

That belongs in memory.

The underlying verified fact could be:

```text
repo X
version 4.3
runtime Cloudflare
trial Y
gate Z = FALSE
```

That belongs in QP/trajectory evidence.

Excellent separation:

```text
               QP VERIFIED FACTS
                      │
                      ▼
                MEMORY COMPILER
              /                 \
             /                   \
 durable principles         project memories
       │                          │
       └───────────┬──────────────┘
                   ▼
               worker context
```

Memory may generalize.

Truth may not.

---

# 6. Letta's Git-backed memory is extremely aligned with our Git thinking

Letta's MemFS/context repository stores long-term memory as Markdown with YAML metadata, backed by Git. Important memory can be loaded directly into the system prompt; less-important knowledge stays discoverable outside active context. ([GitHub][6])

I would steal this nearly verbatim at the conceptual level.

For each persistent business/worker:

```text
context/
├── system/
│   ├── identity.md
│   ├── operating-principles.md
│   └── durable-business-state.md
│
├── knowledge/
│   ├── customers/
│   ├── products/
│   └── providers/
│
├── skills/
│
├── lessons/
│
└── ideas/
```

Git commits capture changes.

But again:

```text
git commit to memory
≠
QP truth
```

A memory commit is a **policy/context revision**.

Which is perfect for Seed0:

```text
same ContractRoot

memory branch A
memory branch B
memory branch C

→ Harbor tournament
→ compare outcomes
→ promote best context revision
```

This is potentially huge.

Now Seed0 isn't just optimizing prompts/models/components.

It can optimize **memory/context itself**.

---

# 7. This gives Seed0 another experimental dimension

Eventually a lane becomes:

```text
Lane =
{
    model,
    worker_policy,
    memory_root,
    skill_root,
    implementation_sha,
    GitGoblin route,
    environment
}
```

against:

```text
same ContractRoot
```

Then we learn:

$$
P(PASS \mid model, policy, memory, skills, code, environment)
$$

This is more powerful than just agent tournaments.

---

# 8. Letta already evaluates exactly the memory problem we'll face

Letta's Context-Bench V2 distinguishes:

**memory usage**:

* adherence,
* retrieval;

and **memory generation**:

* generalization,
* hygiene. ([Letta][7])

Those four dimensions are worth stealing directly.

Every memory promotion could have:

```text
adherence
retrievability
generalization
hygiene
```

So the agent isn't rewarded just for writing more “lessons.”

It must prove:

```text
future analogous task
→ relevant memory retrieved
→ memory improves outcome
→ irrelevant tasks unaffected
```

That's exactly the anti-memory-bloat test we need.

---

# 9. Letta Mods is basically a cousin of our primitive promotion system

Letta lets agents adapt their harness through executable “Mods” that can add tools, lifecycle events, permissions, providers and UI surfaces. ([Letta][8])

I would **not import their Mods runtime** because OpenAI Agents is our preferred cognition harness.

But conceptually:

```text
our promoted primitive
≈
their harness mod
```

Except ours has a stronger proof path:

```text
observation
→ candidate primitive
→ Harbor replay
→ Seed0 tournament
→ QP promotion
→ available capability
```

---

# 10. Agent Harbor is another thing worth watching

Separate from **Harbor Framework**, there is also **Agent Harbor**, an orchestration system for long-running coding agents.

It already provides isolated workspaces, parallel agents, recording/replay, automatic rollback/recovery and targeted web-search attempts. Its docs explicitly position its copy-on-write environment as faster/lighter than Git worktrees. ([Agent Harbor Docs][9])

This overlaps almost exactly with our proposed:

```text
git worktree lanes
+
anti-halting agent
+
recording
```

So:

**don't build a sophisticated worktree manager yet.**

Use raw Git worktrees for v1.

If workspace overhead/parallelism becomes a real bottleneck, test Agent Harbor.

Again, Seesaw:

```text
problem doesn't exist yet
→ don't solve it
```

---

# 11. Temporal fills a different missing layer

Temporal is not an agent cognition framework.

It provides durable execution: workflow state automatically survives process failure, timeouts and long waits such as human approval. They now have explicit AI patterns for long-running stateful agent loops and durable MCP servers. ([GitHub][10])

That may eventually be useful for:

```text
invoice sent
↓
wait 14 days
↓
check payment
↓
follow up
↓
wait
↓
escalate
```

or:

```text
customer approval
↓
3-day external process
↓
callback
↓
continue
```

OpenAI Agents sessions may cover a lot of cognition continuity, but they are not necessarily where we want to place our **business-process durability guarantee**.

Eventually:

```text
Temporal workflow
       │
       ├── OpenAI agent turn
       ├── wait
       ├── QP grant
       ├── external action
       ├── callback
       └── resume
```

could be extremely good.

But **not P0**.

First real action.

Then discover whether process durability is actually painful.

---

# 12. Standardize telemetry outward using OpenTelemetry

OpenTelemetry now has a dedicated GenAI semantic-conventions repository covering GenAI agents, MCP, provider fields, metrics and spans. ([GitHub][11])

The conventions are still evolving/development-status in 2026, so don't make them our canonical data schema. ([John Hodge][12])

Correct direction:

```text
AgentCom canonical event
        ↓
OTel exporter
        ↓
Braintrust / Grafana / whatever
```

Not:

```text
AgentCom internal truth
=
whatever current OTel spec says
```

This gives us interoperability without schema capture.

---

# 13. Braintrust can save us from building the observability UI

Braintrust already does nested agent traces, scoring, experiment comparison, production trace classification and conversion of production failures directly into eval datasets. ([Braintrust][13])

So don't build:

```text
beautiful trace explorer
evaluation dashboard
experiment comparison UI
```

yet.

Export OTel/trajectories into something like Braintrust.

Our scarce layer is not visualization.

---

# The architecture I now think is strongest

```text
                           SEESAW
                        what matters?
                             │
                             ▼
                          AGENTCOM
                         what next?
                             │
                             ▼
                         AUTOBUILD
                  what would TRUE mean?
                             │
                             ▼
                         GITGOBLIN
                   what already exists?
                             │
                             ▼
                           SEED0
                  what route should we test?
                             │
                             ▼
                          HARBOR
              trial + sandbox + arbitrary agent
                             │
                    Git candidate SHA
                             │
                             ▼
                         ACTUALITY
                             │
                             ▼
                            QP
                         commits truth
                             │
                             ▼
                         ATIF BANK
                    full replay experience
                             │
               ┌─────────────┴─────────────┐
               ▼                           ▼
             Seed0                   Memory compiler
          evaluation/RL                    │
                                           ▼
                                  Letta trajectory view
                                           │
                                           ▼
                                    Context Repository
                                           │
                                           ▼
                                     next agent run
```

That feels close to complete.

---

# What we're actually missing now

I would reduce it to **five practical gaps**:

1. **A standard full-fidelity rollout format** → use **Harbor ATIF**.
2. **A real experiment runner/environment abstraction** → use **Harbor** behind Seed0.
3. **A distinct persistent memory/context layer** → use the **Letta Context Repository pattern**, potentially with `agent-trajectory`.
4. **Memory-quality evaluation** → steal Letta's retrieval/adherence/generalization/hygiene axes.
5. **External telemetry interoperability** → export OpenTelemetry GenAI; optionally use Braintrust.

Everything else can wait.

And this gives a particularly nice new invariant:

$$
\boxed{
\text{QP facts are immutable truth candidates;}
\quad
\text{trajectories are experience;}
\quad
\text{memory is an optimized interpretation of experience.}
}
$$

That distinction is critical.

It means an agent can aggressively rewrite its memory and improve itself **without ever rewriting history or truth**.

That may be the cleanest answer yet to continual self-improvement.

[1]: https://github.com/harbor-framework/harbor?utm_source=chatgpt.com "GitHub - harbor-framework/harbor · GitHub"
[2]: https://www.harborframework.com/docs/agents/trajectory-format?utm_source=chatgpt.com "Agent Trajectory Format (ATIF)"
[3]: https://www.letta.com/blog/trajectory/?utm_source=chatgpt.com "Trajectory: A Standard Format for Agent Experience Data | Letta"
[4]: https://github.com/letta-ai/trajectory?utm_source=chatgpt.com "GitHub - letta-ai/trajectory: Convert sessions across harnesses to a unified trajectory format - designed to be consumed by agents (e.g. for memory formation, dreaming, search) · GitHub"
[5]: https://www.letta.com/blog/stateful-agents/?utm_source=chatgpt.com "Stateful Agents: The Missing Link in LLM Intelligence | Letta"
[6]: https://github.com/letta-ai/letta-docs-md/blob/main/concepts/memfs/index.md?utm_source=chatgpt.com "letta-docs-md/concepts/memfs/index.md at main · letta-ai/letta-docs-md · GitHub"
[7]: https://www.letta.com/blog/evaluating-memory-in-production-agents/?utm_source=chatgpt.com "Evaluating Memory in Production Agents | Letta"
[8]: https://letta-ai/agent/mods/?utm_source=chatgpt.com "Letta Code Mods | Letta"
[9]: https://docs.agent-harbor.com/?utm_source=chatgpt.com "Agent Harbor: Orchestration for AI Engineers"
[10]: https://github.com/temporalio/documentation/blob/main/docs/ai/index.mdx?utm_source=chatgpt.com "Documentation/docs/ai/index.mdx at main · temporalio/documentation · GitHub"
[11]: https://github.com/open-telemetry/semantic-conventions-genai?utm_source=chatgpt.com "GitHub - open-telemetry/semantic-conventions-genai · GitHub"
[12]: https://john-hodge.com/blog/opentelemetry-genai-semantic-conventions/?utm_source=chatgpt.com "The state of the OpenTelemetry GenAI semantic conventions (July 2026) · John Hodge"
[13]: https://customers-page-2.preview.braintrust.dev/articles/agent-observability-complete-guide-2026?utm_source=chatgpt.com "Agent observability: The complete guide for 2026 · Articles · OpenAI"
```

---

# SIMPLIFICATION (decided 2026-09-14 — this overrides the above where they conflict)

Yes. I think this is the right simplification.

`/cg` is already much closer to what we actually need **right now** than Harbor or Letta. It has the pieces that matter for our current phase: deterministic async runs, content-addressed `RunReceipt`s, hard quality gates, layered dev/validation/secret suites, expectation management, layered dev/validation/secret suites, evolution recipes, an experience layer, and a lightweight SQLite scheduler. Critically, its Hydra memory layer is optional and the core deliberately continues working without it. Its Git-ledger design is also almost exactly our current AgentCom direction: candidate + scenario + seed + Merkle-rooted events produce a deterministic run identity, while Git stores durable source/worldpack/run artifacts rather than pretending to be the trust system.

So I would revise the architecture to:

```text
SEESAW
   ↓
AGENTCOM
   ↓
AUTOBUILD
ContractRoot
   ↓
GITGOBLIN
reuse plan
   ↓
SEED0
choose competing policies/routes
   ↓
CG
fast local experiment runner
   ↓
OPENAI AGENTS API
actual worker cognition
   ↓
local Git worktree / repo
   ↓
A-LOG / probes
   ↓
ACTUALITY
   ↓
QP
commit truth
   ↓
CG RunReceipt + trajectory
   ↓
SEED0 learns
```

### No Docker by default

I would make the default execution mode extremely cheap:

```text
mode = LOCAL_FAST
```

Meaning:

```text
git worktree
+
normal local process
+
OpenAI Agents API
+
execution envelope
+
actuality validators
```

No Docker.

No Harbor.

No persistent Letta service.

No Hydra required.

No VM boot.

The OpenAI Agents API explicitly lets you choose where the agent works: OpenAI-hosted sandbox, your own infrastructure, or partner sandboxes. The hosted sandbox is optional. ([OpenAI][1])

So during development we can simply run the OpenAI harness while pointing it at our local/project environment.

That should be dramatically faster.

### What replaces Docker's guarantees for now?

Our execution envelope.

Before running anything, bind:

```text
candidate_sha
cwd
executable
argv
environment allowlist
input hashes
ContractRoot
timeout
network policy
```

Then hash that.

So we know exactly what was executed even though it wasn't in a container.

This is sufficient for our current goal:

> **Can AgentCom autonomously improve AgentCom and prove the improvement?**

It is not sufficient for:

> “Can arbitrary strangers upload malicious code and have us safely execute it?”

We don't have that problem yet.

This is Seesaw again: don't pay the sandbox tax before isolation is binding.

### Risk-derived execution modes

One simple hierarchy:

```text
LOCAL_FAST
known repo
known agent
no dangerous credentials
fast iteration

OPENAI_SANDBOX
unknown dependency/code
broader shell access
agent-generated install scripts

HARD_ISOLATED
third-party/untrusted code
multi-tenant
serious credentials
financial/external authority
adversarial security workloads
```

Autobuild could eventually choose the minimum execution class required by the contract.

That's much better than containerizing everything.

### `/cg` should absorb the experimental plumbing

I'd stop building Seed0's runner layer independently.

Seed0 becomes:

```text
EXPERIMENT DESIGNER
```

and `/cg` becomes:

```text
EXPERIMENT EXECUTOR
```

Seed0 says:

```text
same ContractRoot

lane A = direct
lane B = gitgoblin-first
lane C = seeker3
```

CG executes all three and returns:

```text
RunReceipt A
RunReceipt B
RunReceipt C
```

with:

```text
gate results
events
cost
latency
candidate hashes
```

Then Seed0 ranks them.

That's actually what `/cg` was built to do. Its documented core loop is already essentially:

```text
world
→ AsyncRunner
→ RunReceipt
→ hard gates
→ rank survivors
→ experience
→ evolution
→ repeat
```

We shouldn't build that twice.

### OpenAI Agents should be a CG executor

This is the nicest integration.

CG already has:

```text
executors.py
```

and an executor registry.

So add something conceptually like:

```text
OpenAIAgentsExecutor
```

Its job:

```text
CG CandidateArtifact
+
scenario
+
ContractRoot
+
worktree
        ↓
OpenAI Agents session
        ↓
agent edits/runs/researches
        ↓
events normalized
        ↓
CG Event stream
        ↓
RunReceipt
```

CG doesn't need to understand OpenAI's architecture deeply.

It only needs a standardized executor contract.

Then later:

```text
OpenAIAgentsExecutor
ClaudeExecutor
LocalModelExecutor
CodexCLIExecutor
```

can all compete under the same gates.

That's powerful.

### We don't need Letta right now either

The distinction I made before still matters:

```text
truth ≠ trajectories ≠ memory
```

But that doesn't imply:

```text
install Letta
```

right now.

We can simply retain:

```text
CG full RunReceipts
+
AgentCom trajectories
+
structured facts/negative facts/ideas
```

Then, when context retrieval becomes an actual bottleneck, add a **memory projection**:

```text
100 historical trajectories
      ↓
memory compiler
      ↓
20 useful lessons for this task
```

Whether the backend is Letta, SQLite, files, git, embeddings, or something better in three months doesn't matter.

Do not pay the Letta latency tax now.

### Same with Harbor

Harbor becomes a later CG backend, if useful.

Not foundational.

Maybe eventually:

```text
CG executor:
  local
  openai_hosted
  harbor
  modal
  e2b
```

The experiment contract stays identical.

If we reach:

```text
50 simultaneous agents
untrusted repositories
GPU environments
reproducible benchmark publishing
```

then Harbor becomes compelling.

We're nowhere near the point where that is our limiting factor.

### When do we turn sandboxing on?

I'd make it a **risk-derived execution mode**, not a universal architectural requirement.

Autobuild could eventually choose the minimum execution class required by the contract.

That's much better than containerizing everything.

OpenAI's environment templates already support files, packages, skills, plugins, environment values and network configuration, so when we need stronger isolation we don't need to design the container infrastructure ourselves. ([OpenAI Developers][2])

### The immediate architecture I'd give the agent

Don't add Harbor.

Don't add Letta.

Don't add Temporal.

Don't build Docker orchestration.

Do these:

1. **Wire `/cg` into AgentCom as the canonical experimental runner.** A CG run receives `ContractRoot`, candidate Git SHA, Seed0 policy ID and execution envelope.

2. **Add `OpenAIAgentsExecutor` to `/cg`.** First version can even use a mocked/scripted session until the API key path is available; then replace it with the real Agents API.

3. **Use Git worktrees as CG's initial workspace provider.** `base_sha → lane worktree → candidate_sha`.

4. **Feed Actuality gate results into the CG receipt.** CG can record them but QP remains the authority determining whether a consequential transition becomes canonical.

5. **Normalize every run into both:** a CG `RunReceipt` for deterministic experiment identity and an AgentCom `Trajectory` for cross-project learning.

6. **Run the first self-build tournament:** remove the remaining ab1/ab2/ab3 dependencies from `openai_native`, with 2–3 policies against the same frozen ContractRoot.

7. **Then test whether run #2 improves using run #1's banked information.** That's far more valuable right now than any sandbox feature.

The really elegant final shape is:

```text
                   AgentCom
                      │
                frozen problem
                      │
                       ▼
                    Seed0
              chooses experiments
                      │
                      ▼
                     CG
        reproducible experiment kernel
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Git worktree          OpenAI Agents API
   implementation state      cognition/harness
          │                       │
          └───────────┬───────────┘
                      ▼
                 A-LOG reality
                      ▼
                  Actuality
                      ▼
                     QP
                      ▼
                  RunReceipt
                      ▼
                     CG
                      ▼
             experience/evolution
```

That is leaner.

And importantly, `/cg` itself already embodies the principle we're converging on: **hard gates dominate, deterministic runs are receipts, and experience feeds the next candidate.**

So yes: **CG + Git + OpenAI Agents + QP is enough for the current phase.** Sandbox/container infrastructure can wait until isolation becomes a measured bottleneck rather than an imagined one.

[1]: https://openai.com/index/introducing-the-agents-api/?utm_source=chatgpt.com "Introducing the Agents API | OpenAI"
[2]: https://developers.openai.com/api/reference/java/resources/beta/subresources/agents/subresources/environments/subresources/templates/methods/create?utm_source=chatgpt.com "Create an agent environment template | OpenAI API Reference"
