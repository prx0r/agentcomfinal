"""Run records: every run is data. Shape enforced at append, not by trust.

next10 holds EXACTLY 10 (forces prioritization). visionary holds >=1
(forces endgame thinking). working claims name validations; failures name
fixtures so no later run re-walks the dead route.
"""
import json
import os

from ab1.canonical import canonical, sha12


class BadRecord(ValueError):
    pass


def new_run(project, attempt, started="2026-09-14T00:00:00Z"):
    rid = "run:" + sha12(canonical({"project": project, "attempt": attempt,
                                    "started": started}))[:16]
    return {"run_id": rid, "project": project, "attempt": attempt,
            "started": started, "working": [], "not_working": [],
            "next10": [], "visionary": []}


def _need(cond, reasons, msg):
    if not cond:
        reasons.append(msg)
    return cond


def check_record(rec):
    """Returns (ok, reasons). Pure; never raises on bad input."""
    reasons = []
    try:
        if not isinstance(rec, dict):
            return False, ["not-an-object"]
        for k in ("run_id", "project", "attempt", "working", "not_working",
                  "next10", "visionary"):
            _need(k in rec, reasons, "missing:%s" % k)
        if reasons:
            return False, reasons
        for i, w in enumerate(rec.get("working", [])):
            _need(isinstance(w, dict) and w.get("claim")
                  and w.get("validation"), reasons,
                  "working[%d] needs claim+validation" % i)
        for i, w in enumerate(rec.get("not_working", [])):
            _need(isinstance(w, dict) and w.get("claim") and w.get("failure")
                  and w.get("fixture"), reasons,
                  "not_working[%d] needs claim+failure+fixture" % i)
        nx = rec.get("next10", [])
        _need(isinstance(nx, list) and len(nx) == 10, reasons,
              "next10 must hold exactly 10 (got %s)"
              % (len(nx) if isinstance(nx, list) else "?"))
        for i, t in enumerate(nx if isinstance(nx, list) else []):
            ok = isinstance(t, dict) and t.get("task") and t.get("justification") \
                and isinstance(t.get("impact"), int) and 1 <= t["impact"] <= 5
            _need(ok, reasons, "next10[%d] needs task+justification+impact1-5" % i)
        vz = rec.get("visionary", [])
        _need(isinstance(vz, list) and len(vz) >= 1, reasons,
              "visionary needs >=1 idea")
        for i, v in enumerate(vz if isinstance(vz, list) else []):
            _need(isinstance(v, dict) and v.get("idea")
                  and v.get("endgame_link") and v.get("falsifier"), reasons,
                  "visionary[%d] needs idea+endgame_link+falsifier" % i)
    except Exception:  # noqa: BLE001 - checker never raises
        return False, reasons + ["checker-error"]
    return (not reasons), reasons


def append(path, rec):
    ok, reasons = check_record(rec)
    if not ok:
        raise BadRecord("; ".join(reasons))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(canonical(rec).decode() + "\n")
    return rec["run_id"]


def load_all(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh.read().splitlines() if l.strip()]
