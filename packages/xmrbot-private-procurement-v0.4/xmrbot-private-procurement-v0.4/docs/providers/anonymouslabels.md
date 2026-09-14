# AnonymousLabels

- ID: `anonymouslabels`
- Canonical URL: https://anonymouslabels.com/
- Categories: shipping, logistics
- Agentability: 0.64
- Status: active

## Capabilities

### `quote_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `false`
- requires grant: `false`
- description: Prepare dimensions/route for carrier quote.

### `label_purchase_proposal`
- class: `propose`
- mode: `manual_bridge`
- state-changing: `true`
- requires grant: `true`
- description: Prepare shipping label purchase.

## Privacy notes

- Shipping necessarily involves recipient/sender logistics data even when payment is private.

## Sources

- https://anonymouslabels.com/
- https://anonymouslabels.com/pay-with-monero
