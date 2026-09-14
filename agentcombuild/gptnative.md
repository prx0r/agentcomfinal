# gptnative.md — OpenAI as replaceable cognition substrate (saved 2026-09-14)

Status: BINDING DIRECTION. OpenAI owns cognition/harness; we own strategy,
contracts, authority, actuality, assets, outcomes, trajectories, learning.
Next experiment is `openai-native-0`, not `autobuild4`.

Yes. I would now make **OpenAI the replaceable cognition/harness substrate underneath AgentCom**, rather than continuing to build our own general agent loop.

The timing is unusually good: OpenAI launched the **Agents API in public beta on September 10, 2026**. It exposes the managed Codex harness with long-running sessions, subagents, tool search, MCP/custom tools, OpenAI-hosted or external sandboxes, environment templates, vaults, skills/plugins, and a live session-event stream. ([OpenAI][1])

The architecture I would freeze is:

```text
                    HUMAN / CUSTOMER
                ┌──────┼─────────┐
                │      │         │
             ChatGPT  Voice     Web/API
                │      │         │
            Plugin   GPT-Live   normal app
                │      │         │
                └──────┼─────────┘
                       ▼
                AGENTCOM GATEWAY
                       │
          CampaignRoot / ContractRoot
                       │
                       ▼
               OPENAI AGENTS API
          managed Codex agent harness
          sessions / subagents / skills
          context / tools / sandbox
                       │
        ┌──────────────┼───────────────┐
        ▼              ▼               ▼
   GitGoblin MCP   Company MCPs    Built-in tools

                       │
                 CONSEQUENTIAL?
                       │
                       ▼
                  QP GATEWAY
        grant + scope + Actuality contract
                       │
                 PASS / REFUSE
                       │
                       ▼
                    REALITY
             email / call / booking
             money / listing / etc.
                       │
                       ▼
             INDEPENDENT READBACK
                       │
                       ▼
                 ACTUALITY DAG
                       │
                       ▼
                 QP RECEIPT
                       │
          ┌────────────┴─────────────┐
          ▼                          ▼
       SEED0                       SEESAW
 learn execution policy      reprice allocation
          │                          │
          └──────── AGENTCOM ────────┘
```

That is much better than trying to make AgentCom itself a frontier harness.

## Agents API should replace a lot of our soft machinery

OpenAI is now explicitly saying that the Agents API handles the harness they learned from Codex and ChatGPT Work: context management over long sessions, parallel subagents, tool discovery, programmatic tool use, files/code execution, and persistent working environments. Agents can run in an OpenAI-managed sandbox, your infrastructure, or supported sandbox providers. ([OpenAI][1])

So things like:

```text
generic context compaction
generic subagent spawning
generic tool-loop orchestration
long-running agent infrastructure
sandbox lifecycle
generic coding harness
```

are now **REUSE/OpenAI** according to Seesaw.

Our scarce layers stay:

```text
what should the agent pursue?              Seesaw
what exactly counts as success?            Autobuild
what already exists?                       GitGoblin
is the external action authorized?         QP
did reality actually change?               Actuality
what execution policy works best?          Seed0
what project receives resources next?      AgentCom
```

This is a very clean split.

---

# Agents API becomes the worker CPU

A real AgentCom campaign should eventually create a managed Agents API session.

OpenAI's current API allows a session to specify the model, tools, multi-agent settings, vault IDs, environment and initial input. Sessions also have metadata, status, usage, required actions and persistent environments. ([OpenAI Developers][2])

So AgentCom can bind lineage directly:

```json
{
  "metadata": {
    "project": "agentcom-uk",
    "campaign": "lead-reply-v3",
    "contract": "c_8d72...",
    "plan": "p_f109...",
    "policy": "seed0-seeker3"
  }
}
```

The API only allows a limited metadata map, so the complete lineage remains in our event store; these are lookup keys.

Then the actual prompt given to the agent is relatively mundane:

