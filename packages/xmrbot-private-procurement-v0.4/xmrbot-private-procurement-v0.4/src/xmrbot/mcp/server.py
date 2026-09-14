from __future__ import annotations
import json
from xmrbot import __version__

PROTOCOL_VERSION = "2025-06-18"


class MCPServer:
    def __init__(self, registry):
        self.registry = registry

    async def handle(self, message: dict) -> dict | None:
        method = message.get("method")
        request_id = message.get("id")
        if method and method.startswith("notifications/"):
            return None
        try:
            if method == "initialize":
                result = {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {"listChanged": False}, "resources": {"listChanged": False}},
                    "serverInfo": {"name": "xmrbot", "version": __version__},
                    "instructions": (
                        "Monero knowledge, mining economics, blog/content workflows and local-first execution planning. "
                        "Discover tools before calling them. Wallet seeds/private keys are never accepted."
                    ),
                }
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": [
                    {"name": t.name, "description": t.description, "inputSchema": t.input_schema,
                     "annotations": {
                         "readOnlyHint": t.risk_class.value.startswith("R0"),
                         "destructiveHint": False,
                         "idempotentHint": t.risk_class.value.startswith("R0"),
                     }}
                    for t in self.registry.metadata()
                ]}
            elif method == "tools/call":
                params = message.get("params", {})
                value = await self.registry.call(params["name"], params.get("arguments", {}))
                text = json.dumps(value, default=str, separators=(",", ":"))
                result = {"content": [{"type": "text", "text": text}], "structuredContent": value, "isError": False}
            elif method == "resources/list":
                result = {"resources": self.registry.resources()}
            elif method == "resources/read":
                params = message.get("params", {})
                uri = params["uri"]
                value = self.registry.read_resource(uri)
                if isinstance(value, str):
                    text = value
                    mime = "text/plain"
                else:
                    text = json.dumps(value, default=str, separators=(",", ":"))
                    mime = "application/json"
                result = {"contents": [{"uri": uri, "mimeType": mime, "text": text}]}
            else:
                return self._error(request_id, -32601, f"Method not found: {method}")
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except Exception as exc:
            return self._error(request_id, -32000, str(exc))

    @staticmethod
    def _error(request_id, code: int, message: str) -> dict:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}
