"""Seeker: the stuck loop. SEARCH → PROPOSE ×3 → TEST each → LOG all.

The seeker stays dark about validation internals: it submits candidates to
`validate_fn` and records verdicts + reasons, but can never self-pass.
Failures are first-class outputs (fixtures for later runs), never garbage.
"""
from . import research


def propose(problem, hits):
    """Exactly 3 full candidates, distinct mechanisms. A candidate without
    its own falsifier is a wish, not a candidate — refused at construction."""
    cands = []
    for i, h in enumerate(hits[:3]):
        cands.append({
            "id": "cand-%d" % i,
            "approach": h.get("summary", "")[:300],
            "mechanism": h.get("source", "?"),
            "origin": "%s:%s" % (h.get("backend", "?"), h.get("url", ""))[:200],
            "falsifier": problem.get("acceptance", "no acceptance stated"),
            "invariant": problem.get("invariant_id", "?")})
    base = len(cands)
    for i in range(base, 3):
        cands.append({
            "id": "cand-%d" % i,
            "approach": "local baseline: shrink scope to the smallest "
                        "observable leaf of <%s> and prove that"
                        % problem.get("invariant_id", "?"),
            "mechanism": "local",
            "origin": "local:underengineer",
            "falsifier": problem.get("acceptance", "no acceptance stated"),
            "invariant": problem.get("invariant_id", "?")})
    return cands


def seek(problem, backends, validate_fn, log_fn):
    """Run one stuck-loop. Returns {problem, candidates, results, winner}.

    validate_fn(candidate) -> {verdict: PASS|FAIL, reasons[]}.
    log_fn(entry) records {candidate, verdict}; its exceptions are captured,
    never fatal (a lost log line is reported, not hidden).
    """
    hits, errors = research.multi_search(problem.get("context", ""), backends)
    candidates = propose(problem, hits)
    results, logged = [], 0
    for c in candidates:
        try:
            v = validate_fn(c)
            verdict = {"verdict": v.get("verdict", "FAIL"),
                       "reasons": list(v.get("reasons", []))}
        except Exception as exc:  # noqa: BLE001
            verdict = {"verdict": "FAIL", "reasons": ["raised:%s"
                                                     % type(exc).__name__]}
        results.append({"candidate": c["id"], "verdict": verdict["verdict"],
                        "reasons": verdict["reasons"]})
        try:
            log_fn({"candidate": c, "verdict": verdict})
            logged += 1
        except Exception as exc:  # noqa: BLE001
            results[-1]["log_error"] = str(exc)[:160]
    winner = next((c["id"] for c, r in zip(candidates, results)
                   if r["verdict"] == "PASS"), None)
    return {"invariant": problem.get("invariant_id"), "candidates": candidates,
            "results": results, "winner": winner, "logged": logged,
            "research_errors": errors}
