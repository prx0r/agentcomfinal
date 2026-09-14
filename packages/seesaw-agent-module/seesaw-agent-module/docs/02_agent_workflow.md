# 2. Autonomous Agent Workflow

## 2.1 Inputs

Seesaw accepts:

### A. Disruptive event
Example:
- new frontier model;
- OpenAI platform feature;
- new protocol;
- regulatory change;
- robotics breakthrough;
- energy price shift;
- marketplace API;
- new OSS capability.

### B. Project state
- project thesis;
- current owned assets;
- dependencies;
- feature backlog;
- users/revenue;
- trajectory data;
- permissions;
- physical state.

### C. Evidence
- GitHub;
- product announcements;
- prices;
- usage traces;
- customer behavior;
- competitor behavior;
- API/platform docs;
- revenue data.

## 2.2 Agent steps

```text
STEP 1: Parse event
- capability delta
- cost delta
- reliability delta
- access delta

STEP 2: Map constraints
- loosened
- tightened
- newly binding
- destroyed

STEP 3: Reprice scarcity classes
- cognition
- compute
- memory
- power
- data
- physical execution
- authority
- trust
- verification
- distribution
- network liquidity

STEP 4: Re-score projects
- what became commodity?
- what became more valuable?
- what remains external?

STEP 5: Re-score every feature
- OWN
- BUILD
- REUSE
- BUY
- VALIDATE
- WATCH
- DROP

STEP 6: GitHub archaeology for every REUSE candidate
- search existing implementation
- compare maturity/license/security
- integrate best component
- avoid rebuilding

STEP 7: Design proprietary state loop
For each OWN/BUILD feature:
state_t -> action_t -> outcome_t+1 -> stored trajectory

STEP 8: Define falsifier
No strategic claim ships without a measurable falsifier.

STEP 9: Allocate hours/money
Choose work maximizing marginal strategic value per unit cost.

STEP 10: Observe outcome and update
Every real outcome becomes evidence.
```

## 2.3 Agent output contract

Every run should emit:

```json
{
  "event": {},
  "constraint_deltas": [],
  "project_updates": [],
  "feature_actions": [],
  "reuse_searches": [],
  "experiments": [],
  "falsifiers": [],
  "new_proprietary_state_to_capture": []
}
```

## 2.4 "Steal vs build" rule

Use the term **REUSE**, not theft.

For code/components:

```text
If it is commodity:
  search GitHub / official SDK / API first

If reusable:
  integrate subject to license/security

If missing:
  build only missing delta

If proprietary advantage requires ownership:
  own state, not boilerplate
```

The agent should be penalized for unnecessary code.

Suggested objective:

\[
Utility =
StrategicValue
+ EvidenceGain
- NewCode
- Maintenance
- SecuritySurface
- PlatformDependence
\]

## 2.5 Continuous mode

Seesaw can run periodically:

```text
new event detected
→ update constraint graph
→ compare against last project scores
→ only alert if decision changes
```

Example alert:

```text
EVENT:
OpenAI ships native company-email agent.

CHANGE:
Cmail generic drafting/routing moat collapses.

KEEP:
verified-domain identity, sending authority, deliverability history,
consent state, reply outcomes.

ACTION:
DROP generic composer UI.
OWN identity + permission + outcome ledger.
REUSE OpenAI cognition layer.
```

