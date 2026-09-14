"""Review autobuild3: every criterion cites executable gates (Rule 0)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild0"))
import reviewkit  # noqa: E402

ATTEMPT = "autobuild3"
T = "tests/test_ab3.py::"


def _env():
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([
        os.path.join(ADIR, "..", "autobuild1", "src"),
        os.path.join(ADIR, "src")])
    return env


def main():
    rows = [
        {"id": "honest-run-go",
         "tests": [T + "test_honest_run_go"]},
        {"id": "no-log-no-claim",
         "tests": [T + "test_claim_without_log_nogo",
                   T + "test_uncovered_index_nogo",
                   T + "test_ref_only_insufficient"]},
        {"id": "forgery-and-mismatch-fail",
         "tests": [T + "test_forged_line_nogo",
                   T + "test_command_mismatch_nogo",
                   T + "test_nonzero_exit_nogo",
                   T + "test_disallowed_command_refused_and_harmless",
                   T + "test_planted_verdict_ignored",
                   T + "test_stale_flagged"]},
        {"id": "refusals-hold",
         "tests": [T + "test_unknown_task_refused",
                   T + "test_bad_index_refused",
                   T + "test_secret_evidence_refused",
                   T + "test_covers_checked"]},
        {"id": "validator-contract",
         "tests": [T + "test_validator_false_nogo",
                   T + "test_validator_crash_nogo",
                   T + "test_validator_bad_json_nogo",
                   T + "test_validator_timeout_nogo"]},
        {"id": "judges-total",
         "tests": [T + "test_cel_basics", T + "test_cel_unknowns",
                   T + "test_schema_l0"]},
        {"id": "dag-semantics",
         "tests": [T + "test_dag_all_true", T + "test_dag_false_wins",
                   T + "test_dag_unknown_blocks", T + "test_actuality_record",
                   T + "test_readback", T + "test_registry",
                   T + "test_probe_verdict_ignored",
                   T + "test_true_validator_cannot_excuse_gap"]},
    ]
    rows, overall = reviewkit.verify_rows(ADIR, _env(), rows)
    tests = {"ok": overall == "PASS", "passed": 0, "failed": 0, "tail": []}
    payload = reviewkit.write_verdict(ADIR, ATTEMPT,
                                      [r["id"] for r in rows], rows, tests,
                                      [], [])
    reviewkit.write_next(ADIR, ATTEMPT, [], ["frozen history; see core/"])
    print("overall: %s" % payload["overall"])
    return 0 if payload["overall"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
