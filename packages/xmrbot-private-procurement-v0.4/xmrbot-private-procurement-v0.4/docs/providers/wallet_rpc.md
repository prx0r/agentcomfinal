# monero-wallet-rpc

- ID: `wallet_rpc`
- Canonical URL: https://www.getmonero.org/
- Categories: wallet, settlement
- Agentability: 1.00
- Status: active

## Capabilities

### `balance`
- class: `discover`
- mode: `local_api`
- state-changing: `false`
- requires grant: `false`
- description: Read wallet balance.

### `create_address`
- class: `propose`
- mode: `local_api`
- state-changing: `true`
- requires grant: `false`
- description: Create a subaddress locally.

### `validate_address`
- class: `verify`
- mode: `local_api`
- state-changing: `false`
- requires grant: `false`
- description: Validate Monero address.

### `transfer`
- class: `execute`
- mode: `local_api`
- state-changing: `true`
- requires grant: `true`
- description: Transfer XMR only under exact QP grant.

## Privacy notes

- Run locally; XMRBot never accepts/export seed phrases or private spend keys through MCP.

## Sources

- https://docs.getmonero.org/rpc-library/wallet-rpc/
