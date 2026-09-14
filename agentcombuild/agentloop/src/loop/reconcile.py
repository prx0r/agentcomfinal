"""Reconciler: close the dual-custody loop. Local telemetry (hash-chained
a-logs, receipts, mirror spans) is cross-checked against provider-exported
trace payloads (SDK export() shape). Agreement is itself evidence; any
divergence is a finding, never silently dropped.

Inputs are plain dicts (mirror exports or provider export payloads), so this
runs keyless and offline. Pure; never raises on malformed input.
"""
from . import tracing


def _spans_of(items):
    out = []
    for it in items or []:
        if isinstance(it, dict) and it.get("object") == "trace.span":
            out.append(it)
    return out


def reconcile(exported_items, local_traces):
    """exported_items: provider/mirror span payloads. local_traces:
    [{trace_id, verdict, receipts[]}] (verdict GO|NOGO from our judges).

    Returns {matched, missing_provider, missing_local, error_mismatch,
    verdict_conflict, findings[]}.
    """
    rep = {"matched": [], "missing_provider": [], "missing_local": [],
           "error_mismatch": [], "verdict_conflict": [], "findings": []}
    try:
        spans = _spans_of(exported_items)
        by_trace = {}
        for s in spans:
            by_trace.setdefault(s.get("trace_id"), []).append(s)
        local_ids = {t.get("trace_id") for t in (local_traces or [])
                     if isinstance(t, dict)}
        for tid in sorted(local_ids):
            if tid not in by_trace:
                rep["missing_provider"].append(tid)
                rep["findings"].append("%s: local verdict has no provider copy"
                                       % tid)
                continue
            local = next(t for t in local_traces if t.get("trace_id") == tid)
            errs = [s for s in by_trace[tid] if s.get("error")]
            if bool(errs) != (local.get("verdict") == "NOGO"):
                rep["error_mismatch"].append(tid)
                rep["findings"].append(
                    "%s: provider errors=%d vs local verdict %s"
                    % (tid, len(errs), local.get("verdict")))
                continue
            if local.get("verdict") == "GO":
                bad = [s["id"] for s in by_trace[tid]
                       if not s.get("ended_at")]
                if bad:
                    rep["error_mismatch"].append(tid)
                    rep["findings"].append("%s: unfinished spans %s" % (tid, bad))
                    continue
            rep["matched"].append(tid)
        for tid in sorted(set(by_trace) - local_ids):
            rep["missing_local"].append(tid)
            rep["findings"].append("%s: provider copy with no local record "
                                   "(orphan telemetry)" % tid)
    except Exception as exc:  # noqa: BLE001 - reconciler never raises
        rep["findings"].append("reconciler-error:%s" % type(exc).__name__)
    return rep


def cross_check_run(run_record, mirror_spans, provider_spans):
    """One RUN's dual-custody verdict. Returns (ok, report)."""
    tid = (run_record or {}).get("trace_id", "?")
    verdict = (run_record or {}).get("verdict", "UNKNOWN")
    rep = reconcile(list(mirror_spans or []) + list(provider_spans or []),
                    [{"trace_id": tid, "verdict": verdict}])
    ok = tid in rep["matched"]
    return ok, {"trace_id": tid, "reconciled": ok,
                "findings": rep["findings"]}
