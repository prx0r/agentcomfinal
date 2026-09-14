"""Canonical autobuild: promoted surviving primitives (E0).

Provenance: compiler/specgate+seesaw derive from agentcombuild/autobuild1
(ab1, frozen); actuality/* derive from agentcombuild/autobuild3 (ab3,
frozen); registry derives from ab3 validators. Frozen sources are never
edited — this package imports them (reference, not copy) except where
semantics deliberately changed (priority formula, proposal channel,
execution envelopes), which are fresh implementations noted inline.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BUILD = os.path.normpath(os.path.join(_HERE, "..", "agentcombuild"))
for _d in ("autobuild1/src", "autobuild3/src", "agentloop/src"):
    _p = os.path.join(_BUILD, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
