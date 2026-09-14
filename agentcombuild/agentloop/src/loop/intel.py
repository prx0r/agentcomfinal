"""RunIntelligence: the canonical run artifact. Derived FROM data, never
hand-written; prose summaries generate from it, not vice versa.

Filed truth stays small (RUN record via runlog); this builds the rich view:
target, hypotheses, attempts, research, facts, ideas, risks, next tasks,
economics. Unknown telemetry stays null (atask law), never estimated.
"""
from . import compile as comp


def build_intel(run_record, seek_trace=None, validations=None, costs=None,
                model="?", policy_id="autobuild-worker-v1", contract_root="",
                plan_root=""):
    """All inputs are recorded structures. Returns the RunIntelligence dict."""
    seek_trace, validations = seek_trace or {}, validations or {}
    costs = costs or {}
    rec = run_record or {}
    attempts = seek_trace.get("attempts", [])
    n_att = len(attempts)
    validated = sum(1 for r in seek_trace.get("results", [])
                    if r.get("verdict") == "PASS")
    econ = {"tokens": costs.get("tokens"),
            "wall_time_ms": costs.get("wall_time_ms"),
            "api_cost": costs.get("api_cost"),
            "human_minutes": costs.get("human_minutes", 0),
            "useful_yield": round(validated / max(1, n_att), 4)}
    intel = {
        "schema": "run-intelligence-v1",
        "run_id": rec.get("run_id", "?"),
        "contract_root": contract_root, "plan_root": plan_root,
        "worker_policy": policy_id, "model": model,
        "target": {"invariant": seek_trace.get("invariant", "?"),
                   "starting_state": "UNKNOWN"},
        "actions": ["seek"], "research": [seek_trace.get("research", {})],
        "hypotheses": [c.get("hypothesis") for c in
                       seek_trace.get("candidates", [])],
        "solutions_considered": [c.get("solution_id") for c in
                                 seek_trace.get("candidates", [])],
        "attempts": attempts, "observations": [],
        "validation_results": seek_trace.get("results", []),
        "new_facts": [], "negative_facts": [],
        "unknowns": seek_trace.get("research_errors", []),
        "conflicts": [], "components_evaluated": [], "new_fixtures": [],
        "ideas": rec.get("visionary", []), "risks": [],
        "next_tasks": rec.get("next10", []), "cost": econ,
        "worker_summary": summarize(rec, validated, n_att)}
    return intel


def summarize(rec, validated, attempts):
    r = rec or {}
    return ("run %s: %d/%d attempts validated; %d working, %d failing; "
            "%d next tasks; %d ideas banked." % (
                r.get("run_id", "?"), validated, attempts,
                len(r.get("working", [])), len(r.get("not_working", [])),
                len(r.get("next10", [])), len(r.get("visionary", []))))
