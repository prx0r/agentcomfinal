# XMRBazaar

- ID: `xmrbazaar`
- Canonical URL: https://xmrbazaar.com/
- Categories: marketplace, goods, services, escrow, wanted
- Agentability: 0.72
- Status: active

## Capabilities

### `search`
- class: `discover`
- mode: `read_only_web`
- state-changing: `false`
- requires grant: `false`
- description: Discover public listings.

### `purchase_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Create a bounded order/offer proposal without spending.

### `wanted_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Prepare a Wanted listing for human/API submission.

### `order_status`
- class: `status`
- mode: `manual_bridge`
- state-changing: `false`
- requires grant: `false`
- description: Attach order state as evidence.

### `api_future`
- class: `execute`
- mode: `upcoming_api`
- state-changing: `true`
- requires grant: `true`
- description: JSON automation API announced May 2026; adapter seam reserved.

## Privacy notes

- Non-custodial direct XMR and client-side 2-of-3 multisig escrow are available on supported listings.
- Physical delivery can reveal delivery information to the seller.

## Caveats

- Transactional JSON API is announced but not launched as of the 2026-08-16 changelog.

## Sources

- https://xmrbazaar.com/changelog/
- https://xmrbazaar.com/faq/
- https://xmrbazaar.com/escrow-guide/