```text
You are executing ContractRoot c_8d72.

Work only on READY requirements.

Use available skills/tools.

When blocked, research and try alternate routes.

You cannot decide whether a requirement is complete.
Completion is external.
```

Most of `agents.md` can become a **Skill**.

OpenAI now has a proper Skills API, and skills are reusable bundles of instructions, examples, scripts and supporting resources. They are also usable across parts of the OpenAI ecosystem. ([OpenAI Help Center][3])

So we could compile:

```text
agent_policy.json
       ↓
OpenAI Skill
       ↓
installed into the Agent environment
```

This means WorkerPolicy versions themselves become deployable objects.

---

# Autobuild should now compile an OpenAI-native BusinessBundle

This is the big move.

Not:

```text
Plan → Python project
```

but:

```text
BusinessSpec
     ↓
AUTOBUILD
     ↓
BusinessBundle
```

containing:

```text
business.bundle/
├── strategic.json
├── contract.json
├── actuality.json
├── agent/
│   ├── instructions.md
│   ├── agent.json
│   └── environment.json
├── skills/
│   ├── business-operator/
│   └── domain-specific/
├── mcp/
│   ├── company-state.json
│   ├── gitgoblin.json
│   └── qp-gateway.json
├── plugin/
│   ├── app/
│   ├── skills/
│   └── directory/
├── voice/
│   ├── persona.json
│   ├── call-policy.json
│   └── escalation.json
├── security/
│   ├── tool-policy.json
│   ├── data-policy.json
│   └── grants.json
├── telemetry/
│   ├── events.schema.json
│   └── retention.json
└── evals/
    └── actuality/
```

Now an autonomous business is just another compiled deployment target.

---

# OpenAI environments are particularly useful for this

Agents API environment templates can already include:

* files,
* packages,
* network configuration,
* capability directories,
* **Skills**,
* **Plugins**,
* environment values,
* confidential setup commands. ([OpenAI Developers][4])

That is almost absurdly aligned with Autobuild.

We should make:

```text
Autobuild TargetSpec
        ↓
OpenAI EnvironmentTemplate
```

a first-class compiler target.

For example:

```text
PlumberBusinessSpec
         ↓
EnvironmentTemplate

skills:
  plumber-operations
  uk-trade-compliance
  quoting
  customer-service

plugins:
  AgentCom Business Plugin

capabilities:
  /workspace/capabilities/company
  /workspace/capabilities/actuality

MCP:
  cmail
  accounting
  calendar
  qp-gateway

network:
  strict allowlist
```

Then every new agent session starts in the correct business operating environment.

---

# Secrets: OpenAI Vault + QP gateway

Agents API now has **Vaults**, specifically collections of credentials that agent tools can use to authenticate to MCP servers. Sessions can be given selected vault IDs. ([OpenAI Developers][5])

But I would split credentials into two classes.

```text
LOW-CONSEQUENCE / READ CREDENTIALS
→ OpenAI Vault can hold them

CONSEQUENTIAL AUTHORITY
→ keep behind our QP-controlled service
```

For example:

```text
Google Maps lookup token
→ Vault

public company-data API
→ Vault

send company email credential
→ QP MCP gateway

payment key
→ QP gateway

marketplace write credential
→ QP gateway

bank/accounting mutation
→ QP gateway
```

The OpenAI agent never needs the raw write credential.

It only calls:

```text
company.send_email(...)
```

and our MCP server does:

```text
tool proposal
    ↓
QP grant validation
    ↓
scope constraints
    ↓
execute
    ↓
independent readback
    ↓
QP receipt
```

That preserves the architecture even if the model is compromised.

---

# OpenAI approvals fit QP surprisingly well

The Agents SDK currently supports approvals for function tools, MCP tools, nested agents, shell and patch tools; approval can pause execution and resume the same run. Hosted MCP can be configured to require approval always. ([OpenAI GitHub][6])

So externally we can use:

