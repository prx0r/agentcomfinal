# XMR Checkout

- ID: `xmrcheckout`
- Canonical URL: https://xmrcheckout.com/
- Categories: merchant, checkout, webhooks
- Agentability: 0.94
- Status: active

## Capabilities

### `server_info`
- class: `discover`
- mode: `local_api`
- state-changing: `false`
- requires grant: `false`
- description: Check self-hosted checkout server.

### `list_webhooks`
- class: `discover`
- mode: `local_api`
- state-changing: `false`
- requires grant: `false`
- description: List store webhooks.

## Privacy notes

- Self-hostable non-custodial checkout; wallet receives XMR while checkout observes invoice state.

## Sources

- https://xmrcheckout.com/docs
- https://xmrcheckout.com/guides
