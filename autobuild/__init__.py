"""Canonical autobuild: promoted surviving primitives (E0, gitbuild1).

Provenance: semantics promoted from frozen agentcombuild/autobuild1+3 into
self-sufficient implementations here (judges/dag/readback/specgate/seesaw/
registry). Frozen sources are never edited AND never imported by canonical
code (isolation gate enforces). Only remaining cross-tree import is the
agentloop compiler helper used by priority.py (agentloop is policy layer,
not frozen history).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BUILD = os.path.normpath(os.path.join(_HERE, "..", "agentcombuild"))
_p = os.path.join(_BUILD, "agentloop/src")
if _p not in sys.path:
    sys.path.insert(0, _p)
