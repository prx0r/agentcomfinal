"""Review autobuild1 vs its criteria scope. Writes VERDICT.json + NEXT.md."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "autobuild0"))
import reviewkit  # noqa: E402

ATTEMPT = "autobuild1"
ADIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPE = ["B4", "C2-partial", "W5-partial", "H2-partial", "G5-deferred",
         "suite-green"]


def main():
    tests = reviewkit.run_pytest(ADIR)
    files = reviewkit.check_required_files(ADIR, [
        "SPEC.md", "VALIDATION.md", "VALIDATION.json",
        "src/ab1/canonical.py", "src/ab1/specgate.py", "src/ab1/seesaw.py",
        "src/ab1/gates.py", "src/ab1/receipts.py", "src/ab1/store.py",
        "src/ab1/cli.py", "tests/test_ab1.py",
        "examples/breadup_plan.json", "examples/breadup_evidence.json"])
    bans = reviewkit.grep_ban_py(ADIR, [
        "TransitionReceipt(", "qp_claim", "CLAIM-", "verify_grant("])
    rows = [
        reviewkit.row("B4",
                      "PASS" if not bans else "FAIL",
                      "no QP fabrication in src" if not bans
                      else "banned hits: %s" % bans),
        reviewkit.row("C2-partial", "PARTIAL",
                      "receipt+chain lineage present; 7-root lineage is ab4+ scope"),
        reviewkit.row("W5-partial", "PARTIAL",
                      "no outcome/readback object in ab1; rule specified in GATES.md L3"),
        reviewkit.row("H2-partial", "PARTIAL",
                      "runs emit receipts; KnowledgeContribution is attempt 5+ scope"),
        reviewkit.row("G5-deferred", "DEFERRED",
                      "receipts unsigned V0 by design; signing is autobuild2"),
        reviewkit.row("suite-green",
                      "PASS" if tests["ok"] and tests["failed"] == 0 else "FAIL",
                      "%s passed, %s failed" % (tests["passed"],
                                                tests["failed"])),
    ]
    if any(not f["ok"] for f in files):
        rows.append(reviewkit.row(
            "files", "FAIL",
            "missing: %s" % [f["path"] for f in files if not f["ok"]]))
    payload = reviewkit.write_verdict(ADIR, ATTEMPT, SCOPE, rows, tests,
                                      files, bans)
    debt = ["C2: full 7-root lineage (ab4)", "W5: outcome/readback + UNKNOWN rule (ab5)",
            "H2: KnowledgeContribution output (ab5)", "G5: signed receipts (ab2)",
            "T1: live canonical gate needs real QP adapter (ab3+)"]
    reviewkit.write_next(ADIR, ATTEMPT, debt,
                         ["autobuild2 scope: G1, G2, G5, T1-simulated (signed receipts + grant gates)",
                          "keep ab1 suite green; ab2 must not regress ab1 criteria"])
    print("overall: %s | tests: %s passed %s failed" % (
        payload["overall"], tests["passed"], tests["failed"]))
    return 0 if payload["overall"] != "FAIL" else 2


if __name__ == "__main__":
    sys.exit(main())
