"""Knowledge ledger: typed records, never a soup. Promotion is governed
elsewhere; this ledger only files honestly-typed entries.

Types: FACT NEGATIVE_FACT HYPOTHESIS UNKNOWN IDEA RISK PREDICTION DECISION
OBSERVATION. Ideas carry STORE_NOT_EXECUTE discipline via the idea buffer:
emitting an idea never changes the current target (scope guard tested).
"""
import json
import os

from ab1.canonical import canonical, sha12

TYPES = ("FACT", "NEGATIVE_FACT", "HYPOTHESIS", "UNKNOWN", "IDEA", "RISK",
         "PREDICTION", "DECISION", "OBSERVATION")

REQUIRED = {"type", "subject", "statement", "origin_run"}


class BadEntry(ValueError):
    pass


def check_entry(e):
    reasons = []
    if not isinstance(e, dict):
        return False, ["not-an-object"]
    if e.get("type") not in TYPES:
        reasons.append("bad-type:%r" % (e.get("type"),))
    for k in ("subject", "statement", "origin_run"):
        if not e.get(k):
            reasons.append("missing:%s" % k)
    if e.get("type") == "IDEA":
        if e.get("action", "STORE_NOT_EXECUTE") != "STORE_NOT_EXECUTE":
            reasons.append("idea-must-store-not-execute")
    return (not reasons), reasons


def append(path, entry):
    ok, reasons = check_entry(entry)
    if not ok:
        raise BadEntry("; ".join(reasons))
    rec = dict(entry)
    rec["entry_id"] = "ke:" + sha12(canonical(entry))[:16]
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(canonical(rec).decode() + "\n")
    return rec["entry_id"]


def load_all(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh.read().splitlines() if l.strip()]


def idea_buffer(idea, origin_run, endgame_link="", falsifier="",
                idea_type="GENERAL", horizon="LATER"):
    """Side-channel emit: structured, scope-safe by construction (no target
    field exists to mutate, and compile.py never promotes ideas to tasks)."""
    return {"type": "IDEA", "idea_type": idea_type, "subject": idea,
            "statement": idea, "origin_run": origin_run,
            "endgame_link": endgame_link, "falsifier": falsifier,
            "horizon": horizon, "action": "STORE_NOT_EXECUTE"}
