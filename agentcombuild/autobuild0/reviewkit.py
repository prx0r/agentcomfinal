"""Shared review harness for autobuild attempts. Stdlib only.

Each attempt keeps review/check.py (thin, attempt-specific scope) that calls
into here. Outputs: review/VERDICT.json (machine) + review/NEXT.md (human).
Statuses: PASS / PARTIAL / DEFERRED / FAIL. No FAIL allowed to promote.
"""
import datetime
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_ROOT = os.path.dirname(HERE)  # agentcombuild/


def today():
    return datetime.date.today().isoformat()


def run_pytest(attempt_dir):
    """Run the attempt suite. Returns dict(ok, passed, failed, tail)."""
    try:
        p = subprocess.run([sys_exe(), "-m", "pytest", "tests/", "-q"],
                           cwd=attempt_dir, capture_output=True, text=True,
                           timeout=300)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "passed": 0, "failed": -1,
                "tail": "harness-error:%s" % exc}
    tail = (p.stdout + p.stderr).strip().splitlines()[-3:]
    passed, failed, ok = 0, 0, p.returncode == 0
    for line in (p.stdout + p.stderr).splitlines():
        if " passed" in line:
            try:
                passed = int(line.split(" passed")[0].split()[-1])
            except ValueError:
                pass
        if " failed" in line:
            try:
                failed = int(line.split(" failed")[0].split()[-1])
            except ValueError:
                pass
    return {"ok": ok, "passed": passed, "failed": failed, "tail": tail}


def sys_exe():
    import sys
    return sys.executable


def check_required_files(attempt_dir, relpaths):
    out = []
    for rel in relpaths:
        full = os.path.join(attempt_dir, rel)
        out.append({"path": rel,
                    "ok": os.path.exists(full)})
    return out


def grep_ban_py(attempt_dir, banned):
    """Banned patterns must not appear in src/**/*.py. Returns hits.

    Patterns starting with 're:' are regex-searched per line; others are
    plain substrings. Files with 'vendored' in the name are skipped:
    vendoring external code with a provenance header is allowed (never copy
    schemas silently), and the header itself names the source repo.
    """
    import re as _re
    hits = []
    src = os.path.join(attempt_dir, "src")
    for root, _, files in os.walk(src):
        for fn in sorted(files):
            if not fn.endswith(".py") or "vendored" in fn:
                continue
            full = os.path.join(root, fn)
            try:
                with open(full, encoding="utf-8") as fh:
                    text = fh.read()
            except OSError:
                continue
            rel = os.path.relpath(full, attempt_dir)
            for pat in banned:
                if pat.startswith("re:"):
                    if any(_re.search(pat[3:], ln) for ln in
                           text.splitlines()):
                        hits.append({"pattern": pat, "file": rel})
                elif pat in text:
                    hits.append({"pattern": pat, "file": rel})
    return hits


def row(cid, status, note="", tests=None):
    assert status in ("PASS", "FAIL", "UNEVALUATED", "SKIPPED")
    return {"id": cid, "status": status, "note": note,
            "tests": list(tests or [])}


def run_nodes(workdir, env, nodes):
    """Run exact pytest node ids. Returns {node: PASS|FAIL|ERROR|SKIPPED}.
    Nodes never observed in output are reported MISSING (a gate that did
    not execute is not a gate that passed)."""
    import re as _re
    try:
        p = subprocess.run(
            [sys_exe(), "-m", "pytest", "--tb=no", "-v"] + list(nodes),
            cwd=workdir, capture_output=True, text=True, timeout=600,
            env=env)
    except Exception as exc:  # noqa: BLE001
        return {n: "ERROR:harness" for n in nodes}
    seen = {}
    for line in (p.stdout + p.stderr).splitlines():
        m = _re.match(r"^(\S+::\S+)\s+(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)",
                      line.strip())
        if m:
            seen[m.group(1)] = m.group(2)
    out = {}
    for n in nodes:
        out[n] = seen.get(n, "MISSING")
    return out


def verify_rows(workdir, env, rows):
    """Row PASS iff it cites >=1 test and EVERY cited test PASSED.
    SKIPPED (env-dependent) propagates as SKIPPED, never PASS. Anything
    else (FAIL/ERROR/MISSING/XFAIL/XPASS, empty cites) is FAIL except
    all-SKIPPED which is SKIPPED. Returns (rows_out, overall) with
    overall PASS only when every row passed."""
    wanted = sorted({t for r in rows for t in r.get("tests", [])})
    results = run_nodes(workdir, env, wanted) if wanted else {}
    out = []
    for r in rows:
        cited = r.get("tests", [])
        states = [results.get(t, "MISSING") for t in cited]
        if not cited:
            status, note = "UNEVALUATED", "no executable gate cited"
        elif all(s == "PASSED" for s in states):
            status, note = "PASS", "%d/%d gates green" % (
                len(states), len(states))
        elif states and all(s == "SKIPPED" for s in states):
            status, note = "SKIPPED", "env-dependent, not evaluated here"
        else:
            bad = {t: s for t, s in zip(cited, states) if s != "PASSED"}
            status, note = "FAIL", "not-green: %s" % bad
        out.append({"id": r["id"], "status": status, "note": note,
                    "tests": cited, "results": states})
    overall = "PASS" if out and all(r["status"] in ("PASS", "SKIPPED")
                                       for r in out) else "FAIL"
    return out, overall


def write_verdict(attempt_dir, attempt, scope, rows, tests, files, bans):
    fails = [r["id"] for r in rows
             if r["status"] not in ("PASS", "SKIPPED")]
    overall = "FAIL" if (fails or not tests.get("ok")) else "PASS"
    # NOTE (test2.md Rule 0): PARTIAL/DEFERRED/"PASS WITH DEBT" retired.
    # A criterion is PASS only if its cited executable gates ran green.
    payload = {"attempt": attempt, "date": today(), "scope": scope,
               "overall": overall, "criteria": rows, "tests": tests,
               "files": files, "banned_hits": bans,
               "fails": fails}
    out = os.path.join(attempt_dir, "review", "VERDICT.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return payload


def write_next(attempt_dir, attempt, debt_lines, next_scope):
    lines = ["# NEXT after %s (%s)" % (attempt, today()), "",
             "## Carried debt"]
    lines += ["- %s" % d for d in debt_lines] or ["- none"]
    lines += ["", "## Next attempt scope", ""]
    lines += ["- %s" % s for s in next_scope]
    lines += ["", "_Generated by review/check.py. Human edits welcome._", ""]
    with open(os.path.join(attempt_dir, "review", "NEXT.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def run_file_summary(workdir, env, path):
    """Run one test file; return {passed, failed, skipped}. A file whose
    tests all SKIP (e.g. live provider tests without credentials) reports
    skipped — NOT_CONFIGURED, never PASS, never FAIL."""
    import re as _re
    try:
        pr = subprocess.run(
            [sys_exe(), "-m", "pytest", "--tb=no", "-q", path],
            cwd=workdir, capture_output=True, text=True, timeout=600,
            env=env)
    except Exception:  # noqa: BLE001
        return {"passed": 0, "failed": -1, "skipped": 0}
    out = pr.stdout + pr.stderr
    passed = failed = skipped = 0
    m = _re.search(r"(\d+) passed", out)
    if m:
        passed = int(m.group(1))
    m = _re.search(r"(\d+) failed", out)
    if m:
        failed = int(m.group(1))
    m = _re.search(r"(\d+) skipped", out)
    if m:
        skipped = int(m.group(1))
    return {"passed": passed, "failed": failed, "skipped": skipped}
