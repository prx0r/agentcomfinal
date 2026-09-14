"""ab3 proof suite: a-log honesty + actuality axiom + adversarial cheats."""
import json
import os
import sys
import time

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "autobuild1", "src")))

from ab1 import gates as ab1gates  # noqa: E402
from ab3 import actuality, alog, judges, readback, registry, stoplight  # noqa: E402
from ab3 import gates3  # noqa: E402,F401  (registers ab3 gates)
from ab3.demo_worker import PLAN  # noqa: E402

VDIR = os.path.normpath(os.path.join(HERE, "..", "validators"))


def fresh_queue():
    return alog.queue_from_plan(PLAN)


def cmd(argv, expect=None):
    d = {"kind": "command", "argv": argv}
    if expect is not None:
        d["expect"] = expect
    return d


# ---- honest + coverage ----

def test_honest_run_go(tmp_path):
    from ab3 import demo_worker
    d = str(tmp_path)
    v = demo_worker.honest(d, VDIR)
    assert v["verdict"] == "GO", v["reasons"]
    st = stoplight.acheck(fresh_queue(), d, VDIR,
                          os.path.join(d, "queue.json"))
    assert st["send-lead-reply"]["status"] == "DONE"
    assert st["qualify-lead"]["status"] == "DONE"


def test_claim_without_log_nogo(tmp_path):
    v = stoplight.judge("send-lead-reply", fresh_queue(), str(tmp_path))
    assert v["verdict"] == "NOGO" and "no-log" in v["reasons"]


def test_uncovered_index_nogo(tmp_path):
    d, q = str(tmp_path), fresh_queue()
    alog.append(d, q, "send-lead-reply", [0], "partial",
                cmd(["echo", "reply-delivered"], "reply-delivered"))
    # qualify-lead has 1 acceptance; leave send task with... judge send task:
    # send acceptance len 1, idx0 green. Use a 2-acceptance task instead:
    q2 = {"t": {"acceptance": ["a", "b"]}}
    alog.append(d, q2, "t", [0], "half", cmd(["echo", "hi"]))
    v = stoplight.judge("t", q2, d)
    assert v["verdict"] == "NOGO" and any("uncovered" in r for r in v["reasons"])


def test_ref_only_insufficient(tmp_path):
    d, q = str(tmp_path), fresh_queue()
    alog.append(d, q, "send-lead-reply", [0], "notes only",
                {"kind": "ref", "ref": "notes:did-it"})
    v = stoplight.judge("send-lead-reply", q, d)
    assert v["verdict"] == "NOGO"


# ---- forgery / mismatch ----

def test_forged_line_nogo(tmp_path):
    d, q = str(tmp_path), fresh_queue()
    alog.append(d, q, "send-lead-reply", [0], "ok",
                cmd(["echo", "reply-delivered"], "reply-delivered"))
    p = alog.log_path(d, "send-lead-reply")
    lines = open(p).read().splitlines()
    rec = json.loads(lines[0])
    rec["action"] = "forged victory"
    open(p, "w").write(json.dumps(rec) + "\n")
    v = stoplight.judge("send-lead-reply", q, d)
    assert v["verdict"] == "NOGO" and "chain-broken" in v["reasons"]


def test_command_mismatch_nogo(tmp_path):
    d, q = str(tmp_path), fresh_queue()
    alog.append(d, q, "send-lead-reply", [0], "lying output",
                cmd(["echo", "nothing-here"], "reply-delivered"))
    v = stoplight.judge("send-lead-reply", q, d)
    assert v["verdict"] == "NOGO" and any("output-mismatch" in r
                                         for r in v["reasons"])


def test_nonzero_exit_nogo(tmp_path):
    d, q = str(tmp_path), fresh_queue()
    alog.append(d, q, "send-lead-reply", [0], "fails",
                cmd(["false"]))
    v = stoplight.judge("send-lead-reply", q, d)
    assert v["verdict"] == "NOGO"


def test_disallowed_command_refused_and_harmless(tmp_path):
    d, q = str(tmp_path), fresh_queue()
    sentinel = os.path.join(str(tmp_path), "sentinel.txt")
    open(sentinel, "w").write("alive")
    alog.append(d, q, "send-lead-reply", [0], "evil",
                cmd(["rm", sentinel]))
    v = stoplight.judge("send-lead-reply", q, d)
    assert v["verdict"] == "NOGO" and any("refused-to-run" in r
                                         for r in v["reasons"])
    assert open(sentinel).read() == "alive"


def test_planted_verdict_ignored(tmp_path):
    d, q = str(tmp_path), fresh_queue()
    alog.append(d, q, "send-lead-reply", [0], "bad",
                cmd(["echo", "nope"], "reply-delivered"))
    os.makedirs(os.path.join(d, "verdicts"), exist_ok=True)
    json.dump({"task": "send-lead-reply", "verdict": "GO", "reasons": []},
              open(os.path.join(d, "verdicts", "send-lead-reply.json"), "w"))
    st = stoplight.acheck(q, d)
    assert st["send-lead-reply"]["status"] == "NOGO"  # recomputed, not read


