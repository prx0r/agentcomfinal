"""Review autobuild2: every criterion cites executable gates (Rule 0)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild0"))
import reviewkit  # noqa: E402

ATTEMPT = "autobuild2"
T = "tests/test_ab2.py::"


def _env():
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([
        os.path.join(ADIR, "..", "autobuild1", "src"),
        os.path.join(ADIR, "src")])
    return env


def main():
    rows = [
        {"id": "grant-matrix-fail-closed",
         "tests": [T + n for n in (
             "test_grant_expired", "test_grant_wrong_capability",
             "test_grant_unknown_constraint", "test_grant_over_limit",
             "test_grant_predicate_false", "test_grant_unsigned",
             "test_grant_amount_unknown_denied")]},
        {"id": "consequential-requires-grant",
         "tests": [T + n for n in (
             "test_consequential_without_grant_refused",
             "test_wrong_scope_refused",
             "test_unscoped_consequential_refused")]},
        {"id": "signatures-verify",
         "tests": [T + n for n in (
             "test_roundtrip", "test_signed_build_verifies",
             "test_tamper_sig_fails")]},
        {"id": "no-regression-ab1",
         "tests": [T + "test_ab1_still_green"]},
    ]
    rows, overall = reviewkit.verify_rows(ADIR, _env(), rows)
    tests = {"ok": overall == "PASS", "passed": 0, "failed": 0, "tail": []}
    bans = reviewkit.grep_ban_py(ADIR, ["TransitionReceipt("])
    if bans:
        rows.append({"id": "no-qp-fabrication", "status": "FAIL",
                     "note": "hits: %s" % bans, "tests": [], "results": []})
        overall = "FAIL"
    payload = reviewkit.write_verdict(ADIR, ATTEMPT,
                                      [r["id"] for r in rows], rows, tests,
                                      [], bans)
    reviewkit.write_next(ADIR, ATTEMPT, [], ["frozen history; see core/"])
    print("overall: %s" % payload["overall"])
    return 0 if payload["overall"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
