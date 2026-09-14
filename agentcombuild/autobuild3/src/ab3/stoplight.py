"""Stoplight: re-execute every a-log claim now. The agent never judges.

Evidence re-runs for real. `command` only runs when argv[0] is allowlisted
(simulation sandbox); anything else is refused-to-run, never executed —
a hostile log line can never make the judge run arbitrary commands.
`file` checks existence (+hash). `ref` is context-only, never sufficient.
Any red re-run fails the task (false telemetry, not bad luck).
"""
import hashlib
import json
import os
import subprocess
import time

from . import alog

ALLOW_COMMANDS = ("echo", "python3", "ls", "cat", "test", "true", "false")
VALIDATOR_TIMEOUT = 60


def rerun(evidence, timeout=10):
    """Re-execute one evidence item. Returns (green, detail)."""
    if not isinstance(evidence, dict):
        return False, "bad-evidence"
    kind = evidence.get("kind")
    if kind == "command":
        argv = evidence.get("argv", [])
        if not argv or os.path.basename(str(argv[0])) not in ALLOW_COMMANDS:
            return False, "refused-to-run"
        try:
            p = subprocess.run([str(a) for a in argv], capture_output=True,
                               text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return False, "timeout"
        except Exception as exc:  # noqa: BLE001
            return False, "exec-error:%s" % type(exc).__name__
        if p.returncode != 0:
            return False, "exit=%d" % p.returncode
        expect = evidence.get("expect")
        if expect is not None and expect not in (p.stdout or ""):
            return False, "output-mismatch"
        return True, "ok"
    if kind == "file":
        path = evidence.get("path", "")
        if not path or not os.path.exists(path):
            return False, "missing-file"
        want = evidence.get("sha256")
        if want:
            try:
                with open(path, "rb") as fh:
                    got = hashlib.sha256(fh.read()).hexdigest()
            except OSError:
                return False, "unreadable-file"
            if got != want:
                return False, "hash-mismatch"
        return True, "ok"
    return False, "not-rerunnable"


def run_validator(vpath, task, queue_path, alog_path, timeout=VALIDATOR_TIMEOUT):
    """atask validator contract: argv[task queue alog], exit 0 + one JSON line
    {"pass","reasons"}. Anything else is a validator-error (fails loudly)."""
    try:
        p = subprocess.run(["python3", vpath, task, queue_path, alog_path],
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, ["validator-timeout"], True
    except Exception as exc:  # noqa: BLE001
        return False, ["validator-exec-error:%s" % type(exc).__name__], True
    if p.returncode != 0:
        return False, ["validator-exit=%d" % p.returncode], True
    try:
        verdict = json.loads((p.stdout or "").strip().splitlines()[-1])
        return bool(verdict["pass"]), list(verdict.get("reasons", [])), False
    except (ValueError, KeyError, IndexError, TypeError):
        return False, ["validator-bad-json"], True


def judge(task, queue, logdir, validators_dir=None, queue_path="queue.json",
          timeout=VALIDATOR_TIMEOUT):
    """Independent judgment. Returns {task, verdict GO|NOGO, reasons, ...}."""
    reasons = []
    if task not in queue:
        return {"task": task, "verdict": "NOGO",
                "reasons": ["unknown-task"], "lines": 0, "green": 0}
    lines = alog.read_lines(logdir, task)
    if not lines:
        return {"task": task, "verdict": "NOGO", "reasons": ["no-log"],
                "lines": 0, "green": 0}
    if not alog.verify_chain(logdir, task):
        return {"task": task, "verdict": "NOGO", "reasons": ["chain-broken"],
                "lines": len(lines), "green": 0}
    acc = queue[task]["acceptance"]
    green_idx, green_n = set(), 0
    for line in lines:
        ev = line.get("evidence", {})
        green, detail = rerun(ev)
        if green:
            green_n += 1
            for i in line.get("idx", []):
                if isinstance(i, int) and 0 <= i < len(acc):
                    green_idx.add(i)
        else:
            reasons.append("seq%d:%s" % (line.get("seq", "?"), detail))
    for i in range(len(acc)):
        if i not in green_idx:
            reasons.append("acceptance[%d] uncovered" % i)
    if validators_dir:
        vpath = os.path.join(validators_dir, task + ".py")
        if os.path.exists(vpath):
            ok, vreasons, verr = run_validator(
                vpath, task, queue_path, alog.log_path(logdir, task),
                timeout)
            for r in vreasons:
                reasons.append("validator:%s" % r)
            if verr:
                reasons.append("validator-error")
            elif not ok and not vreasons:
                reasons.append("validator:fail")
    verdict = "GO" if not reasons else "NOGO"
    return {"task": task, "verdict": verdict, "reasons": reasons,
            "lines": len(lines), "green": green_n}


def acheck(queue, logdir, validators_dir=None, queue_path="queue.json",
           stale_hours=24, now=None):
    """Derived status per task. Recomputes every verdict; planted verdict
    files are ignored (there is nothing to trust)."""
    now = time.time() if now is None else now
    out = {}
    for task in queue:
        lines = alog.read_lines(logdir, task)
        if not lines:
            out[task] = {"status": "PROPOSED", "reasons": ["no-log"]}
            continue
        v = judge(task, queue, logdir, validators_dir, queue_path)
        if v["verdict"] == "GO":
            out[task] = {"status": "DONE", "reasons": []}
            continue
        try:
            mtime = os.path.getmtime(alog.log_path(logdir, task))
        except OSError:
            mtime = now
        if now - mtime > stale_hours * 3600:
            out[task] = {"status": "STALE", "reasons": v["reasons"]}
        else:
            out[task] = {"status": "NOGO", "reasons": v["reasons"]}
    return out
