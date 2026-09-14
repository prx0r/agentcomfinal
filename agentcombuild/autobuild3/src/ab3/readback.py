"""Independent readback: action channel + independent channel must agree.

Consequential actions require independent postcondition readback where
possible. Same-channel 'Success!' proves almost nothing: the actor can
display success. Rule: action evidence names an id; readback evidence must
present the SAME id from an independent source. Missing readback → UNKNOWN
(not FALSE, not TRUE). Mismatch → FALSE.
"""
from .judges import FALSE, TRUE, UNKNOWN


def check_readback(action_evidence, readback_evidence, key="created_id"):
    """Returns (TRUE|FALSE|UNKNOWN, detail). Pure; no I/O, no exceptions."""
    try:
        if not isinstance(action_evidence, dict):
            return UNKNOWN, "no-action-evidence"
        claimed = action_evidence.get(key)
        if claimed is None:
            return UNKNOWN, "action-names-no-id"
        if not isinstance(readback_evidence, dict):
            return UNKNOWN, "no-readback"
        found = readback_evidence.get(key)
        if found is None:
            return UNKNOWN, "readback-missing-id"
        if found != claimed:
            return FALSE, "id-mismatch"
        if action_evidence.get("source") and readback_evidence.get("source") \
                and action_evidence["source"] == readback_evidence["source"]:
            return UNKNOWN, "channels-not-independent"
        return TRUE, "agree"
    except Exception:  # noqa: BLE001 - judges never raise
        return UNKNOWN, "judge-error"
