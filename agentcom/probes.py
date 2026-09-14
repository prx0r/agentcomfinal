"""Primitive probes + judges (chainloop.md validator library, wave 1).

Every probe returns an OBSERVATION dict (never a verdict). Every judge maps
observation -> TRUE|FALSE|UNKNOWN (never raises). Live-dependent probes
return UNKNOWN with a reason when their world is absent — an untestable
gate is UNKNOWN, not PASS and not FAIL.

Probes here are the only code allowed to touch the world (TinyProbeRuntime:
subprocess, file reads, timers, urllib). Judges are pure.
"""
import hashlib
import json
import os
import subprocess
import time
import urllib.request

TRUE, FALSE, UNKNOWN = "TRUE", "FALSE", "UNKNOWN"


def _git(repo, *args, timeout=30):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                       text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args),
                                           (p.stderr or "")[:160]))
    return p.stdout.strip()


# ---- git probes ----

def probe_git_candidate(repo, claimed_sha):
    """exact-candidate observation: claimed vs tested tree state."""
    head = _git(repo, "rev-parse", "HEAD")
    return {"probe": "git.clean_checkout", "candidate_sha": claimed_sha,
            "tested_sha": head,
            "tree_sha": _git(repo, "rev-parse", "HEAD^{tree}"),
            "dirty": bool(_git(repo, "status", "--porcelain"))}


def judge_exact_candidate(obs):
    if obs.get("dirty"):
        return FALSE, "worktree dirty"
    if not obs.get("candidate_sha"):
        return UNKNOWN, "no candidate claimed"
    if obs["candidate_sha"] == obs.get("tested_sha"):
        return TRUE, "candidate == tested, clean"
    return FALSE, "claimed %s, tested %s" % (
        (obs.get("candidate_sha") or "")[:12],
        (obs.get("tested_sha") or "")[:12])


def probe_git_clean(repo):
    return {"probe": "git.clean", "dirty": bool(
        _git(repo, "status", "--porcelain"))}


def judge_git_clean(obs):
    return (TRUE, "clean") if not obs.get("dirty") else (FALSE, "dirty")


# ---- pytest probe (brief's pytest-v1 observation shape) ----

def probe_pytest(nodes, cwd, env=None, timeout=600):
    """Run nodes; observation carries executable/argv/cwd/validator pins +
    exit code + stdout hash + duration. Never judges (that's the judge's job)."""
    exe = os.path.realpath("/usr/bin/python3")
    t0 = time.monotonic()
    p = subprocess.run([exe, "-m", "pytest"] + list(nodes), capture_output=True,
                       text=True, timeout=timeout, cwd=cwd, env=env)
    out = (p.stdout or "") + (p.stderr or "")
    files = sorted({n.split("::")[0] for n in nodes})
    pins = {}
    for f in files:
        fp = os.path.join(cwd, f)
        if os.path.exists(fp):
            with open(fp, "rb") as fh:
                pins[f] = hashlib.sha256(fh.read()).hexdigest()
    return {"probe": "pytest-v1",
            "subject": {"repo": cwd},
            "execution": {"executable": exe, "argv": ["-m", "pytest"] + nodes,
                          "validator_sha": pins},
            "observation": {"exit_code": p.returncode,
                            "stdout_sha256": hashlib.sha256(
                                out.encode()).hexdigest(),
                            "duration_ms": int((time.monotonic() - t0) * 1000)},
            "tail": out.strip().splitlines()[-3:]}


def judge_pytest_exit_zero(obs, required_commit=None):
    if obs["observation"]["exit_code"] != 0:
        return FALSE, "exit %s" % obs["observation"]["exit_code"]
    return TRUE, "exit 0"


# ---- QP probes (real ~/qp via adapters/qp) ----

def probe_qp_receipt_valid(receipt, evidence):
    import sys
    sys.path.insert(0, "/agentcomfinal")
    from adapters import qp as _qp
    r = _qp.verify_settlement(receipt or {}, evidence or [])
    return {"probe": "qp.receipt_valid", "ok": bool(r.get("ok")),
            "reason": r.get("reason", "")}


def judge_qp_receipt_valid(obs):
    return (TRUE, obs.get("reason", "")) if obs.get("ok") else \
        (FALSE, obs.get("reason", ""))


