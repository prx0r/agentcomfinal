# Adapters

Autobuild defines contracts; it does not copy upstream repos.

## QP
`autobuild.bridges.qp_bridge(TargetSpec)` emits claim/task candidates, deterministic gate specs and grant templates. Local integration should pass these through `/qp` constructors and gate registration. QP stays authoritative for canonical state, gate hashes, grants, receipts and settlement.

## A-Task
`autobuild.bridges.atask_bridge(TargetSpec)` emits one goal, indexed acceptance, bounded tasks, rerunnable evidence and validator specs. Local integration should create the real queue through `/atask`. A-Task stays authoritative for stoplight/proof/DONE.

## GitGoblin
`autobuild.prebuild.make_request(TargetSpec)` emits structured component-search jobs. GitGoblin should provide tools such as `prebuild_analyse`, `find_existing_capability`, `compare_repos`, `reuse_plan`, `missing_delta` and return a `ReusePlan`.
