"""Review autobuild3 vs scope ACT1-ACT7 + chain no-regression."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild0"))
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild1", "src"))
sys.path.insert(0, os.path.join(ADIR, "src"))
import reviewkit  # noqa: E402

ATTEMPT = "autobuild3"
SCOPE = ["ACT1", "ACT2", "ACT3", "ACT4", "ACT5", "ACT6", "ACT7",
         "chain-no-regression", "suite-green"]


def main():
    tests = reviewkit.run_pytest(ADIR)
    ab1 = reviewkit.run_pytest(os.path.join(ADIR, "..", "autobuild1"))
    ab2 = reviewkit.run_pytest(os.path.join(ADIR, "..", "autobuild2"))
    files = reviewkit.check_required_files(ADIR, [
        "SPEC.md", "VALIDATION.md", "VALIDATION.json",
        "src/ab3/alog.py", "src/ab3/stoplight.py", "src/ab3/gates3.py",
        "src/ab3/judges.py", "src/ab3/actuality.py", "src/ab3/readback.py",
        "src/ab3/registry.py", "src/ab3/cli.py", "src/ab3/demo_worker.py",
        "tests/test_ab3.py", "examples/lead3_plan.json",
        "validators/send-lead-reply.py", "validators/registry.json"])
    bans = reviewkit.grep_ban_py(ADIR, [
        "TransitionReceipt(", "qp_claim", "import qp", "from qp import",
        "subprocess.run([\"rm", "os.system", "re:\\beval\\s*\\(",
        "re:\\bexec\\s*\\("])
    rows = [
        reviewkit.row("ACT1-ACT7",
                      "PASS" if tests["ok"] and tests["failed"] == 0 else "FAIL",
                      "%s passed, %s failed (27-test axiom matrix)"
                      % (tests["passed"], tests["failed"])),
        reviewkit.row("chain-no-regression",
                      "PASS" if ab1["ok"] and ab2["ok"] else "FAIL",
                      "ab1 %s/ab2 %s suites green"
                      % (ab1["passed"], ab2["passed"])),
        reviewkit.row("suite-green",
                      "PASS" if tests["ok"] else "FAIL",
                      "%s passed" % tests["passed"]),
        reviewkit.row("no-qp-fabrication",
                      "PASS" if not bans else "FAIL",
                      "clean" if not bans else "hits: %s" % bans),
    ]
    if any(not f["ok"] for f in files):
        rows.append(reviewkit.row(
            "files", "FAIL",
            "missing: %s" % [f["path"] for f in files if not f["ok"]]))
    payload = reviewkit.write_verdict(ADIR, ATTEMPT, SCOPE, rows, tests,
                                      files, bans)
    reviewkit.write_next(ADIR, ATTEMPT,
                         ["C2: full 7-root lineage (ab4)", "L2 OPA/Rego judges (ab4+)",
                          "probe adapters for Playwright/k6/etc (ab5+)", "live QP adapter (ab3 deferred: T1)"],
                         ["autobuild4 scope: WASM validator ABI + ContractRoot invariance + lineage roots",
                          "keep ab1+ab2+ab3 suites green; GO.sh stays one-click"])
    print("overall: %s | ab3: %s/%s" % (payload["overall"], tests["passed"],
                                        tests["failed"]))
    return 0 if payload["overall"] != "FAIL" else 2


if __name__ == "__main__":
    sys.exit(main())
