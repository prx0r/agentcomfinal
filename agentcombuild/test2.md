# test2.md — proof-hygiene directive (saved 2026-09-14)

Status: BINDING THIS CYCLE. No architecture, no memory features, no voice,
no domain packs, no green review files. Objective: make review labels,
candidate identity, live paths, and build statuses truthful.

The latest push fixed two real problems, but the repo is still **claiming more than it has proved**. The main issue now is not architecture. It is proof hygiene.

The good fixes are real: readback now precedes QP settlement, and `ContractRoot` now commits freshness, authority, evidence schema and proof level rather than only a subset of acceptance semantics.

But several of the review labels are currently misleading.

| Claim                                  | Actuality                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **“all suites real+green”**            | False as phrased. The session log itself shows E4 running in `"mode": "SIMULATED"` and the “live-wire” stage says `OPENAI_API_KEY is not set, skipping trace export`.                                                                                                                                                          |
| **“7 trajectories banked / verified”** | Misleading. `file_trajectory()` writes everything into a directory literally named `verified/`, even when the trajectory is only `L0-observation`.  A committed example under `trajectory/verified/` has `level: "L0-observation"` and `qp_receipts: []`.                                                                      |
| **“selfhost promoted”**                | Invalid experiment identity. The promotion artifact claims candidate SHA `a097...`, but the readback fix is in its child commit `59f2...`.  The receipt says tests passed for `a097...`, but `build_selfhost()` actually executes pytest against the current working directory and only calls `git rev-parse HEAD` afterwards. |
| **“LIVE+CG lanes”**                    | Not yet. `run_lane()` calls an arbitrary AgentCom `work_fn()` itself and uses CG only to calculate hashes. It explicitly does not run CG's actual AsyncRunner.                                                                                                                                                                 |
| **“agentcom build orchestrator”**      | Mostly packaging right now. The selfhost path does not create a lane, invoke OpenAI, use GitGoblin, run CG, produce a candidate commit, validate that commit, or obtain a QP promotion receipt.                                                                                                                                |
| **“UK business product”**              | Fixture demonstration. `business.lookup` reads `examples/business_directory.json`, not real company data.  The spec itself asks for `acme-plumbing-leeds`.                                                                                                                                                                     |
| **“routing eval”**                     | Self-authored keyword matching, not ChatGPT routing. `route()` checks a fixed tuple of words and then tests a corpus designed around those words.                                                                                                                                                                              |
| **“plugin built”**                     | A local JSON/Skill bundle exists. ChatGPT installation, invocation and final publication lint are still explicitly `UNKNOWN`, yet `report["ok"]` can be true and the CLI exits 0.                                                                                                                                              |
| **“live workflow”**                    | Placeholder. The actual `agentcom-live.yml` only prints that no credentials are configured.                                                                                                                                                                                                                                    |

The most serious error is the self-host receipt. **A build system whose receipt points at code that was not actually tested has broken its own core invariant.** Fix that before doing anything clever.

There is also a likely defect in the supposedly live OpenAI path. Current official Managed Agents API docs put agent configuration under `agent`/`agent_id`; model and tools belong to that agent configuration. The current `run_live()` calls `sessions.create(model=model, tools=...)` at the session top level, which does not match the documented current Python request shape. ([OpenAI Developers][1]) Current session events are typed `AgentSessionEvent` objects, whereas `run_live()` only retains events for which `isinstance(event, dict)` is true—so a real stream can plausibly produce an empty trajectory even after the request shape is fixed. The official event API returns a union of typed event classes. ([OpenAI Developers][2])

And the test called “SDK wire” doesn't catch this because it tests `agents.Agent` and `MCPServerStdio` from the **Agents SDK**, while `run_live()` uses the separate `openai.OpenAI().beta.agents.sessions` **managed Agents API client**.

So I would give the agent this exact next brief:

# Current objective

Do not add architecture.

Do not add memory features.

Do not add voice.

Do not add more domain packs.

Do not generate more green review files.

The only objective of the next development cycle is:

> **Make one exact committed source candidate be produced by an OpenAI worker, evaluated from a clean checkout under a frozen contract, recorded by the real experiment runner, and promoted only after the exact candidate SHA passes.**

Then use the same machinery to build the first real UK-business ChatGPT surface.

---

# Rule 0 — reviews may not infer proof from test counts

Delete the current idea that:

```text
38 pytest tests passed
=
records-enforced
=
seeker-honest
=
compiler-compounds
```

The current review checker essentially runs pytest, verifies files exist, greps a few banned strings, and then emits PASS for broad semantic claims. That is not independent review.

Every review criterion must point to one exact executable gate.

Example:

