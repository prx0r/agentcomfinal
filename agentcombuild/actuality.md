# actuality.md — system axiom (saved 2026-09-14)

Status: **AXIOM**. This document outranks implementation choices. When any
module conflicts with it, the module is wrong.

Yes. This is the cleanest version of the system yet.

The key abstraction is not “testing.” It is:

$$
\boxed{\textbf{Actuality}}
$$

For every claim the agent wants to advance:

> **What observation of reality would make this claim TRUE rather than merely plausible?**

Then progress is impossible until that observation exists.

That is basically the deep idea already latent in A-Task + QP.

## The crucial split: probe vs validator

I would **not** choose between `.py` and WASM globally.

Split the world into two things:

```text
PROBE
effectful
touches reality
        ↓
Evidence JSON
        ↓
JUDGE
pure + deterministic
        ↓
TRUE / FALSE / UNKNOWN
```

The **probe** can be Python, Node, Playwright, Schemathesis, k6, curl, SQL, whatever is best.

The **judge** should ideally be tiny, deterministic, side-effect-free, content-addressed and sandboxed.

That distinction is extremely important.

A Playwright script should never be allowed to say:

> “Website works = PASS.”

It should say:

```json
{
  "button_visible": true,
  "button_clicked": true,
  "request_status": 201,
  "created_id": "order_9281",
  "readback_status": 200,
  "readback_body_hash": "...",
  "duration_ms": 482
}
```

Then a separate validator decides whether that evidence satisfies the frozen acceptance contract.

That is how the agent loses the ability to cheat.

---

# WASM vs Python

I would use:

$$
\boxed{\textbf{Python/Node/etc. for probes}}
$$

and:

$$
\boxed{\textbf{CEL / Rego / WASM for judges}}
$$

Python is excellent for obtaining evidence, but arbitrary Python is a poor long-term canonical gate language because it can do almost anything: network, filesystem, clocks, randomness, monkeypatching, environment access.

For simple judges I actually think **CEL may be better than WASM**.

CEL is deliberately non-Turing-complete, mutation-free, side-effect-free and terminating. It is designed precisely for evaluating structured data into decisions and has canonical serializable ASTs. ([GitHub][1])

So this:

```text
evidence.status == 201
&& evidence.readback.exists
&& evidence.latency_ms < 1000
```

does not need Python or WASM.

It should be CEL.

### My proposed judge ladder

```text
Level 0
JSON Schema / CUE
"Is this evidence structurally valid?"

Level 1
CEL
"Does this simple deterministic predicate hold?"

Level 2
OPA/Rego
"Does this larger policy over structured state hold?"

Level 3
WASM
"Run this arbitrary but sandboxed deterministic validator."

Level 4
external/human evaluator
only where reality cannot be reduced further
```

CUE is particularly good for compositional structured constraints and validation. ([CUE Labs][2])

OPA is already built specifically to evaluate policy over JSON-like structured data and can compile Rego policies to WebAssembly. ([Open Policy Agent][3])

For genuinely custom validators, Wasmtime gives us fuel exhaustion, execution limits and store resource limits, so a malicious/broken validator cannot run forever. ([Wasmtime][4])

So:

```text
.py is not the constitutional layer.

WASM isn't necessarily the authoring language either.

Structured validator IR is the constitution.
```

Then we compile/evaluate it using whatever engine is appropriate.

---

# The frontier gives us an insane amount of validation machinery already

We should absolutely **import adapters around existing projects rather than write most validators ourselves**.

The first validator packs I would build are:

| Pack            | Existing engine            | What reality it proves                            |
| --------------- | -------------------------- | ------------------------------------------------- |
| `web.browser`   | Playwright                 | actual browser/user flows                         |
| `api.contract`  | Schemathesis               | API conforms under normal + adversarial inputs    |
| `api.consumer`  | Pact                       | consumer/provider interaction actually compatible |
| `perf.http`     | k6                          | actual latency/error distributions                |
| `perf.web`      | k6 browser / Lighthouse CI | actual page/web-vital budgets                     |
| `web.a11y`      | axe-core                   | machine-verifiable accessibility rules            |
| `security.repo` | Trivy                      | secrets/vulns/misconfig/licenses                  |
| `environment`   | Testcontainers             | behavior against real ephemeral services          |
| `policy`        | CEL/OPA                    | deterministic policy over evidence                |
| `custom`        | Wasmtime                   | sandboxed custom gate                             |

