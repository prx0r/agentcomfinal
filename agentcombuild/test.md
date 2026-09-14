# test.md — build brief: make it build one thing for real (saved 2026-09-14)

Status: BINDING THIS CYCLE. Stop extending architecture. No new conceptual
subsystems. Tests and wiring only, then one product and one self-build.

The latest push is much better. You now have enough architecture. The priority should switch almost completely from **designing AgentCom** to **making AgentCom build one thing for real**.

The good news first: canonical code is now isolated from `ab1/2/3`; the QP adapter calls the real `/qp`; the OpenAI-native path has official MCP-client compatibility tests; security defaults were hardened fail-closed; and contracts are no longer just decorative schemas.    The plugin side is also not starting from zero—you already have a serious plugin conformance kit plus a plugin factory that takes a working MCP capability and produces/scorers a plugin packet.

But I would **not put a live credential into the current chain yet**.

The most serious bug is in `openai_native/chain.py`: QP settlement happens before the independent readback, and the QP evidence already contains a successful `"readback.found_id": "lead-123"` even when `readback_ok=False`. The later readback can fail while a valid QP receipt and L1 trajectory have already been created.  The negative test only asserts the overall run fails; it does not assert that **no receipt/fact was minted**.

That violates the central constitution:

$$
\boxed{\text{Reality must precede settlement.}}
$$

The proper flow is:

```text
ACTION
  ↓
PROVIDER RESPONSE
  ↓
INDEPENDENT READBACK
  ↓
NORMALIZED EVIDENCE
  ↓
ACTUALITY JUDGES
  ↓
QP SETTLEMENT
  ↓
QP RECEIPT
```

Never:

```text
fabricate expected evidence
→ settle QP
→ later check whether reality agreed
```

There is another important contract bug. `ContractRoot` currently commits only leaf `id + judge + evidence_class`. It explicitly excludes `freshness`, `evidence_schema` and `authority`.  That means changing:

```text
freshness: 5 minutes → 30 days
authority: grant → none
required evidence structure: strict → weak
```

can leave the same `ContractRoot`.

Those are changes to **what counts as success**, not merely HOW.

I would freeze:

$$
ContractRoot =
H(
claim,
leaf.id,
evidence\_schema,
judge,
evidence\_class,
freshness,
authority,
proof\_requirement
)
$$

while keeping only things like:

```text
probe implementation
repo/library
worker model
policy
runner
```

inside `PlanRoot`.

The third gap is simply that OpenAI execution still isn't live. `OpenAIAgentsExecutor v0` is a scripted local executor.  And `test_wire_live.py` proves the older Agents SDK objects and official MCP package accept your shapes, which is useful, but it does **not** create a managed Agents API session.  The current managed API has a real `beta.agents.sessions.create(...)` endpoint, can run with `environment={"type":"none"}`, and can stream session events. ([OpenAI Developers][1])

That is the next OpenAI test—not another mock.

Similarly, `/cg` is only half-wired. The adapter proves imports and converts a lane to a worldpack-shaped manifest, but it explicitly doesn't execute the CG `AsyncRunner`.  That's fine; just don't count it as integrated yet.

And Gitbuild is promising but currently unproven as self-building. The README says there was a first live scanner tournament, but the committed `gitbuild/` directory only contains the contract and runner; I don't see committed candidate receipts/results.   There are also still no GitHub commit status checks on current HEAD.

So my verdict is:

$$
\boxed{\text{The pieces exist. The product loop does not yet exist.}}
$$

That is actually a good place to be.

The goal now should be one command:

```text
agentcom build specs/uk-business-plugin.json
```

that goes all the way through.

Current OpenAI product direction reinforces this. Plugins are now the primary discovery surface across ChatGPT and Codex, and a plugin can package Skills, connected Apps and app templates. OpenAI also supports importing a plugin marketplace from GitHub and syncing it, which is *perfect* for our Git-native development loop. ([OpenAI Help Center][2])

So don't begin with public Plugin Directory submission.

Begin with:

```text
Autobuild
  ↓
GitHub plugin repository
  ↓
private/workspace marketplace
  ↓
ChatGPT
  ↓
real host eval
```

That gives us actual ChatGPT feedback without waiting on public review.

Here is the build brief I would give the coding agent now.

# Objective

Stop extending architecture.

Make `agentcomfinal` capable of taking one structured product specification and producing, testing and committing a functioning implementation.

The first external product target is:

**AgentCom UK Business Plugin v1**

The first self-host target is:

**AgentComBuild fixes and validates one of its own requirements using the same build loop.**

---

# Definition of `agentcom build`

Implement one canonical command:

```bash
agentcom build <spec.json>
```

A successful invocation must perform:

```text
SPEC
 ↓
Autobuild Actuality Contract
 ↓
ContractRoot
 ↓
GitGoblin reuse search
 ↓
PlanRoot
 ↓
Git candidate worktree
 ↓
OpenAI Agents worker
 ↓
implementation
 ↓
probes
 ↓
Actuality validation
 ↓
QP settlement
 ↓
candidate commit
 ↓
run/trajectory receipt
 ↓
PASS or FAIL
```

