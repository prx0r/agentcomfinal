"""agentcom build orchestrator (brief P3): boring wiring, no strategy.

Dispatches spec kind: product -> build_product, selfhost -> worktree
candidate flow (test2.md P0/P1). Strategic intelligence lives in
Seesaw/scheduler, never here. Exit contract: returns report dict with
ok bool; CLI maps to exit codes.
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def load_spec(path):
    with open(path) as fh:
        spec = json.load(fh)
    if not isinstance(spec, dict) or not spec.get("kind"):
        raise ValueError("spec needs kind")
    return spec


def _git(repo, *args, timeout=60):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                       text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args),
                                           (p.stderr or "")[:200]))
    return p.stdout.strip()


def _head_sha(repo):
    return _git(repo, "rev-parse", "HEAD")


def _porcelain(repo):
    return _git(repo, "status", "--porcelain")


def build_selfhost(spec, out_root, repo=None, worker_fn=None,
                   work_parent="/tmp"):
    """P0/P1 candidate flow. BASE -> lane worktree -> worker edits+commits
    (explicit paths only) -> detached validation worktree @ CANDIDATE_SHA
    with FROZEN validator files -> receipt -> single-lane tournament.

    worker_fn(worktree_path) -> {"commit_paths": [...], "message": str}.
    worker_fn None (or empty commit) means NO WORK HAPPENED: receipt records
    validation-only, promotion REFUSED (a validation run is not a build).
    Returns report; banks artifacts under out_root/experiments/selfhost/<id>/.
    """
    from adapters import gitgoblin as _gg
    repo = repo or ROOT
    spec_id = spec.get("id", "selfhost")
    base_sha = spec.get("base_sha") or _head_sha(repo)
    if _porcelain(repo):
        raise RuntimeError("base repo dirty: commit or stash first")
    dest = os.path.join(out_root, "experiments", "selfhost", spec_id)
    os.makedirs(dest, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    lane = "exp/%s/direct-%s" % (spec_id, stamp)
    lane_path = os.path.join(work_parent, "agentcom-lane-%s" % stamp)
    t0 = time.monotonic()

    prebuild = _gg.reuse_plan(spec.get("contract", spec_id),
                              spec.get("contract", spec_id))
    _git(repo, "branch", lane, base_sha)
    try:
        _git(repo, "worktree", "add", lane_path, lane)
        worked = None
        if worker_fn is not None:
            worked = worker_fn(lane_path) or {}
        commit_paths = (worked or {}).get("commit_paths", [])
        if commit_paths:
            _git(lane_path, "add", "--", *commit_paths)
            _git(lane_path, "-c", "user.email=agentcom-builder",
                 "-c", "user.name=agentcom-builder", "commit", "-m",
                 (worked or {}).get("message", "exp: candidate"))
        dirty = _git(lane_path, "status", "--porcelain")
        candidate_sha = _git(lane_path, "rev-parse", "HEAD")
        candidate_tree = _git(lane_path, "rev-parse", "HEAD^{tree}")
        diff_stat = _git(repo, "diff", "--stat",
                         base_sha + ".." + candidate_sha) if \
            candidate_sha != base_sha else ""
        if dirty:
            receipt = {"base_sha": base_sha, "candidate_sha": candidate_sha,
                       "verdict": "REFUSED",
                       "reason": "dirty-tree: uncommitted work cannot validate",
                       "policy_id": spec.get("policy_id", "direct"),
                       "contract": spec.get("contract", "")}
            ok_all, results, vpath = False, [], None
        else:
            touched = _validator_touched(repo, base_sha, candidate_sha, spec)
            if touched:
                ok_all, results = False, [{
                    "node": "frozen-validator", "passed": False,
                    "tail": "frozen-validator: lane edited frozen "
                            "acceptance; disqualified without running tests"}]
                vinfo = {"head": candidate_sha, "tree": candidate_tree}
            else:
                ok_all, results, vinfo = _validate_detached(
                    repo, spec, candidate_sha, base_sha)
            receipt = {
                "base_sha": base_sha, "candidate_sha": candidate_sha,
                "candidate_tree_sha": candidate_tree,
                "validator_sha": base_sha,
                "contract_root": spec.get("contract", ""),
                "dirty_before_validation": False,
                "validation_worktree_head": vinfo["head"],
                "validation_worktree_tree": vinfo["tree"],
                "diff_stat": diff_stat,
                "prebuild": {"verdict": prebuild.get("verdict"),
                             "candidates": len(prebuild.get("candidates", []))},
                "results": results, "passed": ok_all,
                "policy_id": spec.get("policy_id", "direct"),
                "wall_ms": int((time.monotonic() - t0) * 1000),
                "verdict": "PASS" if ok_all else "FAIL"}
        changed = candidate_sha != base_sha
        promotable = (receipt.get("verdict") == "PASS" and changed
                      and not _validator_touched(repo, base_sha, candidate_sha,
                                                 spec))
        if receipt.get("verdict") == "PASS" and not changed:
            reason = "no-change: validation-only run, nothing to promote"
        else:
            reason = receipt.get("reason", "gates-or-identity failed")
        tournament = {"lanes": ["direct"],
                      "winner": "direct" if promotable else None,
                      "failures": [] if promotable else [receipt.get("verdict",
                                        "REFUSED")]}
        promoted = {"state": "PROMOTED" if promotable else "REFUSED",
                    "candidate_sha": candidate_sha,
                    "reason": None if promotable else reason}
        for name, obj in (("contract.json", spec),
                          ("candidates.json", [{"policy": "direct",
                                                "sha": candidate_sha,
                                                "diff_stat": receipt.get(
                                                    "diff_stat", "")}]),
                          ("receipts.json", [receipt]),
                          ("tournament.json", tournament),
                          ("promoted.json", promoted)):
            json.dump(obj, open(os.path.join(dest, name), "w"), indent=2)
        return {"kind": "selfhost", "id": spec_id,
                "ok": promotable, "dir": dest,
                "winner": tournament["winner"], "receipt": receipt}
    finally:
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force",
                        lane_path], capture_output=True)
        subprocess.run(["git", "-C", repo, "branch", "-D", lane],
                       capture_output=True)


def _validator_files(spec):
    return [n.split("::")[0] for n in spec.get("test_nodes", [])]


def _validator_touched(repo, base_sha, candidate_sha, spec):
    """True if the candidate modified any validator/test file (disqualify:
    lanes may not edit frozen acceptance)."""
    try:
        out = _git(repo, "diff", "--name-only",
                   base_sha + ".." + candidate_sha)
    except RuntimeError:
        return True
    changed = set(out.splitlines())
    return any(f in changed for f in _validator_files(spec))


def _validate_detached(repo, spec, candidate_sha, base_sha):
    """Fresh detached worktree at EXACTLY candidate_sha; frozen validator
    files pinned from base; pytest nodes run there. Returns
    (ok_all, results, vpath-before-cleanup... ) — vpath is removed before
    return; head/tree recorded while it exists."""
    vpath = "/tmp/agentcom-validate-%s" % candidate_sha[:12]
    subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", vpath],
                   capture_output=True)
    _git(repo, "worktree", "add", "--detach", vpath, candidate_sha)
    vinfo = {"head": _git(vpath, "rev-parse", "HEAD"),
             "tree": _git(vpath, "rev-parse", "HEAD^{tree}")}
    try:
        if _git(vpath, "status", "--porcelain"):
            return False, [{"node": "worktree",
                            "passed": False,
                            "tail": "validation worktree not clean"}], vinfo
        if vinfo["head"] != candidate_sha:
            return False, [{"node": "identity",
                            "passed": False,
                            "tail": "head != candidate"}], vinfo
        for f in _validator_files(spec):
            if _git(repo, "rev-parse", "%s:%s" % (candidate_sha, f)) != \
                    _git(repo, "rev-parse", "%s:%s" % (base_sha, f)):
                return False, [{"node": "frozen-validator",
                                "passed": False,
                                "tail": "validator touched: %s" % f}], vinfo
        env = dict(os.environ, PYTHONPATH=":".join([
            os.path.join(vpath, "experiments", "openai_native", "src"),
            os.path.join(vpath, "agentcombuild", "agentloop", "src"), vpath]))
        results, ok_all = [], True
        for node in spec.get("test_nodes", []):
            p = subprocess.run([sys.executable, "-m", "pytest", node, "-q"],
                               capture_output=True, text=True, timeout=300,
                               cwd=vpath, env=env)
            passed = p.returncode == 0
            ok_all = ok_all and passed
            results.append({"node": node, "passed": passed,
                            "tail": (p.stdout + p.stderr)[-300:]})
        return ok_all, results, vinfo
    finally:
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force",
                        vpath], capture_output=True)


def build(spec_path, out_root=None):
    """Kind-dispatched build. Returns a JSON-serializable report."""
    spec = load_spec(spec_path)
    kind = spec["kind"]
    if kind == "product":
        from agentcom import build_product
        return dict(build_product.build(
            spec_path, out_root or os.path.join(ROOT, "dist")),
            kind="product")
    if kind == "selfhost":
        return dict(build_selfhost(spec, out_root or ROOT), kind="selfhost")
    raise ValueError("unknown spec kind:%s" % (kind,))
