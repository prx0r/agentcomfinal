# KYCnot.me

- ID: `kycnot`
- Canonical URL: https://kycnot.me/
- Categories: registry, privacy, discovery
- Agentability: 0.90
- Status: active

## Capabilities

### `service_get`
- class: `discover`
- mode: `native_api`
- state-changing: `false`
- requires grant: `false`
- description: Fetch structured service metadata by id/slug/url.

### `service_search`
- class: `discover`
- mode: `manual_bridge`
- state-changing: `false`
- requires grant: `false`
- description: Search/browse service registry; exact API search contract may change.

## Privacy notes

- Returns KYC level and verification metadata; verification is evidence, not a safety guarantee.

## Sources

- https://kycnot.me/docs/api
