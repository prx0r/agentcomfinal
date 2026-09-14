"""Provider-native telemetry: OpenAI Agents API Traces/Spans + local mirror.

Security model: the agent's telemetry is legit only if a second party holds
a copy the agent cannot rewrite. Local a-logs are hash-chained (tamper-
evident); provider-exported traces are the independent copy. A RUN record
binds both: {run_id, trace_id}. Either copy alone proves little; together
they are cross-checkable (independent readback, applied to telemetry).

Native mapping (OpenAI Agents SDK, verified against 0.22.2 surface):
  RUN record   -> trace(workflow_name, group_id=project, metadata)
  attempt      -> custom_span("attempt/ATT-n", observation fields only)
  validation   -> custom_span("validation/<id>", verdict + reasons)
  research     -> custom_span("research/<id>", sources, never full context)
  grant check  -> custom_span("grant/<capability>", verdict only)
Usage maps to generation_span-compatible {input_tokens, output_tokens,
cached_tokens, reasoning_tokens} (acom-openai usage_to_record shape).

Rules:
- SDK imported lazily; absent SDK (or no key) -> local mirror only, in the
  SDK export() payload shape, so the same verifier works offline.
- Scrub-before-export: secret patterns refused in a-logs AND scrubbed from
  span data (defense in depth). Sensitive model I/O needs
  trace_include_sensitive_data explicitly enabled (default OFF =
  ENABLED_WITHOUT_DATA posture: structure without content).
- Spans carry observations, never verdicts-as-truth and never secrets.
- Processor errors never break execution (SDK contract); ours never raise.
"""
import secrets
import time

SECRET_MARKERS = ("sk-", "ghp_", "gho_", "pina_", "xox", "BEGIN PRIVATE KEY",
                  "api_key", "password")
TRACE_PREFIX = "trace_"


def gen_trace_id():
    return TRACE_PREFIX + secrets.token_hex(16)


def scrub(obj):
    """Redact secret-shaped strings from span data. Pure; never raises."""
    try:
        if isinstance(obj, dict):
            return {k: ("<redacted>" if any(
                m in str(k).lower() for m in ("secret", "token", "password",
                                              "api_key", "apikey", "private"))
                else scrub(v)) for k, v in obj.items()}
        if isinstance(obj, list):
            return [scrub(v) for v in obj]
        if isinstance(obj, str):
            if any(m in obj for m in SECRET_MARKERS):
                return "<redacted>"
            return obj[:2000]
        return obj
    except Exception:  # noqa: BLE001 - scrubbing never breaks tracing
        return "<redacted>"


def usage_record(input_tokens=None, output_tokens=None, cached_tokens=None,
                 reasoning_tokens=None, cost=None):
    """Generation-span-compatible usage. Unknowns stay None (atask law)."""
    return {"input_tokens": input_tokens, "output_tokens": output_tokens,
            "cached_tokens": cached_tokens,
            "reasoning_tokens": reasoning_tokens, "cost": cost}


class MirrorSpan(object):
    """SDK export()-shaped span for offline use. Same verifier both ways."""

    def __init__(self, name, data, trace_id, parent_id=None):
        self.name = name
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.ended_at = None
        self.data = scrub(data or {})
        self.error = None

    def finish(self, error=None):
        self.ended_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.error = error

    def export(self):
        return {"object": "trace.span", "id": self.name,
                "trace_id": self.trace_id, "parent_id": self.parent_id,
                "started_at": self.started_at, "ended_at": self.ended_at,
                "span_data": {"name": self.name, "data": self.data},
                "error": self.error}


class TraceSession(object):
    """One RUN's telemetry. use_sdk=True attempts the real provider;
    anything missing (package, key, network) degrades to mirror-only —
    and says so in `mode` (never silently)."""

    def __init__(self, workflow, project, trace_id=None, use_sdk=False,
                 include_sensitive_data=False):
        self.workflow = workflow
        self.project = project
        self.trace_id = trace_id or gen_trace_id()
        self.include_sensitive = bool(include_sensitive_data)
        self.spans = []
        self.sdk_trace = None
        self._trace_ctx = None
        self.mode = "mirror"
        if use_sdk:
            try:
                from agents.tracing import trace as sdk_trace
                self.sdk_trace = sdk_trace(
                    workflow, trace_id=self.trace_id, group_id=project,
                    metadata={"agentcom": "agentloop/0.1"})
                self._trace_ctx = self.sdk_trace
                self._trace_ctx.__enter__()
                self.mode = "provider"
            except Exception as exc:  # noqa: BLE001 - degrade loudly
                self.sdk_trace = None
                self.mode = "mirror:sdk-unavailable:%s" % type(exc).__name__

    def finish(self):
        if self._trace_ctx is not None:
            try:
                self._trace_ctx.__exit__(None, None, None)
            except Exception:  # noqa: BLE001
                pass
            self._trace_ctx = None

    def span(self, name, data, parent=None):
        data = dict(scrub(data or {}))
        if not self.include_sensitive:
            data.pop("input", None)
            data.pop("output", None)
        if self.sdk_trace is not None:
            try:
                from agents.tracing import custom_span
                ctx = custom_span(name, data)
                ctx.__enter__()
                self.spans.append(("sdk", name, ctx))
                return ("sdk", name)
            except Exception:  # noqa: BLE001 - mirror still records
                pass
        m = MirrorSpan(name, data, self.trace_id,
                       parent[1] if parent else None)
        self.spans.append(("mirror", name, m))
        return ("mirror", name)

    def finish_span(self, handle, error=None):
        kind, name = handle
        for k, n, ref in self.spans:
            if (k, n) == (kind, name) and hasattr(ref, "finish"):
                try:
                    if kind == "sdk":
                        if error:
                            ref.set_error({"message": str(error)[:200],
                                           "data": {}})
                        ref.__exit__(None, None, None)
                    else:
                        ref.finish(error={"message": str(error)[:200]}
                                   if error else None)
                except Exception:  # noqa: BLE001
                    pass
                return True
        return False

    def export_mirror(self):
        return [ref.export() for k, _, ref in self.spans
                if k == "mirror" and hasattr(ref, "export")]

    def bind(self, run_record):
        """Bind provider trace to RUN record (both directions auditable)."""
        rec = dict(run_record or {})
        rec["trace_id"] = self.trace_id
        rec["telemetry_mode"] = self.mode
        return rec
