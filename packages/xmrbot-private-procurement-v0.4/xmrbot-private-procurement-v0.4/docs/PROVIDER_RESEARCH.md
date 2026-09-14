# Provider research ledger

Research snapshot: **2026-09-13**. This ledger records why each integration mode is what it is. It is not an endorsement of any provider. Live services change; adapters must fail closed when contracts drift.

| Provider | Verified surface | XMRBot integration decision | Primary source |
|---|---|---|---|
| KYCnot.me | Service API exposes service metadata, verification status and KYC level | Native read API / evidence oracle | https://kycnot.me/docs/api |
| XMRBazaar | Listings/orders/escrow marketplace; JSON API announced and still described as upcoming | Read/manual bridge today; API-ready contract | https://xmrbazaar.com/changelog/ |
| Monero.Jobs | XMR-denominated job/freelance marketplace | Manual/read bridge until a supported API is published | https://monero.jobs/ |
| Haveno | Local `havenod` exposes wallet/offers/trades/market data over gRPC | Local API via explicit bridge boundary | https://docs.haveno.exchange/users/haveno-api/ |
| OrbitSwap | REST currencies/rates/transaction creation/status | Native REST adapter | https://orbitswap.io/api-docs |
| Trocador / AnonPay | Programmatic invoice creation/status/webhooks | Native HTTP adapter | https://trocador.app/anonpaydocumentation |
| 1gwei.dev | Quote/order/status API for EVM gas paid by XMR/x402/etc. | Native REST adapter | https://1gwei.dev/guides/agent-api-scripted-gas-top-ups |
| BasicSwapDEX | Local JSON API; non-custodial swap client | Local API adapter | https://docs.basicswapdex.com/docs/user-guides/web-ui-authentication/ |
| monero-wallet-rpc | Canonical wallet JSON-RPC | Local settlement adapter; private-key/seed exports intentionally absent | https://docs.getmonero.org/rpc-library/wallet-rpc/ |
| XMR Checkout | Self-hosted non-custodial merchant API / BTCPay-compatible API | Native/self-hosted API adapter | https://xmrcheckout.com/docs |
| Kuno | Non-custodial XMR fundraising | Manual bridge; never transmit private view keys via cloud MCP | https://kuno.anne.media/faq/ |
| Njalla | Domains/VPS/VPN, XMR accepted | Provider discovery/manual bridge unless a supported transaction API is configured | https://njal.la/ |
| 1984 Hosting | Hosting/VPS/domains with XMR payment | Manual bridge | https://1984.hosting/ |
| Servers Guru | XMR VPS offers | Manual bridge | https://servers.guru/monero-vps/ |
| Silent Link | eSIM/data service with XMR payment | Manual bridge | https://silent.link/ |
| AnonymousLabels | Shipping labels paid with XMR | Manual bridge pending stable public API | https://anonymouslabels.com/pay-with-monero |
| XMR.CARDS | XMR gift-card purchase surface | Manual bridge pending stable public API | https://xmr.cards/ |
| CoinsBee | Gift cards/mobile topups, XMR supported | Manual/commercial bridge pending supported API contract | https://www.coinsbee.com/en/buy-gift-cards-with-monero/ |
| ShopinBit Concierge | Human-backed procurement/concierge accepting XMR | Manual concierge adapter | https://shopinbit.com/concierge/ |
| BTCPay Server | Self-hosted merchant/payment infrastructure | Descriptor/manual integration in this release; XMR Checkout covers the tested BTCPay-compatible API path | https://docs.btcpayserver.org/ |

## Contract rule

`IntegrationMode` is part of the machine contract. A manual or upcoming provider **must not** silently become a browser-writing adapter. Promotion to `native_api` requires documented endpoints, fixtures, contract tests, and a source-ledger update.

## Privacy rule

XMR settlement can reduce financial-graph disclosure, but it does not make every transaction anonymous. Physical delivery, account recovery, counterparties, network metadata, browser fingerprinting, jurisdictional requirements, and provider logs can all reveal information. XMRBot models those as separate exposure dimensions and does not promise "untraceability".
