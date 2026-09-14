"""agentcom build tests: product pipeline + selfhost + CLI e2e."""
import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)

from agentcom import build as _build  # noqa: E402
from agentcom import build_product as _prod  # noqa: E402

SPEC = os.path.join(ROOT, "specs", "agentcom-uk-business-profile.json")
SELFHOST = os.path.join(ROOT, "specs", "selfhost",
                        "readback-before-settlement.json")


def test_product_build_dag_counts(tmp_path):
    r = _prod.build(SPEC, str(tmp_path))
    assert r["ok"] is True
    assert (r["dag"]["true"], r["dag"]["unknown"], r["dag"]["false"]) == \
        (13, 3, 0)
    assert r["world_codes"]  # world-dependent gates recorded, not waived
    assert os.path.exists(os.path.join(
        str(tmp_path), "dist", "plugins", "agentcom-uk", "plugin.json"))
    assert os.path.exists(os.path.join(
        str(tmp_path), "dist", "plugins", "agentcom-uk", "catalog.json"))
    assert os.path.exists(os.path.join(
        str(tmp_path), "dist", "plugins", "agentcom-uk", "skills",
        "business-operator", "SKILL.md"))


def test_product_host_leaves_unknown(tmp_path):
    r = _prod.build(SPEC, str(tmp_path))
    by_id = {l["id"]: l["value"] for l in r["dag"]["leaves"]}
    assert by_id["host-install"] == "UNKNOWN"
    assert by_id["host-invocation"] == "UNKNOWN"
    assert by_id["lint-final-gates"] == "UNKNOWN"


def test_product_latency_recorded(tmp_path):
    r = _prod.build(SPEC, str(tmp_path))
    assert isinstance(r["latency_ms"], int) and r["latency_ms"] >= 0


def test_selfhost_build_banks_artifacts(tmp_path):
    """Validation-only run against a pristine worktree of THIS repo:
    artifacts banked, receipt carries exact SHAs, nothing promoted
    (no worker ran — a validation run is not a build)."""
    import subprocess as _sp
    wt = str(tmp_path / "wt-clean")
    base = _sp.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                   capture_output=True, text=True).stdout.strip()
    _sp.run(["git", "-C", ROOT, "worktree", "add", "--detach", wt, base],
            check=True, capture_output=True)
    try:
        r = _build.build_selfhost(
            dict(json.load(open(SELFHOST))), str(tmp_path / "out"),
            repo=wt, worker_fn=None, work_parent=str(tmp_path / "lanes"))
    finally:
        _sp.run(["git", "-C", ROOT, "worktree", "remove", "--force", wt],
                capture_output=True)
    assert r["receipt"]["base_sha"] == base
    for name in ("contract.json", "candidates.json", "receipts.json",
                 "tournament.json", "promoted.json"):
        assert os.path.exists(os.path.join(r["dir"], name)), name
    promo = json.load(open(os.path.join(r["dir"], "promoted.json")))
    assert promo["state"] == "REFUSED"  # no worker, no change, no promotion
    assert "no-change" in promo["reason"]


def test_selfhost_refuses_dirty_base(tmp_path):
    import subprocess as _sp
    repo = str(tmp_path / "r")
    os.makedirs(repo)
    _sp.run(["git", "init"], capture_output=True, cwd=repo)
    _sp.run(["git", "config", "user.email", "t@t"], capture_output=True,
            cwd=repo)
    _sp.run(["git", "config", "user.name", "t"], capture_output=True, cwd=repo)
    open(os.path.join(repo, "f.txt"), "w").write("x")
    _sp.run(["git", "add", "-A"], capture_output=True, cwd=repo)
    _sp.run(["git", "commit", "-m", "b"], capture_output=True, cwd=repo)
    open(os.path.join(repo, "dirty.txt"), "w").write("uncommitted")
    with pytest.raises(RuntimeError, match="dirty"):
        _build.build_selfhost(
            {"kind": "selfhost", "id": "t", "contract": "c",
             "test_nodes": [], "policy_id": "direct"},
            str(tmp_path / "out"), repo=repo,
            work_parent=str(tmp_path / "lanes"))


def test_cli_end_to_end_product(tmp_path):
    p = subprocess.run(
        [sys.executable, "-m", "agentcom.cli", "build", SPEC,
         "--out", str(tmp_path)], capture_output=True, text=True, timeout=300,
        cwd=ROOT, env=dict(os.environ, PYTHONPATH=ROOT))
    assert p.returncode == 3, p.stdout[-500:] + p.stderr[-500:]  # LOCAL_PASS
    assert "13 TRUE / 3 UNKNOWN / 0 FALSE" in p.stdout
    assert "status: LOCAL_PASS" in p.stdout
    assert "Artifact:" in p.stdout
    p = subprocess.run(
        [sys.executable, "-m", "agentcom.cli", "build", SPEC,
         "--out", str(tmp_path), "--stage", "local"],
        capture_output=True, text=True, timeout=300,
        cwd=ROOT, env=dict(os.environ, PYTHONPATH=ROOT))
    assert p.returncode == 0, p.stdout[-500:] + p.stderr[-500:]