```text
OpenAI approval
```

as a **first safety belt**.

But:

$$
\boxed{\text{OpenAI approval } \neq \text{ QP authority}}
$$

QP remains authoritative.

For a sensitive tool:

```text
Agent decides:
call marketplace.purchase(...)

        ↓

OpenAI:
approval required

        ↓

AgentCom callback:
qp.authorize(action)

        ↓

QP:
grant valid?
scope valid?
budget valid?
asset valid?
fresh?
        ↓
PASS / REFUSE
```

Even better, the MCP service itself should independently enforce QP, because then bypassing the OpenAI approval layer still does nothing.

---

# Telemetry becomes much better if we build directly around OpenAI events

This is another reason I would migrate quickly.

Agents API exposes a live session-event endpoint. The stream currently includes session/turn events, environment lifecycle events, subagent creation/activity/closure, command execution deltas, content/output events and many other event variants. ([OpenAI Developers][7])

So build:

```text
OpenAIEventAdapter
```

immediately.

Every event becomes a normalized AgentCom telemetry record:

```json
{
  "event_id": "...",
  "source": "openai.agents",

  "session_id": "...",
  "turn_id": "...",
  "subagent_id": "...",

  "contract_root": "...",
  "plan_root": "...",

  "event_type": "tool.call",
  "tool": "cmail.send",

  "args_hash": "...",
  "output_hash": "...",

  "guardrail": null,
  "approval": null,

  "tokens": null,
  "latency_ms": null,
  "cost_usd": null,

  "observed_at": "...",

  "qp_receipt": null
}
```

Don't make OpenAI's event schema our permanent schema.

Normalize it.

That means we can later route another agent provider through exactly the same AgentCom telemetry model.

---

# The Agents SDK tracing layer is useful too

Separately, the Agents SDK has built-in tracing for:

```text
turns
agents
model generations
function calls
MCP
guardrails
handoffs
speech-to-text
text-to-speech
custom spans
```

and supports **custom trace processors** to send telemetry somewhere other than, or in addition to, OpenAI's dashboard. ([OpenAI GitHub][8])

So I would export everything to our own:

```text
trajectory/
```

store.

Conceptually:

```text
OPENAI TRACE
     ↓
TraceAdapter
     ↓
TrajectoryEvent
     ↓
AgentCom ledger
```

Then Seed0 gets the full execution trace.

This is exactly the data we wanted.

---

# Voice: one correction — LiveKit isn't OpenAI

There are now two sensible routes.

## Route A — OpenAI-native direct voice

OpenAI released **GPT-Live-1 in the API on September 10**. It is full-duplex, handles interruptions, can delegate deeper reasoning/tool calls to a backend model, and includes telephony support. It provides transcripts and response text natively. ([OpenAI][9])

OpenAI's Realtime API also has direct SIP call handling; there is an endpoint for accepting an incoming SIP call and configuring its realtime session. ([OpenAI Developers][10])

So the most OpenAI-native path is:

```text
phone
 ↓
SIP
 ↓
GPT-Live-1
 ↓
AgentCom backend
 ↓
Agents API / Astra
 ↓
QP tools
```

That's now completely viable.

## Route B — LiveKit transport + OpenAI intelligence

LiveKit is a separate company/open-source realtime framework. It has a first-class OpenAI Realtime integration, and can bridge browser WebRTC / SIP telephony to OpenAI Realtime. ([LiveKit Docs][11])

For **your** use case, LiveKit still has one very compelling advantage:

### recording + media telemetry.

LiveKit Egress can record complete sessions or individual tracks, including an example that puts the AI agent and caller on separate audio channels. ([LiveKit Docs][12])

That is fantastic for AgentCom.

You could store:

```text
call.wav
├── channel L: agent
└── channel R: customer
```

alongside:

```text
transcript.jsonl
toolcalls.jsonl
security.jsonl
qp_receipts.jsonl
turns.jsonl
latency.jsonl
```

