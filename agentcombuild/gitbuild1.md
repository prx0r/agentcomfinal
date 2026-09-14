# gitbuild1.md — self-hosting build directive (saved 2026-09-14)

Status: BINDING THIS CYCLE. Stop feature expansion; fix boundaries first.
Baseline: `be869c0910a221f171d8b9c18c41cbc0d3dc5ddf` tagged
`agentcom-e0-openai-native0`. End state per item R below.

The recent push is a real step forward. The architecture is now substantially cleaner: `CANONICAL.md` freezes one owner per responsibility, old `autobuild1/2/3` are explicitly historical, and the core tests enforce full SHA-256 IDs, lineage, scheduler rules, Actuality envelopes, real QP constructors, A-Task sandboxing, Seed0 candidate lessons, and trajectory promotion rules.

The latest `openai-native-0` push is also disciplined about what it has *actually* proven: its build notes explicitly call it a simulation, with live Agents API, GPT-Live, plugin generation and WASM/Rego judges still deferred.  That honesty is exactly what we want.

But I would **stop feature expansion for one cycle**. There are several boundary failures worth fixing before this ever touches real credentials.

The most important contradiction is that your canonical architecture says `autobuild1/2/3` are frozen experimental history, yet `openai_native` directly imports `ab2` grants/crypto and `ab3` readback, and its tests explicitly put those historical source trees back on `sys.path`.    Even worse, the OpenAI MCP gateway's default QP dependency is still `ab2.grants`/`ab2.build`, not the real canonical `/qp` adapter.

So `openai-native-0` currently proves:

$$
\text{OpenAI-shaped harness} \rightarrow \text{old prototype authority semantics}
$$

rather than:

$$
\boxed{\text{OpenAI} \rightarrow \text{real QP}}
$$

The second big issue is that the claimed acceptance chain does not yet contain a QP transition. `chain.py` checks authorization and independent readback, but constructs its trajectory with `qp_receipts=[]`.  That should structurally prevent the test from being called an accepted transition.

There are also three concrete fail-open security bugs I'd make P0. `request_approval()` treats an unknown approval policy as “no approval”; `decide()` allows `approval="skipped"` to continue if QP says yes; `enforce()` only knows two consequential tool names and classifies everything else as non-consequential.  The Vault classifier has the same pattern: an empty/unknown capability defaults to `VAULT`, i.e. low-consequence read-only. Unknown should go the other direction—`QP_GATEWAY` or refuse classification entirely.

One more subtle thing: telemetry hashes are currently truncated to 16 hex characters. That's fine as a display key, but not as durable trajectory/evidence identity.  Your core has already correctly standardized on full SHA-256; use that everywhere anything may later participate in evidence or deduplication.

And externally, GitHub currently reports **no combined CI statuses on the latest commit**. So at the moment all green evidence is produced by the same repo/build environment that produced the code. That is the perfect next thing to fix.

The Git idea is now especially useful because Git can give us the primitive self-hosting experiment substrate without inventing another subsystem.

# AgentComBuild — Build the System Using a Primitive Version of the System

## Objective

Do not add major new product features until AgentComBuild can use its own primitive architecture to improve itself.

The immediate target is:

```text
one frozen ContractRoot
        ↓
multiple isolated implementation lanes
        ↓
same external validator
        ↓
exact commit SHAs
        ↓
machine-selected winner
        ↓
QP-backed promotion
        ↓
main advances
```

Git is the experiment substrate.

QP is still truth.

Seed0 compares.

A-Task executes.

Git does **not** decide correctness.

---

# A. Freeze the current baseline

Current baseline:

```text
be869c0910a221f171d8b9c18c41cbc0d3dc5ddf
```

Treat this as:

```text
BASE_SHA
```

Do not rewrite it.

Create a lightweight baseline tag such as:

```bash
git tag agentcom-e0-openai-native0 be869c0910a221f171d8b9c18c41cbc0d3dc5ddf
```

This is an experiment reference, not proof.

---

# B. Define one self-hosting ContractRoot

Create a structured contract for:

```text
agentcombuild-selfhost-v1
```

