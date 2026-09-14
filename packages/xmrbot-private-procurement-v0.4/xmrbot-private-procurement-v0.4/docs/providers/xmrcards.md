# XMR.CARDS

- ID: `xmrcards`
- Canonical URL: https://xmr.cards/
- Categories: gift_cards, retail_router
- Agentability: 0.64
- Status: active

## Capabilities

### `catalog`
- class: `discover`
- mode: `read_only_web`
- state-changing: `false`
- requires grant: `false`
- description: Discover current gift-card catalog/limits.

### `purchase_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Prepare card purchase without exposing wallet authority.

## Sources

- https://xmr.cards/
