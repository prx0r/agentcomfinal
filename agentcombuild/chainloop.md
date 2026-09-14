# chainloop.md — validation-DAG bootstrap (saved 2026-09-14)

Status: BINDING. Replaces manual peer review of validators with QP-settled
leaf receipts. Reviews become projections of QP state, never authorities.

Yes. The loop exists because **we are still manually peer-reviewing the validator instead of letting the architecture validate itself**.

The bootstrap should be:

$$
\boxed{\text{Git identifies the exact candidate} \rightarrow
\text{probes observe it} \rightarrow
\text{QP settles the observations} \rightarrow
\text{review is only a view of QP state}}
$$

QP should not go out and run GitHub/OpenAI/pytest itself. QP stays tiny and deterministic. Everything outside QP produces evidence; QP decides whether that evidence satisfies the frozen contract. That is already the direction of the corrected action/readback chain: external observations exist first, then QP settles.

Right now we have the pieces but aren't using them recursively enough.

## The missing object: `ValidationContract`

For every build, including AgentCom itself, Autobuild should compile an exact contract such as:

```json
{
  "claim": "candidate is a valid implementation of agentcom-selfhost-v1",

  "subject": {
    "repo": "prx0r/agentcomfinal",
    "candidate_sha": "abc123...",
    "tree_sha": "def456..."
  },

  "requirements": [
    {
      "id": "exact-candidate",
      "probe": "git.clean_checkout",
      "judge": "candidate_sha == tested_sha"
    },
    {
      "id": "tests-pass",
      "probe": "pytest.run",
      "judge": "exit_code == 0"
    },
    {
      "id": "readback-before-settlement",
      "probe": "adversarial.readback_false",
      "judge": "qp_receipts == []"
    },
    {
      "id": "managed-openai-live",
      "probe": "openai.session",
      "judge": "real_session_id && event_count > 0"
    },
    {
      "id": "cg-real-run",
      "probe": "cg.run",
      "judge": "receipt_origin == cg"
    }
  ]
}
```

Autobuild already has the right idea for ContractRoot: acceptance semantics such as evidence schema, judge, freshness, authority and proof requirement are frozen into WHAT counts as success.

That becomes the constitution of the experiment.

---

## Then validation becomes a DAG

Instead of me repeatedly looking at the repo and saying:

> “Actually that test isn't real.”

the system should expose:

```text
agentcom-selfhost-v1

├── exact_git_candidate
│      FALSE
│
├── frozen_validator
│      TRUE
│
├── clean_checkout
│      UNKNOWN
│
├── local_tests
│      TRUE
│
├── adversarial_actuality
│      TRUE
│
├── real_cg_episode
│      FALSE
│
├── real_openai_session
│      UNKNOWN
│
└── github_ci
       UNKNOWN
```

That is the entire review.

No prose `VERDICT.json` saying “overall PASS.”

The root is simply:

$$
Root = AND(
exact\_git\_candidate,
frozen\_validator,
clean\_checkout,
local\_tests,
adversarial\_actuality,
real\_cg,
real\_openai,
ci
)
$$

Therefore currently:

$$
\boxed{AgentComBuild = UNKNOWN/FALSE}
$$

and that's fine.

The system tells us precisely what remains.

---

## QP should issue one receipt per established leaf

Example:

```text
probe: git.clean_checkout

observation:
 candidate_sha = 59f2...
 tested_sha = a097...
```

Judge:

```text
candidate_sha == tested_sha
```

Result:

```text
FALSE
```

QP receipt:

```json
{
  "claim": "exact-git-candidate",
  "result": "FALSE",
  "contract_root": "...",
  "evidence_root": "...",
  "gate": "git-exact-candidate-v1"
}
```

Now nobody gets to write:

```text
PROMOTED
```

because promotion structurally requires:

```text
exact-git-candidate == TRUE
```

This would have caught the precise bug we just manually found: the self-host receipt claimed `a097...`, while the tested working tree contained later uncommitted changes.

---

# This is actually where the validator library begins

We need a few primitive probes/judges immediately.

```text
git.exact_tree.v1
git.clean.v1
git.base_fails_candidate_passes.v1

pytest.exit_zero.v1

github.ci_success.v1

openai.real_session.v1
openai.tool_roundtrip.v1

mcp.official_client_roundtrip.v1

cg.real_receipt.v1

qp.receipt_valid.v1
qp.no_receipt_on_failed_readback.v1

chatgpt.plugin_installed.v1
chatgpt.tool_invoked.v1
```

Each primitive has:

```text
PROBE
→ observation JSON

JUDGE
→ TRUE / FALSE / UNKNOWN
```

Then Autobuild composes them.

That is exactly the validator-library architecture we discussed earlier.

---

# The clever part: AgentCom should build against the failed leaves

This also removes the question:

> “What should the agent work on next?”

Suppose root state is:

```text
exact candidate      FALSE
real CG              FALSE
real OpenAI           UNKNOWN
ChatGPT host          UNKNOWN
```

AgentCom asks:

```text
Which FALSE/UNKNOWN node is currently actionable
and gives the largest expected root progress?
```

Maybe:

```text
exact candidate
```

wins.

Then A-Task gives the worker:

