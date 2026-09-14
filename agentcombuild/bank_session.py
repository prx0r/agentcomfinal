"""Session banker: execute everything real, bank every result, log every step.

No mocks: pytest suites, E4 tournament (real gates), UK compile (real
hashes), redteam (real attacks), venv live wire tests (real SDK/MCP).
Outputs: trajectory/verified/* (full+ATIF+compact, fidelity-gated),
runs/session-*.jsonl (RUN records), SESSION_LOG.md (human-readable log).
Exit nonzero if anything fails — a green bank with a red step is a lie.
"""
import json
import os
import subprocess
import sys
import time

ROOT = "/agentcomfinal"
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "agentloop", "src"))
sys.path.insert(0, os.path.join(ROOT, "agentcombuild", "autobuild1", "src"))

STAMP = time.strftime("%Y%m%d-%H%M%S")
SESSDIR = os.path.join(ROOT, "agentcombuild", "runs", "sess-" + STAMP)
os.makedirs(SESSDIR, exist_ok=True)

from loop import compile as _compile  # noqa: E402
from loop import runlog as _runlog  # noqa: E402
from trajectory import bank as _bank  # noqa: E402
from trajectory import trajectory as _traj  # noqa: E402

LOG = []


def sh(name, cmd, cwd=ROOT, env=None):
    t0 = time.monotonic()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900,
                       cwd=cwd, env=env)
    wall_ms = int((time.monotonic() - t0) * 1000)
    tail = (p.stdout + p.stderr).strip().splitlines()[-4:]
    rec = {"step": name, "cmd": " ".join(cmd), "rc": p.returncode,
           "wall_ms": wall_ms, "tail": tail}
    LOG.append(rec)
    print("[%s] rc=%d %dms :: %s" % (name, p.returncode, wall_ms,
                                    " | ".join(tail)[-160:]))
    return rec


def bank_suite(name, contract_root, rec):
    ok = rec["rc"] == 0
    traj = _traj.build(
        contract_root, "plan:bank-session", "policy.direct",
        [{"attempt_id": "ATT-0",
          "action": {"description": rec["cmd"][:160]},
          "observed_effect": {"verdict": "PASS" if ok else "FAIL",
                              "reasons": rec["tail"]},
          "cost": {"duration_ms": rec["wall_ms"], "tokens": None}}],
        {"suite": "UNKNOWN"}, {"suite": "TRUE" if ok else "FALSE"},
        cost={"tokens": None, "wall_ms": rec["wall_ms"], "usd": 0,
              "human_minutes": 0})
    out = _bank.file_trajectory(os.path.join(ROOT, "trajectory"), traj)
    rec["banked"] = out["dir"]
    return ok


