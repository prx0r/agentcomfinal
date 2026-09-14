"""Live wire-compat vs the real OpenAI Agents SDK (0.22.2).

Skips cleanly when the SDK is absent (system python); runs for real under
.venvs/agentcom. Keyless: no API key -> backend export no-ops, while our
capturing processor still receives everything synchronously.
"""
import os
import sys

import pytest

agents = pytest.importorskip("agents")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.normpath(os.path.join(
    HERE, "..", "..", "autobuild1", "src")))

from agents.tracing import (TracingProcessor, add_trace_processor,
                            custom_span, trace)
from loop import tracing as lt


class Capture(TracingProcessor):
    def __init__(self):
        self.traces, self.spans = [], []

    def on_trace_start(self, t):
        self.traces.append(("start", t.trace_id))

    def on_trace_end(self, t):
        self.traces.append(("end", t.trace_id))

    def on_span_start(self, s):
        pass

    def on_span_end(self, s):
        self.spans.append(s)

    def shutdown(self):
        pass

    def force_flush(self):
        pass


def test_live_trace_and_span_roundtrip():
    cap = Capture()
    add_trace_processor(cap)
    sess = lt.TraceSession("agentloop-live", "proj",
                           trace_id="trace_" + "cd" * 16, use_sdk=True)
    assert sess.mode == "provider"
    h = sess.span("attempt/ATT-0", {"observation": "echo ok", "exit": 0})
    assert sess.finish_span(h) is True
    sess.finish()
    assert ("start", sess.trace_id) in cap.traces
    assert ("end", sess.trace_id) in cap.traces
    mine = [s for s in cap.spans if s.trace_id == sess.trace_id]
    assert mine, "our span reached a real TracingProcessor"
    data = mine[0].span_data.data
    assert data["exit"] == 0 and data["observation"] == "echo ok"


def test_live_custom_span_nesting():
    cap = Capture()
    add_trace_processor(cap)
    with trace("nest-check", trace_id="trace_" + "ef" * 16):
        with custom_span("outer", {"k": 1}):
            with custom_span("inner", {"k": 2}):
                pass
    inners = [s for s in cap.spans
              if getattr(s.span_data, "name", "") == "inner"]
    assert inners and inners[0].parent_id is not None
