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
    r["next10"] = []
    ok, reasons = runlog.check_record(r)
    assert not ok and any("1-10" in x for x in reasons)
    r = good_record()
    r["next10"] = r["next10"] + [{"task": "extra", "justification": "j",
                                  "impact": 1}]
    ok, reasons = runlog.check_record(r)
    assert not ok and any("1-10" in x for x in reasons)
    r = good_record()
    r["next10"] = r["next10"][:4]
    ok, reasons = runlog.check_record(r)
    assert ok, reasons


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
                    lambda c: {"verdict": "PASS" if c["solution_id"] == "sol-1" else "FAIL",
                               "reasons": ["sim"]},
                    logged.append)
    assert v["winner"] == "sol-1" and v["logged"] == 3
    # ranked highest-value-first: sol-1 (local, cheaper) outranks sol-0
    assert [r["candidate"] for r in v["results"]] == ["sol-1", "sol-2", "sol-0"]
    assert [r["verdict"] for r in v["results"]] == ["PASS", "FAIL", "FAIL"]
    assert all("attempt" in r for r in v["results"])


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


# ---- worker-advice upgrades ----

def test_policy_generates_projections(tmp_path):
    from loop import policy
    p = policy.load()
    assert p["policy_id"] == "autobuild-worker-v1"
    md = policy.render_agents_md(p)
    assert "cannot declare completion" in md
    assert "Do not hand-edit" in md
    sp = policy.render_system_prompt(p)
    assert "speculative execution unit" in sp
    import shutil
    shutil.copy(os.path.join(HERE, "..", "agent_policy.json"), str(tmp_path))
    out = policy.write_projections(str(tmp_path))
    assert out == "autobuild-worker-v1"
    gen = open(os.path.join(str(tmp_path), "AGENTS.md")).read()
    assert "cannot declare completion" in gen


def test_knowledge_ledger():
    from loop import knowledge
    ok, _ = knowledge.check_entry({"type": "NOPE", "subject": "s",
                                   "statement": "x", "origin_run": "r"})
    assert not ok
    ok, _ = knowledge.check_entry({"type": "IDEA", "subject": "s",
                                   "statement": "x", "origin_run": "r",
                                   "action": "EXECUTE_NOW"})
    assert not ok  # ideas store, never execute
    buf = knowledge.idea_buffer("streaming validators", "run:1",
                                "endgame corpus", "no corpus effect")
    assert "target" not in buf and buf["action"] == "STORE_NOT_EXECUTE"
    ok, reasons = knowledge.check_entry(buf)
    assert ok, reasons


def test_blocker_lifecycle(tmp_path):
    from loop import blocker
    b = blocker.open_blocker("checkout.order", "API_INCOMPATIBILITY",
                             observed=["201 != 200"], unknowns=["provider TLS"])
    b = blocker.attach_attempt(b, "sol-0", "FAIL", ["timeout"])
    b = blocker.set_untried(b, ["sol-1"])
    assert b["state"] == "OPEN" and len(b["attempted_solutions"]) == 1
    b = blocker.resolve(b, "ATT-4")
    bid = blocker.save(str(tmp_path / "b.jsonl"), b)
    assert bid.startswith("blk:")
    with pytest.raises(blocker.BadBlocker):
        blocker.save(str(tmp_path / "b.jsonl"), {"nope": 1})


def test_solutions_rich_and_distinct():
    hits = [{"source": "github", "backend": "github", "url": "u1", "summary": "s1"},
            {"source": "github", "backend": "github", "url": "u2", "summary": "s2"},
            {"source": "arxiv", "backend": "arxiv", "url": "u3", "summary": "s3"}]
    cands = seeker.propose(PROBLEM, hits)
    assert len(cands) == 3
    mechs = [c["mechanism"] for c in cands]
    assert len(set(mechs)) == 3  # materially distinct, never 3 timeout tweaks
    for c in cands:
        assert c["falsifier"] and c["cost"] and "reversibility" in c


def test_ordering_cheapest_info_first():
    cands = seeker.propose(PROBLEM, [])
    ranked = seeker.order(cands, {"sol-0": {"p": 0.1}, "sol-1": {"p": 0.9},
                                  "sol-2": {"p": 0.5}})
    assert ranked[0][0]["solution_id"] == "sol-1"
    assert "score_inputs" in ranked[0][0] and ranked[0][1] > 0


def test_attempts_measured():
    logged = []
    v = seeker.seek(PROBLEM, [FakeBackend()],
                    lambda c: {"verdict": "FAIL", "reasons": []}, logged.append)
    assert all(a["attempt_id"].startswith("ATT-") for a in v["attempts"])
    assert all(a["cost"]["duration_ms"] >= 0 for a in v["attempts"])
    assert v["blocker_hint"] == "open-blocker"  # all failed -> durable halt
    assert v["states"][0] == "OBSERVE" and "DISCOVERY" in v["states"]


