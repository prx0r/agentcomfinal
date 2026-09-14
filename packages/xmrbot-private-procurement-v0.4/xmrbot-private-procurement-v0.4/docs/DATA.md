# Data and methodology

## Chain truth

When enabled, `MoneroRPCClient` pulls `get_info`, `get_last_block_header`, `get_fee_estimate` and transaction-pool stats from the configured monerod. Estimated network hashrate uses `difficulty / target_seconds`.

## Price truth

XMR/USD is intentionally a separate configured input in this release. A future exchange/price adapter can replace it without contaminating chain-derived values.

## Offline mode

Offline mode creates an explicit `offline-seed-config` observation with confidence 0.25. This makes the site usable without lying that bootstrapped numbers are live.

## Hardware

Bundled CPU records are seeds for the data model and UI. They carry a source string and `verified` flag. A production crawler/benchmark ingestion pipeline should append measured observations rather than overwrite provenance.