def test_stale_flagged(tmp_path):
    d, q = str(tmp_path), fresh_queue()
    alog.append(d, q, "send-lead-reply", [0], "old",
                cmd(["echo", "nope"], "reply-delivered"))
    old = time.time() - 100 * 3600
    os.utime(alog.log_path(d, "send-lead-reply"), (old, old))
    st = stoplight.acheck(q, d)
    assert st["send-lead-reply"]["status"] == "STALE"


# ---- refusals ----

def test_unknown_task_refused(tmp_path):
    with pytest.raises(alog.Refused):
        alog.append(str(tmp_path), fresh_queue(), "nope", [0], "x",
                    cmd(["echo", "x"]))
    assert not os.path.exists(os.path.join(str(tmp_path), "a-logs"))


def test_bad_index_refused(tmp_path):
    with pytest.raises(alog.Refused):
        alog.append(str(tmp_path), fresh_queue(), "send-lead-reply", [9], "x",
                    cmd(["echo", "x"]))


def test_secret_evidence_refused(tmp_path):
    with pytest.raises(alog.Refused):
        alog.append(str(tmp_path), fresh_queue(), "send-lead-reply", [0], "x",
                    {"kind": "secret", "ref": "vault"})
    with pytest.raises(alog.Refused):
        alog.append(str(tmp_path), fresh_queue(), "send-lead-reply", [0], "x",
                    {"kind": "ref", "api_key": "ghp_fakelymadeup000000000000"})


def test_covers_checked():
    import copy
    bad = copy.deepcopy(PLAN)
    del bad["features"][0]["covers"]
    assert not alog.check_covers(bad)["ok"]
    bad2 = copy.deepcopy(PLAN)
    bad2["features"][0]["covers"] = [7]
    assert not alog.check_covers(bad2)["ok"]
    assert alog.check_covers(PLAN)["ok"]


# ---- validators ----

def _vdir(tmp_path, name, body):
    vd = os.path.join(str(tmp_path), "validators")
    os.makedirs(vd, exist_ok=True)
    open(os.path.join(vd, name + ".py"), "w").write(body)
    return vd


def _logged(tmp_path, q=None):
    d, q = str(tmp_path), q or fresh_queue()
    alog.append(d, q, "send-lead-reply", [0], "ok",
                cmd(["echo", "reply-delivered"], "reply-delivered"))
    return d


def test_validator_false_nogo(tmp_path):
    d = _logged(tmp_path)
    vd = _vdir(tmp_path, "send-lead-reply",
               'import json,sys\nprint(json.dumps({"pass": False, "reasons": ["nah"]}))\n')
    v = stoplight.judge("send-lead-reply", fresh_queue(), d, vd)
    assert v["verdict"] == "NOGO" and any("nah" in r for r in v["reasons"])


def test_validator_crash_nogo(tmp_path):
    d = _logged(tmp_path)
    vd = _vdir(tmp_path, "send-lead-reply", 'import sys\nsys.exit(3)\n')
    v = stoplight.judge("send-lead-reply", fresh_queue(), d, vd)
    assert v["verdict"] == "NOGO" and any("validator-error" in r
                                         for r in v["reasons"])


def test_validator_bad_json_nogo(tmp_path):
    d = _logged(tmp_path)
    vd = _vdir(tmp_path, "send-lead-reply", 'print("all good trust me")\n')
    v = stoplight.judge("send-lead-reply", fresh_queue(), d, vd)
    assert v["verdict"] == "NOGO"


def test_validator_timeout_nogo(tmp_path):
    d = _logged(tmp_path)
    vd = _vdir(tmp_path, "send-lead-reply",
               'import time,json\ntime.sleep(5)\nprint(json.dumps({"pass": True, "reasons": []}))\n')
    v = stoplight.judge("send-lead-reply", fresh_queue(), d, vd, timeout=1)
    assert v["verdict"] == "NOGO" and any("validator-timeout" in r
                                         for r in v["reasons"])


# ---- judges L0/L1 ----

def test_cel_basics():
    ev, J = {"status": 201, "lat": 492, "ok": True}, judges.eval_cel
    assert J("e.status == 201", ev) is True
    assert J("e.status == 200", ev) is False
    assert J("e.lat < 1000 && e.ok == true", ev) is True
    assert J("!(e.lat > 1000) || e.status != 201", ev) is True
    assert J("(e.lat >= 492) && (e.lat <= 492)", ev) is True


