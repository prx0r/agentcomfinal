# Trocador AnonPay

- ID: `trocador`
- Canonical URL: https://trocador.app/
- Categories: swap, payment_router, merchant
- Agentability: 0.92
- Status: active

## Capabilities

### `create_invoice`
- class: `propose`
- mode: `native_api`
- state-changing: `true`
- requires grant: `true`
- description: Create an indirect AnonPay transaction bound to receiver/amount.

### `status`
- class: `status`
- mode: `native_api`
- state-changing: `false`
- requires grant: `false`
- description: Check AnonPay status by ID.

## Sources

- https://trocador.app/anonpaydocumentation
