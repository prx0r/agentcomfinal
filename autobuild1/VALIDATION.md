# ab1 VALIDATION

Criteria (from DEV_PLAN §6), each mapped to tests + a manual check.

1. Determinism — `test_determinism`: two builds, same `--now` → identical bytes.
2. Fail closed — `test_unknown_gate`, `test_raising_gate`, `test_missing_evidence_gate`,
   `test_fail_keeps_state`: FAIL verdicts, state unchanged.
3. No trust-only work — `test_plan_rejects_missing_acceptance`,
   `test_plan_rejects_trust_only_feature`: specgate refuses.
4. Receipts verify — `test_receipt_pass`, `test_tamper_fails`: id recomputed
   from bytes; tampered copy fails.
5. Chain verifies — `test_store_chain`, `test_store_evil_line`: append-only
   replay; tampered line fails loudly.
6. Seesaw sane — `test_seesaw_ordering`, `test_substitutable_never_own`,
   `test_gate_threshold`: moat ordering holds; substitutable never OWN.
7. Suite green — full `pytest tests/ -q` pass recorded below.

Manual: `PYTHONPATH=src python3 -m ab1.cli demo` prints receipt + report JSON.
