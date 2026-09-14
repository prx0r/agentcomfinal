# BasicSwap

- ID: `basicswap`
- Canonical URL: https://basicswapdex.com/
- Categories: swap, atomic_swap, dex
- Agentability: 0.86
- Status: active

## Capabilities

### `wallets`
- class: `discover`
- mode: `local_api`
- state-changing: `false`
- requires grant: `false`
- description: Inspect local BasicSwap wallets via JSON API.

### `swap_proposal`
- class: `propose`
- mode: `local_api`
- state-changing: `true`
- requires grant: `true`
- description: Prepare atomic-swap offer/take parameters.

## Privacy notes

- Local, non-custodial atomic swap protocol; protect local JSON API with client authentication.

## Sources

- https://docs.basicswapdex.com/docs/user-guides/web-ui-authentication/
- https://basicswapdex.com/protocol.html
