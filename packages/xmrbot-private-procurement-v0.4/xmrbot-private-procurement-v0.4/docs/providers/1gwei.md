# 1gwei.dev

- ID: `1gwei`
- Canonical URL: https://1gwei.dev/
- Categories: gas, evm, bridge
- Agentability: 0.99
- Status: active

## Capabilities

### `quote`
- class: `quote`
- mode: `native_api`
- state-changing: `false`
- requires grant: `false`
- description: Quote native gas top-up.

### `create_order`
- class: `execute`
- mode: `native_api`
- state-changing: `true`
- requires grant: `true`
- description: Create gas order using XMR/LN/x402 payment method.

### `order_status`
- class: `status`
- mode: `native_api`
- state-changing: `false`
- requires grant: `false`
- description: Poll gas order status.

## Privacy notes

- XMR can fund native EVM gas; the destination EVM payout remains public on the destination chain.

## Sources

- https://1gwei.dev/guides/agent-api-scripted-gas-top-ups
