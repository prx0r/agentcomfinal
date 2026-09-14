#!/usr/bin/env python3
"""validators/send-lead-reply.py — mechanical judge (atask contract).

argv: [validator, task_id, queue_path, alog_path]. stdout: one JSON line.
Dumb string/file checks only; the stoplight already re-ran the evidence.
"""
import json
import sys

_, tid, queue_path, alog_path = sys.argv
reasons = []
try:
    lines = [json.loads(l) for l in open(alog_path).read().splitlines()
             if l.strip()]
except OSError:
    lines = []
mine = [l for l in lines if isinstance(l, dict) and l.get("task") == tid]
if not any("reply-delivered" in json.dumps(l.get("evidence", {}))
           for l in mine):
    reasons.append("no a-log line carries reply-delivered evidence")
print(json.dumps({"pass": not reasons, "reasons": reasons}))