Its hard Actuality leaves should be approximately:

```text
canonical_archive_isolation
real_qp_authority_path
real_qp_transition_receipt
real_atask_execution
official_mcp_wire_compatibility
openai_sdk_wire_compatibility
security_defaults_fail_closed
independent_readback_required
telemetry_full_hash
seed0_same_contract_tournament
git_commit_bound_validation
promotion_requires_external_validation
```

Each leaf requires executable evidence.

Do not accept prose.

---

# C. P0 tests before any new work

Implement these tests first.

## `canonical_archive_isolation`

FAIL if canonical code or current experiments import:

```text
agentcombuild/autobuild1
agentcombuild/autobuild2
agentcombuild/autobuild3
```

Historical tests may import them.

Canonical/openai-native production code may not.

Use AST/import/path scanning rather than grep where practical.

The current code must FAIL this initially.

That is good.

---

## `real_qp_authority_path`

Call the actual `/qp` entrypoint.

Do not import `ab2.grants`.

Input:

```text
action
grant
facts
caller-supplied time
```

Expected:

```text
real QP result
```

No locally recreated authority semantics.

If QP lacks a usable external settlement/authorization interface, add that interface **inside `/qp`**, not inside AgentCom.

---

## `real_qp_transition_receipt`

A successful consequential test must end with:

```text
qp_receipts.length >= 1
```

and:

```text
qp.verify(receipt) == PASS
```

A trajectory with:

```json
"qp_receipts": []
```

must never graduate beyond observation.

---

## `unknown_approval_policy_refuses`

These must all refuse:

```text
approval policy = "foobar"
approval policy = null
approval required + approval = skipped
approval required + approval missing
```

Unknown policy can never mean “no approval needed.”

---

## `unknown_tool_refuses`

Remove the dangerous logic:

```text
if known dangerous tool:
    authorize
else:
    authorized=True
```

Replace with a registry:

```text
tool
→ declared consequence class
→ capability
→ authority rule
```

Unknown tool:

```text
REFUSE
```

Only an explicitly classified:

```text
NON_CONSEQUENTIAL
```

tool may bypass QP authority.

---

## `unknown_credential_class_refuses`

These must never become OpenAI Vault credentials:

```text
{}
{"kind": "unknown"}
missing capability metadata
invalid capability class
```

Correct result:

```text
UNCLASSIFIED / REFUSE
```

or conservative:

```text
QP_GATEWAY
```

Never `VAULT`.

---

## `real_mcp_client_handshake`

The current homemade JSON-RPC server is not proven MCP merely because its own tests can call it.

Use an actual supported MCP client/library.

The validator should:

```text
launch server
→ initialize
→ enumerate tools
→ invoke gg.search
→ invoke qp.authorize negative case
→ shutdown
```

If the official client cannot connect, the gate is FALSE.

Do not modify the validator to match the implementation.

Fix the implementation.

---

## `openai_sdk_wire_test`

Use the pinned OpenAI Agents SDK.

No network/key required initially.

Validate that generated:

```text
Agent configuration
tool definitions
MCP configuration
Skill bundle
session metadata
```

are accepted by actual SDK constructors/types.

A dictionary that merely “looks like the API” is insufficient.

---

## `telemetry_full_identity`

Anything potentially entering:

```text
trajectory
evidence
dedupe
lineage
```

uses full SHA-256.

Short IDs may exist only as:

```text
display_id
```

Canonical:

```text
sha256:<64 hex>
```

---

# D. Git becomes the experiment substrate

Do not have multiple agents switch branches inside one working tree.

For each lane:

```bash
git worktree add /tmp/agentcom-<RUN>-A -b exp/<CONTRACT>/A BASE_SHA
git worktree add /tmp/agentcom-<RUN>-B -b exp/<CONTRACT>/B BASE_SHA
git worktree add /tmp/agentcom-<RUN>-C -b exp/<CONTRACT>/C BASE_SHA
```

Each lane receives:

```text
same BASE_SHA
same ContractRoot
same frozen validator root
different policy/solution
```

Example:

