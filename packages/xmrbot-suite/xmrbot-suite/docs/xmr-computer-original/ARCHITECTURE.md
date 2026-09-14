# Architecture

## Product thesis

Monero/RandomX acts as a reserve buyer for compatible idle CPU capacity. `xmr.computer` compares that reserve bid with higher-value permitted workloads and routes a machine to the best net return, denominated in XMR.

## Components

### 1. Node agent
Runs locally. Detects hardware, measures hashrate/power, enforces thermal/resource budgets, and executes only signed/allowlisted adapters.

### 2. Market adapters
Small modules that translate a compute market into a common offer schema. Candidate future adapters: Qubic, decentralized compute markets, rendering/transcoding markets, research-compute bounties, and ordinary cloud/job queues.

### 3. Economic router
Normalizes every workload to net XMR/hour after electricity, hardware amortization, fees, and optional risk discount.

### 4. Reserve bid
RandomX mining is the fallback. This creates a live floor price for CPU capacity rather than leaving idle machines economically undefined.

### 5. Privacy boundary
Wallet custody is explicitly outside third-party adapters. A production design should use per-market disposable identities, payout indirection where legally/technically supported, Tor/SOCKS for network privacy where allowed, and never expose seed phrases/private keys to workers.

### 6. Settlement
MVP only calculates XMR-denominated value. Production settlement can support direct XMR payments, exchange/atomic-swap conversion, or user-selected payout providers. Settlement must be modular because counterparty and regulatory constraints vary.

## Scheduler decision

`offer_value = revenue - fees - energy - amortization - risk_cost`

The scheduler should later add switching cost, task duration confidence, thermal cost, interruption probability, FX/slippage, and settlement risk.

## Qubic seam

Qubic should be integrated as one adapter, not made a hard dependency. If Qubic's useful-compute/mining economics beat native RandomX after all costs, Qubic wins that scheduling interval. If not, another market or RandomX wins.

This preserves the central property: **the node optimizes for the user, not for a particular network.**