And these are not toy projects.

Playwright supports browser interaction and direct server-side API requests, which lets us validate frontend action and backend postcondition independently. ([Playwright][5])

Schemathesis is almost perfectly aligned with Autobuild: it generates property-based tests from OpenAPI/GraphQL, runs coverage/fuzzing/stateful phases, and can **record/replay the precise failing cases** it finds. ([GitHub][6])

k6 thresholds literally turn quantitative reality like:

```text
error rate < 1%
p95 latency < 200 ms
```

into process exit PASS/FAIL. ([Grafana Labs][7])

Lighthouse CI already supports preventing regressions and enforcing performance budgets across runs. ([GitHub][8])

Axe-core automatically tests a significant subset of accessibility requirements and explicitly marks uncertain cases incomplete rather than pretending certainty. ([GitHub][9])

Trivy gives filesystem/container vulnerability, secret, license and configuration scans with structured output and custom policy support. ([GitHub][10])

Testcontainers lets us test against actual PostgreSQL/Redis/etc. rather than mocks. ([GitHub][11])

This is basically a validator goldmine.

---

# Your website example is exactly right

Suppose the specification says:

> **“The website fully works for the user.”**

That statement is completely useless to an autonomous agent.

Autobuild should recursively ask:

> What would make that TRUE?

Maybe:

```text
website_works
│
├─ site_reachable
│
├─ page_renders
│
├─ no_fatal_js_errors
│
├─ primary_navigation_works
│
├─ signup_works
│  ├─ form_visible
│  ├─ valid_submission_accepted
│  ├─ API_returns_success
│  ├─ user_record_exists
│  └─ refresh_preserves_session
│
├─ core_action_works
│  ├─ button_visible
│  ├─ click accepted
│  ├─ backend action occurred
│  ├─ external state changed
│  └─ independent readback confirms it
│
├─ invalid_inputs_fail_correctly
│
├─ accessibility_threshold
│
├─ latency_threshold
│
└─ security_gates
```

Now every leaf is **observable**.

That means the root can become:

$$
WebsiteWorks=
\bigwedge_{i=1}^{n}Leaf_i
$$

And critically:

$$
Leaf_i \in \{TRUE,FALSE,UNKNOWN\}
$$

not merely Boolean.

Then:

$$
\boxed{
Progress_i=1
\iff
Leaf_i=TRUE
}
$$

`UNKNOWN` blocks.

That's exactly the anti-cheating behavior we want.

---

# “Certainty of 1” needs one careful definition

We should not claim philosophical certainty.

Instead define:

$$
A(C,E)=1
$$

to mean:

> **All frozen acceptance predicates for claim C passed against admissible, sufficiently fresh evidence E.**

So:

```text
Actuality = 1
```

means **contractually established actuality**, not omniscience.

For example:

```json
{
  "claim": "checkout works",
  "actuality": "TRUE",
  "contract_root": "...",
  "evidence_root": "...",
  "validator_root": "...",
  "environment": "prod-like-2026-09-14",
  "observed_at": "...",
  "proof_class": "external_readback"
}
```

That is extremely strong.

---

# There is another key primitive: independent readback

This matters enormously.

Suppose the agent clicks:

```text
BUY
```

and the UI shows:

```text
Success!
```

That proves almost nothing.

The same application could simply display success.

The stronger chain is:

```text
ACTION CHANNEL
Playwright clicks Buy
        ↓
request 201

INDEPENDENT CHANNEL
query order API/database/provider
        ↓
order #123 actually exists
```

Then:

$$
ActionEvidence + IndependentReadback
\rightarrow Actuality
$$

I'd make this a general Autobuild rule:

$$
\boxed{\text{Consequential actions require independent postcondition readback where possible.}}
$$

For email:

```text
send API says 202
+
provider/message readback exists
```

For marketplace listing:

```text
create call succeeds
+
public/provider listing can be fetched
```

