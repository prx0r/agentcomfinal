"""agentloop proof suite: records enforced, seeker honest, compiler compounds."""
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "autobuild1", "src")))

from loop import compile as comp  # noqa: E402
from loop import research, runlog, seeker  # noqa: E402


def good_record():
    r = runlog.new_run("demo-proj", "autobuild3")
    r["working"] = [{"claim": "stoplight judges", "validation": "29/29 pytest"}]
    r["not_working"] = [{"claim": "wasm judges", "failure": "no runtime",
                         "fixture": "attempt deferred to ab4"}]
    r["next10"] = [{"task": "task-%d" % i, "justification": "why-%d" % i,
                    "impact": (i % 5) + 1} for i in range(10)]
    r["visionary"] = [{"idea": "idea-%d" % i, "endgame_link": "endgame",
                       "falsifier": "fals-%d" % i} for i in range(2)]
    return r


def test_good_record_validates():
    ok, reasons = runlog.check_record(good_record())
    assert ok, reasons


def test_next10_count_enforced():
    r = good_record()
    r["next10"] = r["next10"][:9]
    ok, reasons = runlog.check_record(r)
    assert not ok and any("exactly 10" in x for x in reasons)
    r = good_record()
    r["next10"] = r["next10"] + [{"task": "extra", "justification": "j",
                                  "impact": 1}]
    ok, reasons = runlog.check_record(r)
    assert not ok and any("exactly 10" in x for x in reasons)


def test_visionary_required():
    r = good_record()
    r["visionary"] = []
    ok, _ = runlog.check_record(r)
    assert not ok


def test_working_needs_validation():
    r = good_record()
    r["working"] = [{"claim": "vibes"}]
    ok, _ = runlog.check_record(r)
    assert not ok


def test_failure_needs_fixture():
    r = good_record()
    r["not_working"] = [{"claim": "x", "failure": "y"}]
    ok, _ = runlog.check_record(r)
    assert not ok


def test_impact_range():
    r = good_record()
    r["next10"][0]["impact"] = 9
    ok, _ = runlog.check_record(r)
    assert not ok


def test_append_rejects_and_roundtrips(tmp_path):
    p = str(tmp_path / "runs.jsonl")
    with pytest.raises(runlog.BadRecord):
        runlog.append(p, {"nope": True})
    assert runlog.load_all(p) == []
    rid = runlog.append(p, good_record())
    assert runlog.load_all(p)[0]["run_id"] == rid


class FakeBackend(research.Backend):
    name = "fake"

    def __init__(self, hits=None, boom=False):
        self._hits, self._boom = hits, boom

    def search(self, query):
        if self._boom:
            raise ValueError("net-down")
        return self._hits if self._hits is not None else [
            {"source": "fake", "url": "fake://a", "summary": "hit A"},
            {"source": "fake", "url": "fake://b", "summary": "hit B"}]


PROBLEM = {"invariant_id": "ACT5", "context": "readback channels",
           "acceptance": "independent channel agrees"}


def test_seeker_picks_winner_and_logs_all():
    logged = []
    v = seeker.seek(PROBLEM, [FakeBackend()],
                    lambda c: {"verdict": "PASS" if c["id"] == "cand-1" else "FAIL",
                               "reasons": ["sim"]},
                    logged.append)
    assert v["winner"] == "cand-1" and v["logged"] == 3
    assert [r["verdict"] for r in v["results"]] == ["FAIL", "PASS", "FAIL"]


def test_seeker_all_fail_honest():
    logged = []
    v = seeker.seek(PROBLEM, [FakeBackend()],
                    lambda c: {"verdict": "FAIL", "reasons": ["nope"]},
                    logged.append)
    assert v["winner"] is None and v["logged"] == 3


def test_seeker_backend_error_recorded():
    logged = []
    v = seeker.seek(PROBLEM, [FakeBackend(boom=True)], lambda c: {"verdict": "FAIL", "reasons": []}, logged.append)
    assert len(v["candidates"]) == 3 and v["research_errors"]
    assert v["research_errors"][0]["backend"] == "fake"


def test_seeker_validator_raise_captured():
    def boom(c):
        raise RuntimeError("judge exploded")
    v = seeker.seek(PROBLEM, [FakeBackend()], boom, lambda e: None)
    assert all(r["verdict"] == "FAIL" for r in v["results"])


def test_sim_backend_deterministic():
    b = research.SimBackend()
    assert b.search("readback channels") == b.search("readback channels")


def test_compile_banks_20_by_run4():
    recs = []
    for run in range(4):
        r = good_record()
        r["run_id"] = "run:%d" % run
        r["visionary"] = [{"idea": "vision-run%d-%d" % (run, i),
                           "endgame_link": "endgame proof DAG",
                           "falsifier": "fals"} for i in range(5)]
        recs.append(r)
    out = comp.compile_runs(recs)
    assert out["stats"] == {"runs": 4, "ideas": 20, "failures_banked": 4,
                            "tasks_proposed": 40}
    assert len(out["ideas_bank"]) == 20


def test_compile_merges_leaderboard():
    a, b = good_record(), good_record()
    a["run_id"], b["run_id"] = "run:a", "run:b"
    for r in (a, b):
        for t in r["next10"]:
            t["impact"] = 1
    a["next10"][0] = {"task": "Ship readback gate", "justification": "j1", "impact": 5}
    b["next10"][0] = {"task": "ship READBACK gate ", "justification": "j2", "impact": 4}
    out = comp.compile_runs([a, b])
    top = out["next10"][0]
    assert top["task"] == "Ship readback gate" and top["impact"] == 9
    assert top["runs"] == ["run:a", "run:b"]


def test_tags_deterministic():
    assert comp.tag("endgame proof DAG library") == comp.tag("endgame proof DAG library")
    assert "endgame" in comp.tag("vision of the endgame horizon")