Nothing else is required for v1.

No portfolio scheduler is necessary.

No Harbor.

No Docker.

No Letta.

No voice.

No public-plugin submission.

---

# P0 — repair truth semantics first

Before executing a live OpenAI agent, add failing regression tests for the two constitutional bugs.

### Readback-before-settlement

For:

```text
readback_ok = false
```

require:

```text
QP settlement DOES NOT OCCUR

qp_receipts == []

trajectory.level == L0-observation

claim state != TRUE
```

Refactor the chain:

```text
send
→ obtain action evidence
→ obtain independent readback
→ judge readback
→ only if TRUE construct QP evidence
→ QP settlement
```

The simulated provider must not be allowed to construct the evidence that proves itself.

---

### ContractRoot completeness

Create a test proving that changing each of these changes `ContractRoot`:

```text
judge
evidence_schema
evidence_class
freshness
authority
minimum proof requirement
```

Changing only these must preserve `ContractRoot` while changing `PlanRoot`:

```text
probe implementation
repo/library
worker model
policy
runner
```

This test becomes constitutional.

---

# P1 — live OpenAI Agents API

Replace the scripted executor with two modes:

```text
SCRIPTED
LIVE
```

Keep SCRIPTED for deterministic tests.

Implement LIVE using the current official OpenAI client:

```python
client.beta.agents.sessions.create(...)
```

Start with:

```text
environment.type = none
```

No sandbox.

Bind:

```text
project
campaign
ContractRoot
PlanRoot
policy
```

into session metadata.

Stream every session event into the existing telemetry adapter.

Do not attempt a consequential action first.

First live acceptance:

```text
real Agents API session starts
→ agent can call gg.search MCP
→ result comes back
→ session finishes
→ OpenAI events normalized
→ trajectory produced
```

This should cost almost nothing and proves the real worker CPU.

---

# P2 — connect CG minimally

Do not redesign CG.

Add one real call:

```text
AgentCom lane
→ adapters.cg
→ CG AsyncRunner
→ OpenAI executor
→ CG RunReceipt
```

Required run identity inputs:

```text
ContractRoot
PlanRoot
base commit SHA
candidate SHA
policy ID
seed
event root
```

Store the resulting CG receipt reference inside the AgentCom trajectory.

Do not move QP truth into CG.

CG = experiment record.

QP = truth.

---

# P3 — implement the actual orchestrator

Create:

```text
agentcom/
    cli.py
    build.py
```

`build.py` should be boring orchestration.

Pseudo-flow:

```python
spec = load_spec()

contract = autobuild.compile(spec)
assert contract.compilable

reuse = gitgoblin.prebuild(contract)

lane = gitbuild.new_lane(...)

run = cg.run(
    contract=contract,
    plan=reuse,
    executor=openai
)

evidence = actuality.probe(run)

result = actuality.judge(evidence)

if result != TRUE:
    bank_failure()
    return FAIL

receipt = qp.settle(...)

commit = git.commit_exact_candidate(...)

return BuildResult(...)
```

Do not place strategic intelligence here.

---

# P4 — first thing it builds: itself

Input:

```text
specs/selfhost/readback-before-settlement.json
```

Goal:

> Fix AgentCom so QP cannot settle a consequential claim before independent readback establishes the postcondition.

The evaluator is frozen before the worker begins.

Create 2 or 3 policies if cheap:

```text
direct
test-first
gitgoblin-first
```

They operate in isolated worktrees.

Use the same ContractRoot.

The OpenAI agent modifies code.

Frozen tests evaluate candidate SHAs.

CG records runs.

Seed0 chooses the passing/cheapest candidate.

Promotion occurs only after external validation.

This is the first genuine Autobuild self-build.

Commit the complete experiment artifacts:

```text
experiments/selfhost/readback-v1/
    contract.json
    candidates.json
    receipts.json
    tournament.json
    promoted.json
```

Now README may truthfully say the factory built itself.

---

# P5 — first product build: UK Business Plugin

Do not start with email sending.

Start read-only.

Specification:

```text
product:
    agentcom-uk-business-profile

user:
    UK small business owner

job:
    "Show me how my business appears to ChatGPT and expose verified
     company/business context through ChatGPT."

surface:
    ChatGPT Plugin

capabilities:
    business.lookup
    business.profile
```

Initial implementation can use existing company/business sources and current project code.

The purpose is proving:

```text
Autobuild
→ MCP
→ plugin
→ ChatGPT
```

rather than proving every business feature.

---

# Plugin Actuality DAG

The build is TRUE only if all of these are TRUE:

```text
MCP starts

official MCP client connects

tools/list exposes intended tools

business.lookup returns real structured information

invalid company returns bounded deterministic error

plugin spec validates canonical JSON schema

plugin lint has zero ERROR

routing-positive corpus routes correctly

routing-negative corpus does not invoke plugin

Skill package builds

plugin package builds

workspace marketplace catalog validates

real ChatGPT workspace can install/import it

real ChatGPT invocation calls the intended tool

result renders successfully

latency recorded
```

