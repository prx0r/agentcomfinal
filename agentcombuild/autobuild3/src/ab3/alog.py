"""a-log telemetry: hash-chained per-task logs. Agents append; never judge.

Refusals raise ValueError and file nothing: unknown task, bad index,
secret-shaped evidence. Chain: hash = sha12(canonical(line minus hash)).
"""
import json
import os

from ab1.canonical import canonical, sha12

GENESIS = "GENESIS"
SECRET_KEYS = ("secret", "token", "password", "api_key", "apikey", "private")
SECRET_VALUES = ("sk-", "ghp_", "gho_", "pina_", "xox", "BEGIN PRIVATE KEY")


class Refused(ValueError):
    pass


def queue_from_plan(plan):
    """Features become tasks. Returns {task_id: {acceptance, covers}}."""
    q = {}
    for f in plan.get("features", []):
        if isinstance(f, dict) and f.get("id"):
            q[f["id"]] = {"acceptance": list(f.get("acceptance", [])),
                          "covers": list(f.get("covers", []))}
    return q


def check_covers(plan):
    """Every feature maps to >=1 valid goal acceptance index (atask rule)."""
    errors = []
    goal = plan.get("goal", {}) if isinstance(plan, dict) else {}
    n = len(goal.get("acceptance", [])) if isinstance(goal, dict) else 0
    feats = plan.get("features", []) if isinstance(plan, dict) else []
    for f in feats:
        if not isinstance(f, dict):
            continue
        fid = f.get("id", "?")
        covers = f.get("covers", [])
        if not isinstance(covers, list) or not covers:
            errors.append("%s: covers missing/empty (map to goal indices)" % fid)
        else:
            for c in covers:
                if not isinstance(c, int) or c < 0 or c >= n:
                    errors.append("%s: covers bad index %r" % (fid, c))
    return {"ok": not errors, "errors": errors}


def _looks_secret(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            if any(s in kl for s in SECRET_KEYS):
                return True
            if _looks_secret(v):
                return True
        return False
    if isinstance(obj, list):
        return any(_looks_secret(v) for v in obj)
    if isinstance(obj, str):
        return any(s in obj for s in SECRET_VALUES)
    return False


def log_path(logdir, task):
    return os.path.join(logdir, "a-logs", task + ".jsonl")


def read_lines(logdir, task):
    p = log_path(logdir, task)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh.read().splitlines() if l.strip()]


def append(logdir, queue, task, idx, action, evidence):
    if task not in queue:
        raise Refused("refused:unknown-task:%s" % task)
    acc = queue[task]["acceptance"]
    idx = list(idx)
    for i in idx:
        if not isinstance(i, int) or i < 0 or i >= len(acc):
            raise Refused("refused:bad-index:%r" % (i,))
    if not isinstance(evidence, dict) or not evidence.get("kind"):
        raise Refused("refused:bad-evidence")
    if evidence.get("kind") == "secret" or _looks_secret(evidence):
        raise Refused("refused:secret")
    lines = read_lines(logdir, task)
    prev = lines[-1]["hash"] if lines else GENESIS
    line = {"seq": len(lines), "task": task, "idx": idx, "action": action,
            "evidence": evidence, "prev": prev}
    line["hash"] = sha12(canonical(line))
    os.makedirs(os.path.join(logdir, "a-logs"), exist_ok=True)
    with open(log_path(logdir, task), "a", encoding="utf-8") as fh:
        fh.write(canonical(line).decode() + "\n")
    return line


def verify_chain(logdir, task):
    prev = GENESIS
    for i, line in enumerate(read_lines(logdir, task)):
        if not isinstance(line, dict) or line.get("seq") != i:
            return False
        if line.get("prev") != prev:
            return False
        body = {k: v for k, v in line.items() if k != "hash"}
        if line.get("hash") != sha12(canonical(body)):
            return False
        prev = line["hash"]
    return True
