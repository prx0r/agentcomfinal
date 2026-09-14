# Architecture

## Five layers

```text
L0 STRATEGY       Seesaw
L1 SPECIFICATION  autobuild
L2 PREBUILD       GitGoblin
L3 RUNTIME        QP / A-COM
L4 EXECUTION      A-Task / workers
```

### L0 — Seesaw

Produces `StrategicSpec`: durable scarcity, owned layer, commodity layer, lab-attack thesis, positive-AI-beta claim, falsifiers, and minimum moat-producing outcome.

### L1 — autobuild

Compiles a plan into `TargetSpec`: capabilities, atomic requirements, evidence contracts, deterministic validators, completion circuits, authority requirements, and economic outcome circuits.

### L2 — GitGoblin

Receives a `PrebuildRequest` and returns `ReusePlan`: candidates, provenance, license/rights, quality, fit, integration cost, action (`REUSE | BUY | BUILD | BLOCK`), and uncovered delta.

### L3 — QP / A-COM

QP stays domain blind. Autobuild maps its objects into QP concepts:

```text
Target claim       -> CLAIM
validator output   -> EVIDENCE
work unit          -> TASK
worker attempt     -> RUN
acceptance program -> GATE
external authority -> GRANT
accepted change    -> TransitionReceipt
```

QP remains authoritative for settlement.

### L4 — A-Task

A-Task receives one goal, indexed acceptances, tasks covering indices, rerunnable evidence declarations, and validator commands. Workers never declare completion.

## Technical vs economic success

Technical completion and economic validation are separate.

```text
TechnicalComplete = AND(all hard requirements)
EconomicValidated = Circuit(real outcomes)
```

A product can be technically perfect and economically false.

## Frozen success semantics

```text
ContractRoot = sha256(canonical(normative_success_projection))
PlanRoot     = sha256(canonical(full_TargetSpec_with_reuse_plan))
LineageRoot  = sha256(canonical(strategy_and_compiler_ancestry))
```

Every task/receipt references the frozen `ContractRoot` plus the current `PlanRoot`. Changing a library, model, worker, or reuse route changes `PlanRoot` but **must not** change `ContractRoot`. Changing acceptance semantics creates a new `ContractRoot` and exact ChangeSet. This makes A/B replay across implementation routes valid.

## Additive runs

Every run emits both:

```text
OperationalResult
KnowledgeContribution
```

A failed operational run can still improve the system if it adds durable structured information.