Then run security monitors in real time:

```text
caller audio
   ↓
transcript
   ↓
┌─────────────────────────────┐
│ prompt injection monitor    │
│ secret/PII monitor          │
│ social-engineering monitor  │
│ action-risk monitor         │
│ fraud/anomaly monitor       │
└─────────────────────────────┘
   ↓
security events
```

Critically, those monitors can inform decisions, but QP remains the enforcement layer.

For call recording, implement explicit consent/retention policy appropriate to the relevant jurisdiction; don't assume one recording rule globally.

---

# GPT-Live-1 should be the receptionist, not necessarily the brain

OpenAI's own architecture for GPT-Live-1 explicitly supports delegating deeper reasoning/actions to a backend model while keeping the spoken conversation going. ([OpenAI][9])

That maps perfectly to this:

```text
                    PHONE
                      │
                      ▼
                GPT-LIVE-1
            low latency conversation
                      │
         simple       │       deep/action
         answer       │
             ┌────────┴─────────┐
             ▼                  ▼
          Live reply        AgentCom
                                │
                                ▼
                          Agents API
                         GPT-6 Astra
                                │
                          tools/subagents
                                │
                                ▼
                               QP
```

So a customer can hear:

> “Yep, I can check that for you.”

while the backend agent is doing the heavy work.

This is basically the SparkAgent/Cmail vision with much less custom infrastructure.

---

# ChatGPT plugins then become a deployment surface, not another system

The plugin ecosystem has also changed substantially.

As of July 9, OpenAI says the **Plugin Directory is the primary place to discover workflow capabilities across ChatGPT and Codex**. Plugins may package Skills, connected Apps and app templates. ([OpenAI Help Center][14])

The Apps SDK is based on MCP, can provide UI inside ChatGPT, and can connect directly to an existing backend. ([OpenAI Help Center][15])

So our source should become:

```text
CAPABILITY
    │
    ├── MCP
    │     ├── Agents API
    │     └── ChatGPT App
    │
    ├── Skill
    │     ├── Agents API
    │     ├── ChatGPT
    │     └── Codex
    │
    └── Plugin
          └── Plugin Directory
```

Not four implementations.

One capability.

Four surfaces.

---

# The really exciting endstate: compile an autonomous business

Imagine:

```yaml
business:
  vertical: plumber
  geography: UK

  identity:
    domain: ...
    email: ...
    phone: ...

  goals:
    - maximize profitable booked jobs

  capabilities:
    - answer_phone
    - answer_email
    - qualify_lead
    - quote
    - book
    - invoice
    - request_review

  authority:
    email.send:
      autonomous: true

    booking.create:
      autonomous: true

    quote.send:
      max_value_gbp: 1000

    refund:
      human: true

  channels:
    voice: true
    chatgpt_plugin: true
    web: true

  actuality:
    booked_job:
      ...
```

Autobuild emits:

```text
OpenAI Agent
OpenAI environment
OpenAI skills
MCP backend
ChatGPT plugin
phone agent
QP policies
Actuality validators
telemetry
Seed0 experiment configuration
```

Now you have:

$$
\boxed{\text{BusinessSpec} \rightarrow \text{running agent-native company}}
$$

That feels like the natural endgame of AgentCom.

---

# I would revise our canonical architecture accordingly

```text
             SEESAW
      strategic allocation
                │
                ▼
             AGENTCOM
      economic control plane
                │
                ▼
            AUTOBUILD
      proof/business compiler
                │
       ┌────────┼─────────┐
       │        │         │
       ▼        ▼         ▼
   OpenAI    GitGoblin   QP
   Agent     prebuild   authority
   Bundle                │
       │                 │
       ▼                 │
   AGENTS API ─── MCP ───┘
       │
       ├── ChatGPT Plugin
       ├── GPT-Live voice
       ├── web
       └── background agent
       │
       ▼
      REALITY
       │
       ▼
    Actuality
       │
       ▼
       QP
       │
       ▼
   Trajectories
       │
   ┌───┴────┐
   ▼        ▼
 SEED0    SEESAW
 learns    reprices
 execution economics
```

