"""Review agentloop: every criterion cites executable gates (Rule 0)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild0"))
import reviewkit  # noqa: E402

ATTEMPT = "agentloop"
T = "tests/test_loop.py::"
TL = "tests/test_tracing_live.py::"


def _env():
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([
        os.path.join(ADIR, "..", "autobuild1", "src"),
        os.path.join(ADIR, "src")])
    return env


def main():
    rows = [
        {"id": "records-enforced-shape",
         "tests": [T + n for n in (
             "test_good_record_validates", "test_next10_count_enforced",
             "test_visionary_required", "test_working_needs_validation",
             "test_failure_needs_fixture", "test_impact_range",
             "test_append_rejects_and_roundtrips")]},
        {"id": "seeker-honest-and-logged",
         "tests": [T + n for n in (
             "test_seeker_picks_winner_and_logs_all",
             "test_seeker_all_fail_honest",
             "test_seeker_backend_error_recorded",
             "test_seeker_validator_raise_captured",
             "test_attempts_measured", "test_holdout_opacity",
             "test_causes_cited_by_candidates")]},
        {"id": "research-backends-behave",
         "tests": [T + n for n in (
             "test_sim_backend_deterministic",
             "test_escalate_stops_early_and_defers_human",
             "test_research_record_shape")]},
        {"id": "compiler-compounds",
         "tests": [T + n for n in (
             "test_compile_banks_20_by_run4",
             "test_compile_merges_leaderboard",
             "test_tags_deterministic", "test_priority_outranks_motion",
             "test_cluster_and_scope_guard",
             "test_memory_view_covers_bank")]},
        {"id": "policy-knowledge-blocker-typed",
         "tests": [T + n for n in (
             "test_policy_generates_projections", "test_knowledge_ledger",
             "test_blocker_lifecycle")]},
        {"id": "intel-built-from-data",
         "tests": [T + "test_intel_built_from_data"]},
        {"id": "telemetry-dual-custody",
         "tests": [T + n for n in (
             "test_trace_id_shape", "test_mirror_export_shape",
             "test_scrub_defense_in_depth",
             "test_sensitive_io_dropped_by_default",
             "test_binding_and_degraded_mode",
             "test_degraded_without_sdk",
             "test_verdicts_pass_through_unredacted",
             "test_usage_record_unknowns_null",
             "test_reconcile_matched_and_divergent")]},
    ]
    rows, overall = reviewkit.verify_rows(ADIR, _env(), rows)
    live = reviewkit.run_file_summary(ADIR, _env(),
                                      "tests/test_tracing_live.py")
    if live["failed"]:
        rows.append({"id": "live-provider-path", "status": "FAIL",
                     "note": "live provider tests failed: %s" % live,
                     "tests": [], "results": []})
        overall = "FAIL"
    elif live["passed"]:
        rows.append({"id": "live-provider-path", "status": "PASS",
                     "note": "%d live gates green" % live["passed"],
                     "tests": [], "results": []})
    else:
        rows.append({"id": "live-provider-path", "status": "SKIPPED",
                     "note": "NOT_CONFIGURED: no SDK/key here (%d skipped)"
                     % live["skipped"], "tests": [], "results": []})
    tests = {"ok": overall == "PASS", "passed": 0, "failed": 0, "tail": []}
    payload = reviewkit.write_verdict(ADIR, ATTEMPT,
                                      [r["id"] for r in rows], rows, tests,
                                      [], [])
    reviewkit.write_next(ADIR, ATTEMPT, [],
                         ["policy.seeker3 inside Seed0 lanes; see CANONICAL.md"])
    print("overall: %s" % payload["overall"])
    return 0 if payload["overall"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
