"""Blocker objects: durable halt records. When progress stops, the halt
itself becomes data — retrievable when another project hits the same wall.

States: OPEN → (attempts attach) → RESOLVED (by a passing attempt ref) or
STALE. Untried solutions are explicit so the next agent doesn't re-derive
what was already considered.
"""
import json
import os

from ab1.canonical import canonical, sha12


class BadBlocker(ValueError):
    pass


def open_blocker(requirement_id, failure_class, observed=None,
                 unknowns=None, research_state="NEEDS_EXTERNAL_DISCOVERY"):
    b = {"blocker_id": "blk:" + sha12(canonical(
        {"requirement_id": requirement_id, "failure_class": failure_class,
         "observed": observed or []}))[:16],
        "requirement_id": requirement_id, "state": "OPEN",
        "failure_class": failure_class, "observed": observed or [],
        "known_causes": [], "unknowns": unknowns or [],
        "attempted_solutions": [], "untried_solutions": [],
        "research_state": research_state}
    return b


def attach_attempt(blocker, solution_id, verdict, reasons=None):
    blocker = dict(blocker)
    done = list(blocker.get("attempted_solutions", []))
    done.append({"solution": solution_id, "verdict": verdict,
                 "reasons": list(reasons or [])})
    blocker["attempted_solutions"] = done
    return blocker


def set_untried(blocker, solution_ids):
    blocker = dict(blocker)
    blocker["untried_solutions"] = list(solution_ids)
    return blocker


def resolve(blocker, attempt_ref):
    blocker = dict(blocker)
    blocker["state"] = "RESOLVED"
    blocker["resolved_by"] = attempt_ref
    return blocker


def save(path, blocker):
    if not isinstance(blocker, dict) or not blocker.get("blocker_id"):
        raise BadBlocker("missing blocker_id")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(canonical(blocker).decode() + "\n")
    return blocker["blocker_id"]
