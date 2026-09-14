# OrbitSwap

- ID: `orbitswap`
- Canonical URL: https://orbitswap.io/
- Categories: swap, exchange
- Agentability: 0.96
- Status: active

## Capabilities

### `currencies`
- class: `discover`
- mode: `native_api`
- state-changing: `false`
- requires grant: `false`
- description: List supported assets.

### `rate`
- class: `quote`
- mode: `native_api`
- state-changing: `false`
- requires grant: `false`
- description: Get public swap quote/limits.

### `create_transaction`
- class: `execute`
- mode: `native_api`
- state-changing: `true`
- requires grant: `true`
- description: Create a swap transaction with an API key.

### `transaction_status`
- class: `status`
- mode: `native_api`
- state-changing: `false`
- requires grant: `false`
- description: Read transaction status.

## Sources

- https://orbitswap.io/api-docs
