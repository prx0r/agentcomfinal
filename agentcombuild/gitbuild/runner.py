"""Gitbuild runner: git as the experiment substrate (gitbuild1 §D–J).

Lanes are branches + worktrees off a frozen base. Validation runs in a
detached worktree at the exact candidate SHA against the FROZEN evaluator
(never the lane's edited copy). Receipts record base/candidate/tree SHAs +
diff; tournaments pick winners gates-first; notes attach metadata
(noncanonical index); promotion merges (never force) and tags.

Builder rules enforced by convention + tests: one lane = one branch +
one worktree, explicit paths, no force-push, no self-merge.
"""
import json
import os
import subprocess
import time


class GitError(RuntimeError):
    pass


def sh(repo, *args, timeout=120):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                       text=True, timeout=timeout)
    if p.returncode != 0:
        raise GitError("git %s: %s" % (" ".join(args),
                                       (p.stderr or p.stdout)[:300]))
    return p.stdout.strip()


def head_sha(repo):
    return sh(repo, "rev-parse", "HEAD")


def tree_sha(repo, rev="HEAD"):
    return sh(repo, "rev-parse", rev + "^{tree}")


def new_lane(repo, base_sha, name, contract):
    """Create branch exp/<contract>/<name> + worktree. Returns worktree path."""
    branch = "exp/%s/%s" % (contract, name)
    path = "/tmp/agentcom-%s-%s" % (os.getpid(), name)
    try:
        sh(repo, "branch", "-D", branch)
    except GitError:
        pass
    sh(repo, "branch", branch, base_sha)
    sh(repo, "worktree", "add", path, branch)
    return path


def remove_lane(repo, path, branch, keep_branch=True):
    sh(repo, "worktree", "remove", "--force", path)
    if not keep_branch:
        try:
            sh(repo, "branch", "-D", branch)
        except GitError:
            pass


def file_sha(repo, rev, path):
    return sh(repo, "rev-parse", "%s:%s" % (rev, path))


def validate_candidate(repo, candidate_sha, test_cmd, contract_root,
                       policy_id, base_sha, validator_files=(), env=None):
    """Frozen-evaluator validation in a DETACHED worktree at candidate_sha.
    validator_files: {path: expected_sha} pinned from the protected side —
    mismatch means the lane touched the validator (disqualify). Returns a
    run receipt (pass/fail + SHAs + diff + cost)."""
    vpath = "/tmp/validate-%s" % candidate_sha[:12]
    subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", vpath],
                   capture_output=True)
    sh(repo, "worktree", "add", "--detach", vpath, candidate_sha)
    try:
        for fpath, expected in (validator_files or ()):
            got = sh(repo, "rev-parse", "%s:%s" % (candidate_sha, fpath))
            if got != expected:
                return {"base_sha": base_sha, "candidate_sha": candidate_sha,
                        "contract_root": contract_root, "policy_id": policy_id,
                        "verdict": "DISQUALIFIED",
                        "reason": "validator-touched:%s" % fpath}
        t0 = time.monotonic()
        p = subprocess.run(test_cmd, capture_output=True, text=True,
                           timeout=600, cwd=vpath, env=env)
        wall_ms = int((time.monotonic() - t0) * 1000)
        tail = (p.stdout + p.stderr).strip().splitlines()[-5:]
        verdict = "PASS" if p.returncode == 0 else "FAIL"
    finally:
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force",
                        vpath], capture_output=True)
    return {"base_sha": base_sha, "candidate_sha": candidate_sha,
            "candidate_tree": tree_sha(repo, candidate_sha),
            "contract_root": contract_root, "policy_id": policy_id,
            "verdict": verdict, "returncode": p.returncode,
            "tail": tail, "cost": {"wall_ms": wall_ms},
            "diff_stat": sh(repo, "diff", "--stat",
                            base_sha + ".." + candidate_sha)}


def tournament(receipts):
    """Gates-first, then cheapest. Returns {winner, ranking, failures}."""
    ok = [r for r in receipts if r.get("verdict") == "PASS"]
    ranked = sorted(ok, key=lambda r: (r.get("cost", {}).get("wall_ms", 0),
                                       r.get("candidate_sha", "")))
    rest = sorted([r for r in receipts if r.get("verdict") != "PASS"],
                  key=lambda r: r.get("candidate_sha", ""))
    ranking = [(r["candidate_sha"][:12], r["verdict"]) for r in ranked + rest]
    return {"winner": (ranked[0]["candidate_sha"] if ranked else None),
            "ranking": ranking,
            "failures": [{"sha": r["candidate_sha"][:12],
                          "verdict": r["verdict"],
                          "reason": r.get("reason", ""),
                          "tail": r.get("tail", [])} for r in rest]}


def write_note(repo, sha, ref, message):
    sh(repo, "notes", "--ref=" + ref, "add", "-f", "-m", message, sha)
    return True


def read_note(repo, sha, ref):
    try:
        return sh(repo, "notes", "--ref=" + ref, "show", sha)
    except GitError:
        return ""


def promote(repo, sha, tag=None):
    """Merge winner (ff preferred, never force), then tag. Returns tag."""
    base = head_sha(repo)
    try:
        sh(repo, "merge", "--ff-only", sha)
    except GitError:
        sh(repo, "merge", "--no-ff", "-m", "promote: %s" % sha[:12], sha)
    if tag:
        sh(repo, "tag", "-a", tag, "-m", "proven state %s" % sha[:12])
    return {"merged": sha[:12], "previous_head": base[:12],
            "new_head": head_sha(repo)[:12], "tag": tag}
