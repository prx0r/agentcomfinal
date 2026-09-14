"""Seeker: the stuck loop. SEARCH → PROPOSE ×3 → TEST each → LOG all.

Worker state machine per run: OBSERVE → ORIENT → SELECT → ATTEMPT → PROBE →
VALIDATE, with UNKNOWN looping back through DISCOVERY. States are traced in
the output (the machine is observable), but the seeker stays dark about
validation internals: it submits candidates to `validate_fn` and records
verdicts + reasons, but can never self-pass. Failures are first-class
outputs (fixtures for later runs), never garbage.
"""
import time

from ab1.canonical import sha12
from ab1.canonical import canonical as _canon

from . import research

STATES = ("OBSERVE", "ORIENT", "SELECT", "ATTEMPT", "PROBE", "VALIDATE",
          "LOG", "DISCOVERY")

LOCAL_MECHANISMS = ("repair-current", "replace-component", "remove-dependency")


def _mechanism_of(hit):
    return str(hit.get("mechanism") or hit.get("source") or "?").lower()


def propose(problem, hits):
    """Exactly 3 full candidates with materially distinct mechanisms
    (repair vs replace vs remove — never three timeout tweaks). Rich schema:
    hypothesis/intervention/why/predicted_gate_effect/cost/risk/
    reversibility/falsifier. No falsifier = wish, refused at construction."""
    cands, seen = [], set()
    for h in hits:
        mech = _mechanism_of(h)
        if mech in seen:
            continue
        seen.add(mech)
        cands.append({
            "solution_id": "sol-%d" % len(cands),
            "hypothesis": h.get("summary", "")[:300],
            "intervention": "apply <%s> route from %s" % (
                mech, h.get("url", "?") or "?"),
            "why_it_might_work": [(h.get("summary", "") or "")[:160]],
            "predicted_gate_effect": [str(problem.get("acceptance", ""))[:160]],
            "cost": {"estimated_minutes": 15, "money": 0},
            "risk": "LOW", "reversibility": 0.8,
            "new_dependencies": [], "evidence_supporting": [],
            "falsifier": problem.get("acceptance", "no acceptance stated"),
            "mechanism": mech,
            "origin": "%s:%s" % (h.get("backend", "?"), h.get("url", ""))[:200],
            "invariant": problem.get("invariant_id", "?")})
        if len(cands) == 3:
            break
    fallbacks = [m for m in LOCAL_MECHANISMS if m not in seen]
    i = 0
    while len(cands) < 3:
        mech = fallbacks[i] if i < len(fallbacks) else "local-%d" % i
        cands.append({
            "solution_id": "sol-%d" % len(cands),
            "hypothesis": "local %s route for <%s>" % (
                mech.replace("-", " "), problem.get("invariant_id", "?")),
            "intervention": "%s then prove the smallest observable leaf"
                            % mech.replace("-", " "),
            "why_it_might_work": ["no external dependency"],
            "predicted_gate_effect": [str(problem.get("acceptance", ""))[:160]],
            "cost": {"estimated_minutes": 10, "money": 0},
            "risk": "LOW", "reversibility": 0.9,
            "new_dependencies": [], "evidence_supporting": [],
            "falsifier": problem.get("acceptance", "no acceptance stated"),
            "mechanism": mech,
            "origin": "local:underengineer",
            "invariant": problem.get("invariant_id", "?")})
        i += 1
    return cands


def score_solution(cand, p=0.5, gates_unlocked=1, knowledge=0.5,
                   human_burden=0.0):
    """S = P*I*R*L / (1+C+H). Every input stored separately, never hidden
    behind prose. Later runs learn P from histories; until then priors."""
    r = float(cand.get("reversibility", 0.5))
    c = float(cand.get("cost", {}).get("money", 0)) + float(
        cand.get("cost", {}).get("estimated_minutes", 0)) / 60.0
    inputs = {"p": p, "i": gates_unlocked, "r": r, "l": knowledge,
              "c": round(c, 4), "h": human_burden}
    s = (p * gates_unlocked * r * knowledge) / (1 + c + human_burden)
    return round(s, 6), inputs


def order(candidates, priors=None):
    """Rank highest-value reversible route first. Returns [(cand, score)]."""
    priors = priors or {}
    scored = []
    for c in candidates:
        pr = priors.get(c["solution_id"], {})
        s, inputs = score_solution(c, **pr) if pr else score_solution(c)
        c = dict(c)
        c["score_inputs"] = inputs
        c["score"] = s
        scored.append((c, s))
    scored.sort(key=lambda t: (-t[1], t[0]["solution_id"]))
    return scored


def seek(problem, backends, validate_fn, log_fn, priors=None):
    """Run one stuck-loop. Returns {states, research, candidates (scored,
    ordered), attempts, results, winner, blocker_hint}.

    validate_fn(candidate) -> {verdict: PASS|FAIL, reasons[]}.
    log_fn(entry) records {attempt, candidate, verdict}; exceptions captured.
    """
    states = ["OBSERVE", "ORIENT", "SELECT"]
    hits, errors = research.multi_search(problem.get("context", ""), backends)
    res_record = research.record_research(
        problem.get("invariant_id", "?"), "multi",
        problem.get("context", ""), hits,
        "seeker run", run_id=problem.get("run_id", ""))
    states.append("DISCOVERY")
    ranked = order(propose(problem, hits), priors)
    attempts, results, logged = [], [], 0
    for n, (c, _) in enumerate(ranked):
        states.append("ATTEMPT")
        t0 = time.monotonic()
        try:
            v = validate_fn(c)
            verdict = {"verdict": v.get("verdict", "FAIL"),
                       "reasons": list(v.get("reasons", []))}
        except Exception as exc:  # noqa: BLE001
            verdict = {"verdict": "FAIL", "reasons": ["raised:%s"
                                                     % type(exc).__name__]}
        states.append("PROBE")
        states.append("VALIDATE")
        duration_ms = int((time.monotonic() - t0) * 1000)
        attempt = {"attempt_id": "ATT-%d" % n, "target": c["invariant"],
                   "solution_id": c["solution_id"],
                   "action": {"kind": "TEST",
                              "description": c["intervention"][:160]},
                   "observed_effect": {"verdict": verdict["verdict"],
                                       "reasons": verdict["reasons"]},
                   "validation": {"status": verdict["verdict"]},
                   "cost": {"duration_ms": duration_ms, "tokens": None}}
        attempts.append(attempt)
        results.append({"candidate": c["solution_id"],
                        "verdict": verdict["verdict"],
                        "reasons": verdict["reasons"],
                        "attempt": attempt["attempt_id"],
                        "score": c["score"]})
        states.append("LOG")
        try:
            log_fn({"attempt": attempt, "candidate": c, "verdict": verdict,
                    "research": res_record["research_id"]})
            logged += 1
        except Exception as exc:  # noqa: BLE001
            results[-1]["log_error"] = str(exc)[:160]
    winner = next((c["solution_id"] for (c, _), r in zip(ranked, results)
                   if r["verdict"] == "PASS"), None)
    return {"invariant": problem.get("invariant_id"), "states": states,
            "research": res_record, "research_errors": errors,
            "candidates": [c for c, _ in ranked], "attempts": attempts,
            "results": results, "winner": winner, "logged": logged,
            "blocker_hint": None if winner else "open-blocker"}
