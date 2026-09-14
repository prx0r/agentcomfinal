"""Compiler: runs become banks. Deterministic; keyword themes, no models.

ideas_bank: every visionary idea ever, with runs + theme tags.
decisions: every next10 entry ever proposed, with run + impact.
next10: merged leaderboard — deduped by normalized task, impact summed,
  best justification kept, top 10.
stats: counts that prove compounding (runs → ideas → failures banked).
"""
import re

THEMES = {
    "endgame": ("endgame", "horizon", "future", "terminal", "50k", "50000"),
    "scale": ("scale", "fleet", "thousand", "million", "library", "registry"),
    "proof": ("proof", "receipt", "validat", "verif", "gate", "evidence"),
    "speed": ("speed", "latency", "fast", "p95", "speedup"),
    "cost": ("cost", "cheap", "budget", "spend", "margin"),
    "autonomy": ("autonom", "agent", "self-", "unsupervised"),
}


def tag(text):
    t = (text or "").lower()
    return sorted(k for k, words in THEMES.items()
                  if any(w in t for w in words))


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def compile_runs(records):
    ideas, decisions = [], []
    board, seen_idea = {}, set()
    for rec in records or []:
        rid = rec.get("run_id", "?")
        for v in rec.get("visionary", []):
            key = norm(v.get("idea"))
            if key not in seen_idea:
                seen_idea.add(key)
                ideas.append({"idea": v.get("idea"),
                              "endgame_link": v.get("endgame_link"),
                              "falsifier": v.get("falsifier"),
                              "runs": [rid],
                              "themes": tag("%s %s" % (v.get("idea"),
                                                       v.get("endgame_link")))})
            else:
                for e in ideas:
                    if norm(e["idea"]) == key and rid not in e["runs"]:
                        e["runs"].append(rid)
        for t in rec.get("next10", []):
            key = norm(t.get("task"))
            decisions.append({"run": rid, "task": t.get("task"),
                              "justification": t.get("justification"),
                              "impact": t.get("impact", 0)})
            cur = board.get(key)
            entry = {"task": t.get("task"),
                     "justification": t.get("justification"),
                     "impact": t.get("impact", 0), "runs": [rid]}
            if cur is None:
                board[key] = entry
            else:
                cur["impact"] += t.get("impact", 0)
                if rid not in cur["runs"]:
                    cur["runs"].append(rid)
                if t.get("impact", 0) >= cur.get("best", 0):
                    cur["best"] = t.get("impact", 0)
                    cur["justification"] = t.get("justification")
    for cur in board.values():
        cur.pop("best", None)
    leaderboard = sorted(board.values(),
                         key=lambda e: (-e["impact"], e["task"] or ""))[:10]
    failures = sum(len(r.get("not_working", [])) for r in records or [])
    return {"ideas_bank": ideas, "decisions": decisions,
            "next10": leaderboard,
            "stats": {"runs": len(records or []), "ideas": len(ideas),
                      "failures_banked": failures,
                      "tasks_proposed": len(decisions)}}


def priority(task):
    """Priority(t) = P(dActuality)*Centrality*InfoGain*Strategic /
    (1+Cost+Human+Irreversibility), 0..1. Tasks without expected_progress
    fall back to impact/5 on the same 0..1 scale (motion never outranks
    evidence by scale trickery — only by number)."""
    if task.get("expected_progress") is None:
        return round(float(task.get("impact", 0)) / 5.0, 6), \
            {"mode": "impact-fallback"}
    p = float(task["expected_progress"])
    b = float(task.get("bottleneck_centrality", 0.5))
    g = float(task.get("information_value", 0.5))
    s = float(task.get("strategic_value", 0.5))
    c = float(task.get("cost", 0.5))
    h = float(1 if task.get("human_needed") else 0)
    r = 1.0 - float(task.get("reversibility", 0.5))
    inputs = {"p": p, "bottleneck": b, "info": g, "strategic": s, "cost": c,
              "human": h, "irreversibility": round(r, 4)}
    return round((p * b * g * s) / (1 + c + h + r), 6), inputs


def rank_tasks(tasks):
    """Rank by priority where available, else impact. Inputs stored per task."""
    out = []
    for t in tasks or []:
        t = dict(t)
        score, inputs = priority(t)
        t["priority_score"] = score
        t["priority_inputs"] = inputs
        out.append(t)
    out.sort(key=lambda e: (-e["priority_score"], e.get("task") or ""))
    return out


def cluster(ideas_bank):
    """Duplicates (reinforcing, runs>1), themes, cross-project primitive
    candidates (scale/proof themes). Ideas never become tasks here — the
    scope guard: compile output tasks come only from RUN next10 entries."""
    by_theme, reinforcing, prims = {}, [], []
    for idea in ideas_bank or []:
        for th in idea.get("themes", []):
            by_theme.setdefault(th, []).append(idea.get("idea"))
        if len(idea.get("runs", [])) > 1:
            reinforcing.append(idea.get("idea"))
        if set(idea.get("themes", [])) & {"scale", "proof"}:
            prims.append(idea.get("idea"))
    return {"by_theme": {k: sorted(set(v)) for k, v in by_theme.items()},
            "reinforcing": sorted(set(reinforcing)),
            "primitive_candidates": sorted(set(prims))}
