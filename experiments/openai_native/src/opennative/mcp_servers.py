"""Minimal stdio MCP servers (stdlib JSON-RPC). Two namespaces, one enforcer.

qp-gateway: qp.authorize (grant check), qp.verify (receipt re-check).
  The gateway enforces QP ITSELF on every call: bypassing any outer
  approval layer still hits this check — approval != authority.
gitgoblin: gg.search (local archaeology -> candidates).

Protocol: newline-delimited {jsonrpc:2.0, id, method, params} on stdin;
{jsonrpc, id, result|error} on stdout. Methods: initialize, tools/list,
tools/call. Pure dispatch is importable without stdio (tests use call()).
"""
import json
import sys

TOOLS = {
    "qp.authorize": {"description": "Grant check for a proposed action",
                     "input": ["action", "grant", "facts", "now"]},
    "qp.verify": {"description": "Re-verify a settled receipt reference",
                  "input": ["receipt", "pubkey"]},
    "gg.search": {"description": "Local component archaeology",
                  "input": ["query"]},
}


def _qp_authorize(params, deps):
    grants = deps["grants"]
    ok, reason = grants.verify_grant(params.get("grant", {}),
                                     params.get("action", ""),
                                     params.get("facts", {}),
                                     params.get("now", ""))
    return {"authorized": ok, "reason": reason}


def _qp_verify(params, deps):
    build = deps["build"]
    ok = build.verify_signed(params.get("receipt", {}),
                             params.get("pubkey", ""))
    return {"valid": ok}


def _gg_search(params, deps):
    gg = deps["gitgoblin"]
    cands = gg.search_local(params.get("query", ""))
    return {"candidates": cands}


DISPATCH = {"qp.authorize": _qp_authorize, "qp.verify": _qp_verify,
            "gg.search": _gg_search}


def default_deps():
    """Wire real modules (ab2 grants/build + local archaeology)."""
    import os as _os
    root = _os.path.normpath(_os.path.join(
        _os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", ".."))
    for _d in ("agentcombuild/autobuild1/src", "agentcombuild/autobuild2/src"):
        _p = _os.path.join(root, _d)
        if _p not in sys.path:
            sys.path.insert(0, _p)
    if root not in sys.path:
        sys.path.insert(0, root)
    from ab2 import build as _build
    from ab2 import grants as _grants
    from adapters import gitgoblin as _gg
    return {"grants": _grants, "build": _build, "gitgoblin": _gg}


def call(tool, params, deps=None):
    """Direct dispatch (tests + in-process use). Returns result or raises."""
    if tool not in DISPATCH:
        raise ValueError("unknown-tool:%s" % tool)
    return DISPATCH[tool](params or {}, deps or default_deps())


def handle(request, deps=None):
    """One JSON-RPC request -> response dict. Never raises."""
    try:
        method = request.get("method", "")
        rid = request.get("id")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": rid,
                    "result": {"protocol": "mcp/0.1",
                               "tools": sorted(TOOLS)}}
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": rid,
                    "result": {"tools": [
                        {"name": n, "description": t["description"]}
                        for n, t in sorted(TOOLS.items())]}}
        if method == "tools/call":
            p = request.get("params", {})
            try:
                return {"jsonrpc": "2.0", "id": rid,
                        "result": call(p.get("name", ""), p.get("arguments", {}),
                                       deps)}
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
        sys.stdout.write(json.dumps(handle(req, deps)) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    serve()
