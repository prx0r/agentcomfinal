# Handoff to coding agent

Canonical name: `autobuild`.

## Keep responsibilities separate
- `/qp`: cryptographic truth/authority runtime.
- `/atask`: execution queue + deterministic stoplight.
- `/gitgoblin`: prebuild archaeology/reuse oracle.
- `autobuild`: plan -> target graph compiler + additive knowledge model.

## First integration work
1. Thin QP adapter from `qp_bridge.json` to current `/qp` constructors.
2. Thin A-Task adapter from `atask_bridge.json` to `/atask` goal/task creation.
3. GitGoblin prebuild output compatible with `fixtures/prebuild_response.json`.
4. Do not fork those repos into autobuild.
5. Version-detect their current local contracts.
6. Preserve QP as sole authority for cryptographic settlement.

## Core acceptance

```text
same structured input -> same ContractRoot + PlanRoot
workers cannot alter acceptance without new ContractRoot
missing evidence -> UNKNOWN
only prebuild missing delta -> build tasks
failed runs survive in ledger
exact duplicate knowledge does not inflate dataset
QP bridge references frozen ContractRoot and exact execution PlanRoot
A-Task bridge declares rerunnable proof
```
