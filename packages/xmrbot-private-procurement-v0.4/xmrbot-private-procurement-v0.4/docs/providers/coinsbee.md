# CoinsBee

- ID: `coinsbee`
- Canonical URL: https://www.coinsbee.com/
- Categories: gift_cards, mobile_topup, retail_router
- Agentability: 0.55
- Status: active

## Capabilities

### `catalog`
- class: `discover`
- mode: `read_only_web`
- state-changing: `false`
- requires grant: `false`
- description: Discover gift cards/mobile topups.

### `purchase_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Prepare card/top-up purchase.

## Sources

- https://www.coinsbee.com/
