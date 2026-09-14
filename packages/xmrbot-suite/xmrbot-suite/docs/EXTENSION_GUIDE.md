# Coding-agent extension guide

## Add a compute venue

Implement `xmrcomputer.markets.base.MarketAdapter.offers()`, return `MarketOffer`s, and add the adapter to the bridge policy. Never place venue-specific logic in the scheduler.

## Add a live price source

Create a provider returning an observed XMR/USD value with source/timestamp/confidence. Keep price separate from monerod chain facts.

## Add a CPU observation

Append a record with measured hashrate, watts, configuration and source. Prefer an observations table once multiple measurements per CPU are collected.

## Add an MCP tool

1. define a Pydantic input model in `agent/tools.py`;
2. register description and handler in `ToolRegistry.specs`;
3. add a risk class;
4. add tests for schema, handler and negative cases.

Do not add raw arbitrary RPC passthrough tools. Explicit typed tools are the security boundary.

## Add wallet execution later

Keep wallet RPC local. Use exact transaction proposals and bind approval to destination, amount, fee ceiling and expiry. Never expose seed/private-key export in the MCP registry.