OpenAI owns:

```text
cognition
context
subagents
tool selection
sandbox
voice intelligence
surface distribution
```

We own:

```text
strategy
contracts
authority
actuality
capability assets
customer state
economic outcomes
trajectory data
cross-project learning
```

That is a much stronger Seesaw position.

---

## What I would build next

I would stop `autobuild4` and make the next experiment **`openai-native-0`**:

1. Compile `agentcom-uk` into one Agents API environment/session.
2. Install one AgentCom Skill generated from `agents.md`.
3. Expose **GitGoblin and QP as MCP servers**.
4. Stream every Agents API session event into the AgentCom trajectory schema.
5. Make exactly one non-consequential Cmail read operation work.
6. Add one consequential operation behind `QP → approval → execute → independent readback`.
7. Then attach GPT-Live-1; if recordings are a priority, use LiveKit as the media/SIP/egress layer.
8. Once the same backend works over voice, generate its ChatGPT Apps SDK/Plugin surface from the same MCP + Skill definitions.

The acceptance condition should be wonderfully small:

$$
\boxed{
\text{one OpenAI Agent session}
\rightarrow
\text{one MCP action}
\rightarrow
\text{one QP-authorized real transition}
\rightarrow
\text{one independent readback}
\rightarrow
\text{one full trajectory}
}
$$

Once that works, we have the substrate for the autonomous-business factory.

[OpenAI Agents API announcement](https://openai.com/index/introducing-the-agents-api/?utm_source=chatgpt.com)
[OpenAI Apps SDK overview](https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk?utm_source=chatgpt.com)

Because this API stack was released only days ago and will change quickly in beta, I can monitor the Agents API, GPT-Live, and Plugin/Apps SDK docs for breaking changes that affect this architecture.

[1]: https://openai.com/index/introducing-the-agents-api/ "Introducing the Agents API | OpenAI"
[2]: https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/subresources/sessions/methods/create?utm_source=chatgpt.com "Create an agent session | OpenAI API Reference"
[3]: https://help.openai.com/en/articles/20001066?utm_source=chatgpt.com "Skills in ChatGPT | OpenAI Help Center"
[4]: https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/subresources/environments/subresources/templates/methods/create?utm_source=chatgpt.com "Create an agent environment template | OpenAI API Reference"
[5]: https://developers.openai.com/api/reference/typescript/resources/beta/subresources/agents/subresources/vaults/methods/create?utm_source=chatgpt.com "Create a vault | OpenAI API Reference"
[6]: https://openai.github.io/openai-agents-python/human_in_the_loop/?utm_source=chatgpt.com "Human-in-the-loop | OpenAI GitHub"
[7]: https://developers.openai.com/api/reference/python/resources/beta/subresources/agents/subresources/sessions/subresources/events/methods/stream?utm_source=chatgpt.com "Stream agent session events | OpenAI API Reference"
[8]: https://openai.github.io/openai-agents-python/tracing/?utm_source=chatgpt.com "Tracing - OpenAI Agents SDK"
[9]: https://openai.com/index/introducing-gpt-live-1-in-the-api/?utm_source=chatgpt.com "Build more native voice experiences with GPT‑Live‑1 in the API | OpenAI"
[10]: https://developers.openai.com/api/reference/python/resources/realtime/subresources/calls/methods/accept?utm_source=chatgpt.com "Accept call | OpenAI API Reference"
[11]: https://docs.livekit.io/agents/models/realtime/plugins/openai/?utm_source=chatgpt.com "OpenAI Realtime API plugin guide | LiveKit Documentation"
[12]: https://docs.livekit.io/transport/media/ingress-egress/egress/?utm_source=chatgpt.com "Egress overview | LiveKit Documentation"
