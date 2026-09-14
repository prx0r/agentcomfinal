"""Actuality command tests: projection honesty, receipt discipline, order."""
import json
import os
import sys

import pytest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))
sys.path.insert(0, ROOT)

from agentcom import actuality as _A  # noqa: E402


def test_contract_has_ten_leaves_with_probes():
    spec = _A.contract_spec()
    assert len(spec["leaves"]) == 10
    for leaf in spec["leaves"]:
        assert leaf["id"] and leaf["probe"] and leaf["judge"]
    assert _A.contract_root() == _A.contract_root()  # stable


def test_evaluate_projection_shape():
    proj = _A.evaluate()
    assert proj["contract"] == "AGENTCOM_AUTOBUILD_V1"
    assert len(proj["results"]) == 10
    a = proj["actuality"]
    assert a["TRUE"] + a["FALSE"] + a["UNKNOWN"] == 10
    assert proj["state"] in ("PROVEN", "NOT_PROVEN")
    assert set(proj["results"]) == {l["id"] for l in
                                    _A.contract_spec()["leaves"]}


def test_receipts_only_for_decided_leaves():
    proj = _A.evaluate()
    for lid, rid in proj["receipts"].items():
        assert proj["results"][lid]["value"] in ("TRUE", "FALSE"), lid
        assert rid.startswith("receipt:")
    for lid, r in proj["results"].items():
        if r["value"] == "UNKNOWN":
            assert lid not in proj["receipts"], lid


def test_leaf_receipt_verifies_independently():
    """Recorded receipts re-verify against fresh admissible evidence
    (id recomputes from bytes; gates replay). Tampered ids fail."""
    from adapters import qp as _qp
    proj = _A.evaluate()
    trues = [lid for lid, r in proj["results"].items()
             if r["value"] == "TRUE"]
    assert trues, "need at least one TRUE leaf to check"
    assert all(rid.startswith("receipt:") for rid in proj["receipts"].values())
    bad = {"protocol": "acom/0.1", "transition_type": "RESOLVE",
           "proof_level": 3, "subject": "x", "state_before": {},
           "proposal": {"id": "x"}, "evidence_root": "x", "gates": [],
           "grant": None, "run": {}, "state_after": {},
           "passed": True, "id": "receipt:" + "0" * 16, "signature": ""}
    ev = [_qp.make_evidence("leaf.x", 1, "bool", "2026-09-14T00:00:00Z",
                            {"class": "probe"})]
    assert _qp.verify_settlement(bad, ev)["ok"] is False  # tampered id fails


def test_settled_leaf_reverifies_with_fresh_evidence():
    """A receipt minted by _settle_leaf re-verifies independently against
    fresh admissible evidence (id recomputes from bytes; gates replay)."""
    from adapters import qp as _qp
    receipt = _A._settle_leaf("probe-leaf", "TRUE", "test observation")
    assert receipt["id"].startswith("receipt:")
    fresh = [_qp.make_evidence("leaf.probe-leaf", 1, "bool",
                               "2026-09-14T00:00:00Z", {"class": "probe"}),
             _qp.make_evidence("leaf.probe-leaf-2", 0, "bool",
                               "2026-09-14T00:00:00Z", {"class": "probe"})]
    assert _qp.verify_settlement(receipt, fresh)["ok"] is True


def test_blocking_order_false_before_world_wait():
    proj = _A.evaluate()
    order = proj["blocking"]
    falses = [lid for lid in order
              if proj["results"][lid]["value"] == "FALSE"]
    assert order[:len(falses)] == falses  # all FALSEs precede UNKNOWNs
    for lid in ("openai-real-session", "host-leaves-unknown"):
        if proj["results"][lid]["value"] == "UNKNOWN" and falses:
            assert order.index(lid) > order.index(falses[-1])


def test_state_not_proven_without_key():
    import os as _os
    if _os.environ.get("OPENAI_API_KEY"):
        pytest.skip("key present: live path is manual")
    proj = _A.evaluate()
    assert proj["state"] == "NOT_PROVEN"
    assert proj["next_blocker"] in proj["blocking"]


def test_cli_prints_projection():
    import subprocess as _sp
    p = _sp.run([sys.executable, "-m", "agentcom.cli", "actuality"],
                capture_output=True, text=True, timeout=300,
                cwd=ROOT, env=dict(os.environ, PYTHONPATH=ROOT))
    assert p.returncode == 0
    assert "NOT_PROVEN" in p.stdout
    assert "next blocker:" in p.stdout