```json
{
  "criterion": "candidate-is-exactly-tested-code",
  "judge": "git_candidate_identity_v1",
  "evidence": {
    "candidate_sha": "...",
    "candidate_tree": "...",
    "validation_worktree_tree": "..."
  },
  "result": "TRUE"
}
```

Do not emit `overall: PASS` for criteria that were not actually evaluated.

---

# Rule 1 — fix vocabulary immediately

There are only these states:

```text
SIMULATED
LOCAL_OBSERVED
EXTERNALLY_OBSERVED
QP_VERIFIED
LIVE_PROVIDER_VERIFIED
HOST_VERIFIED
```

Never call:

```text
SIMULATED → real
L0 → verified
keyless SDK construction → live
pytest PASS → autonomous build
```

Rename:

```text
trajectory/verified/
```

to a level-neutral store:

```text
trajectory/bank/
```

or route by level:

```text
trajectory/
  observations/       L0
  facts/              L1
  patterns/           L2
  candidates/         L3
  replay_proven/      L4
  promoted/           L5
```

Hard test:

```text
L0 cannot be filed under facts/verified/promoted.
```

---

# P0 — repair candidate identity

This is mandatory before any further self-build claim.

The current selfhost executor runs pytest against the working directory and then labels HEAD as the candidate.

Remove that completely.

Required sequence:

```text
BASE_SHA
   ↓
new isolated worktree
   ↓
worker modifies files
   ↓
worker commits
   ↓
CANDIDATE_SHA
   ↓
dirty state must be empty
   ↓
new detached validation worktree @ CANDIDATE_SHA
   ↓
frozen validator from VALIDATOR_SHA
   ↓
PASS/FAIL
```

Receipt MUST contain:

```json
{
  "base_sha": "...",
  "candidate_sha": "...",
  "candidate_tree_sha": "...",
  "validator_sha": "...",
  "contract_root": "...",
  "dirty_before_validation": false,
  "validation_worktree_head": "...",
  "validation_worktree_tree": "...",
  "result": "PASS"
}
```

Invariant:

```text
candidate_sha
==
validation_worktree_head
```

and:

```text
git status --porcelain
==
""
```

inside validation.

Add:

```text
test_dirty_tree_cannot_be_promoted
test_candidate_sha_must_contain_fix
test_validator_runs_detached_at_candidate_sha
test_receipt_sha_matches_validation_sha
```

The current `experiments/selfhost/readback-v1/promoted.json` should be marked:

```text
INVALIDATED
reason = candidate-sha-did-not-identify-tested-tree
```

Do not silently rewrite history.

---

# P1 — make selfhost actually BUILD

Current `build_selfhost()` only runs tests.

That is not Autobuild.

Change it to:

```text
contract
  ↓
GitGoblin prebuild
  ↓
new worktree
  ↓
OpenAI worker receives failing requirement
  ↓
worker edits repo
  ↓
worker commits candidate
  ↓
detached validator
  ↓
CG receipt
  ↓
QP promotion decision
  ↓
merge
```

For v1 there may be one lane.

That is fine.

But it must actually contain:

```text
BEFORE: failing gate
WORKER ACTION
AFTER: passing gate
```

Otherwise nothing was built.

Hard acceptance:

```text
candidate diff is nonempty

base fails frozen test

candidate passes same frozen test

candidate was produced after contract freeze

candidate SHA identifies tested code
```

This is the first true self-build.

---

# P2 — use CG for real or stop saying CG

`adapters.cg.run_lane()` currently uses CG only for IDs.

Replace it with an adapter that calls the actual `/cg` run primitive.

The implementation must not reproduce CG receipt semantics.

Acceptance:

```text
monkeypatch / instrument CG AsyncRunner
→ AgentCom invokes it
→ CG executes episode
→ CG itself emits RunReceipt
→ AgentCom stores receipt ID
```

Required test:

```text
test_agentcom_lane_calls_real_cg_runner
```

It must fail if the AgentCom adapter simply creates its own receipt-shaped dict.

Until that passes, label:

```text
CG_COMPATIBLE
```

not:

```text
CG_RUN
```

---

# P3 — repair the Managed Agents API client

Do not use the Agents SDK constructor test as evidence that Managed Agents API works.

Use the actual `openai` client schema.

Construct approximately:

```python
client.beta.agents.sessions.create(
    environment={"type": "none"},
    agent={
        "model": MODEL,
        "instructions": INSTRUCTIONS,
        "tools": TOOLS
    },
    input=USER_INPUT,
    metadata=METADATA
)
```

Use the exact installed/current OpenAI schema rather than hard-coding from this brief if it changes.