```text
TARGET:
git-exact-candidate = TRUE

CURRENT EVIDENCE:
tested SHA != claimed SHA

ACCEPTANCE:
candidate SHA must equal clean detached validation SHA

YOU MAY:
edit implementation

YOU MAY NOT:
change validator or ContractRoot
```

The worker fixes it.

Probe reruns.

QP says TRUE or not.

No human peer review required.

---

# And when the worker gets stuck, our agent harness activates

This plugs directly into the earlier microprocessor idea.

```text
QP leaf remains FALSE
        ↓
worker gets failure evidence
        ↓
local knowledge lookup
        ↓
GitGoblin
        ↓
web/GitHub/docs
        ↓
3 candidate mechanisms
        ↓
CG lanes
        ↓
attempt A / B / C
        ↓
same QP gate
        ↓
one becomes TRUE
```

This is the actual autonomous loop.

The agent doesn't need to know whether I think its approach is good.

It just needs to make:

```text
FALSE → TRUE
```

under an immutable external gate.

---

# Reviews therefore disappear as an authority layer

Keep a dashboard/readable review, but generate it.

Instead of:

```json
{
  "overall": "PASS",
  "note": "38 tests passed"
}
```

produce:

```json
{
  "contract_root": "...",
  "subject_sha": "...",

  "actuality": {
    "TRUE": 12,
    "FALSE": 2,
    "UNKNOWN": 3
  },

  "blocking": [
    "real-openai-session",
    "exact-candidate",
    "real-cg-run"
  ],

  "receipts": {
    "...": "receipt:..."
  },

  "state": "NOT_PROVEN"
}
```

That review contains **no judgment code**.

It's simply a projection of QP state.

---

# We need one bootstrap trust root

There is necessarily a bottom.

Otherwise you get infinite recursion:

```text
Who validates validator?
Who validates validator's validator?
...
```

Our root should be deliberately tiny:

```text
Git object hashing
canonical JSON hashing
QP canonical serialization
QP gate evaluator
signature verification
basic process exit observation
```

These are the pieces we audit heavily once.

Everything above them is content-addressed and compositional.

Conceptually:

$$
\boxed{
TrustBase =
Git +
CanonicalHash +
QP +
TinyProbeRuntime
}
$$

Not:

```text
LLM
review script
README
pytest count
```

The smaller that base is, the stronger this gets.

---

# There is one correction to make to QP itself

QP should not trust:

```text
"this test passed"
```

as prose.

It should receive something like:

```json
{
  "probe": "pytest-v1",

  "subject": {
    "repo": "...",
    "commit": "...",
    "tree": "..."
  },

  "execution": {
    "executable": "...",
    "argv": ["-m", "pytest", "..."],
    "cwd_hash": "...",
    "validator_sha": "..."
  },

  "observation": {
    "exit_code": 0,
    "stdout_sha256": "...",
    "duration_ms": 1449
  },

  "result": {
    "exit_code": 0,
    "validator_sha": "...",
    "stdout_sha256": "..."
  }
}
```

Then QP's deterministic judge asks only:

```text
subject.commit == required candidate
AND
execution.validator_sha == frozen validator
AND
result.exit_code == 0
```

That is a much stronger fact.

---

# This also tells us exactly how to fix the current repo

Don't ask the agent to “peer review AgentCom again.”

Give it one meta-contract:

```text
AGENTCOM_AUTOBUILD_V1
```

with these hard leaves:

1. exact committed candidate tested;
2. validator frozen independently;
3. baseline fails/candidate passes for self-build;
4. actual CG runner produces receipt;
5. actual OpenAI managed session produces real provider events;
6. same session performs a real MCP read round-trip;
7. GitHub CI independently validates exact SHA;
8. no FAILED/UNKNOWN hard leaf can produce `PROMOTED`;
9. product fixture data cannot satisfy `real business` claims;
10. ChatGPT host leaves remain UNKNOWN until actual host evidence exists.

Then run:

```text
agentcom actuality AGENTCOM_AUTOBUILD_V1
```

It should initially say something like:

```text
TRUE     4
FALSE    3
UNKNOWN  3

NEXT ACTIONABLE BLOCKER:
git-exact-candidate
```

The worker fixes that.

Run again.

```text
TRUE     5
FALSE    2
UNKNOWN  3
```

Then it moves on.

That's the self-hosting system.

## The key shift

We have been doing:

```text
agent writes implementation
↓
agent writes tests
↓
agent writes review
↓
I inspect review
↓
find bullshit
↓
agent patches
↓
repeat
```

We want:

```text
Autobuild freezes Actuality DAG
↓
agent writes implementation
↓
independent probes observe exact candidate
↓
QP evaluates frozen gates
↓
failed leaves return to agent
↓
agent tries again
↓
all leaves TRUE
↓
QP promotion
```

That removes me from the normal validation loop.

I should only need to help design **new classes of invariant** when we discover one we didn't encode yet. Once encoded, that failure class should never require manual rediscovery again.

And that's exactly what makes the system compound:

$$
\boxed{
\text{Every peer-review bug we discover once becomes a permanent validator primitive.}
}
$$

That's what I would have the agent implement now, before touching another feature.
