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
