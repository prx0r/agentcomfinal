# agentcomcriteria.md — binary rubric for the factory (seed0 style)

Distilled from `agentcomidea.md` + seed0 `criteria/criteria1.md` convention:
one row per claim, each with the exact test/demo/review that proves it.
No attempt is promoted until every row in its scope is green.
Owner `machine` = checked by `review/check.py`; `human` = judged at review.

## B — boundaries (idea §1)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| B1 | `CANONICAL.md` exists and names exactly one owner per responsibility (seesaw / agentcom / autobuild / gitgoblin / qp / atask) | review `test_canonical_single_owner` | machine |
| B2 | AgentCom creates no QP object ids and no QP receipts (references only) | review `test_no_qp_fabrication` + grep `TransitionReceipt` constructors absent | machine |
| B3 | Seesaw code paths execute no work and prove no technical completion | review: seesaw module has no executor/prover imports | human |
| B4 | An AgentCom `PROVEN` display never counts as canonical truth without a verified QP receipt | test `test_proven_requires_receipt` | machine |

## P — packages (idea §2–3)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| P1 | v3 is the single canonical runtime shell; campaign + v2 runtimes demoted (reference/archive, not live) | review `test_canonical_packages` | machine |
| P2 | autobuild-v0.2 is the canonical compiler; ab1+ contract shape compatible with its TargetSpec | test `test_contract_shape` | machine |
| P3 | plugin-canonical is a domain pack (`domainpacks/chatgpt-plugin`), not root ontology | review: no root schema imports plugin kit | human |
| P4 | Checkpoint ontology (CampaignSpec/Checkpoint/EvidenceContract/Validator/DAG) preserved from campaign-control-plane | review `test_checkpoint_ontology_present` | machine |

## T — truth demotion (idea §4)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| T1 | No live canonical state advances without a verified QP receipt | test `test_no_receipt_no_advance` | machine |
| T2 | Local attestation/HMAC kept as reference tests only, never on the proof path | review: attestation module path contains `reference` | machine |
| T3 | qp_adapter only translates (detect version, map request, map reference); zero business logic | review `test_adapter_thin` | human |

## C — contracts + lineage (idea §5–6)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| C1 | `contracts/` holds the 12 orchestration schemas and none of QP's 7 objects | review `test_contracts_no_qp_overlap` | machine |
| C2 | Lineage chain StrategicRoot→CampaignRoot→ContractRoot→PlanRoot→RunRoot→Receipt→OutcomeRoot computable, hashes stable | test `test_lineage_hashes` | machine |
| C3 | Swapping implementation changes PlanRoot, preserves ContractRoot | test `test_contract_invariant` | machine |
| C4 | Worker-edited acceptance forces a new ContractRoot (old task cannot adopt it) | test `test_acceptance_edit_new_contract` | machine |

## W — worlds, circuits, evidence (idea §12–15)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| W1 | WORLD_SELECT scores cost vs information and never graduates a market claim from simulation | test `test_world_select_no_sim_graduation` | machine |
| W2 | Four evidence ceilings (A_TRUTH/B_DEMAND/C_ECONOMIC/D_SCARCE_STATE) enforced per claim class | test `test_evidence_ceiling` | machine |
| W3 | TechnicalCircuit TRUE + EconomicCircuit FALSE reads as thesis failure, never success | test `test_circuits_separate` | machine |
| W4 | Strategy stats admit only `qp.verify(receipt)==PASS` outcomes, not `receipt_ref != null` | test `test_verified_outcomes_only` | machine |
| W5 | Missing outcome readback yields outcome UNKNOWN even when technical state passes | test `test_missing_readback_unknown` | machine |

## H — humans, runs, primitives (idea §16–18)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| H1 | Exactly two human objects exist: StrategicQuestion (agentcom) and execution H-task (atask); one surface renders both | review `test_two_queues` | machine |
| H2 | Every run emits OperationalResult + KnowledgeContribution; failures retained and queryable | test `test_run_dual_output` | machine |
| H3 | Promotion OBSERVATION→…→PROMOTED_PRIMITIVE is itself a governed transition with receipt | test `test_promotion_receipt` | machine |
| H4 | `data/primitives/` entries carry provides/requires/schemas/validator/evidence_level/implementations/performance/promotion_receipt | review `test_primitive_shape` | machine |

## G — grants + adversarial (idea §8, §24)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| G1 | Consequential action without a grant is REFUSED | test `test_no_grant_refused` | machine |
| G2 | Wrong-scope grant (email.send vs marketplace.purchase) is REFUSED | test `test_wrong_scope_refused` | machine |
| G3 | Worker `source=live ok=true` self-attestation yields NOT PROVEN | test `test_no_self_proof` | machine |
| G4 | GitHub commits alone yield CODE_PRESENT, never PROVEN | test `test_commits_not_proof` | machine |
| G5 | Receipts are signed (attempt ≥2) and tampered copies fail verification | test `test_signed_tamper_fails` | machine |

## ACT — actuality axiom (actuality.md; attempt ≥3)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| ACT1 | No log, no claim: uncovered acceptance never passes | test `test_claim_without_log_nogo`, `test_uncovered_index_nogo` | machine |
| ACT2 | Probes emit observations only; only judges decide (probe verdicts ignored) | test `test_disallowed_command_refused`, probe-lies red-team | machine |
| ACT3 | Judges are pure/total/terminating: malformed evidence and eval errors yield UNKNOWN, judges never raise | test `test_cel_unknowns`, `test_schema_l0` | machine |
| ACT4 | DAG is AND over TRUE/FALSE/UNKNOWN leaves; UNKNOWN blocks progress | test `test_dag_unknown_blocks`, `test_dag_false_wins` | machine |
| ACT5 | Consequential actions require independent postcondition readback; missing readback is UNKNOWN, mismatch is FALSE | test `test_readback` | machine |
| ACT6 | A(C,E)=1 records carry claim/actuality/contract/evidence/validator roots + environment + proof class | test `test_actuality_record` | machine |
| ACT7 | Agent telemetry is re-executed at judgment: forged/mismatched lines fail, planted verdicts ignored, secrets refused | tests `test_forged_line_nogo` … `test_secret_evidence_refused`, `test_planted_verdict_ignored` | machine |

## D — done (idea §21, §27)

| ID | Statement | Verification | Owner |
|---|---|---|---|
| D1 | Simulated pilot chain A–P runs end-to-end (sandbox action + readback) with full lineage | demo `GO.sh` exits 0, lineage command traces all roots | machine |
| D2 | Scheduler invariant holds: infrastructure never outbids an asset campaign for a scarce permission | test `test_scheduler_invariant` | machine |
| D3 | Worker model is replaceable without changing the hard system (same contracts, same receipts shape) | review: no model id inside contract/receipt bytes | human |
| D4 | Real pilot DONE = 12 linked artifacts (campaign→…→reallocation), else IMPLEMENTED_UNVERIFIED | human sign-off against lineage trace | human |

Scope rule (from seed0): out-of-scope items are logged in the attempt README, never gated. Attempt 1 scope = B4, C2(partial), G5(unsigned→deferred to attempt 2), W5, H2(partial). Attempt 2 scope = G1, G2, G5, T1. Attempt 3 scope = ACT1–ACT7, A-log A1–A6 (criteria A-section folded into ACT), chain no-regression.