Normalize SDK objects correctly:

```python
if hasattr(event, "model_dump"):
    raw = event.model_dump(mode="json")
elif isinstance(event, dict):
    raw = event
else:
    refuse_unknown_event_type()
```

Do not silently discard non-dict events.

First LIVE test should be deliberately tiny:

```text
OPENAI_API_KEY present

create managed session
→ input "return the exact string AGENTCOM_LIVE_OK"
→ observe real session id
→ observe >=1 actual session event
→ observe output
→ normalize events
→ trajectory event_count > 0
```

No tool yet.

Required artifact:

```json
{
  "mode": "LIVE",
  "session_id": "sess_...",
  "provider": "openai",
  "events": 5,
  "output": "...",
  "usage": {...}
}
```

The test cannot skip and then be counted as PASS.

Possible results:

```text
PASS
FAIL
NOT_CONFIGURED
```

`NOT_CONFIGURED != PASS`.

---

# P4 — then prove one REAL tool round-trip

After basic live session passes:

```text
OpenAI managed session
  ↓
agent calls one tool
  ↓
gg.search
  ↓
tool result submitted back
  ↓
agent consumes result
  ↓
final response references it
```

Use a non-consequential read tool.

Acceptance requires evidence of:

```text
tool call event
tool arguments
tool output
agent continuation
final output
```

Do not merely prove that MCP works separately and OpenAI works separately.

The same session must cross the boundary.

---

# P5 — fix "all suites real"

Rewrite `bank_session.py`.

Every step records:

```json
{
  "mode": "SIMULATED | LOCAL | LIVE",
  "configured": true,
  "executed": true,
  "result": "PASS | FAIL | UNKNOWN"
}
```

Session status:

```text
PROVEN
```

only when every hard required LIVE leg actually executes.

Example:

```text
pytest local                           LOCAL/PASS
E4 synthetic tournament               SIMULATED/PASS
MCP official client                    LOCAL/PASS
OpenAI API key absent                  LIVE/UNKNOWN
ChatGPT host untested                  LIVE/UNKNOWN
```

Overall:

```text
LOCAL_GREEN / LIVE_INCOMPLETE
```

not:

```text
all suites real+green
```

The documentation string saying:

```text
No mocks: execute everything real
```

must be deleted until it is actually true.

---

# P6 — stop self-reporting review semantic claims

Replace mutable `review/VERDICT.json` files as authority with generated projections from evidence.

A review should NEVER say:

```text
"seeker-honest": PASS
```

because pytest happened to exit 0.

For each semantic criterion define a validator.

Examples:

```text
seeker-does-not-fabricate-sources
→ inject missing backend
→ require UNKNOWN/refusal

compiler-preserves-contract
→ mutate route
→ ContractRoot stable

compiler-detects-acceptance-change
→ mutate authority
→ ContractRoot changes

actuality-no-self-proof
→ worker says PASS
→ canonical state unchanged

candidate-identity
→ dirty-tree mismatch attack
→ promotion refused
```

Then the review is simply a rendering of those results.

---

# P7 — `agentcom build` must stop exiting 0 for incomplete product builds

Current behavior:

```text
13 TRUE
3 UNKNOWN
0 FALSE
→ ok=True
→ exit 0
```

is wrong for a command whose claimed purpose is to build a functioning product.

Introduce statuses:

```text
REFUSED
FAILED
LOCAL_PASS
LIVE_PASS
PRODUCT_PROVEN
```

For the UK plugin right now:

```text
status = LOCAL_PASS
exit != "fully proven"
```

Either:

```text
exit 3 = incomplete/UNKNOWN
```

or explicitly require:

```bash
agentcom build ... --stage local
```

for local success.

Default `agentcom build` only returns success when every hard contract leaf is TRUE.

---

# P8 — stop claiming fixture business data is verified business context

`business.lookup` currently reads:

```text
examples/business_directory.json
```

That is a fixture.

Rename it:

```text
fixture.business.lookup
```

or attach:

```json
{
  "source_class": "FIXTURE",
  "verification": "SIMULATED"
}
```

It cannot satisfy:

```text
business-identity-verified
```

for a real product contract.

Wire the first real read from an actual source.

Given current parallel work, preferred source is:

```text
cgraphuk / BQ Oracle
```

If that adapter isn't ready, use Companies House directly for v1.

Required result:

```json
{
  "business_id": "company-number",
  "name": "...",
  "status": "...",
  "sic": [...],
  "source": "companies-house | oracle-uk",
  "observed_at": "...",
  "evidence_ref": "..."
}
```

Now `business.lookup` becomes genuinely useful.

---

# P9 — routing tests must stop marking themselves

