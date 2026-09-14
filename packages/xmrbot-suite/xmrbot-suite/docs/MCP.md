# MCP surface

Current tools:

- `xmr_search` R0
- `xmr_network_status` R0
- `xmr_mining_profitability` R0
- `xmr_cpu_lookup` R0
- `xmr_mine_or_buy` R0
- `xmr_resource_find` R0
- `xmr_node_plan` R0 (plan only)
- `xmr_wallet_plan` R0 (plan only; describes R2 execution boundary)
- `xmr_machine_inspect` R0
- `xmr_machine_benchmark` R1 semantics, currently non-invasive catalog estimate
- `xmr_computer_opportunities` R0

The tool list includes read-only annotations. No tool moves funds. No tool accepts a wallet seed or private spend key.

`MCPServer` is transport independent. `/mcp` provides HTTP JSON-RPC and `xmrbot.mcp.stdio` provides newline-delimited stdio JSON-RPC.
