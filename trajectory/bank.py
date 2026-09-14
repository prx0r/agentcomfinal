"""Trajectory bank: duality enforced at file time (gitplans P11).

Filing a trajectory writes THREE views atomically: full record
(verified/), ATIF replay (alongside), compact memory projection
(alongside). The fidelity gate refuses the whole filing if the compact
view loses verdicts/costs/ids — a bank that can't prove its own fidelity
is a write-only swamp. Index line appended to index.jsonl (queryable).
"""
import json
import os

from trajectory import atif, memory


class FidelityRefused(ValueError):
    pass


def file_trajectory(root, traj, agent=None, session_id=""):
    """Returns {dir, files}. Raises FidelityRefused on projection loss."""
    compact = memory.project(traj.get("attempts", []),
                             source="bank")
    ok, missing = memory.fidelity(traj.get("attempts", []), compact)
    if not ok:
        raise FidelityRefused("; ".join(missing))
    tid = "".join(c for c in str(traj.get("trajectory_id", "t"))
                  if c.isalnum() or c in "-_:") or "t"
    d = os.path.join(root, "verified", tid)
    os.makedirs(d, exist_ok=True)
    full_p = os.path.join(d, "trajectory.json")
    atif_p = os.path.join(d, "trajectory.atif.json")
    mem_p = os.path.join(d, "trajectory.memory.json")
    with open(full_p, "w") as fh:
        json.dump(traj, fh, indent=2, sort_keys=True)
    with open(atif_p, "w") as fh:
        json.dump(atif.from_trajectory(traj, agent, session_id), fh,
                  indent=2, sort_keys=True)
    with open(mem_p, "w") as fh:
        json.dump(compact, fh, indent=2, sort_keys=True)
    with open(os.path.join(root, "index.jsonl"), "a") as fh:
        fh.write(json.dumps({"trajectory_id": traj.get("trajectory_id"),
                             "policy": traj.get("policy_id"),
                             "level": traj.get("level"),
                             "reduction": compact["reduction"],
                             "dir": d}, sort_keys=True) + "\n")
    return {"dir": d, "files": [full_p, atif_p, mem_p]}
