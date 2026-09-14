"""MCP servers over real QP (stdlib JSON-RPC, official wire shapes).

qp-gateway: qp.authorize (REAL qp grant verification), qp.verify (REAL qp
settlement check). The gateway enforces QP ITSELF on every call: bypassing
any outer approval layer still hits this check — approval != authority.
No ab1/ab2/ab3 imports anywhere in this file (isolation gate enforces).
gitgoblin: gg.search (local archaeology -> candidates).

Wire: newline-delimited JSON-RPC on stdio. initialize answers with
protocolVersion/capabilities/serverInfo (official client compatible);
tools carry inputSchema; tool results are content blocks; notifications
(no id) receive no reply.
"""
import json
import sys

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "agentcom-qp-gateway", "version": "0.2.0"}

TOOLS = {

    "qp.authorize": {"description": "Real QP grant check for a proposed action",
                     "inputSchema": {"type": "object",
                                     "required": ["action", "grant"],
                                     "properties": {
                                         "action": {"type": "object"},
                                         "grant": {"type": "object"},
                                         "facts": {"type": "object"},
                                         "now": {"type": "string"}}}},
    "qp.verify": {"description": "Real QP settlement check of a receipt",
                  "inputSchema": {"type": "object",
                                  "required": ["receipt", "evidence"],
                                  "properties": {
                                      "receipt": {"type": "object"},
                                      "evidence": {"type": "array"}}}},
    "gg.search": {"description": "Local component archaeology",
                  "inputSchema": {"type": "object",
                                  "required": ["query"],
                                  "properties": {"query": {"type": "string"}}}},
    "business.lookup": {"description": "Read-only verified business context lookup",
                        "inputSchema": {"type": "object",
                                        "required": ["company"],
                                        "properties": {
                                            "company": {"type": "string"}}}},
}


def _directory():
    import os as _os
    base = _os.path.normpath(_os.path.join(
        _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "examples",
        "business_directory.json"))
    with open(base, encoding="utf-8") as fh:
        return json.load(fh)


def _business_lookup(params, deps):
    del deps
    want = str(params.get("company", "")).strip().lower()
    for b in _directory().get("businesses", []):
        if want and (want == b["id"] or want in b["name"].lower()
                     or want in b["domain"].lower()):
            return {"found": True, "business": b}
    known = [b["id"] for b in _directory().get("businesses", [])]
    return {"found": False, "error": "unknown-company",
            "known": known}


def _qp_authorize(params, deps):
    qp = deps["qp"]
    action = params.get("action", {})
    if isinstance(action, str):
        action = {"capability": action}
    return qp.authorize(action, params.get("grant", {}),
                        params.get("facts", {}), params.get("now", ""))


def _qp_verify(params, deps):
    qp = deps["qp"]
    r = qp.verify_settlement(params.get("receipt", {}),
                             params.get("evidence", []))
    return {"valid": bool(r.get("ok")), "reason": r.get("reason", "")}


def _gg_search(params, deps):
    gg = deps["gitgoblin"]
    cands = gg.search_local(params.get("query", ""))
    return {"candidates": cands}


DISPATCH = {"qp.authorize": _qp_authorize, "qp.verify": _qp_verify,
            "gg.search": _gg_search, "business.lookup": _business_lookup}


def default_deps():
    """Wire canonical modules (real QP adapter + local archaeology)."""
    import os as _os
    root = _os.path.normpath(_os.path.join(
        _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", ".."))
    if root not in sys.path:
        sys.path.insert(0, root)
    from adapters import gitgoblin as _gg
    from adapters import qp as _qp
    return {"qp": _qp, "gitgoblin": _gg}


def call(tool, params, deps=None):
    """Direct dispatch (tests + in-process use). Returns result or raises."""
    if tool not in DISPATCH:
        raise ValueError("unknown-tool:%s" % tool)
    return DISPATCH[tool](params or {}, deps or default_deps())


def handle(request, deps=None):
    """One JSON-RPC request -> response dict (None for notifications).
    Never raises."""
    try:
        method = request.get("method", "")
        rid = request.get("id")
        if "id" not in request:
            if method == "notifications/initialized":
                return None
            return None  # notifications get no reply, ever
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": rid,
                    "result": {"protocolVersion": PROTOCOL_VERSION,
                               "capabilities": {"tools": {}},
                               "serverInfo": SERVER_INFO}}
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": rid,
                    "result": {"tools": [
                        {"name": n, "description": t["description"],
                         "inputSchema": t["inputSchema"]}
                        for n, t in sorted(TOOLS.items())]}}
        if method == "tools/call":
            p = request.get("params", {})
            try:
                out = call(p.get("name", ""), p.get("arguments", {}), deps)
                return {"jsonrpc": "2.0", "id": rid,
                        "result": {"content": [
                            {"type": "text",
                             "text": json.dumps(out, sort_keys=True)}]}}
            except Exception as exc:  # noqa: BLE001 - errors are responses
                return {"jsonrpc": "2.0", "id": rid,
                        "error": {"code": -32000, "message": str(exc)[:200]}}
        return {"jsonrpc": "2.0", "id": rid,
                "error": {"code": -32601, "message": "unknown-method"}}
    except Exception as exc:  # noqa: BLE001
        return {"jsonrpc": "2.0", "id": request.get("id"),
                "error": {"code": -32700, "message": str(exc)[:200]}}


def serve(deps=None):
    """Stdio loop. Each line in, one line out. EOF ends."""
    deps = deps or default_deps()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except ValueError:
            sys.stdout.write(json.dumps(
                {"jsonrpc": "2.0", "id": None,
                 "error": {"code": -32700, "message": "parse-error"}}) + "\n")
            sys.stdout.flush()
            continue
        resp = handle(req, deps)
        if resp is None:  # notification: no reply, ever
            continue
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    serve()
