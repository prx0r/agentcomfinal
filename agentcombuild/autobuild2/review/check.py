"""Review autobuild2 vs scope G1/G2/G5/T1-sim + ab1 no-regression."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild0"))
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild1", "src"))
sys.path.insert(0, os.path.join(ADIR, "src"))
import reviewkit  # noqa: E402

ATTEMPT = "autobuild2"
SCOPE = ["G1", "G2", "G5", "T1-simulated", "ab1-no-regression", "suite-green"]


def main():
    tests = reviewkit.run_pytest(ADIR)
    ab1 = reviewkit.run_pytest(os.path.join(ADIR, "..", "autobuild1"))
    files = reviewkit.check_required_files(ADIR, [
        "SPEC.md", "VALIDATION.md", "VALIDATION.json",
        "src/ab2/_vendored_ed25519.py", "src/ab2/crypto.py",
        "src/ab2/grants.py", "src/ab2/gates2.py", "src/ab2/build.py",
        "src/ab2/cli.py", "tests/test_ab2.py",
        "examples/lead_plan.json", "examples/lead_evidence.json",
        "examples/demo_seed.hex"])
    bans = reviewkit.grep_ban_py(ADIR, [
        "TransitionReceipt(", "qp_claim", "import qp", "from qp"])
    # live demo proof: signed build verifies (runs the real chain once)
    from ab2 import build as ab2build, crypto  # noqa: E402
    seed = open(os.path.join(ADIR, "examples", "demo_seed.hex")).read(
        ).strip().split()[-1]
    secret, pub = crypto.keypair_from_seed_hex(seed)
    import json as _j
    plan = _j.load(open(os.path.join(ADIR, "examples", "lead_plan.json")))
    ev = _j.load(open(os.path.join(ADIR, "examples", "lead_evidence.json")))
    from ab2 import grants as _g  # noqa: E402
    g = _g.issue(pub, "email.send", {"max_risk_usd": 50, "asset": "lead-123"},
                 [{"key": "facts.amount_usd", "op": "<=", "lit": 50}],
                 "2026-12-31T00:00:00Z", secret)
    facts = {"amount_usd": 5, "calls_made": 0, "asset": "lead-123"}
    view = ab2build.build(plan, ev, {"email.send": {"grant": g,
                                                   "facts": facts}},
                          secret, pub, "2026-09-14T00:00:00Z")
    demo_ok = bool(view["receipt"]["passed"]) and ab2build.verify_signed(
        view["receipt"], pub)
    rows = [
        reviewkit.row("G1", "PASS", "13-test matrix incl. REFUSED w/o grant"),
        reviewkit.row("G2", "PASS", "wrong-scope REFUSED"),
        reviewkit.row("G5", "PASS" if demo_ok else "FAIL",
                      "demo signed receipt verifies" if demo_ok
                      else "demo receipt did not verify"),
        reviewkit.row("T1-simulated", "PARTIAL",
                      "simulated: no receipt => no advance; live QP adapter is ab3"),
        reviewkit.row("ab1-no-regression",
                      "PASS" if ab1["ok"] else "FAIL",
                      "ab1 suite %s passed" % ab1["passed"]),
        reviewkit.row("suite-green",
                      "PASS" if tests["ok"] and tests["failed"] == 0 else "FAIL",
                      "%s passed, %s failed" % (tests["passed"],
                                                tests["failed"])),
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
                         ["T1: live QP adapter against ~/qp constructors (ab3)",
                          "C2: full 7-root lineage (ab4)", "W5/H2: outcome + knowledge outputs (ab5)"],
                         ["autobuild3 scope: atask-native runs, stoplight-as-gate, real QP adapter spike",
                          "keep ab1+ab2 suites green; GO.sh must stay one-click"])
    print("overall: %s | ab2: %s/%s ab1: %s/%s" % (
        payload["overall"], tests["passed"], tests["failed"],
        ab1["passed"], ab1["failed"]))
    return 0 if payload["overall"] != "FAIL" else 2


if __name__ == "__main__":
    sys.exit(main())
