# Servers Guru

- ID: `serversguru`
- Canonical URL: https://servers.guru/
- Categories: vps, infrastructure, compute
- Agentability: 0.62
- Status: active

## Capabilities

### `catalog`
- class: `discover`
- mode: `read_only_web`
- state-changing: `false`
- requires grant: `false`
- description: Discover XMR-paid VPS plans.

### `purchase_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Prepare bounded VPS purchase.

## Sources

- https://servers.guru/monero-vps/
