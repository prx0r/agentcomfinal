# 3. How Seesaw Should Shape Projects

## 3.1 Universal architecture

Projects should increasingly resemble:

```text
SCARCE STATE
  |
  +-- proprietary data
  +-- permissions
  +-- real-world supply
  +-- trajectories
  +-- trust
  +-- network state
  |
  v
CAPABILITY KERNEL
  |
  v
ADAPTERS
  +-- ChatGPT plugin
  +-- MCP
  +-- API
  +-- x402
  +-- web UI
  +-- CLI
```

The adapters are replaceable.

The scarce state is not.

## 3.2 Feature hierarchy

### Tier 1 — Own aggressively

Features that accumulate or control:

- authoritative identity;
- action permissions;
- exclusive/live data;
- transaction history;
- state/action/outcome trajectories;
- physical execution;
- marketplace liquidity;
- reputation / verification;
- real customer relationships;
- economic supply.

### Tier 2 — Build selectively

Features necessary to operate the scarce state safely:

- deterministic validators;
- policy/permission engines;
- audit logs;
- settlement/escrow;
- durable event schemas;
- evaluation tied to real outcomes;
- synchronization with external systems.

### Tier 3 — Reuse

Usually commodity:

- generic chat UI;
- auth primitives;
- generic LLM orchestration;
- generic embeddings/vector stores;
- generic MCP servers;
- generic web scraping framework;
- CRUD dashboards;
- billing primitives;
- agent loops;
- generic prompt/eval frameworks;
- ordinary analytics.

### Tier 4 — Avoid as moat

- prompts;
- wrappers;
- generic copilots;
- generic RAG;
- generic summarizers;
- generic "AI for X" UI;
- generic plugin conversion;
- model routing without proprietary outcomes;
- metadata tricks dependent on one host.

## 3.3 Every project needs a trajectory loop

The most valuable default asset is:

\[
(s_t, a_t, s_{t+1}, r_t)
\]

Examples:

### Commerce
product state → listing/creative → clicks/sales → margin

### Security
environment → finding/attack → mitigation → exploit/no exploit

### Email
lead/context → message/action → reply/no reply → conversion

### Voice
call state → conversational action → booking/payment/outcome

### Reselling
item/photo → pricing/listing → time-to-sale → realized margin

### Geo/install-base
location/company → observed equipment → intervention/sale → verified installation

## 3.4 Every project should expose capabilities, not depend on a surface

A project is healthy when:

```text
ChatGPT disappears tomorrow
-> capability still valuable

MCP disappears tomorrow
-> capability still valuable

website disappears tomorrow
-> state + action kernel still valuable
```

That is platform robustness.