def test_cli_refuses_bad_spec(tmp_path):
    bad = os.path.join(str(tmp_path), "bad.json")
    json.dump({"nope": 1}, open(bad, "w"))
    p = subprocess.run(
        [sys.executable, "-m", "agentcom.cli", "build", bad],
        capture_output=True, text=True, timeout=60,
        cwd=ROOT, env=dict(os.environ, PYTHONPATH=ROOT))
    assert p.returncode == 2 and "REFUSED" in p.stdout


# ---- P0 candidate identity (fixture repos only, never /agentcomfinal) ----

def _fixture_repo(path):
    import subprocess as _sp
    os.makedirs(path, exist_ok=True)
    for args in (["init"], ["config", "user.email", "t@t"],
                 ["config", "user.name", "t"]):
        r = _sp.run(["git", "init"] if args == ["init"] else ["git"] + args,
                    capture_output=True, cwd=path)
        assert r.returncode == 0
    os.makedirs(os.path.join(path, "tests"), exist_ok=True)
    open(os.path.join(path, "tests", "test_frozen.py"), "w").write(
        "def test_ok():\n    assert True\n")
    r = _sp.run(["git", "add", "-A"], capture_output=True, cwd=path)
    assert r.returncode == 0
    r = _sp.run(["git", "commit", "-m", "base"], capture_output=True, cwd=path)
    assert r.returncode == 0
    return path


def _spec():
    return {"kind": "selfhost", "id": "t", "contract": "test-contract",
            "test_nodes": ["tests/test_frozen.py::test_ok"],
            "policy_id": "direct"}


def _fixing_worker(repo):
    def worker(worktree):
        with open(os.path.join(worktree, "FIX.txt"), "w") as fh:
            fh.write("the fix\n")
        return {"commit_paths": ["FIX.txt"], "message": "exp: the fix"}
    return worker


def test_dirty_tree_cannot_be_promoted(tmp_path):
    from agentcom import build as _b
    repo = _fixture_repo(str(tmp_path / "r"))

    def dirty_worker(worktree):
        with open(os.path.join(worktree, "DIRTY.txt"), "w") as fh:
            fh.write("uncommitted\n")
        return {}

    out = _b.build_selfhost(_spec(), str(tmp_path / "out"), repo=repo,
                            worker_fn=dirty_worker,
                            work_parent=str(tmp_path / "wt"))
    assert out["ok"] is False
    assert out["receipt"]["verdict"] == "REFUSED"
    assert "dirty" in out["receipt"]["reason"]


def test_candidate_sha_must_contain_fix(tmp_path):
    import subprocess as _sp
    from agentcom import build as _b
    repo = _fixture_repo(str(tmp_path / "r"))
    out = _b.build_selfhost(_spec(), str(tmp_path / "out"), repo=repo,
                            worker_fn=_fixing_worker(repo),
                            work_parent=str(tmp_path / "wt"))
    assert out["ok"] is True
    sha = out["receipt"]["candidate_sha"]
    assert sha != out["receipt"]["base_sha"]
    shown = _sp.run(["git", "-C", repo, "show", sha + ":FIX.txt"],
                    capture_output=True, text=True)
    assert shown.stdout.strip() == "the fix"


def test_validator_runs_detached_at_candidate_sha(tmp_path):
    from agentcom import build as _b
    repo = _fixture_repo(str(tmp_path / "r"))
    out = _b.build_selfhost(_spec(), str(tmp_path / "out"), repo=repo,
                            worker_fn=_fixing_worker(repo),
                            work_parent=str(tmp_path / "wt"))
    r = out["receipt"]
    assert r["validation_worktree_head"] == r["candidate_sha"]
    import subprocess as _sp
    tree = _sp.run(["git", "-C", repo, "rev-parse",
                    r["candidate_sha"] + "^{tree}"],
                   capture_output=True, text=True).stdout.strip()
    assert r["candidate_tree_sha"] == tree


def test_receipt_sha_matches_validation_sha(tmp_path):
    import subprocess as _sp
    from agentcom import build as _b
    repo = _fixture_repo(str(tmp_path / "r"))
    out = _b.build_selfhost(_spec(), str(tmp_path / "out"), repo=repo,
                            worker_fn=_fixing_worker(repo),
                            work_parent=str(tmp_path / "wt"))
    r = out["receipt"]
    assert r["candidate_sha"] == r["validation_worktree_head"]
    assert r["candidate_tree_sha"] == r["validation_worktree_tree"]
    assert r["diff_stat"] != ""  # nonempty diff proven
    assert out["winner"] == "direct"


def test_validator_touch_disqualifies(tmp_path):
    from agentcom import build as _b
    repo = _fixture_repo(str(tmp_path / "r"))

    def evil_worker(worktree):
        with open(os.path.join(worktree, "tests", "test_frozen.py"),
                  "w") as fh:
            fh.write("def test_ok():\n    assert True  # touched\n")
        return {"commit_paths": ["tests/test_frozen.py"],
                "message": "exp: touch validator"}

    out = _b.build_selfhost(_spec(), str(tmp_path / "out"), repo=repo,
                            worker_fn=evil_worker,
                            work_parent=str(tmp_path / "wt"))
    assert out["ok"] is False
    assert out["winner"] is None
    assert any("frozen-validator" in r.get("tail", "")
               for r in out["receipt"]["results"])

