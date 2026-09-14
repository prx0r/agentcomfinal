# LEGO / accretive system model

The long-term asset is not a pile of generated code. It is a growing library of typed, measured transformations.

Every reusable brick declares:

```json
{
  "requires": ["item.observation"],
  "provides": ["listing.draft"],
  "transform": "...",
  "validator": "..."
}
```

The primitive id is content-derived from its semantic signature. Project-local names do not define identity.

## Why this matters

A build becomes a graph of auditable transformations:

```text
state/capability A
-> primitive P1
-> state/capability B
-> primitive P2
-> state/capability C
```

Each brick can independently accumulate:
- success/failure counts;
- cost/latency;
- environments where it works;
- known incompatibilities;
- validation fixtures;
- alternatives;
- downstream outcomes.

Future optimization can rearrange bricks without changing target success semantics.

## Promotion rule

A pattern starts project-local. Repeated independent use makes it a promotion candidate. Promotion must eventually settle through QP rather than by agent assertion.

## Design consequence

The system should optimize transformations, not prose. A good run either:
- proves a target;
- falsifies a route;
- improves a primitive;
- discovers a reusable component;
- adds an outcome;
- or sharpens a gate.
