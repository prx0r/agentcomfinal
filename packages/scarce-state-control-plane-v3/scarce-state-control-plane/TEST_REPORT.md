# v3 test report — 2026-09-14

## Automated checks

- Unit tests: **32/32 PASS**
- Campaign graph: **ACYCLIC**
- Behavioral checkpoints: **156**
- Fixture validator contracts: **156/156 PASS**
- Live `PROVEN` created from fixtures/self-report: **0**
- JSON files: syntax validated
- Python modules: byte-compiled successfully
- Dashboard JavaScript: `node --check` PASS
- API smoke endpoints: **7/7 PASS**

## Important invariant tests

- A self-reported live `ok=true` event cannot produce `PROVEN`.
- Simulation has `SIMULATION_ONLY` proof state and no canonical effect.
- Simulation successes do not promote a strategy family.
- Resolved real experiment outcomes require an external receipt reference.
- Single-capacity resource constraints cannot be double-allocated.
- Infrastructure cannot outbid an asset campaign for an external experiment slot.
- Seesaw Market Lab is present as the explicit calibration-lab exception.
- Invalid `debugging` H-tasks are rejected.
- Bounded H-task choices reject answers outside the supplied options.
- Repo drift/activity never proves user-visible behavior.

## Current empty-state behavior

The package intentionally ships with:

- zero real experiment outcomes in `experiment_runs.jsonl`;
- zero open H-tasks;
- zero acquired scarce assets in the canonical asset ledger.

Fixtures test the machinery only. They do not bootstrap fake business evidence.