def test_escalate_stops_early_and_defers_human():
    lv = {"L0-target": [FakeBackend(hits=[])],
          "L5-github": [FakeBackend(hits=[{"source": "github", "url": "u", "summary": "s"}])]}
    out = research.escalate("q", lv)
    assert out["tried"] == ["L0-target", "L5-github"] and len(out["hits"]) == 1
    out2 = research.escalate("q", {"L0-target": [FakeBackend(hits=[])]})
    assert out2["hits"] == [] and "L8-human:deferred" in out2["tried"]


def test_research_record_shape():
    rec = research.record_research("q?", "GITHUB", "q",
                                   [{"url": "u1"}], "raised sol-2", "run:9")
    assert rec["research_id"].startswith("res:") and rec["origin_run"] == "run:9"


def test_priority_outranks_motion():
    probe = {"task": "probe X", "justification": "resolves UNKNOWN",
             "impact": 1, "expected_progress": 0.9, "bottleneck_centrality": 0.9,
             "information_value": 0.9, "strategic_value": 0.8, "cost": 0.1,
             "human_needed": False, "reversibility": 1.0}
    feat = {"task": "build big feature", "justification": "motion",
            "impact": 2}
    ranked = comp.rank_tasks([feat, probe])
    assert ranked[0]["task"] == "probe X"  # tiny probe beats big motion
    assert "priority_inputs" in ranked[0]


def test_cluster_and_scope_guard():
    bank = [{"idea": "validator trace corpus", "themes": ["proof", "scale"],
             "runs": ["run:1", "run:2"], "endgame_link": "e", "falsifier": "f"},
            {"idea": "faster timeouts", "themes": ["speed"], "runs": ["run:1"],
             "endgame_link": "e", "falsifier": "f"}]
    cl = comp.cluster(bank)
    assert cl["reinforcing"] == ["validator trace corpus"]
    assert "validator trace corpus" in cl["primitive_candidates"]
    assert "validator trace corpus" in cl["by_theme"]["proof"]
    # scope guard: ideas never leak into task outputs
    tasks = {t for t in cl["by_theme"].get("tasks", [])}
    assert tasks == set()


def test_intel_built_from_data():
    from loop import intel
    rec = good_record()
    logged = []
    v = seeker.seek(PROBLEM, [FakeBackend()],
                    lambda c: {"verdict": "PASS", "reasons": []}, logged.append)
    out = intel.build_intel(rec, v, contract_root="cr:1", model="sim",
                            costs={"wall_time_ms": 120, "human_minutes": 0})
    assert out["schema"] == "run-intelligence-v1"
    assert out["cost"]["tokens"] is None  # unknown stays null
    assert out["cost"]["useful_yield"] == 1.0
    assert out["worker_summary"].startswith("run ")
    assert len(out["next_tasks"]) == 10 and len(out["ideas"]) == 2


def test_holdout_opacity():
    """Validator holds a check candidates never see; still enforced."""
    logged = []
    def hidden(c):
        if c.get("mechanism") == "fake":
            return {"verdict": "FAIL", "reasons": ["holdout: route class banned"]}
        return {"verdict": "PASS", "reasons": []}
    v = seeker.seek(PROBLEM, [FakeBackend()], hidden, logged.append)
    # the fake-sourced candidate fails a rule stated nowhere in the contract;
    # local-mechanism candidates still pass -> winner is not sol-0
    by_id = {r["candidate"]: r for r in v["results"]}
    assert by_id["sol-0"]["verdict"] == "FAIL"
    assert any("holdout" in x for x in by_id["sol-0"]["reasons"])
    assert v["winner"] in ("sol-1", "sol-2")
    # ...yet the candidates themselves carry no trace of the rule
    assert all("holdout" not in json.dumps(c) for c in v["candidates"])


def test_reconcile_matched_and_divergent():
    from loop import reconcile
    local = [{"trace_id": "trace_ok", "verdict": "GO"},
             {"trace_id": "trace_bad", "verdict": "GO"}]
    exported = [
        {"object": "trace.span", "id": "s1", "trace_id": "trace_ok",
         "parent_id": None, "started_at": "t", "ended_at": "t",
         "span_data": {}, "error": None},
        {"object": "trace.span", "id": "s2", "trace_id": "trace_bad",
         "parent_id": None, "started_at": "t", "ended_at": "t",
         "span_data": {}, "error": {"message": "boom"}}]
    rep = reconcile.reconcile(exported, local)
    assert "trace_ok" in rep["matched"]
    assert "trace_bad" in rep["error_mismatch"]
    rep2 = reconcile.reconcile(exported, [{"trace_id": "trace_ok",
                                           "verdict": "GO"}])
    assert "trace_bad" in rep2["missing_local"]  # orphan telemetry
    ok, report = reconcile.cross_check_run({"trace_id": "trace_ok",
                                            "verdict": "GO"}, exported[:1], [])
    assert ok and report["trace_id"] == "trace_ok"


