"""Independent readback: promoted from ab3 (frozen). Same-channel success
is UNKNOWN; mismatch FALSE; agreement TRUE."""
from ab3 import readback as _r


def check_readback(action_evidence, readback_evidence, key="created_id"):
    return _r.check_readback(action_evidence, readback_evidence, key)