```text
A = direct repair
B = canonical-adapter-first
C = GitGoblin/reuse-first
```

This is literally a Seed0 tournament implemented with Git worktrees.

The directories themselves can be passed to Seed0's existing tournament machinery.

---

# E. Builder rules

Every lane must obey:

```text
never work in another lane's worktree
never share an index
never force-push
never rewrite another lane
never use git add .
stage explicit owned paths only
commit every coherent attempted solution
```

After each coherent attempt:

```bash
git add path/you/changed.py tests/test_you_changed.py
git commit -m "exp: real qp gateway"
```

The commit SHA is the implementation identity.

No uncommitted working tree may be submitted for validation.

---

# F. Separate builder from validator

This is crucial.

The coding agent must not validate from its dirty builder tree.

For candidate:

```text
CANDIDATE_SHA
```

create a fresh validation worktree:

```bash
git worktree add --detach /tmp/validate-$SHORT $CANDIDATE_SHA
```

Then run the frozen evaluator there.

The run receipt records:

```json
{
  "base_sha": "...",
  "candidate_sha": "...",
  "candidate_tree": "...",
  "contract_root": "...",
  "validator_sha": "...",
  "policy_id": "...",
  "tests": [],
  "actuality_before": {},
  "actuality_after": {},
  "cost": {}
}
```

This ensures:

```text
what was tested == exact Git object
```

not:

```text
roughly whatever happened to be in the agent's directory.
```

---

# G. The validator itself must be frozen separately

The agent must not get progress by editing:

```text
tests
acceptance
validator
ContractRoot
```

inside its lane.

The canonical evaluator is loaded from:

```text
VALIDATOR_SHA
```

on the baseline/protected side.

Candidate implementation:

```text
CANDIDATE_SHA
```

is the test target.

Conceptually:

```text
validator @ V
       ↓
candidate @ C
       ↓
PASS / FAIL / UNKNOWN
```

not:

```text
candidate modifies validator
       ↓
candidate passes itself
```

If acceptance legitimately needs to change:

```text
new ContractRoot
```

and a separate governed change.

---

# H. Use Git diff as the ChangeSet

Do not invent another diff format for source changes.

Record:

```bash
git diff --stat BASE_SHA..CANDIDATE_SHA
git rev-parse CANDIDATE_SHA^{tree}
```

The run record can contain:

```text
base commit
candidate commit
tree id
changed paths
diff hash
```

Git already gives us a Merkle-DAG-backed immutable representation of the implementation.

Use it.

---

# I. Git notes: useful, but noncanonical

Use a dedicated notes ref:

```text
refs/notes/agentcom
```

to attach derived experiment metadata to candidate commits:

```text
ContractRoot
RunRoot
Seed0 score
QP receipt ref
validation summary
cost
winner/loser status
```

Example:

```bash
git notes --ref=agentcom add -m '<receipt summary>' CANDIDATE_SHA
```

Important:

```text
Git notes are an index/view.
QP receipts remain truth.
```

Notes can change independently of source commits, so never treat them as canonical proof.

It is excellent for:

```bash
git log --show-notes=agentcom
```

and asking:

> What did this exact implementation actually achieve?

---

# J. Promotion

A lane cannot merge itself.

Promotion happens only after:

```text
ContractRoot unchanged
AND
hard Actuality leaves TRUE
AND
QP verification passes where applicable
AND
hidden/regression tests pass
AND
Seed0 tournament accepts candidate
```

Then:

```text
candidate SHA
→ promotion request
→ external revalidation
→ merge/cherry-pick
→ main
```

Prefer fast-forward when main still equals the lane's base.

Never force.

After promotion, rerun validation against new `main`.

Tag meaningful proven states:

```text
proven/agentcom-selfhost-v1
```

The tag is a convenient anchor.

The QP receipt is still the actual proof.

---

# K. Failed lanes are useful

Do not erase all failed branches immediately.

Every failed lane emits:

```text
failure class
candidate SHA
failed gates
attempted mechanism
cost
useful observations
```

High-information failures may remain as experiment branches.

Low-value duplicates can later be deleted once their structured failure record has been banked.

