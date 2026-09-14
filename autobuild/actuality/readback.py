"""Independent readback (PROMOTED to canonical 2026-09-14).

Provenance: semantics promoted from agentcombuild/autobuild3/src/ab3
(frozen). Same-channel success is UNKNOWN; mismatch FALSE; agreement TRUE.
"""
from .judges import FALSE, TRUE, UNKNOWN


def check_readback(action_evidence, readback_evidence, key="created_id"):
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