For payment:

```text
checkout UI succeeds
+
processor transaction exists
```

For DNS:

```text
API says changed
+
independent DNS resolution observes it
```

For GitHub:

```text
agent says pushed
+
remote commit/tree actually contains change
```

That's actuality.

---

# This creates a proper Validator Registry

I think this should become a serious first-class package:

```text
validators/
├── browser/
├── api/
├── data/
├── performance/
├── security/
├── commerce/
├── communications/
├── identity/
├── filesystem/
├── deployment/
└── policy/
```

But each validator should actually be packaged as a reusable primitive.

Something like:

```json
{
  "id": "web.button_effect.v1",
  "version": "1.0.0",

  "claim_class": "behavior",

  "requires": [
    "web.browser.page"
  ],

  "probe": {
    "runner": "playwright",
    "adapter": "playwright.click_readback.v1",
    "network": true,
    "timeout_ms": 10000
  },

  "evidence_schema": "schemas/button-effect.json",

  "judge": {
    "engine": "cel",
    "expression": "e.clicked == true && e.postcondition == true"
  },

  "proof": {
    "minimum_evidence_class": "external_readback",
    "max_age_seconds": 300
  }
}
```

The agent does not get to redefine that.

---

# And each validator becomes a LEGO brick

This connects perfectly to what you said.

A mature validator primitive would expose:

```text
REQUIRES
what evidence/capabilities must exist

PROVIDES
what claim it can establish

PROBE
how observations are obtained

JUDGE
exact deterministic rule

COST PROFILE
time / money / tokens / environment

FAILURE MODES
known invalid evidence states

PERFORMANCE
how often this validator itself misbehaves

VERSION
semantics are frozen
```

Then Autobuild can compile:

```text
"website works"
```

by searching the validator library.

It might find:

```text
web.reachable
web.render
web.no_console_errors
web.click_effect
api.response_contract
api.stateful_workflow
perf.page_load
security.no_secrets
a11y.wcag_auto
```

Then compose them.

No LLM has to invent acceptance criteria from scratch every time.

---

# Over time, the library gets huge

And I think you're right that this may become one of the highest-value outputs of the whole system.

Initially:

```text
50 validator primitives
```

then:

```text
500
```

then:

```text
50,000
```

covering things like:

```text
Stripe payment settled
Shopify product actually listed
email actually delivered
DNS propagated
GitHub PR mergeable
Solana tx finalized
XMR escrow funded
calendar event exists
phone call connected
CRM contact persisted
site login survives reload
file downloadable
image renders
model endpoint stays <500ms p95
...
```

And because each is actual structured code/data rather than prose, agents can compose them automatically.

---

# This gives Autobuild an even cleaner role

Autobuild becomes basically:

```text
DESIRED REALITY
      ↓
decompose claims
      ↓
search validator registry
      ↓
construct Actuality DAG
      ↓
GitGoblin finds implementations
      ↓
A-Task executes missing work
      ↓
probes obtain reality
      ↓
judges evaluate evidence
      ↓
QP settles claims
```

That is stronger than:

> “turn plan into tasks.”

It's:

> **compile intent into a proof graph.**

---

# And A-logs become very important

I would formalize your A-log idea now.

Not:

```text
agent.log
"I successfully completed checkout."
```

Instead:

```text
A-LOG = Actuality Log
```

Every row is some direct observation:

```json
{
  "observation_id": "...",
  "probe_id": "playwright.checkout.v2",
  "run_id": "...",
  "contract_root": "...",

  "observation": {
    "url": "...",
    "http_status": 201,
    "transaction_id": "...",
    "readback_found": true,
    "latency_ms": 492
  },

  "artifacts": {
    "trace_sha256": "...",
    "har_sha256": "...",
    "screenshot_sha256": "..."
  },

  "timestamp": "...",
  "environment": "...",

  "attestor": "probe-worker-7"
}
```

No verdict.

Then QP processes:

```text
A-log
   ↓
evidence object
   ↓
validator
   ↓
claim result
   ↓
receipt
```

That respects QP's existing constitutional distinction:

$$
Evidence \neq Verdict
$$

and QP already explicitly freezes that invariant.

---