def test_causes_cited_by_candidates():
    v = seeker.seek(PROBLEM, [FakeBackend()], lambda c: {"verdict": "FAIL", "reasons": []}, lambda e: None)
    assert len(v["causes"]) >= 1
    by_mech = {c["mechanism"]: c["cause_id"] for c in v["causes"]}
    for c in v["candidates"]:
        if c["mechanism"] in by_mech:
            assert c["cause_id"] == by_mech[c["mechanism"]]


# ---- provider-native telemetry ----

def test_trace_id_shape():
    from loop import tracing
    tid = tracing.gen_trace_id()
    assert tid.startswith("trace_") and len(tid) == 38


def test_mirror_export_shape():
    from loop import tracing
    s = tracing.TraceSession("wf", "proj", trace_id="trace_" + "ab" * 16)
    h = s.span("attempt/ATT-0", {"observation": "echo ok", "exit": 0})
    assert s.finish_span(h) is True
    (payload,) = s.export_mirror()
    assert payload["object"] == "trace.span"
    for k in ("id", "trace_id", "parent_id", "started_at", "ended_at",
              "span_data", "error"):
        assert k in payload, k
    assert payload["span_data"]["data"]["exit"] == 0
    assert payload["trace_id"] == "trace_" + "ab" * 16


def test_scrub_defense_in_depth():
    from loop import tracing
    dirty = {"api_key": "ghp_fakelymadeup0000000000000000000000",
             "nested": {"token": "xox no", "ok": 1},
             "note": "nothing secret here", "big": "z" * 2500}
    clean = tracing.scrub(dirty)
    assert clean["api_key"] == "<redacted>"
    assert clean["nested"]["token"] == "<redacted>"
    assert clean["nested"]["ok"] == 1 and clean["note"] == dirty["note"]
    assert len(clean["big"]) == 2000


def test_sensitive_io_dropped_by_default():
    from loop import tracing
    s = tracing.TraceSession("wf", "proj")
    s.span("gen", {"input": "user secrets here", "exit": 0})
    (payload,) = s.export_mirror()
    assert "input" not in payload["span_data"]["data"]
    s2 = tracing.TraceSession("wf", "proj", include_sensitive_data=True)
    s2.span("gen", {"input": "hello", "exit": 0})
    assert s2.export_mirror()[0]["span_data"]["data"]["input"] == "hello"


def test_binding_and_degraded_mode():
    from loop import tracing
    s = tracing.TraceSession("wf", "proj", use_sdk=True)  # live if SDK present
    s.span("attempt/ATT-0", {"exit": 0})
    assert len(s.export_mirror()) == 1  # mirror records in every mode
    rec = s.bind({"run_id": "run:1"})
    assert rec["trace_id"] == s.trace_id and "telemetry_mode" in rec
    s.finish()


def test_degraded_without_sdk(monkeypatch):
    import sys
    from loop import tracing
    monkeypatch.setitem(sys.modules, "agents", None)
    monkeypatch.setitem(sys.modules, "agents.tracing", None)
    s = tracing.TraceSession("wf", "proj", use_sdk=True)
    assert s.mode.startswith("mirror:sdk-unavailable")
    s.span("attempt/ATT-0", {"exit": 0})
    assert len(s.export_mirror()) == 1
    s.finish()


def test_verdicts_pass_through_unredacted():
    from loop import tracing
    out = tracing.scrub({"verdict": "PASS", "reasons": ["shape-ok"]})
    assert out == {"verdict": "PASS", "reasons": ["shape-ok"]}


def test_usage_record_unknowns_null():
    from loop import tracing
    u = tracing.usage_record(input_tokens=10, output_tokens=5)
    assert u["cached_tokens"] is None and u["cost"] is None
    assert u["input_tokens"] == 10


def test_memory_view_covers_bank():
    from loop import compile as comp
    rec = good_record()
    compiled = comp.compile_runs([rec])
    mv = comp.to_memory_view(compiled)
    assert len(mv["records"]) > 10  # tasks + ideas + meta
    assert mv["reduction"] >= 1.0
    blob = " ".join(x.get("content", "") for x in mv["records"])
    assert "task-0" in blob