Current:

```python
route(query) =
keyword in query
```

and positive examples contain those keywords.

This proves the keyword matcher matches itself.

Rename that leaf:

```text
local-routing-heuristic
```

It may be useful, but it is NOT:

```text
ChatGPT routes correctly
```

The actual host leaf remains:

```text
UNKNOWN
```

until ChatGPT invokes the plugin correctly.

Eventually collect:

```text
positive prompts
negative prompts
host-selected plugin/tool
host result
```

as the routing corpus.

---

# P10 — plugin packaging needs real host actuality

Current local product pipeline can retain:

```text
schema valid
canonical lint local subset clean
MCP protocol works
Skill bundle exists
```

But these must remain different from:

```text
ChatGPT can install plugin
ChatGPT discovers plugin
ChatGPT invokes business.lookup
result renders
```

Those final host leaves must be filled only from real ChatGPT.

First actual product proof:

```text
real UK company
      ↓
Oracle/Companies House
      ↓
business.lookup MCP
      ↓
plugin bundle
      ↓
ChatGPT workspace
      ↓
user asks:
"Show me this business"
      ↓
ChatGPT selects capability
      ↓
MCP receives exact invocation
      ↓
real source data returned
      ↓
ChatGPT renders result
```

Record host evidence.

Then and only then:

```text
PRODUCT_PROVEN
```

---

# P11 — use CI as the independent evaluator

There are workflow files now, but HEAD currently has no returned combined status in GitHub.

Get CI actually reporting.

Also fix naming:

```text
openai-native offline suite (real)
```

is contradictory.

Call it:

```text
openai-native offline suite
```

Keyless CI proves:

```text
determinism
schemas
security
wire compatibility
fixtures
negative tests
```

Live workflow proves:

```text
OpenAI provider
real data provider
ChatGPT host
```

and is permitted to remain UNKNOWN until credentials/H-task are supplied.

Live results are:

```text
PASS | FAIL | NOT_CONFIGURED
```

---

# The exact next self-build

Do not pick another architectural problem.

Create a new frozen contract:

```text
selfhost-exact-candidate-v1
```

Initial gate:

```text
candidate receipt MUST identify the exact tested Git tree
```

Current implementation should FAIL.

Then let the OpenAI worker fix `build.py`.

This is perfect because it tests the factory on its own most important current defect.

Required progression:

```text
BASE_SHA fails
      ↓
ContractRoot frozen
      ↓
OpenAI worker receives blocker
      ↓
candidate worktree
      ↓
worker edits build.py
      ↓
candidate commit
      ↓
detached validation
      ↓
PASS
      ↓
real CG RunReceipt
      ↓
QP promotion receipt
      ↓
merge
```

Commit the full evidence.

That is the first experiment I will accept as:

> AgentCom built part of AgentCom.

---

# Then immediately do the external product

Once that works, freeze:

```text
uk-business-profile-v1
```

and make `agentcom build` produce the real read-only UK business plugin.

No new architecture between those two experiments.

---

# Definition of Autobuild v1

Autobuild v1 exists when one command produces this with truthful values:

```text
ContractRoot: contract:...
PlanRoot: plan:...

Reuse:
  GitGoblin: PASS

Worker:
  provider: OpenAI Agents API
  session: sess_...

Git:
  base: ...
  candidate: ...
  tested: exact candidate SHA
  dirty: false

CG:
  receipt: run:...

Actuality:
  local: TRUE
  provider: TRUE
  host: TRUE

QP:
  verification/promotion receipt: ...

Product:
  artifact: ...
  ChatGPT install: TRUE
  ChatGPT routing: TRUE
  business.lookup: TRUE
  source: Oracle UK / Companies House

Status:
  PRODUCT_PROVEN
```

Anything less must report its actual partial state.

The principle is unchanged:

> **Agents speculate. Reality validates. QP commits. History compounds.**

The change required now is to make the repository obey that sentence rather than merely print it.

The current codebase is close enough that I would **not redesign it again**. The two genuinely good P0 fixes should stay. The next push should be almost entirely about **candidate identity, true live OpenAI execution, real CG execution, honest state names, and one real business data source**.

Once exact-SHA self-building works, this becomes qualitatively different: then we can hand it the plugin problem, the UK-business onboarding problem, BreadUp features, or basically any repo target and finally start testing the original Autobuild thesis instead of testing scaffolding around it.

[1]: https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/subresources/sessions/methods/create?utm_source=chatgpt.com "Create an agent session | OpenAI API Reference"
[2]: https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/subresources/sessions/subresources/events/methods/stream?utm_source=chatgpt.com "Stream agent session events | OpenAI API Reference"