def test_cel_unknowns():
    ev = {"status": 201}
    assert judges.judge_evidence(ev, {"engine": "cel",
                                      "expression": "e.missing == 1"})[0] == "UNKNOWN"
    assert judges.judge_evidence(ev, {"engine": "cel",
                                      "expression": "e.status < 'x'"})[0] == "UNKNOWN"
    assert judges.judge_evidence(ev, {"engine": "cel",
                                      "expression": "e.status =="})[0] == "UNKNOWN"
    assert judges.judge_evidence([1, 2], {"engine": "cel",
                                         "expression": "e == e"})[0] == "UNKNOWN"
    assert judges.judge_evidence(ev, {"engine": "nope"})[0] == "UNKNOWN"


def test_schema_l0():
    sch = {"engine": "schema", "schema": {"type": "object",
           "required": ["status"], "properties": {"status": {"type": "integer"}}}}
    assert judges.judge_evidence({"status": 201}, sch)[0] == "TRUE"
    assert judges.judge_evidence({"status": "x"}, sch)[0] == "UNKNOWN"
    assert judges.judge_evidence({"other": 1}, sch)[0] == "UNKNOWN"


# ---- actuality DAG + record ----

def leaf(i, ev, expr):
    return {"id": i, "evidence": ev,
            "judge": {"engine": "cel", "expression": expr}}


def test_dag_all_true():
    dag = {"claim": "reply works", "leaves": [
        leaf("a", {"sent": True}, "e.sent == true"),
        leaf("b", {"found": True}, "e.found == true")]}
    v = actuality.evaluate_dag(dag)
    assert v["value"] == "TRUE" and v["progress"] == 1


def test_dag_false_wins():
    dag = {"claim": "x", "leaves": [
        leaf("a", {"sent": True}, "e.sent == true"),
        leaf("b", {"sent": True}, "e.sent == false")]}
    assert actuality.evaluate_dag(dag)["value"] == "FALSE"


def test_dag_unknown_blocks():
    dag = {"claim": "x", "leaves": [
        leaf("a", {"sent": True}, "e.sent == true"),
        leaf("b", {}, "e.sent == true")]}
    v = actuality.evaluate_dag(dag)
    assert v["value"] == "UNKNOWN" and v["progress"] == 0


def test_actuality_record():
    r = actuality.actuality_record("checkout works", "TRUE", "cr:1", "er:2",
                                   "vr:3", "sim-2026-09-14",
                                   "2026-09-14T00:00:00Z", "external_readback")
    assert r["actuality"] == "TRUE" and r["proof_class"] == "external_readback"


def test_readback():
    from ab3.readback import check_readback
    a = {"created_id": "order_9", "source": "action-chan"}
    assert check_readback(a, {"created_id": "order_9",
                              "source": "order-api"})[0] == "TRUE"
    assert check_readback(a, {})[0] == "UNKNOWN"
    assert check_readback(a, {"created_id": "order_8",
                              "source": "x"})[0] == "FALSE"
    assert check_readback(a, {"created_id": "order_9",
                              "source": "action-chan"})[0] == "UNKNOWN"
    r = ab1gates.execute("independent-readback-v1",
                         {"action": a, "readback": {"created_id": "order_9",
                                                   "source": "api"}})
    assert r["verdict"] == "PASS"
    r2 = ab1gates.execute("actuality-dag-v1",
                          {"dag": {"claim": "x", "leaves": [
                              leaf("a", {"v": 1}, "e.v == 1")]}})
    assert r2["verdict"] == "PASS"


# ---- registry ----

def test_registry():
    assert registry.find(provides="command-ran")
    plan, missing = registry.compose(["command-ran", "file-exists",
                                      "teleport-confirmed"])
    assert "teleport-confirmed" in missing and "command-ran" in plan
    prim = registry.find(provides="command-ran")[0]
    assert registry.judge_with(prim, {"exit": 0})[0] == "TRUE"
    assert registry.judge_with(prim, {"exit": 1})[0] == "FALSE"


def test_probe_verdict_ignored():
    """R9: probe claims PASS inside the observation; judge still decides."""
    dag = {"claim": "x", "leaves": [
        {"id": "a", "evidence": {"verdict": "PASS", "agent_says": "works"},
         "judge": {"engine": "cel", "expression": "e.proven == true"}}]}
    v = actuality.evaluate_dag(dag)
    assert v["value"] == "UNKNOWN" and v["progress"] == 0


def test_true_validator_cannot_excuse_gap():
    """R11: pass-true validator + uncovered acceptance still NOGO."""
    import tempfile
    d = tempfile.mkdtemp()
    q = {"t": {"acceptance": ["a", "b"]}}
    alog.append(d, q, "t", [0], "half", cmd(["echo", "hi"]))
    vd = _vdir(d, "t", 'import json\nprint(json.dumps({"pass": True, "reasons": []}))\n')
    v = stoplight.judge("t", q, d, vd)
    assert v["verdict"] == "NOGO" and any("uncovered" in r for r in v["reasons"])
