# ab3 VALIDATION

Scope: criteria A1–A6 + chain no-regression.

| criterion | test |
|---|---|
| A1 no log, no claim | `test_claim_without_log_nogo`, `test_empty_log_nogo` |
| A2 agent never judges (re-execution) | `test_honest_run_go`, `test_command_mismatch_nogo`, `test_nonzero_exit_nogo`, `test_disallowed_command_refused`, `test_planted_verdict_ignored` |
| A3 unknown task refused | `test_unknown_task_refused`, `test_bad_index_refused` |
| A4 secrets refused | `test_secret_evidence_refused`, `test_token_value_refused` |
| A5 validator contract | `test_validator_false_nogo`, `test_validator_crash_nogo`, `test_validator_bad_json_nogo`, `test_validator_timeout_nogo` |
| A6 coverage complete | `test_uncovered_index_nogo`, `test_ref_only_insufficient` |
| forgery | `test_forged_line_nogo`, `test_stale_flagged` |
| chain no-regression | ab1 17/17 + ab2 13/15? no — 15/15 via GO.sh; review runs both |

Manual: `PYTHONPATH=../autobuild1/src:src python3 -m ab3.cli demo` → GO.
