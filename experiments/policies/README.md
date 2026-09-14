# experiments/policies — execution-policy lanes (Seed0 method)

Runner: `lanes.py` (`tournament(contract_root, [(name, fn)])` — same
ContractRoot, same gates, gates-first then cost; winner + failure corpus).

| policy id | implementation | status |
|---|---|---|
| policy.direct | inline worker: straight at the requirement | lane-ready (test fakes) |
| policy.seeker3 | `agentcombuild/agentloop` seeker (SEARCH→3→TEST→LOG) | ADAPTED |
| policy.gitgoblin_first | `adapters/gitgoblin.py` prebuild, then direct | lane-ready (local backend) |
| policy.test_first | probe-first: evidence before implementation | stub (ab5+) |
| policy.redteam_first | adversarial cases before happy path | stub (ab5+) |
| policy.repair_first | fix current integration before replacing | stub |
| policy.replace_component | swap component, keep contract | stub |

Rule: no policy is declared best in advance. Lanes race; identical gates
judge; failures bank. Promotion of a policy needs a PromotionReceipt
(`contracts/promotion.schema.json`), never a tournament win alone.