The important asset is not branch count.

It is:

```text
problem
→ attempted intervention
→ exact code state
→ exact gate result
```

---

# L. Use `git bisect` as an Actuality debugger

This is one of the highest-value simple Git integrations.

If:

```text
main@A = Actuality TRUE
main@B = Actuality FALSE
```

and there are many commits between:

```bash
git bisect start B A
git bisect run python external_validator.py --gate <gate-id>
```

Now Git automatically identifies the exact commit where reality stopped satisfying the invariant.

This should become a standard repair primitive.

---

# M. Minimal Git policy in AGENTS.md

Add only this much:

```text
Git is the implementation experiment ledger.

- Never share a worktree/index between active agents.
- One candidate lane = one branch + one worktree.
- Stage explicit paths only; never `git add .`.
- Commit coherent attempts before validation.
- Validation runs against an exact clean commit SHA.
- Do not change frozen validators/acceptance from an implementation lane.
- Never force-push or rewrite another lane.
- Never self-merge.
- Failed commits remain evidence until their structured learning is banked.
```

No larger Git framework is required yet.

---

# N. Self-hosting experiment 1

The first actual tournament should solve:

```text
REMOVE ALL HISTORICAL AB1/AB2/AB3 DEPENDENCIES
FROM OPENAI-NATIVE CANONICAL EXECUTION
```

Freeze that ContractRoot.

Create three worktrees.

Candidate policies:

```text
Lane A:
minimal direct rewrite onto canonical adapters

Lane B:
adapter-first, modify QP/A-Task interfaces only where strictly required

Lane C:
GitGoblin archaeology first, reuse current canonical surfaces wherever possible
```

Run identical external tests.

Measure:

```text
Actuality PASS/FAIL
files changed
LOC changed
attempts
wall time
tokens
regressions
new reusable primitives
```

Promote the smallest passing implementation.

This is an ideal first self-build because current main genuinely fails the intended canonical architecture.

---

# O. Self-hosting experiment 2

Target:

```text
REAL QP RECEIPT IN OPENAI-NATIVE CHAIN
```

Acceptance:

```text
OpenAI-shaped tool request
→ real QP authorization
→ action simulator
→ independent readback
→ real QP settlement
→ verified TransitionReceipt
→ trajectory contains receipt
→ trajectory advances L0 → L1
```

Negative controls:

```text
missing grant → REFUSED
wrong scope → REFUSED
unknown capability → REFUSED
readback disagreement → no successful outcome transition
fabricated receipt → verification FAIL
```

That is the milestone I care about most.

---

# P. Self-hosting experiment 3

Target:

```text
OFFICIAL OPENAI + OFFICIAL MCP WIRE COMPATIBILITY
```

No real external action yet.

Use actual SDKs locally.

Acceptance:

```text
BusinessBundle
→ real OpenAI Agents SDK objects
→ real MCP client/server handshake
→ tool discovery
→ tool invocation
→ normalized telemetry
```

Only after this is TRUE should credentials enter the system.

---

# Q. GitHub CI becomes the independent second machine

The latest commit currently has no GitHub status checks.

Add one keyless workflow:

```text
agentcom-contract
```

It should run on every candidate/PR:

```text
canonical boundary tests
core tests
openai-native offline tests
archive-import prohibition
fail-closed security tests
MCP wire test
SDK constructor/wire tests
tamper tests
secret scan
```

A second workflow can be:

```text
agentcom-live
```

manual/scheduled, with credentials, for genuine OpenAI/live-provider probes later.

Never make keyless CI depend on live services.

---

# R. Definition of success for this development cycle

Do not declare “AgentComBuild improved” after adding more code.

The cycle is complete when:

```text
1 frozen ContractRoot

3 isolated Git worktree lanes

>=1 failed candidate preserved as structured evidence

1 winning candidate chosen by external gates

1 exact commit promoted

1 GitHub CI status proves it independently

1 real QP receipt appears in the OpenAI-native trajectory

0 canonical imports from autobuild1/2/3
```

All green evidence is produced by the same repo/build environment that produced the code.
