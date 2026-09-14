"""ab1 proof suite. Each test maps to VALIDATION.md criterion 1-7."""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ab1 import gates, receipts, seesaw, specgate  # noqa: E402
from ab1.canonical import canonical, obj_id  # noqa: E402
from ab1.store import Store  # noqa: E402

NOW = "2026-09-14T00:00:00Z"
EX = os.path.join(os.path.dirname(__file__), "..", "examples")


def good_plan():
    with open(os.path.join(EX, "breadup_plan.json")) as fh:
        return json.load(fh)


def good_ev():
    with open(os.path.join(EX, "breadup_evidence.json")) as fh:
        return json.load(fh)


# 1. determinism
def test_canonical_byte_identical():
    a = {"z": 1, "a": [3, 2, {"y": "x"}]}
    assert canonical(a) == canonical(json.loads(json.dumps(a)))
    assert obj_id("t", a) == obj_id("t", dict(reversed(list(a.items()))))


# 3. no trust-only work
def test_plan_rejects_missing_acceptance():
    p = good_plan()
    del p["goal"]["acceptance"]
    v = specgate.check_plan(p)
    assert not v["ok"] and any("acceptance" in e for e in v["errors"])


def test_plan_rejects_trust_only_feature():
    p = good_plan()
    p["features"][0]["evidence"] = []
    v = specgate.check_plan(p)
    assert not v["ok"] and any("trust-only" in e for e in v["errors"])


def test_plugin_lint():
    bad = {"name": "x", "tools": [{"name": "t"}]}
    assert not specgate.check_plugin(bad)["ok"]  # no version/description
    ok = {"name": "x", "version": "0.1",
          "tools": [{"name": "t", "description": "d"}]}
    assert specgate.check_plugin(ok)["ok"]


# 6. seesaw sane
def test_seesaw_ordering():
    proj = seesaw.score_project(good_plan()["features"])
    by_id = {s["id"]: s for s in proj["scores"]}
    assert by_id["photo-valuation-crosslist"]["action"] == "OWN"
    assert by_id["photo-valuation-crosslist"]["S"] > by_id["listing-copy"]["S"]
    assert proj["binding"] == "photo-valuation-crosslist"
    assert proj["value"] == pytest.approx(217.01)


def test_substitutable_never_own():
    proj = seesaw.score_project(good_plan()["features"])
    by_id = {s["id"]: s for s in proj["scores"]}
    assert by_id["listing-copy"]["action"] == "REUSE"
    assert by_id["generic-dashboard"]["action"] == "DROP"


def test_ai_exposure():
    assert seesaw.ai_exposure(5, 2) == "TIGHTENS"
    assert seesaw.ai_exposure(1, 4) == "RELAXES"
    assert seesaw.ai_exposure(2, 2) == "NEUTRAL"


# 2. fail closed
def test_unknown_gate():
    assert gates.execute("nope-v9", {})["verdict"] == "FAIL"


def test_raising_gate():
    gates.register("boom-v1", "raise", lambda i: 1 / 0)
    r = gates.execute("boom-v1", {})
    assert r["verdict"] == "FAIL" and r["proof"].startswith("raised:")
    del gates.REGISTRY["boom-v1"]


def test_missing_evidence_gate():
    r = gates.execute("two-sources-v1", {"sources": [{"id": "only"}]})
    assert r["verdict"] == "FAIL"


def test_gate_threshold():
    assert gates.execute("score-threshold-v1",
                         {"value": 217.01, "min": 100})["verdict"] == "PASS"
    assert gates.execute("score-threshold-v1",
                         {"value": 10, "min": 100})["verdict"] == "FAIL"


# 4. receipts
def _build(pass_min=100.0):
    plan, ev = good_plan(), good_ev()
    proj = seesaw.score_project(plan["features"])
    calls = [("specgate-v1", {"spec_verdict": specgate.check_plan(plan)}),
             ("evidence-declared-v1", {"features": plan["features"]}),
             ("two-sources-v1", {"sources": ev["sources"]}),
             ("score-threshold-v1", {"value": proj["value"], "min": pass_min}),
             ("no-duplicate-v1", {"items": [f["id"] for f in
                                            plan["features"]]})]
    return receipts.transition("BUILD", plan["id"], {"cursor": 0, "projects": {}},
                               {"cursor": 1}, {"sources": ev["sources"]},
                               calls, NOW)


def test_receipt_pass():
    r = _build()
    assert r["passed"] and r["state_after"] == {"cursor": 1}
    assert receipts.verify(r)


def test_fail_keeps_state():
    r = _build(pass_min=10**9)
    assert not r["passed"] and r["state_after"] == {"cursor": 0, "projects": {}}
    assert receipts.verify(r)  # FAIL receipts verify too


def test_tamper_fails():
    r = _build()
    r["proposal"] = {"cursor": 999}
    assert not receipts.verify(r)


# 5. store
def test_store_chain(tmp_path):
    s = Store(str(tmp_path / "chain.jsonl"))
    s.append(_build()); s.append(_build(pass_min=10**9))
    assert s.verify_chain()


def test_store_evil_line(tmp_path):
    p = str(tmp_path / "chain.jsonl")
    s = Store(p)
    s.append(_build()); s.append(_build())
    with open(p, "a") as fh:
        fh.write('{"prev":"LIES","receipt":{"id":"receipt:zzz"}}\n')
    assert not s.verify_chain()


# 1. end-to-end determinism
def test_determinism():
    assert (canonical(_build()).decode()
            == canonical(_build()).decode())
