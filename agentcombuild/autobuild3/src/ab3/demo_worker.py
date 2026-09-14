"""Honest worker simulation: does work, logs re-runnable evidence.

The worker NEVER judges — it returns lines logged; the caller runs the
stoplight. Simulation only: echo/python3 probes, temp files, no external
effects. Labeled simulation throughout (atask law: mocks prove wiring).
"""
import os

from ab3 import alog

PLAN = {
    "id": "lead-reply-one",
    "goal": {"statement": "Reply to one lead with a booking offer",
             "acceptance": ["reply delivered to lead-123",
                            "outcome read back"]},
    "features": [
        {"id": "qualify-lead", "description": "score the lead",
         "acceptance": ["score recorded"],
         "evidence": [{"kind": "doc", "ref": "notes:rubric"}],
         "covers": [0]},
        {"id": "send-lead-reply", "description": "send one bounded reply",
         "acceptance": ["reply delivered"],
         "evidence": [{"kind": "doc", "ref": "notes:template"}],
         "covers": [0]},
    ],
}


def honest(workdir, validators_dir=None):
    """Simulated honest run. Returns the stoplight verdict (judged, not claimed)."""
    from ab3 import stoplight
    os.makedirs(workdir, exist_ok=True)
    qpath = os.path.join(workdir, "queue.json")
    import json as _j
    with open(qpath, "w") as fh:
        _j.dump(PLAN, fh)
    queue = alog.queue_from_plan(PLAN)
    score_file = os.path.join(workdir, "score.txt")
    with open(score_file, "w") as fh:
        fh.write("lead-123 score=8/10\n")
    alog.append(workdir, queue, "qualify-lead", [0], "scored lead-123",
                {"kind": "file", "path": score_file})
    alog.append(workdir, queue, "send-lead-reply", [0], "reply delivered (sim)",
                {"kind": "command",
                 "argv": ["echo", "reply-delivered lead-123"],
                 "expect": "reply-delivered"})
    return stoplight.judge("send-lead-reply", queue, workdir, validators_dir,
                           qpath)
