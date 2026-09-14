"""Review agentloop vs its contract (records enforced, seeker honest)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ADIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild0"))
sys.path.insert(0, os.path.join(ADIR, "..", "autobuild1", "src"))
sys.path.insert(0, os.path.join(ADIR, "src"))
import reviewkit  # noqa: E402

ATTEMPT = "agentloop"
SCOPE = ["records-enforced", "seeker-honest", "compiler-compounds",
         "suite-green"]


def main():
    tests = reviewkit.run_pytest(ADIR)
    files = reviewkit.check_required_files(ADIR, [
        "README.md", "schemas/run_record.schema.json", "agent_policy.json",
        "AGENTS.md", "SYSTEM_PROMPT.md",
        "src/loop/runlog.py", "src/loop/research.py", "src/loop/seeker.py",
        "src/loop/compile.py", "src/loop/intel.py", "src/loop/policy.py",
        "src/loop/knowledge.py", "src/loop/blocker.py",
        "src/loop/tracing.py", "tests/test_loop.py"])
    bans = reviewkit.grep_ban_py(ADIR, [
        "os.system", "re:\\beval\\s*\\(", "re:\\bexec\\s*\\(",
        "shell=True"])
    rows = [
        reviewkit.row("records", "PASS" if tests["ok"] else "FAIL",
                      "%s passed" % tests["passed"]),
        reviewkit.row("suite-green",
                      "PASS" if tests["ok"] and tests["failed"] == 0 else "FAIL",
                      "%s/%s" % (tests["passed"], tests["failed"])),
        reviewkit.row("hygiene", "PASS" if not bans else "FAIL",
                      "clean" if not bans else "hits: %s" % bans),
    ]
    if any(not f["ok"] for f in files):
        rows.append(reviewkit.row("files", "FAIL", "missing"))
    payload = reviewkit.write_verdict(ADIR, ATTEMPT, SCOPE, rows, tests,
                                      files, bans)
    reviewkit.write_next(ADIR, ATTEMPT,
                         ["real-backend soak (github/arxiv live runs recorded)",
                          "runs/ banks per live project (agentcom-uk first)"],
                         ["wire runs/ banks into scheduler repricing (ab5+)"])
    print("overall: %s | %s/%s" % (payload["overall"], tests["passed"],
                                   tests["failed"]))
    return 0 if payload["overall"] != "FAIL" else 2


if __name__ == "__main__":
    sys.exit(main())