# We should import rather than rewrite

My concrete first library would be:

```text
validators/probes/
  playwright
  schemathesis
  pact
  k6
  lighthouse
  axe
  trivy
  testcontainers

validators/judges/
  jsonschema
  cue
  cel
  opa
  wasm
```

I would **not fork their source code initially**.

Build deterministic adapters that invoke pinned versions and normalize results.

For example:

```text
Playwright output
      ↓
our normalized BrowserEvidence

Schemathesis output
      ↓
our normalized APIEvidence

k6 output
      ↓
our normalized PerformanceEvidence
```

Then our validator layer remains stable if we later swap implementation engines.

---

# Where WASM becomes very valuable

Not for browser automation.

WASM shines for **portable custom judges**.

Imagine later:

```text
validator package
├── manifest.json
├── input.schema.json
├── validator.wasm
├── testvectors.json
└── metadata.json
```

QP can run:

```text
wasm validator
network = NONE
filesystem = NONE
clock = NONE
random = NONE
memory = 16MB
fuel = 100000
```

against evidence JSON.

Wasmtime's fuel model is explicitly meant to deterministically stop runaway guest execution. ([Wasmtime][12])

That is close to ideal for untrusted third-party validator modules.

---

# But I would start simpler

Don't immediately build a massive WASM plugin platform.

Phase one:

```text
Python/Node probes
+
JSON evidence
+
CEL predicates
+
QP receipts
```

Then add:

```text
OPA/Rego
```

where policies become complex.

Then:

```text
WASM validator ABI
```

for arbitrary user/community validators.

This is another application of Underengineer.

---

# The fundamental invariant

I would put this sentence at the top of Autobuild / AgentCom:

$$
\boxed{
\text{An agent can propose any state transition it likes; the only route to progress is externally produced evidence satisfying frozen deterministic gates.}
}
$$

Or operationally:

```text
NO A-LOG
    ↓
NO EVIDENCE

NO EVIDENCE
    ↓
UNKNOWN

UNKNOWN
    ↓
NO QP RECEIPT

NO QP RECEIPT
    ↓
NO STATE ADVANCE
```

The agent can lie forever.

It gains nothing.

That is the property we actually want.

And yes: I think the **validator/proof-graph library** should now become a core piece of Autobuild. The beautiful part is that every project we build automatically expands it, so eventually “build X” increasingly means:

```text
retrieve existing proof DAG
+
retrieve existing implementations
+
construct only missing leaves
+
prove them
```

which is exactly the LEGO/Qubic-ant direction you've been describing.

[1]: https://github.com/google/cel-spec "https://github.com/google/cel-spec"
[2]: https://cue.dev/docs/official-modules/ "https://cue.dev/docs/official-modules/"
[3]: https://www.openpolicyagent.org/docs/wasm "https://www.openpolicyagent.org/docs/wasm"
[4]: https://docs.wasmtime.dev/examples-interrupting-wasm.html "https://docs.wasmtime.dev/examples-interrupting-wasm.html"
[5]: https://playwright.dev/docs/api-testing "https://playwright.dev/docs/api-testing"
[6]: https://github.com/schemathesis/schemathesis/blob/master/docs/tutorials/cli.md "https://github.com/schemathesis/schemathesis/blob/master/docs/tutorials/cli.md"
[7]: https://grafana.com/docs/k6/latest/using-k6/thresholds/ "https://grafana.com/docs/k6/latest/using-k6/thresholds/"
[8]: https://github.com/googlechrome/lighthouse-ci "https://github.com/googlechrome/lighthouse-ci"
[9]: https://github.com/dequelabs/axe-core "https://github.com/dequelabs/axe-core"
[10]: https://github.com/aquasecurity/trivy/blob/main/docs/guide/scanner/misconfiguration/index.md "https://github.com/aquasecurity/trivy/blob/main/docs/guide/scanner/misconfiguration/index.md"
[11]: https://github.com/testcontainers/testcontainers-python "https://github.com/testcontainers/testcontainers-python"
[12]: https://docs.wasmtime.dev/api/wasmtime/struct.Config.html "https://docs.wasmtime.dev/api/wasmtime/struct.Config.html"
