"""Review autobuild1: every criterion cites executable gates (test2.md Rule 0).
Writes VERDICT.json (rendering of gate results) + NEXT.md (debt log)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "autobuild0"))
import reviewkit  # noqa: E402

ATTEMPT = "autobuild1"
ADIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = "tests/test_ab1.py::"


def main():
    env = dict(os.environ)
    rows = [
        {"id": "specgate-refuses-trust-only",
         "tests": [T + "test_plan_rejects_missing_acceptance",
                   T + "test_plan_rejects_trust_only_feature"]},
        {"id": "gates-fail-closed",
         "tests": [T + "test_unknown_gate", T + "test_raising_gate",
                   T + "test_missing_evidence_gate", T + "test_gate_threshold"]},
        {"id": "receipts-verify-and-hold",
         "tests": [T + "test_receipt_pass", T + "test_fail_keeps_state",
                   T + "test_tamper_fails"]},
        {"id": "chain-appends-and-detects",
         "tests": [T + "test_store_chain", T + "test_store_evil_line"]},
        {"id": "determinism-byte-identical",
         "tests": [T + "test_determinism", T + "test_canonical_byte_identical"]},
        {"id": "seesaw-ordering-holds",
         "tests": [T + "test_seesaw_ordering",
                   T + "test_substitutable_never_own", T + "test_ai_exposure"]},
        {"id": "plugin-lint-present",
         "tests": [T + "test_plugin_lint"]},
    ]
    rows, overall = reviewkit.verify_rows(ADIR, env, rows)
    tests = {"ok": overall == "PASS", "passed": sum(
        1 for r in rows if r["status"] == "PASS"), "failed": sum(
        1 for r in rows if r["status"] == "FAIL"), "tail": []}
    bans = reviewkit.grep_ban_py(ADIR, [
        "TransitionReceipt(", "qp_claim", "CLAIM-", "verify_grant("])
    if bans:
        rows.append({"id": "no-qp-fabrication", "status": "FAIL",
                     "note": "banned hits: %s" % bans, "tests": [],
                     "results": []})
        overall = "FAIL"
    payload = reviewkit.write_verdict(ADIR, ATTEMPT,
                                      [r["id"] for r in rows], rows, tests,
                                      [], bans)
    reviewkit.write_next(ADIR, ATTEMPT,
                         ["C2 full lineage now in core/lineage.py",
                          "W5 outcome/readback now in ab3 + canonical gates",
                          "H2 knowledge output now in agentloop",
                          "G5 signing now in ab2; T1 real QP adapter live"],
                         ["no open debt from ab1 scope; frozen history"])
    print("overall: %s" % payload["overall"])
    return 0 if payload["overall"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
