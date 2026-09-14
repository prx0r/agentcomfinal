"""Execution envelope (devplan §11 — fresh implementation). Reproducibility
for rerunnable command evidence. Binds: resolved executable absolute path,
argv, cwd, environment allowlist hash, timeout. A command re-run under a
different envelope is a different observation (UNKNOWN until rebound).

`python3 test.py` today must provably mean the same thing tomorrow, or the
judge refuses to treat it as the same evidence.
"""
import hashlib
import json
import os
import shutil
import subprocess

from core import ids


def bind_envelope(argv, cwd=None, env_allow=(), timeout=10):
    """Resolve + freeze the execution context. Returns envelope dict."""
    if not argv:
        raise ValueError("empty argv")
    resolved = shutil.which(str(argv[0]))
    if not resolved:
        raise ValueError("unresolvable:%s" % argv[0])
    cwd = os.path.abspath(cwd or os.getcwd())
    env = {k: os.environ.get(k, "") for k in sorted(env_allow)}
    env_hash = ids.sha256_hex(ids.canonical(env))
    envp = {"exe": os.path.abspath(resolved), "argv": [str(a) for a in argv],
            "cwd": cwd, "env_hash": env_hash,
            "env_keys": sorted(env_allow), "timeout": int(timeout)}
    envp["envelope_id"] = ids.obj_id("env", {k: v for k, v in envp.items()
                                             if k != "envelope_id"})
    return envp


def verify_envelope(envelope, argv=None, cwd=None, env_allow=None):
    """Recompute and compare. Returns (ok, reason)."""
    try:
        check = bind_envelope(argv if argv is not None else envelope["argv"],
                              cwd if cwd is not None else envelope["cwd"],
                              env_allow if env_allow is not None
                              else envelope.get("env_keys", ()),
                              envelope.get("timeout", 10))
    except ValueError as exc:
        return False, str(exc)[:120]
    for k in ("exe", "argv", "cwd", "env_hash", "timeout"):
        if check.get(k) != envelope.get(k):
            return False, "envelope-drift:%s" % k
    return True, "envelope-ok"


def run_envelope(envelope):
    """Execute inside the verified envelope. Returns (rc, stdout)."""
    ok, reason = verify_envelope(envelope)
    if not ok:
        raise ValueError(reason)
    env = {k: os.environ.get(k, "") for k in envelope.get("env_keys", [])}
    p = subprocess.run(envelope["argv"], capture_output=True, text=True,
                       timeout=envelope.get("timeout", 10),
                       cwd=envelope["cwd"], env=env if env else None)
    return p.returncode, (p.stdout or "")
