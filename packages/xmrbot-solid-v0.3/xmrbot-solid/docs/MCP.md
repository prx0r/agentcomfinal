# MCP

XMRBot exposes transport-independent MCP JSON-RPC through HTTP (`POST /mcp`) and newline-delimited stdio (`xmrbot-mcp`).

Capabilities:

- tools/list + tools/call
- resources/list + resources/read
- deterministic structuredContent
- risk metadata on tool definitions
- read-only machine resources for site map, LLM guide, network state, blog index and content recipes

State-changing content tools (`xmr_blog_draft`, `xmr_blog_publish`) are R1. HTTP MCP blocks R1/R2 calls unless `XMRBOT_EDITOR_TOKEN` is configured and sent as a bearer token. Local stdio MCP is the recommended trusted internal-agent path.

Core discovery pattern:

1. `resources/list`
2. read `xmrbot://site` or `xmrbot://llms`
3. `tools/list` or `xmr_tools`
4. call the smallest typed tool that satisfies the task

The wallet seed/private-key export surface does not exist.
