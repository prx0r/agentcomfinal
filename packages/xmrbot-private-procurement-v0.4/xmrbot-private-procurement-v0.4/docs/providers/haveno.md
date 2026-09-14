# Haveno

- ID: `haveno`
- Canonical URL: https://haveno.exchange/
- Categories: exchange, p2p, fiat
- Agentability: 0.95
- Status: active

## Capabilities

### `market`
- class: `discover`
- mode: `local_api`
- state-changing: `false`
- requires grant: `false`
- description: Read prices and offers from a local Haveno daemon.

### `offer_proposal`
- class: `propose`
- mode: `local_api`
- state-changing: `true`
- requires grant: `true`
- description: Prepare create/take-offer parameters.

### `trade_status`
- class: `status`
- mode: `local_api`
- state-changing: `false`
- requires grant: `false`
- description: Read trade state.

### `trade_execute`
- class: `execute`
- mode: `local_api`
- state-changing: `true`
- requires grant: `true`
- description: Execute a pre-authorized offer/trade via local Haveno bridge.

## Privacy notes

- Local non-custodial daemon connects over Tor; API grants wallet/trade control and must remain local/firewalled.

## Sources

- https://docs.haveno.exchange/users/haveno-api/
