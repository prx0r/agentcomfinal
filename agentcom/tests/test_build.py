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


def test_selfhost_build_banks_artifacts():
    r = _build.build(SELFHOST)
    assert r["ok"] is True and r["winner"] == "direct"
    for name in ("contract.json", "candidates.json", "receipts.json",
                 "tournament.json", "promoted.json"):
        assert os.path.exists(os.path.join(r["dir"], name)), name
    promo = json.load(open(os.path.join(r["dir"], "promoted.json")))
    assert promo["state"] == "PROMOTED"


def test_cli_end_to_end_product(tmp_path):
    p = subprocess.run(
        [sys.executable, "-m", "agentcom.cli", "build", SPEC,
         "--out", str(tmp_path)], capture_output=True, text=True, timeout=300,
        cwd=ROOT, env=dict(os.environ, PYTHONPATH=ROOT))
    assert p.returncode == 0, p.stdout[-500:] + p.stderr[-500:]
    assert "13 TRUE / 3 UNKNOWN / 0 FALSE" in p.stdout
    assert "Artifact:" in p.stdout


def test_cli_refuses_bad_spec(tmp_path):
    bad = os.path.join(str(tmp_path), "bad.json")
    json.dump({"nope": 1}, open(bad, "w"))
    p = subprocess.run(
        [sys.executable, "-m", "agentcom.cli", "build", bad],
        capture_output=True, text=True, timeout=60,
        cwd=ROOT, env=dict(os.environ, PYTHONPATH=ROOT))
    assert p.returncode == 2 and "REFUSED" in p.stdout
