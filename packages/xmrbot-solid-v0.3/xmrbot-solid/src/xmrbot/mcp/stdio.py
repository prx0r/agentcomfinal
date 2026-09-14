from __future__ import annotations
import asyncio
import json
import sys
from xmrbot.agent.tools import ToolRegistry
from xmrbot.mcp.server import MCPServer
from xmrbot.services import Services


async def run() -> None:
    server = MCPServer(ToolRegistry(Services()))
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = await server.handle(message)
            if response is not None:
                print(json.dumps(response, default=str), flush=True)
        except Exception as exc:
            print(json.dumps({"jsonrpc":"2.0","id":None,"error":{"code":-32700,"message":str(exc)}}), flush=True)


def main() -> None:
    asyncio.run(run())

if __name__ == "__main__":
    main()