def main():
    py = sys.executable
    all_ok = True

    suites = [
        ("ab1", [py, "-m", "pytest", "tests/", "-q"],
         os.path.join(ROOT, "agentcombuild", "autobuild1"), None),
        ("ab2", [py, "-m", "pytest", "tests/", "-q"],
         os.path.join(ROOT, "agentcombuild", "autobuild2"),
         {"PYTHONPATH": "../autobuild1/src:src"}),
        ("ab3", [py, "-m", "pytest", "tests/", "-q"],
         os.path.join(ROOT, "agentcombuild", "autobuild3"),
         {"PYTHONPATH": "../autobuild1/src:src"}),
        ("agentloop", [py, "-m", "pytest", "tests/", "-q"],
         os.path.join(ROOT, "agentcombuild", "agentloop"),
         {"PYTHONPATH": "../autobuild1/src:src"}),
        ("core", [py, "-m", "pytest", "core/tests/", "-q"], ROOT,
         {"PYTHONPATH": ROOT}),
        ("compiler", [py, "-m", "pytest", "autobuild/compiler/",
                      "trajectory/test_formats.py", "contracts/", "-q"], ROOT,
         {"PYTHONPATH": ROOT}),
        ("openai-native", [py, "-m", "pytest", "tests/", "-q"],
         os.path.join(ROOT, "experiments", "openai_native"),
         {"PYTHONPATH": "src:" + os.path.join(
             ROOT, "agentcombuild", "agentloop", "src") + ":" + ROOT}),
    ]
    for name, cmd, cwd, extra in suites:
        env = dict(os.environ)
        if extra:
            env.update(extra)
        rec = sh("suite:" + name, cmd, cwd, env)
        ok = bank_suite(name, "contract:suite-green-" + name, rec)
        all_ok = all_ok and ok and rec["rc"] == 0

    # E4 tournament (real gates) + bank winner trajectory
    rec = sh("e4", [py, "experiments/policies/tournament_e4.py"], ROOT)
    all_ok = all_ok and rec["rc"] == 0

    # UK compile (real hashes) filed as candidate artifact
    rec = sh("uk-compile", [py, "-c",
             "from autobuild.compiler import actuality_compile as A;"
             "import json; c=A.compile_uk();"
             "open('trajectory/candidates/uk_contract.json','w').write("
             "json.dumps(c, indent=2));"
             "print('leaves:', len(c['leaves']), 'unprovable:', c['unprovable'])"], ROOT,
             {"PYTHONPATH": ROOT})
    all_ok = all_ok and rec["rc"] == 0

    # redteam (real attacks)
    rec = sh("redteam", [py, "agentcombuild/autobuild0/redteam_ab12.py"], ROOT)
    all_ok = all_ok and rec["rc"] == 0

    # venv live wire (real SDK + MCP, keyless)
    venv = "/home/ubuntu/.venvs/agentcom/bin/python"
    if os.path.exists(venv):
        rec = sh("live-wire", [venv, "-m", "pytest",
                                "agentcombuild/agentloop/tests/test_tracing_live.py",
                                "experiments/policies/test_sdk_policy.py",
                                "experiments/openai_native/tests/test_wire_live.py",
                                "-q"], ROOT)
        all_ok = all_ok and rec["rc"] == 0
    else:
        LOG.append({"step": "live-wire", "cmd": "SKIP no venv", "rc": 0,
                    "wall_ms": 0, "tail": []})

    with open(os.path.join(SESSDIR, "steps.jsonl"), "w") as fh:
        for r in LOG:
            fh.write(json.dumps(r, sort_keys=True) + "\n")

    # RUN record for the session itself (working/not_working/next/visionary)
    run = _runlog.new_run("agentcomfinal-build", "bank-session")
    run["working"] = [{"claim": r["step"] + " green",
                       "validation": "rc=0, banked=%s" % r.get("banked", "-")}
                      for r in LOG if r["rc"] == 0 and "banked" in r]
    run["not_working"] = [{"claim": r["step"] + " red",
                           "failure": " | ".join(r["tail"])[-200:],
                           "fixture": r["cmd"][:160]}
                          for r in LOG if r["rc"] != 0]
    run["next10"] = [
        {"task": "Close caller-clock trust gap (R5)", "justification": "only known-open telemetry hole", "impact": 5},
        {"task": "Hash judge output into signed receipts (R10)", "justification": "provenance for gate inputs", "impact": 5},
        {"task": "F1 CI live on first PR", "justification": "independent second machine", "impact": 4},
        {"task": "F2a provider read leg on key arrival", "justification": "first live reality", "impact": 4},
        {"task": "Bank 100 trajectories, run memory compiler v1", "justification": "F4 habit", "impact": 3},
    ]
    run["visionary"] = [{"idea": "Tournament lanes as git worktrees with merge-as-promotion",
                         "endgame_link": "self-building system",
                         "falsifier": "no measured convergence speedup in 3 tournaments"}]
    ok, reasons = _runlog.check_record(run)
    assert ok, reasons
    _runlog.append(os.path.join(SESSDIR, "run.jsonl"), run)

    # memory compile over the session bank (prove the loop reads its write)
    compiled = _compile.compile_runs([run])
    mem = _compile.to_memory_view(compiled)
    with open(os.path.join(SESSDIR, "memory.json"), "w") as fh:
        json.dump({"ideas": len(compiled["ideas_bank"]),
                   "leaderboard_top3": compiled["next10"][:3],
                   "memory_records": len(mem["records"]),
                   "reduction": mem["reduction"]}, fh, indent=2)
    print("banked=%s ideas=%d memory_records=%d reduction=%s" % (
        SESSDIR, len(compiled["ideas_bank"]), len(mem["records"]),
        mem["reduction"]))

    with open(os.path.join(ROOT, "agentcombuild", "SESSION_LOG.md"), "w") as fh:
        fh.write("# SESSION LOG %s\n\n" % STAMP)
        fh.write("Steps: %d, failures: %d. Bank: `%s`. All artifacts below.\n\n"
                 % (len(LOG), sum(1 for r in LOG if r["rc"] != 0), SESSDIR))
        for r in LOG:
            fh.write("## %s rc=%d %dms\n```\n%s\n```\n%s\n\n" % (
                r["step"], r["rc"], r.get("wall_ms", 0), r["cmd"],
                "\n".join(r.get("tail", []))))
    print("ALL_OK" if all_ok else "FAILURES_PRESENT")
    return 0 if all_ok else 2


if __name__ == "__main__":
    sys.exit(main())
