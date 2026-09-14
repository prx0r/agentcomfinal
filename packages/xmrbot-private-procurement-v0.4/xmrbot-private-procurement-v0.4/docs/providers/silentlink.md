# Silent Link

- ID: `silentlink`
- Canonical URL: https://silent.link/
- Categories: esim, connectivity
- Agentability: 0.58
- Status: active

## Capabilities

### `catalog`
- class: `discover`
- mode: `read_only_web`
- state-changing: `false`
- requires grant: `false`
- description: Discover eSIM plans and coverage.

### `purchase_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Prepare plan purchase and funding proposal.

## Privacy notes

- No KYC/email required according to provider; eSIM/network usage has its own telecom metadata considerations.

## Sources

- https://silent.link/