def probe_qp_no_receipt_on_failed_readback():
    """Adversarial, executed for real: force readback FALSE through the
    real chain and observe that no receipt is minted and level stays L0."""
    import sys
    sys.path.insert(0, "/agentcomfinal")
    sys.path.insert(0, "/agentcomfinal/experiments/openai_native/src")
    from opennative import chain as _chain
    out = _chain.run_chain({"project": "probe", "campaign": "probe",
                            "contract_root": "contract:probe",
                            "model": "sim"},
                           readback_ok=False)
    return {"probe": "adversarial.readback_false",
            "receipt_minted": out["receipt"] is not None,
            "qp_receipts": out["trajectory"].get("qp_receipts", []),
            "level": out["trajectory"].get("level", "?")}


def judge_no_receipt(obs):
    if obs.get("receipt_minted") or obs.get("qp_receipts"):
        return FALSE, "receipt minted despite FALSE readback"
    if obs.get("level") != "L0-observation":
        return FALSE, "level advanced without settlement"
    return TRUE, "no receipt, L0 held"


# ---- provider / host probes (honest UNKNOWNs without their worlds) ----

def probe_github_ci(owner="prx0r", repo="agentcomfinal", sha="", timeout=20):
    """github.ci_success: check-runs for an exact SHA via public API.
    No key needed (public repo). Network failure -> UNKNOWN, never FALSE."""
    if not sha:
        return {"probe": "github.ci_success", "value": UNKNOWN,
                "reason": "no-sha"}
    url = ("https://api.github.com/repos/%s/%s/commits/%s/check-runs"
           % (owner, repo, sha))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "agentcom"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.load(r)
    except Exception as exc:  # noqa: BLE001 - network is not truth
        return {"probe": "github.ci_success", "value": UNKNOWN,
                "reason": "network:%s" % type(exc).__name__}
    runs = data.get("check_runs", [])
    if not runs:
        return {"probe": "github.ci_success", "value": UNKNOWN,
                "reason": "no-check-runs-yet"}
    states = {(c.get("status"), c.get("conclusion")) for c in runs}
    if all(s == ("completed", "success") for s in states):
        return {"probe": "github.ci_success", "value": TRUE,
                "reason": "%d checks green" % len(runs)}
    if any(s[0] == "completed" and s[1] not in ("success", "skipped", None)
           for s in states):
        return {"probe": "github.ci_success", "value": FALSE,
                "reason": "failing checks present"}
    return {"probe": "github.ci_success", "value": UNKNOWN,
            "reason": "checks pending"}


def probe_openai_real_session():
    """openai.real_session: UNKNOWN without credentials by construction.
    (LIVE executor path exists in opennative/executor.py; no key on box.)"""
    import os as _os
    if not _os.environ.get("OPENAI_API_KEY"):
        return {"probe": "openai.real_session", "value": UNKNOWN,
                "reason": "NOT_CONFIGURED"}
    return {"probe": "openai.real_session", "value": UNKNOWN,
            "reason": "key present: live run is a manual step, not probed here"}


def probe_chatgpt_host(slots_path):
    """chatgpt.* leaves: UNKNOWN until manual/HOST_EVAL.md evidence exists."""
    try:
        with open(slots_path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return {"probe": "chatgpt.host", "value": UNKNOWN,
                "reason": "no-evidence-slots"}
    filled = "[x]" in text.lower()
    return {"probe": "chatgpt.host", "value": UNKNOWN,
            "reason": "host evidence slots %s"
            % ("present-awaiting-human" if filled else "empty")}


def probe_fixture_boundary():
    """business.lookup fixture is labeled FIXTURE/SIMULATED (P8). TRUE iff
    the label is present — the claim is about labeling honesty, and the
    evidence is in-tree and checkable."""
    import sys
    sys.path.insert(0, "/agentcomfinal/experiments/openai_native/src")
    sys.path.insert(0, "/agentcomfinal")
    from opennative import mcp_servers
    out = mcp_servers.call("business.lookup",
                           {"company": "acme-plumbing-leeds"})
    biz = out.get("business", {})
    labeled = out.get("source_class") == "FIXTURE" and \
        out.get("verification") == "SIMULATED"
    return {"probe": "fixture.boundary", "value": TRUE if labeled else FALSE,
            "reason": "fixture labeled" if labeled else "fixture unlabeled"}