The final two leaves are host tests and may initially remain UNKNOWN until a human performs them.

Do not pretend they PASS locally.

---

# Wire the existing plugin packages instead of rebuilding them

Promote adapters around:

```text
packages/agentcom-plugin-canonical/
packages/agent-plugin-factory/
```

Pipeline:

```text
working MCP
 ↓
agent-plugin-factory candidate packet
 ↓
plugin spec
 ↓
agentcom-plugin-canonical schema check
 ↓
plugin_lint.py
 ↓
routing evals
 ↓
submission/workspace bundle
```

Treat every plugin conformance error as an Actuality leaf failure.

Do not write another plugin schema.

---

# Use GitHub as the plugin deployment loop

Generate:

```text
dist/plugins/agentcom-uk/
```

plus a marketplace catalog.

The development flow becomes:

```text
candidate commit
 ↓
CI
 ↓
plugin artifacts
 ↓
GitHub marketplace
 ↓
ChatGPT workspace sync
 ↓
host evals
 ↓
host-eval evidence
 ↓
QP/Actuality result
```

This is directly aligned with the current ChatGPT plugin system.

---

# P6 — then turn on the first real business action

After the read-only plugin works, add:

```text
lead.list
lead.reply
```

Use existing Cmail rather than building email infrastructure inside AgentCom.

The first consequential flow:

```text
ChatGPT:
"reply to this lead"

 ↓

plugin / MCP proposal

 ↓

OpenAI approval belt

 ↓

QP grant check

 ↓

cmail sends

 ↓

provider/API independent readback

 ↓

Actuality TRUE

 ↓

QP settlement

 ↓

receipt

 ↓

lead outcome stored
```

This is the first genuinely interesting AgentCom UK action.

Hard acceptance:

```text
wrong grant       → REFUSE
expired grant     → REFUSE
wrong business    → REFUSE
send API error    → FALSE
send success but no readback → UNKNOWN
readback mismatch → FALSE
matching readback → QP receipt
```

Only the last state means delivered.

---

# P7 — business onboarding compiler

Once one business works, create:

```bash
agentcom business init company.json
```

Input:

```text
business identity
domain
services
service area
hours
contact channels
desired permissions
```

Output:

```text
BusinessSpec

OpenAI agent config
business Skill
plugin/app configuration
MCP tenant config
QP grants template
Actuality contracts
telemetry lineage
```

Then onboarding a plumber/electrician/etc. is compilation rather than another code project.

---

# Do not work on these yet

Until the first real ChatGPT plugin works:

```text
voice
GPT-Live
complex memory systems
ATIF optimization
OTel dashboards
more domain packs
public plugin marketplace
Temporal
Docker/Harbor
multi-project autonomous scheduler
large Seed0 evolution campaigns
```

They are useful later.

They do not currently unblock the product.

---

# Immediate test order

1. `readback_false_mints_no_receipt`
2. `contract_root_changes_on_proof_semantics`
3. `live_agents_session_can_call_gg_search`
4. `cg_runs_one_openai_lane`
5. `selfhost_worker_fixes_one_frozen_contract`
6. `plugin_factory_accepts_autobuild_mcp`
7. `canonical_plugin_lint_passes`
8. `official_mcp_client_invokes_business_lookup`
9. `workspace_plugin_import_manual evidence`
10. `real ChatGPT routes to business.lookup`

No subsequent stage should begin while the previous stage is fake.

---

# Definition of working

AgentCom is not "working" because `GO.sh` is green.

AgentCom is working when this happens:

```text
$ agentcom build specs/agentcom-uk-business-profile.json

Strategic: ACCEPTED
ContractRoot: contract:...
ReusePlan: ...
OpenAI session: session_...
Candidate: a2f...
MCP: PASS
Plugin lint: PASS
Routing eval: PASS
Actuality: 11 TRUE / 2 UNKNOWN
QP receipts: ...
Candidate commit: ...
Artifact: dist/plugins/agentcom-uk/
```

Then I install/sync that generated plugin into ChatGPT and ask:

> "Show me this UK business."

ChatGPT calls our generated capability and returns a verified result.

That is Autobuild v1.

One current OpenAI detail makes this even better: Plugins now package workflows around Skills and Apps, and workspace admins can import/sync plugin marketplaces from GitHub. ([OpenAI Help Center][2]) So your Git-native factory can become the actual distribution pipeline rather than a separate CI toy.

I would therefore make the **next push almost entirely tests and wiring**, with no new conceptual subsystems. The target after that push should be tangible: a real OpenAI managed agent session modifies a Git worktree under a frozen contract, and the subsequent push produces the first installable `agentcom-uk-business-profile` ChatGPT plugin.

[1]: https://developers.openai.com/api/reference/typescript/resources/beta/subresources/agents/subresources/sessions/methods/create?utm_source=chatgpt.com "Create an agent session | OpenAI API Reference"
[2]: https://help.openai.com/en/articles/20001256/?utm_source=chatgpt.com "Plugins in ChatGPT and Codex | OpenAI Help Center"
